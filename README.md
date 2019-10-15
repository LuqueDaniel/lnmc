# lnmc

Allows to create symbolic link in batches from a YAML file and consolidate them in a
specific directory.

Install:

```
pip install --user lnmc
```

Use:

```shell
$ lnmc addons.yaml ./ destination/
```

## Configuration File

lncm as first argument needs a `.yaml` or `.yml` file. The directories, sub-directories
and files that will be the target for symbolic links are specified in this file. For example.

```yaml
reporting-engine:
    - report_xlsx
purchase-workflow:
    - purchase_landed_cost
pos:
    - pos_margin
partner-contact:
    - partner_vat_unique
    - base_location_nuts
    - base_location_geonames_import
    - base_location
mis-builder:
    - mis_builder
    - mis_builder_budget
# It will create symbolic links of all subdirectories and files
l10n-spain:
```

*(Example from an tipical Odoo project)*
