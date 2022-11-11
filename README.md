# validate-package-content

## What

Validates zip package content according to predefined rules

## How

### Usage from command line

*validate-package-content asset_type zip_file*

Example:
    
    validate-package-content braille_magazine test/braille_magazine/br.newyorktimesbookreview_2022-10-16.zip

### Usage from python

```python
from validate_package_content import ValidatePackageContent

vpc = ValidatePackageContent()
vpc.validate_package(asset_type, zip_filename)
```

## Validation rules json format (*src/validation_rules.json*)

```json
{
    "<asset_type>": {
        "package": "<package_file_pattern>",
        "files": [
            {
                "pattern": "<file_pattern>",
                "optional": <boolean>,
                "count": <number>
            }
        ]
    },
    "*": {
        "files": [
        ]
    }
}

```
| Plugin | README |
| ------ | ------ |
| <asset_type> | The name of the asset type, e.g. braille_magazine |
|<package_file_pattern> | Python regexp matching the name of the package |
|<file_pattern> | Python regexp matching a file inside the package |
| optional | False if the pattern is mandatory, else optional |
| count | The exact number of files should match the pattern |
| "*": { | Rules applied on all asset types |
