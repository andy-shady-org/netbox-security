# NetBox Security Plugin

## Plugin Overview

NetBox Security is a Django plugin extending NetBox's IPAM capabilities with advanced security features including address management, NAT pool configuration, custom prefix definitions, firewall policies, security zones, and security-aware IP tracking.

The plugin manages:
- **Addresses** (Address) — Security-aware IP address tracking with assignments
- **Address Collections** (AddressList, AddressSet) — Grouped address management
- **NAT Pools** (NatPool, NatPoolMember) — NAT configuration and member management
- **NAT Rules** (NatRule, NatRuleSet) — NAT rule definitions and grouping
- **Custom Prefixes** (CustomPrefix) — Custom prefix definitions and scope management
- **Firewall Policies** (FirewallFilter, FirewallFilterRule) — Firewall filter rules
- **Security Zones** (SecurityZone, SecurityZonePolicy) — Security zone definitions and policies
- **Applications** (Application, ApplicationItem, ApplicationSet) — Application definitions and grouping
- **Policers** (Policer) — Traffic policing configuration
- **Assignments** — Generic assignment system for tracking IP relationships

## Repository Structure

```text
.
├── netbox_security/
│   ├── __init__.py               — Plugin config (PluginConfig class)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── address.py            — Address model (security-aware IP tracking)
│   │   ├── address_list.py       — AddressList model
│   │   ├── address_set.py        — AddressSet model
│   │   ├── application.py        — Application model
│   │   ├── application_item.py   — ApplicationItem model
│   │   ├── application_set.py    — ApplicationSet model
│   │   ├── custom_prefix.py      — CustomPrefix model
│   │   ├── firewall_filter.py    — FirewallFilter model
│   │   ├── firewall_filter_rule.py — FirewallFilterRule model
│   │   ├── nat_pool.py           — NatPool model (NAT configuration)
│   │   ├── nat_pool_member.py    — NatPoolMember model
│   │   ├── nat_rule.py           — NatRule model
│   │   ├── natruleset.py         — NatRuleSet model
│   │   ├── policer.py            — Policer model
│   │   ├── security_zone_policy.py — SecurityZonePolicy model
│   │   └── securityzone.py       — SecurityZone model
│   ├── migrations/               — Django migrations (auto-generated)
│   ├── api/
│   │   ├── serializers.py        — DRF serializers aggregator
│   │   ├── serializers_/         — Serializers by model
│   │   │   ├── address.py
│   │   │   ├── nat_pool.py
│   │   │   ├── nat_pool_member.py
│   │   │   └── ...               — One file per model
│   │   ├── views.py              — DRF viewsets
│   │   └── urls.py               — API URL routing
│   ├── graphql/
│   │   ├── types.py              — Strawberry GraphQL types
│   │   ├── filters/              — GraphQL filter classes
│   │   └── schema.py             — GraphQL query definitions
│   ├── forms/                    — Django model forms
│   ├── tables/                   — django-tables2 table definitions
│   ├── filtersets.py             — django-filter FilterSets
│   ├── choices.py                — ChoiceSet subclasses
│   ├── views/                    — UI views (Django generic views)
│   ├── urls.py                   — URL routing
│   ├── search.py                 — SearchIndex registrations
│   ├── navigation.py             — Navigation menu registration
│   ├── constants.py              — Domain constants
│   ├── fields/                   — Custom model fields
│   ├── validators/               — Custom validators
│   ├── signals/                  — Django signal definitions
│   ├── mixins/                   — Shared mixins
│   ├── utils/                    — Utility functions
│   ├── template_content.py       — Template content providers
│   ├── templatetags/             — Django template tags
│   └── tests/
│       ├── __init__.py
│       ├── configuration.py       — Test Django settings
│       ├── test_assignment_permissions.py — Global assignment permission tests
│       ├── address/
│       │   ├── __init__.py
│       │   ├── test_api.py        — Address REST API tests
│       │   ├── test_models.py     — Address model tests
│       │   ├── test_views.py      — Address UI view tests
│       │   ├── test_forms.py      — Address form tests
│       │   └── ...
│       ├── address_set/
│       │   ├── test_*.py
│       │   └── ...
│       ├── application/
│       │   ├── test_*.py
│       │   └── ...
│       ├── custom_prefix/
│       │   ├── test_*.py
│       │   └── ...
│       ├── firewall_filter/
│       │   ├── test_*.py
│       │   └── ...
│       ├── nat_pool/
│       │   ├── test_api.py
│       │   ├── test_filtersets.py
│       │   ├── test_member_safety.py — NatPoolMember safety tests
│       │   ├── test_views.py
│       │   └── ...
│       ├── nat_rule_set/
│       │   ├── test_*.py
│       │   └── ...
│       ├── policer/
│       │   ├── test_*.py
│       │   └── ...
│       └── securityzone/
│           ├── test_*.py
│           └── ...
├── docs/
│   ├── using_netbox_security.md
│   └── img/                       — Documentation images
├── pyproject.toml                — Package metadata (version, dependencies)
├── README.md
├── LICENSE
├── SECURITY.md
├── ruff.toml                     — Linter configuration
├── AGENTS.md                     — This file
├── CHANGELOG.md
└── netbox-plugin.yaml            — Plugin manifest (NetBox 4.6+)
```

