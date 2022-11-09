"""
Command line interface to validate_package_content package

usage:
    validate_package_content <asset_type> <zip_file>
"""

import os
import argparse
from validate_package_content import ValidatePackageContent


def main():
    parser = argparse.ArgumentParser(
        prog="validate-package-content",
        description="Validates zip package content according to predefined rules",
        epilog="Github: https://github.com/...",
    )
    parser.add_argument("asset_type")
    parser.add_argument("zip_file")
    args = parser.parse_args()

    vpc = ValidatePackageContent()
    vpc.validate_zip(args.asset_type, args.zip_file)


if __name__ == "__main__":
    main()
