"""
Command line interface to validate_package_content package

usage:
    validate_package_content <asset_type> <zip_file>
"""

import os
import sys
import argparse
import logging
from validate_package_content import ValidatePackageContent


def main():
    parser = argparse.ArgumentParser(
        prog="validate-package-content",
        description="Validates zip package content according to predefined rules",
        epilog="Github: https://github.com/...",
    )
    parser.add_argument("asset_type")
    parser.add_argument("zip_file")
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()
    logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.DEBUG if args.verbose else logging.INFO)
    vpc = ValidatePackageContent()
    success, errors = vpc.validate_package(args.asset_type, args.zip_file)
    if errors:
        print(f'{len(errors)} error{"s" if len(errors) > 1 else ""} found from applying `{args.asset_type}` rules on `{args.zip_file}`:', file=sys.stderr)
        print("\n".join([f"  {i+1}: {error}" for i, error in enumerate(errors)]), file=sys.stderr)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