## Architecture

### Domain Logic (Separation of Concerns)

Each model domain (Address, NatPool, NatPoolMember, CustomPrefix) owns:

- **Models** — Data structure and validation in `models/<domain>.py`
- **Serializers** — REST/GraphQL representation in `api/serializers_/<domain>.py`
- **Forms** — UI input handling in `forms/<domain>.py`
- **Views** — UI and API endpoints in `views/<domain>.py`
- **Filtersets** — Query filtering in `filtersets.py` (shared across domains)
- **Tables** — List rendering in `tables/<domain>.py`
- **Tests** — Behavior verification in `tests/<domain>/test_*.py`

Never reach across domains except via foreign keys (ForeignKey, ManyToMany) or public APIs.

### Assignment System

Security-aware assignment tracking via:
- **Generic assignments** (GenericForeignKey) on Address model
- **Permission gating** — Only users with explicit permissions can assign/modify
- **`GenericAssignmentValidationMixin`** — Validates assignment targets are accessible
- **`restrict(user, permission)`** — Filters results by user permission

Implementation pattern:
- REST: serializers use `GenericAssignmentValidationMixin` and apply `.restrict(user, "view")`
- GraphQL: types exclude assignment fields from mutations; resolvers are read-only
- Form validation: guards against invalid or inaccessible assignment targets

### REST API (DRF)

Located in `api/` with structure:

```
api/
├── serializers.py        — Aggregator (imports from serializers_/)
├── serializers_/
│   ├── address.py
│   ├── nat_pool.py
│   ├── nat_pool_member.py
│   └── custom_prefix.py  — One file per model
├── views.py              — ViewSets (one per model)
└── urls.py               — NetBoxRouter registration
```

**Serializer patterns:**
- Use `PrimaryModelSerializer` as base
- Include `url` field (absolute URL via `HyperlinkedIdentityField`)
- Add `GenericAssignmentValidationMixin` for assignment-aware validation
- Override `create()` / `update()` for permission-aware logic
- Use `restrict(user, "view")` / `restrict(user, "change")` for permission filtering

**ViewSet patterns:**
- Use standard CRUD mixins from `netbox.api.views`
- Restrict querysets with `.restrict(request.user, 'view')`
- Add custom `@action()` methods for domain-specific operations
- Never repeat querysets — use `get_queryset()` once
- Apply permission checks at the API layer

### GraphQL (Strawberry)

Located in `graphql/` with structure:

```
graphql/
├── types.py              — Strawberry types (one per model)
├── filters/
│   └── types.py          — Filter classes for each model
└── schema.py             — Root Query definitions
```

**Type patterns:**
- Use `@strawberry_django.type()` decorator
- Inherit from `PrimaryObjectType`
- Explicitly declare all exposed fields (avoid `fields="__all__"` for large models)
- **Exclude assignment fields** from mutations: `exclude=["assigned_object_type", "assigned_object_id"]`
- Make `assigned_object` read-only via `@strawberry_django.field()`
- Declare FK/M2M relations using lazy imports: `strawberry.lazy("module.path")`

**Filter patterns:**
- Use `django_filter.FilterSet` subclass in `filters/types.py`
- Declare explicit filterable fields
- Register in the type via `filters=...` parameter

**Permission model:**
- GraphQL queries use `.restrict(user, "view")` automatically
- No GraphQL mutations for assignments (read-only interface)
- Resolvers never write assignment data

### UI Views

Located in `views/` and registered via `@register_model_view()`:

