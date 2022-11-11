import os
import logging
from validate_package_content import ValidatePackageContent, ValidateError

SUCCESS_ASSET_TYPES_DIR = 'test/success'
FAILURE_ASSET_TYPES_DIR = 'test/failure'

vpc = ValidatePackageContent()

def scan_with_validate(should_succeed):
    scan_dir = SUCCESS_ASSET_TYPES_DIR if should_succeed else FAILURE_ASSET_TYPES_DIR
    for entry in os.scandir(scan_dir):
        if entry.is_dir():
            asset_type = entry.name
            zip_files_dir = os.path.join(scan_dir, entry.name)
            for filename in os.listdir(zip_files_dir):
                zip_filename = os.path.join(zip_files_dir, filename)
                if os.path.isfile(zip_filename):
                    success, errors = vpc.validate_package(asset_type, zip_filename)
                    if should_succeed:
                        assert success, errors
                    else:
                        assert not success, f'{filename} is expected to fail'

def test_validate_success():
    scan_with_validate(True)

def test_validate_failure():
    scan_with_validate(False)
