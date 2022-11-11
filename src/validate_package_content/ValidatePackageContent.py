import os
import re
import json
import logging
from zipfile import ZipFile


class ValidateError(Exception):
    pass


class ValidatePackageContent:
    def __init__(self, config_file=None):
        if not config_file:
            # the distributed config file is up one folder in the source tree relative to this script file
            config_file = os.path.join(
                os.path.realpath(os.path.dirname(__file__)), 
                '..',
                "validation_rules.json"
            )
        with open(config_file, "r", encoding="utf-8") as fd:
            self.validation_rules = json.load(fd)

    def validate_package(self, asset_type, pkg_filename):
        logging.debug(f'Applying `{asset_type}` rules on `{pkg_filename}`')
        base_pkg_filename = os.path.basename(pkg_filename)
        asset_type = asset_type.lower()
        errors = []

        def collect_error(msg):
            logging.error(msg)
            errors.append(msg)

        if asset_type not in self.validation_rules.keys():
            raise ValidateError(f"Unknown asset type `{asset_type}`")
        asset_rules = self.validation_rules[asset_type]
        # Check if package name matching the pattern
        package_pattern = asset_rules["package"]
        if not re.match(package_pattern, base_pkg_filename):
            collect_error(f"does not match pattern `{package_pattern}`")

        # Walk through the package files and apply each rule until match
        file_rules = asset_rules["files"] + self.validation_rules["*"]["files"]

        # Array of non optional rules expecting to be supplied by the packaged files
        required_rules = [ rule for rule in file_rules if not rule["optional"] ]

        # Maps non optional rule having a count constraint to the number of remaining files to match the rule
        counted_rules = { rule["pattern"]: rule["count"] for rule in required_rules if 'count' in rule }
        with ZipFile(pkg_filename, "r") as zipf:
            for file in zipf.namelist():
                is_matched = False
                for rule in file_rules:
                    pattern = rule["pattern"]
                    if re.match(pattern, file):
                        is_matched = True
                        logging.debug(f'`{file}` is matched by `{pattern}`')
                        if not rule["optional"]:
                            if 'count' in rule:
                                if counted_rules[pattern] == 0:
                                    collect_error(f'too many files matching {rule}')
                                else:
                                    counted_rules[pattern] -= 1
                            else:
                                # Marking non count aware rule as supplied by removing it
                                if rule in required_rules:
                                    required_rules.remove(rule)
                        break
                if not is_matched:
                    collect_error(f'`{file}` not matching any rules')

        # Check if there are remaining not supplied rules
        for rule in required_rules:
            if rule["pattern"] in counted_rules:
                if counted_rules[rule["pattern"]] > 0:
                    collect_error(f'not enough files matching {rule}')
            else:
                collect_error(f"no file matched by {rule}")

        logging.debug(f'`{pkg_filename}` is{" not" if errors else ""} matching `{asset_type}` rules')
        return len(errors) == 0, errors