```python
@register_model_view(Address, name='list', detail=False)
class AddressListView(generic.ObjectListView):
    queryset = Address.objects.all()
    table = AddressTable
    filterset = AddressFilterSet

@register_model_view(Address)
class AddressView(generic.ObjectView):
    queryset = Address.objects.all()
    template_name = 'netbox_security/address.html'
```

**View patterns:**
- List views: inherit from `generic.ObjectListView`
- Detail views: inherit from `generic.ObjectView`
- Edit views: inherit from `generic.ObjectEditView`
- Delete views: inherit from `generic.ObjectDeleteView`
- Bulk views: inherit from `generic.BulkEditView` / `BulkDeleteView`
- Never add `select_related()` or `prefetch_related()` manually — the table/serializer handles it
- Apply `.restrict(request.user, 'view')` for permission-aware display

### Forms

Located in `forms/` and used for UI input:

```python
class AddressForm(NetBoxModelForm):
    class Meta:
        model = Address
        fields = [...]
    
    def clean(self):
        super().clean()
        # Domain-specific validation
        # Check assignment permissions if modified
```

**Form patterns:**
- Use `NetBoxModelForm` as base
- Override `clean()` for cross-field validation (not per-field)
- Never perform database queries in `__init__()` — use `clean()` or lazy evaluation
- Add help text via `help_text=` on fields
- Filter FK choices via `queryset=...` on `ModelChoiceField`
- Validate assignment targets are accessible if assignment is modified

### Filtersets

Located in `filtersets.py` (shared across all models):

```python
class AddressFilterSet(NetBoxModelFilterSet):
    vrf_id = ModelMultipleChoiceFilter(
        queryset=VRF.objects.all(),
        field_name='vrf',
        label='VRF (ID)',
    )
    vrf = ModelMultipleChoiceFilter(
        queryset=VRF.objects.all(),
        field_name='vrf__name',
        to_field_name='name',
        label='VRF (Name)',
    )
    
    class Meta:
        model = Address
        fields = ['address', 'vrf', 'status']
```

**FilterSet patterns:**
- **FK filters MUST be explicit** — add both `<field>_id` (ID lookup) and `<field>` (name/slug lookup)
- Never rely on `Meta.fields` auto-generation for FK relations
- Use `ModelMultipleChoiceFilter` for FK/M2M, not just `Filter`
- Update UI form in `forms/filtersets.py` to expose the field
- Apply `.restrict(user, 'view')` for permission-aware filtering

### Tables

Located in `tables/` and used for list rendering:

```python
class AddressTable(NetBoxTable):
    address = tables.LinkColumn(
        viewname='plugins:netbox_security:address',
        args=[tables.A('pk')],
    )
    vrf = tables.Column(
        linkify=True,
    )
    assigned_object = tables.Column(
        verbose_name='Assigned Object',
    )
    actions = TemplateColumn(template_name='...')
    
    class Meta:
        model = Address
        fields = ['address', 'vrf', 'status', 'assigned_object', 'actions']
```

**Table patterns:**
- Use `NetBoxTable` as base
- LinkColumn for the primary object (via `viewname` and `args`)
- LinkColumn for FK relations (linkify=True)
- TemplateColumn for custom formatting (assignments, etc.)
- Always include an `actions` column

### Choices

Located in `choices.py` and used throughout:

```python
class AddressStatusChoices(ChoiceSet):
    CHOICES = (
        ('active', 'Active'),
        ('reserved', 'Reserved'),
        ('deprecated', 'Deprecated'),
    )
```

**Choice patterns:**
- Inherit from `ChoiceSet`
- Define CHOICES as tuple of (value, label) pairs
- Reference in model via `choices=AddressStatusChoices`

### Constants

Located in `constants.py` for domain facts:

```python
ASSIGNMENT_MODELS = (
    ('dcim', 'interface'),
    ('virtualization', 'vminterface'),
    ...
)
```

**Constants patterns:**
- One home per threshold, format, or schema fact
- Document why each constant exists
- Use in models, API, forms — reference by import, never duplicate

### Validators and Fields

**Custom Validators** (in `validators/`):
- Domain-specific validation logic (IP format checks, range validation, etc.)
- Reusable across forms and serializers

**Custom Fields** (in `fields/`):
- Custom model fields for specialized data (IP networks, CIDR notation, etc.)
- Widget support for UI forms

### Signals

Located in `signals/` for side effects:

