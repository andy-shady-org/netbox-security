"""Request-local resource limits for address-set hierarchy displays."""

from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class HierarchyLimits:
    depth: int = 64
    nodes: int = 1000
    edges: int = 5000
    paths: int = 1000
    steps: int = 10000
    rows: int = 2000
    fetched_rows: int = 20000


class HierarchyBudget:
    def __init__(self, limits=None):
        self.limits = limits or HierarchyLimits()
        self.remaining_rows = self.limits.fetched_rows
        self.truncated = False

    def take(self, queryset, limit=None):
        """Apply a SQL limit before materializing, with one overflow sentinel."""
        limit = min(self.limits.rows if limit is None else limit, self.remaining_rows)
        if limit <= 0:
            self.truncated = True
            return []
        rows = list(queryset[: limit + 1])
        self.remaining_rows -= min(len(rows), limit)
        if len(rows) > limit:
            self.truncated = True
        return rows[:limit]


def discover_parents(seed_ids, fetch_parents, budget):
    """Discover a bounded graph. fetch_parents returns (parent, child) rows."""
    limits = budget.limits
    seeds = sorted(seed_ids)
    if len(seeds) > limits.nodes:
        budget.truncated = True
    nodes = set(seeds[: limits.nodes])
    frontier = nodes.copy()
    parents = defaultdict(set)
    edge_count = 0
    depth = 1
    while frontier:
        rows = budget.take(fetch_parents(frontier), limit=limits.edges - edge_count)
        if depth >= limits.depth:
            if rows:
                budget.truncated = True
            break
        next_frontier = set()
        for parent, child in rows:
            if parent not in nodes:
                if len(nodes) >= limits.nodes:
                    budget.truncated = True
                    return nodes, parents
                nodes.add(parent)
                next_frontier.add(parent)
            parents[child].add(parent)
            edge_count += 1
        frontier = next_frontier
        depth += 1
        if edge_count >= limits.edges and frontier:
            budget.truncated = True
            break
    return nodes, parents


def expand_paths(parent_map, seed_ids, budget):
    """Iterative DFS with global path/step limits, including cycle-only graphs."""
    parents = {node: tuple(sorted(values)) for node, values in parent_map.items()}
    paths = defaultdict(list)
    emitted = steps = 0
    for seed in sorted(seed_ids):
        # Iterator frames keep memory proportional to depth, not branching width.
        stack = [iter((seed,))]
        trail = []
        active = set()
        while stack:
            node = next(stack[-1], None)
            if node is None:
                stack.pop()
                if trail:
                    active.remove(trail.pop())
                continue
            if steps >= budget.limits.steps or emitted >= budget.limits.paths:
                budget.truncated = True
                return paths
            steps += 1
            if node in active:
                budget.truncated = True
                continue
            upstream = parents.get(node, ())
            path = (*trail, node)
            if not upstream or len(path) >= budget.limits.depth:
                if upstream:
                    budget.truncated = True
                paths[seed].append(tuple(reversed(path)))
                emitted += 1
            else:
                trail.append(node)
                active.add(node)
                stack.append(iter(upstream))
    return paths
