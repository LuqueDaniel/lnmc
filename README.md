# lnmc

[![PyPI](https://img.shields.io/pypi/v/lnmc)](https://pypi.org/project/lnmc/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lnmc)
![PyPI - License](https://img.shields.io/pypi/l/lnmc)
[![Build Status](https://travis-ci.com/LuqueDaniel/lnmc.svg?branch=master)](https://travis-ci.com/LuqueDaniel/lnmc)
[![Build status](https://ci.appveyor.com/api/projects/status/mok7jp052rv7j4hb/branch/master?svg=true)](https://ci.appveyor.com/project/LuqueDaniel/lnmc/branch/master)
[![Coverage Status](https://coveralls.io/repos/github/LuqueDaniel/lnmc/badge.svg?branch=master)](https://coveralls.io/github/LuqueDaniel/lnmc?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Allows to create symbolic link in batches from a YAML file and consolidate them in a
specific directory.

Install:

```shell
pip install lnmc
```

Dev Install:
```shell
git clone https://github.com/LuqueDaniel/lnmc.git
cd lnmc
pip install -e ".[test,dev]"
```

Usege:

```shell
lnmc addons.yml ./ destination/
```

## Configuration File

lnmc as first argument needs a `.yaml` or `.yml` file. The directories, sub-directories
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

(Example of a typical Odoo project)