```python
# signals/nat_pool_member.py
"""Signal module for NatPoolMember.

NatPoolMember creation must not mutate referenced IPAM objects or overwrite any
existing assignment on an IP address.
"""
```

**Signal patterns:**
- **Never mutate objects in signals** — side effects go in model methods or serializers
- Document the intent of each signal
- Use `@receiver()` with explicit signal names
- Keep signal handlers short; call model methods for complex logic

### Utilities

Located in `utils/` for shared logic:

```python
# utils/__init__.py
def get_visible_assignment_target(user, target_model, target_id):
    """Check if user can view assignment target."""
```

**Utility patterns:**
- Extract reusable logic from models, views, serializers
- One file per concern (assignment_utils.py, validation_utils.py, etc.)
- Use for both REST and UI layers

## Commands

All commands run from the **NetBox** `netbox/` directory (not the plugin directory).

```bash
# Development setup (from plugin repo root, then cd to NetBox)
export NETBOX_CONFIGURATION=netbox.configuration_testing
python manage.py runserver

# Testing (from NetBox netbox/ directory)
export NETBOX_CONFIGURATION=netbox.configuration_testing
python manage.py test netbox_security

# Single test module
python manage.py test netbox_security.tests.test_api

# Faster runs
python manage.py test --keepdb --parallel 4 netbox_security

# Migrations
python manage.py makemigrations netbox_security

# Linting
ruff check netbox_security/  # from plugin root
```

## Development Workflow

### Add a New Model

1. **Define model** in `models/<domain>.py`
   - Inherit from `PrimaryModel` for full feature support (custom fields, tags, etc.)
   - Add validation in `clean()` or field validators
   - Override `get_absolute_url()` to return canonical URL
   - Use `__str__()` for readable display
   - Consider assignment support via `GenericForeignKey`

2. **Generate migration**
   ```bash
   python manage.py makemigrations netbox_security
   ```

3. **Wire up full surface area:**
   - Serializer in `api/serializers_/<domain>.py` → imported in `api/serializers.py`
   - ViewSet in `api/views.py` → registered in `api/urls.py`
   - FilterSet in `filtersets.py`
   - Form in `forms/<domain>.py`
   - Table in `tables/<domain>.py`
   - UI views in `views/<domain>.py` → registered with `@register_model_view()`
   - Search index in `search.py` if needed
   - GraphQL type in `graphql/types.py` → registered in `graphql/schema.py`

4. **Add tests** in `tests/<domain>/test_*.py` covering:
   - Model creation, validation, constraints
   - API CRUD + filtering + bulk operations
   - UI views (list, create, edit, delete)
   - Forms (validation rules)
   - Filtersets (query behavior)
   - GraphQL queries
   - Assignments (if applicable)

### Add Assignment Support

1. **Add fields to model:**
   ```python
   class MyModel(PrimaryModel):
       assigned_object_type = ForeignKey(
           to='contenttypes.ContentType',
           limit_choices_to=MY_ASSIGNMENT_MODELS,
           on_delete=models.CASCADE,
       )
       assigned_object_id = PositiveBigIntegerField()
       assigned_object = GenericForeignKey(
           ct_field='assigned_object_type',
           fk_field='assigned_object_id',
       )
   ```

2. **Add serializer validation:**
   ```python
   class MySerializer(PrimaryModelSerializer, GenericAssignmentValidationMixin):
       class Meta:
           model = MyModel
           fields = ['assigned_object_type', 'assigned_object_id', ...]
   ```

3. **Exclude from GraphQL mutations:**
   ```python
   @strawberry_django.type(MyModel, exclude=['assigned_object_type', 'assigned_object_id'])
   class MyType(PrimaryObjectType):
       assigned_object = strawberry_django.field(read_only=True)
   ```

### Add a REST API Endpoint

1. Create serializer in `api/serializers_/<domain>.py`
2. Add viewset in `api/views.py`
3. Register route in `api/urls.py` via `NetBoxRouter.register()`
4. Add test in `tests/test_api.py`
5. Apply permission filters: `.restrict(request.user, 'view')`

### Add a GraphQL Query

1. Add type to `graphql/types.py`
2. Register query field in `graphql/schema.py`
3. Add test in `tests/test_api.py` (test_graphql_*)
4. Ensure assignment fields are excluded/read-only

## Testing Patterns

### Model Tests

