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
vpc.validate_zip(asset_type, zip_filename)
```
