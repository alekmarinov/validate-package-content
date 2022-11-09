import os
import re
import json
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

    def validate_zip(self, asset_type, zipfilename):
        basezipfilename = os.path.basename(zipfilename)

        def raise_error(msg):
            raise ValidateError(
                f"Zip file name `{basezipfilename}` for asset type `{asset_type}` {msg}"
            )

        asset_type = asset_type.lower()
        if asset_type not in self.validation_rules.keys():
            raise ValidateError(f"Unknown asset type `{asset_type}`")
        rules = self.validation_rules[asset_type]
        ignored_files = self.validation_rules["ignored_files"]
        mandatory_extensions = set(rules["mandatory"])
        # FIXME: Clarify the meaning of optional list of extension to extension mappings
        # Assuming any key or value in a dict is an optional extension
        optional_extensions = set()
        for d in rules["optional"]:
            for k, v in d.items():
                optional_extensions = optional_extensions.union((k, v))
        # Validate zip file name
        naming_pattern = rules["naming_pattern"]
        matched = re.match(naming_pattern, basezipfilename)
        if not matched:
            raise_error(f"does not match pattern `{naming_pattern}`")
        # Iterate over the list of file names in the zip and apply file names validation
        name = matched[1]
        with ZipFile(zipfilename, "r") as zipf:
            # Collect file extensions
            found_extensions = set()
            for filename in zipf.namelist():
                if filename.endswith(tuple(ignored_files)):
                    continue
                ext = os.path.splitext(filename)[1]
                found_extensions.add(ext)
                filename_pattern = rules.get(f"{ext}_pattern")
                if filename_pattern is not None:
                    if re.match(filename_pattern, filename) is None:
                        raise_error(
                            f"has a file `{filename}` not matching pattern `{filename_pattern}`"
                        )
            common_extensions = found_extensions.intersection(mandatory_extensions)
            if common_extensions != mandatory_extensions:
                missing_extensions = mandatory_extensions - common_extensions
                raise_error(f"has missing files with extensions `{missing_extensions}`")
            unexpected_extensions = (
                found_extensions - mandatory_extensions - optional_extensions
            )
            if unexpected_extensions:
                raise_error(
                    f"has files with unexpected extensions `{unexpected_extensions}`"
                )