```python
class AddressTest(TestCase):
    def setUp(self):
        self.vrf = VRF.objects.create(name='Test')
        self.address = Address.objects.create(
            address='192.0.2.1/32',
            vrf=self.vrf,
        )
    
    def test_get_absolute_url(self):
        url = self.address.get_absolute_url()
        self.assertTrue(url.startswith('/plugins/'))
    
    def test_clean_validation(self):
        obj = Address(address='invalid', vrf=self.vrf)
        self.assertRaises(ValidationError, obj.clean)
```

### API Tests

```python
class AddressAPITest(APIViewTestCase):
    def test_list(self):
        response = self.client.get('/api/plugins/security/addresses/')
        self.assertEqual(response.status_code, 200)
    
    def test_create(self):
        data = {'address': '192.0.2.2/32', 'vrf': self.vrf.pk}
        response = self.client.post('/api/plugins/security/addresses/', data)
        self.assertEqual(response.status_code, 201)
    
    def test_assignment_validation(self):
        # Test that invalid assignment targets are rejected
        data = {
            'address': '192.0.2.3/32',
            'vrf': self.vrf.pk,
            'assigned_object_type': 'invalid_app.InvalidModel',
            'assigned_object_id': 999,
        }
        response = self.client.post('/api/plugins/security/addresses/', data)
        self.assertEqual(response.status_code, 400)
```

### GraphQL Tests

```python
def test_graphql_list(self):
    query = '''
        query {
            netboxSecurityAddressList {
                address
                vrf { id }
                assignedObject { __typename }
            }
        }
    '''
    response = self.client.post('/graphql/', {'query': query})
    self.assertNotIn('errors', response.json())

def test_graphql_assignment_readonly(self):
    # Test that assignment fields cannot be mutated
    mutation = '''
        mutation {
            updateAddress(
                id: "ADDRESS_ID"
                data: { assignedObjectType: "dcim.interface" }
            ) { address }
        }
    '''
    response = self.client.post('/graphql/', {'query': mutation})
    self.assertIn('errors', response.json())
```

## Conventions and Patterns

### Encapsulation

- **Public API:** Serializers, views, model methods accessed by external code
- **Internal implementation:** Private methods (prefixed with `_`), internal helpers
- **Cross-domain communication:** Always through FK relations or public serializers
- **Avoid:** Importing domain models outside their app; reaching into another domain's implementation

### Assignment Permissions

- **REST:** Use `GenericAssignmentValidationMixin` and `.restrict(user, "view")`
- **GraphQL:** Exclude write fields; make resolvers read-only
- **Forms:** Validate assignment targets are accessible to the user
- **Views:** Apply `.restrict(user, 'view')` on display

### Cohesion / Coupling

- One rule change touches one place (one model, one serializer, etc.)
- Duplicate logic → move to shared module (utils, validators, constants)
- FK relations are okay; circular dependencies are not

### DRY (Don't Repeat Yourself)

- Grep before writing logic
- One home per threshold, format, schema fact (use `constants.py`)
- Shared helpers in `utils.py` or domain-specific modules
- Don't abstract coincidental similarity

### KISS / YAGNI

- Simplest working shape; no speculative hooks or frameworks
- Prefer function over class
- No "future-proofing" code

### Single Responsibility

- If you describe something with "and", split it
- Names say intent; comments say why
- Each model owns one business domain

### Depend on Contracts

- Domain code takes and returns plain Python values
- Never import Django request, templates, or app-specific classes in domain logic
- Serializers are the contract between API and domain

### Composition > Inheritance

- Use mixins (like `GenericAssignmentValidationMixin`) for behavior
- Avoid deep inheritance hierarchies
- Open/closed principle: extend via methods, not base classes

### Fail Fast

- Validate at entry points (serializers, forms, API)
- Never swallow errors silently
- Use model `clean()` and `clean_<field>()` for validation
- Check permissions early in request handlers

### No Business Logic in Templates

- Templates display values; they never compute
- All rules/arithmetic live in models or serializers
- If-logic in templates is a sign logic is in the wrong place

### No Side Effects in Signals

- Signals should not mutate objects or change state
- Complex logic goes in model methods or serializers
- Document why each signal exists

## Troubleshooting

- **ImportError on plugin load** — Check circular imports; avoid importing views in models
- **Assignment validation fails** — Ensure target model is in `ASSIGNMENT_MODELS` constant; check permissions
- **GraphQL "field not found"** — Declare field explicitly in type; check for lazy import issues
- **Permission denied on assignment** — Verify user has "view" permission on target model
- **FK filter not working** — Add explicit `<field>_id` FilterSet field; don't rely on auto-generation
- **Tests fail** — Set `NETBOX_CONFIGURATION=netbox.configuration_testing`; use `--keepdb` for speed
- **Signal side effect mutates object** — Move mutation logic to model method or serializer

