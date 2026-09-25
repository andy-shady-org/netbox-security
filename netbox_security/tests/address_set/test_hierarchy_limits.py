from unittest import TestCase

from netbox_security.utils.hierarchy_limits import (
    HierarchyBudget,
    HierarchyLimits,
    discover_parents,
    expand_paths,
)


class HierarchyLimitsTestCase(TestCase):
    def test_small_diamond_keeps_both_paths(self):
        budget = HierarchyBudget()
        paths = expand_paths({1: {2, 3}, 2: {4}, 3: {4}}, [1], budget)
        self.assertEqual(paths[1], [(4, 2, 1), (4, 3, 1)])
        self.assertFalse(budget.truncated)

    def test_chain_beyond_python_recursion_limit(self):
        parents = {n: {n + 1} for n in range(2000)}
        budget = HierarchyBudget(HierarchyLimits(depth=32))
        paths = expand_paths(parents, [0], budget)
        self.assertEqual(len(paths[0][0]), 32)
        self.assertTrue(budget.truncated)

    def test_layered_graph_has_global_path_limit(self):
        parents = {0: {1, 2}}
        for layer in range(1, 21):
            for node in (2 * layer - 1, 2 * layer):
                parents[node] = {2 * layer + 1, 2 * layer + 2}
        budget = HierarchyBudget(HierarchyLimits(paths=7))
        paths = expand_paths(parents, [0, 1, 2], budget)
        self.assertEqual(sum(map(len, paths.values())), 7)
        self.assertTrue(budget.truncated)

    def test_cycle_only_graph_obeys_work_limit(self):
        parents = {node: set(range(12)) - {node} for node in range(12)}
        budget = HierarchyBudget(HierarchyLimits(steps=30))
        self.assertEqual(dict(expand_paths(parents, [0], budget)), {})
        self.assertTrue(budget.truncated)

    def test_cycle_does_not_hide_an_available_root(self):
        budget = HierarchyBudget()
        self.assertEqual(expand_paths({1: {2, 3}, 2: {1}}, [1], budget)[1], [(3, 1)])
        self.assertTrue(budget.truncated)

    def test_exact_path_limit_is_not_truncated(self):
        budget = HierarchyBudget(HierarchyLimits(paths=2))
        self.assertEqual(len(expand_paths({1: {2, 3}}, [1], budget)[1]), 2)
        self.assertFalse(budget.truncated)

    def test_discovery_stops_at_depth_limit(self):
        calls = []

        def fetch(frontier):
            calls.append(frontier)
            return [(child + 1, child) for child in sorted(frontier)]

        budget = HierarchyBudget(HierarchyLimits(depth=4))
        nodes, parents = discover_parents({1}, fetch, budget)
        self.assertEqual(nodes, {1, 2, 3, 4})
        self.assertEqual(len(calls), 4)
        self.assertEqual(dict(parents), {1: {2}, 2: {3}, 3: {4}})
        self.assertTrue(budget.truncated)

    def test_discovery_bounds_nodes_and_edges(self):
        for limits in (HierarchyLimits(nodes=3), HierarchyLimits(edges=2)):
            with self.subTest(limits=limits):
                budget = HierarchyBudget(limits)
                nodes, parents = discover_parents(
                    {0}, lambda frontier: [(n, 0) for n in range(1, 100)], budget
                )
                self.assertLessEqual(len(nodes), limits.nodes)
                self.assertLessEqual(sum(map(len, parents.values())), limits.edges)
                self.assertTrue(budget.truncated)

    def test_seed_nodes_share_one_budget(self):
        budget = HierarchyBudget(HierarchyLimits(nodes=3))
        nodes, _ = discover_parents(range(20), lambda frontier: [], budget)
        self.assertEqual(nodes, {0, 1, 2})
        self.assertTrue(budget.truncated)

    def test_query_is_sliced_before_evaluation(self):
        class Query:
            def __getitem__(self, key):
                self.slice = key
                return range(key.stop)

        query = Query()
        budget = HierarchyBudget(HierarchyLimits(rows=3, fetched_rows=4))
        self.assertEqual(budget.take(query), [0, 1, 2])
        self.assertEqual(query.slice.stop, 4)
        self.assertEqual(budget.take(query), [0])
        self.assertEqual(query.slice.stop, 2)
        self.assertEqual(budget.take(query), [])
        self.assertEqual(budget.remaining_rows, 0)
        self.assertTrue(budget.truncated)
