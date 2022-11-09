import os
from validate_package_content import ValidatePackageContent, ValidateError

TEST_ASSET_TYPES_DIR = 'test'

def test_validate_success():
    config_file = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'validation_rules.json')
    vpc = ValidatePackageContent(config_file=config_file)
    for entry in os.scandir(TEST_ASSET_TYPES_DIR):
        if entry.is_dir():
            asset_type = entry.name
            zip_files_dir = os.path.join(TEST_ASSET_TYPES_DIR, entry.name)
            for filename in os.listdir(zip_files_dir):
                zip_filename = os.path.join(zip_files_dir, filename)
                if os.path.isfile(zip_filename) and zip_filename.lower().endswith('.zip'):
                    vpc.validate_zip(asset_type, zip_filename)