## Plugin Configuration & Initialization

### PluginConfig Class

Located in `netbox_security/__init__.py`:

```python
from netbox.plugins import PluginConfig

class SecurityConfig(PluginConfig):
    name = 'netbox_security'
    verbose_name = 'NetBox Security'
    version = '1.0.0'
    author = 'Your Name'
    author_email = 'your.email@example.com'
    description = 'Advanced security features for NetBox IPAM'
    base_url = 'security'
    required_settings = []  # Required config.py settings
    optional_settings = []  # Optional config.py settings
    default_settings = {}   # Default values for optional settings
    
    def ready(self):
        """Called when the app is ready for use."""
        super().ready()
        # Import signals, register search, etc.
        from . import signals  # noqa
```

### NetBox Configuration

Add to `netbox/netbox/configuration.py`:

```python
PLUGINS = [
    'netbox_security',
]

PLUGINS_CONFIG = {
    'netbox_security': {
        # Optional: custom configuration here
    },
}
```

### Environment Variables

Plugin can read settings via environment variables:

```python
import os
OPTIONAL_SETTINGS = {
    'ASSIGNMENT_ENFORCEMENT': os.getenv('SECURITY_ASSIGNMENT_ENFORCEMENT', 'true').lower() == 'true',
}
```

## Versioning & Release Strategy

### Version Locations

Update version in these locations for each release:

1. **`pyproject.toml`** — Source of truth
   ```toml
   [project]
   version = "1.2.0"
   ```

2. **`netbox_security/__init__.py`** — Optional (for backward compatibility)
   ```python
   __version__ = '1.2.0'
   ```

3. **`README.md`** — Update installation instructions if needed

### Changelog Format

Maintain `CHANGELOG.md` or `docs/release-notes/` following:

```markdown
## [1.2.0] - 2026-10-01

### Added
- New model support
- New security feature

### Changed
- Breaking changes (major versions only)
- Permission model updates

### Fixed
- Assignment validation fix
- Security vulnerability fix

### Deprecated
- Deprecation notice (3+ version warning before removal)

### Security
- Critical security fixes (always separate)
```

### Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` with all changes
3. Test: `python manage.py test netbox_security --keepdb`
4. Lint: `ruff check netbox_security/`
5. Tag: `git tag v1.2.0` and push
6. Build: `python -m build`
7. Publish: `twine upload dist/*`

### Backward Compatibility

- **Patch releases** (1.0.1 → 1.0.2): Bug fixes, zero breaking changes
- **Minor releases** (1.0 → 1.1): New features, backward compatible
- **Major releases** (1.0 → 2.0): Breaking changes allowed
- **Deprecation cycle**: Announce in minor version, remove in next major

## Database Schema & Migrations

### When to Migrate

**Always run migrations when:**
- Adding/removing/renaming fields
- Changing field types or constraints
- Adding new models
- Modifying indexes

**Avoid migrations for:**
- Changing model method implementations
- Changing form field display
- Changing validator/choice logic (no schema change)

### Migration Best Practices

```python
# Good: Include data migration for status changes
class Migration(migrations.Migration):
    operations = [
        migrations.AddField(
            model_name='address',
            name='status',
            field=models.CharField(
                max_length=50,
                choices=StatusChoices,
                default='active',
            ),
        ),
        migrations.RunPython(set_default_status),  # Data migration
    ]

def set_default_status(apps, schema_editor):
    Address = apps.get_model('netbox_security', 'Address')
    Address.objects.filter(status__isnull=True).update(status='active')
```

### Handling Large Migrations

For tables with millions of rows:
- Use `batch_size` parameter
- Create indexes after data migration (faster)
- Test on production-sized data before release
- Provide rollback plan

### Forward/Backward Compatibility

- Don't set `null=False` without default on new fields
- Add new fields with `null=True` initially, tighten constraints later
- Never delete columns without deprecation cycle
- Keep old field names if renaming (map via property)

## Performance & Optimization

### Query Optimization Patterns

**Problem: N+1 queries**
```python
# Bad: N+1 query
for address in Address.objects.all():
    print(address.vrf.name)  # Query per address

# Good: Use select_related for FK
addresses = Address.objects.select_related('vrf')

# Good: Use prefetch_related for assignments
addresses = Address.objects.prefetch_related('assigned_object')
```

**Strategy: Let table/serializer handle prefetching**
- List views: Table class auto-prefetches needed fields
- Detail views: Serializer defines `to_represent` fields
- API viewsets: Override `get_queryset()` once, never per-action

### Caching Patterns

Use Django's cache framework:

```python
from django.core.cache import cache

def get_address_assignments(address_id):
    cache_key = f'address:{address_id}:assignments'
    data = cache.get(cache_key)
    if data is None:
        data = fetch_assignments(address_id)
        cache.set(cache_key, data, timeout=3600)  # 1 hour
    return data
```

Invalidate on model save:

```python
@receiver(post_save, sender=Address)
def invalidate_address_cache(sender, instance, **kwargs):
    cache.delete(f'address:{instance.pk}:assignments')
```

### Indexing Strategy

Add database indexes for:
- Foreign keys (automatic in Django)
- Frequently filtered fields (`filterset` lookups)
- Sorting fields in list views
- Assignment fields (for permission queries)

```python
class Address(PrimaryModel):
    status = models.CharField(
        choices=StatusChoices,
        db_index=True,  # Indexed for filtering
    )
    vrf = ForeignKey(...)  # Auto-indexed by Django
    
    class Meta:
        indexes = [
            models.Index(fields=['vrf', 'status']),  # Composite
            models.Index(fields=['assigned_object_type', 'assigned_object_id']),
        ]
```

### Bulk Operation Handling

For imports/bulk operations:

```python
# Good: Bulk create with batch_size
objects = [Address(...) for _ in range(10000)]
Address.objects.bulk_create(objects, batch_size=1000)

# Good: Bulk update
Address.objects.filter(status='old').update(status='new')

# Avoid: Loop with individual save()
for address in addresses:
    address.status = 'new'
    address.save()  # Bad: N queries
```

## Search & Indexing

### SearchIndex Implementation

Located in `search.py`:

```python
from netbox.search import SearchIndex, register_search

@register_search
class AddressIndex(SearchIndex):
    model = Address
    fields = (
        ('address', 100),            # Field, weight (higher = more relevant)
        ('vrf__name', 90),
        ('assigned_object', 50),
        ('description', 25),
    )
```

### Indexing Strategy

- **Weight 100+**: Primary object identity (address, ID)
- **Weight 50-99**: Related objects, VRF, assignment
- **Weight 25-49**: Descriptions, comments
- **Weight < 25**: Content fields (rarely useful)

### Full-Text Search Performance

- Index only searchable fields (not IDs, booleans)
- Use composite indexes for common searches
- Limit to 10-15 searchable fields per model
- Test with realistic data volume (millions of IPs)

## CI/CD & GitHub Workflows

### GitHub Actions Configuration

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main, feature ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.12', '3.13']
    
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -e .
    
    - name: Lint with ruff
      run: ruff check netbox_security/
    
    - name: Run tests
      run: |
        export NETBOX_CONFIGURATION=netbox.configuration_testing
        python manage.py test netbox_security --keepdb
```

### Coverage Requirements

Set minimum coverage in CI:

```bash
coverage run --source='netbox_security' manage.py test
coverage report --fail-under=80  # 80% minimum
```

## Custom Management Commands

Commands located in `netbox_security/management/commands/`:

```python
# sync_assignments.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Synchronize security assignments with IPAM'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without changes',
        )
    
    def handle(self, *args, **options):
        if options['dry_run']:
            self.stdout.write('Would sync X assignments')
        else:
            # Perform sync
            self.stdout.write(
                self.style.SUCCESS('Successfully synced X assignments')
            )
```

Run via:

```bash
python manage.py sync_assignments --dry-run
```

## Translation/i18n

### Mark Translatable Strings

Use `gettext_lazy` for UI strings:

```python
from django.utils.translation import gettext_lazy as _

class Address(PrimaryModel):
    status = models.CharField(
        max_length=50,
        choices=StatusChoices,
        verbose_name=_('Status'),  # Translated label
        help_text=_('Address operational status'),  # Translated help
    )
```

In templates:

```html
{% load i18n %}
<h1>{% trans "Security Addresses" %}</h1>
```

### Extract Translations

```bash
# Extract strings
django-admin makemessages -l es -l fr

# Compile translations
django-admin compilemessages
```

## Security Best Practices

### Input Validation

Always validate at entry points:

```python
class AddressForm(NetBoxModelForm):
    def clean_address(self):
        address = self.cleaned_data['address']
        # Validate CIDR notation, IP format
        try:
            IPNetwork(address)
        except AddrFormatError:
            raise ValidationError('Invalid IP address/network')
        return address
```

### Permission Checking

Apply permission checks at all layers:

```python
# API viewset
queryset = Address.objects.restrict(request.user, 'view')

# Form: Validate assignment target is accessible
if not request.user.has_perm('ipam.view_ipaddress'):
    # Prevent assignment to IP addresses user can't access

# Template
{% if perms.netbox_security.delete_address %}
    <button>Delete Address</button>
{% endif %}
```

### SQL Injection Prevention

Never use string concatenation with user input:

```python
# Bad
queryset = Address.objects.raw(f"SELECT * FROM address WHERE address = '{user_input}'")

# Good
from django.db.models import Q
queryset = Address.objects.filter(address=user_input)
```

### XSS Prevention

Use template escaping and `mark_safe()` carefully:

```html
{# Bad: User input directly #}
<p>{{ address.description }}</p>

{# Good: Django auto-escapes #}
{{ address.description }}

{# If HTML needed: sanitize first #}
{{ address.html_description|safe }}
```

### Secure Defaults

- All querysets should use `.restrict(user, 'view')`
- Forms should validate assignments are accessible
- Serializers should not expose sensitive fields
- GraphQL should exclude assignment write fields
- Never store credentials or secrets in models

## Debugging & Profiling

### Debug Logging

Enable debug output:

```python
import logging
logger = logging.getLogger('netbox_security')
logger.debug(f'Processing address {address.id}')
```

In `configuration.py`:

```python
LOGGING = {
    'loggers': {
        'netbox_security': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

### Query Profiling

Use Django Debug Toolbar:

```python
# In development configuration.py
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```

Or use `django-silk`:

```python
pip install django-silk
# Then /silk/ endpoint shows all requests, queries, etc.
```

### Breakpoint Debugging

Run tests with breakpoints:

```bash
python -m pdb manage.py test netbox_security.tests.test_api
```

Or use IDE breakpoints + `python manage.py test --pdb`

## Documentation Requirements

### README Structure

Should include:

```markdown
# NetBox Security

## Installation

```bash
pip install netbox-security
```

## Configuration

Add to configuration.py...

## Features

- Advanced IP address tracking
- NAT pool management
- Firewall policies
- Security zones

## Usage

Example: Create an address...

## Assignment System

How assignments work...

## API

REST endpoints...

## GraphQL

Query examples...

## Support

Issues: https://github.com/.../issues
```

### Docs Folder Organization

```
docs/
├── using_netbox_security.md  — User guide
├── api.md                     — REST/GraphQL docs
├── assignments.md             — Assignment system docs
├── configuration.md           — Config options
├── troubleshooting.md         — Common issues
└── img/                       — Screenshots
```

### Model Documentation

Add docstrings to models:

```python
class Address(PrimaryModel):
    """
    Security-aware IP address tracking.
    
    Addresses track IP usage and can be assigned to infrastructure
    objects (interfaces, etc.) for security policy enforcement.
    
    Attributes:
        address: IP address/network in CIDR notation
        vrf: VRF containing this address
        status: Address operational status
        assigned_object: Infrastructure object using this address
    """
```

### Example Configurations

Provide in `docs/examples/`:

```python
# docs/examples/basic_setup.py
# Example: Create address with assignment

from netbox_security.models import Address
from ipam.models import VRF, IPAddress

vrf = VRF.objects.get(name='default')
address = Address.objects.create(
    address='192.0.2.1/32',
    vrf=vrf,
)
# Assignment happens in REST/form layer
```

## References

- NetBox core AGENTS.md: [`/netbox/AGENTS.md`](../netbox_src_plugins/netbox/AGENTS.md)
- Plugin development guide: [NetBox docs/plugins](https://docs.netbox.dev/en/stable/plugins/development/)
- DRF documentation: [Django REST Framework](https://www.django-rest-framework.org/)
- Strawberry GraphQL: [Strawberry Django](https://strawberry-graphql.com/docs/django)
- Security plugin docs: [`docs/using_netbox_security.md`](./docs/using_netbox_security.md)

