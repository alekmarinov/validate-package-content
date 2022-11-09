#!/usr/bin/python3
import json
import os
import re
import sys
from os import listdir
from os.path import isfile, join
import pathlib


def generate_file_list(asset_type, original_package_name, file_list):
    pattern = re.compile(data["naming_pattern"])
    all_mandatory_filenames = dict()
    for entry in file_list:
        if entry.startswith("."):
            if not pattern.match(original_package_name):
                asset_type_modified = asset_type.replace("_"," ").lower()
                generate_error_message(error_file_name, f"package {original_package_name} does not follow naming convention for {asset_type_modified} assets", "", [], [], [])
                exit(1)
            asset_id = f"{pattern.match(original_package_name)[1]}"
            if asset_type == 'braille_magazine':
                asset_pattern = f"{data[f'{entry}_pattern']}"
            else:
                asset_pattern = f"{asset_id}{data[f'{entry}_pattern']}"
            all_mandatory_filenames[entry] = asset_pattern
        else:
            all_mandatory_filenames[entry] = entry
    return all_mandatory_filenames


def check_for_non_compliant_files(all_files_list, mandatory_endings_list, optional_endings_list):
    non_compliant = list()
    for file_name in all_files_list:
        if file_name.endswith(tuple(optional_endings_list)) or file_name in ignored or file_name.endswith(tuple(ignored)):
            print(f"ignore {file_name}")
            continue
        file_ending_list = pathlib.Path(file_name).suffixes
        if len(file_ending_list) > 2:
            file_ending = ''.join(file_ending_list[-2:])
        else:
            file_ending = ''.join(file_ending_list)
        if file_ending not in mandatory_endings_list and file_ending not in optional_endings_list and file_ending not in optional_endings_list.values():
            non_compliant.append(file_name)
    return non_compliant


def check_if_files_are_by_convention(all_files_list, optional_endings_list):
    invalid_files = list()
    for file_name in all_files_list:
        if file_name.endswith(tuple(optional_endings_list)):
            continue
        file_ending = ''.join(pathlib.Path(file_name).suffixes[-2:])
        if file_ending in mandatory_list:
            if re.compile(mandatory_list[file_ending]).match(file_name):
                print(f"file {file_name} is by convention")
            else:
                print(f"file {file_name} not matched by naming convention")
                invalid_files.append(file_name)
    return invalid_files


def check_for_missing_files(all_files_list, mandatory_endings_list):
    files_endings = set()

    for file_name in all_files_list:
        file_ending = ''.join(pathlib.Path(file_name).suffixes[-2:])
        if file_ending in mandatory_endings:
            files_endings.add(file_ending)
    return mandatory_endings_list - files_endings


def generate_optional(optional_endings_list):
    optional_result = dict()
    for optional_ending in optional_endings_list:
        optional_result.update(optional_ending)
    return optional_result


def check_for_optional(all_files_list, optional_endings_list):
    if asset_type == "audio_music":
        return {}
    optional_endings_list_copy = optional_endings_list.copy()
    for file_name in all_files_list:
        file_ending = ''.join(pathlib.Path(file_name).suffixes[-1])
        for key, value in optional_endings_list.items():
            if key == file_ending or value == file_ending:
                if key in optional_endings_list_copy:
                    del optional_endings_list_copy[key]
    return optional_endings_list_copy


def write_file_list(file_names_list, error_filename):
    for file_name in file_names_list:
        error_filename.writelines(f" - {file_name}{os.linesep}")


def generate_error_message(file_name, msg, second_msg, first_list, second_list, third_list):
    error_file = open(file_name, 'a')
    error_file.writelines(msg)
    write_file_list(first_list, error_file)
    error_file.writelines(second_msg)
    write_file_list(second_list, error_file)
    write_file_list(third_list, error_file)


path = sys.argv[1]
asset_type = sys.argv[2].lower()
config_name = sys.argv[3]
zipped_file_name = sys.argv[4]
f = open(config_name, 'r')
error_file_name = f"{path}/package-validation-result.txt"
datastore = json.loads(f.read())
data = None
try:
    data = datastore[asset_type]

except KeyError:
    print(f"invalid asset id! {asset_type}")
    exit(1)
ignored = list(datastore["ignored_files"])
# skipping check for marrakesh non dbg packages
if asset_type.lower() == "marrakesh" and not zipped_file_name.lower().startswith("dbg"):
    print("For Marrakesh asset only dbg packages can be checked...")
    exit(0)

optional_endings = generate_optional(data["optional"])
mandatory_endings = set((data["mandatory"]))
all_files = [f for f in listdir(path) if isfile(join(path, f))]

mandatory_list = generate_file_list(asset_type.lower(), zipped_file_name, mandatory_endings)

needles = check_for_non_compliant_files(all_files, mandatory_endings, optional_endings)
if needles:
    start_msg = f"Package {zipped_file_name} is invalid.The following non-compliant files were found in the package: {os.linesep}"
    end_msg = f'{asset_type.replace("_", " ")} asset may contain the following files:{os.linesep}'
    generate_error_message(error_file_name, start_msg, end_msg, needles, optional_endings.items(), mandatory_endings)
    exit(1)

missing_files = check_for_missing_files(all_files, mandatory_endings)
if missing_files:
    start_msg = f"Package {zipped_file_name} is invalid.The package missing following files: {os.linesep}"
    generate_error_message(error_file_name, start_msg, "", missing_files, [], [])
    exit(1)

files_not_by_convention = check_if_files_are_by_convention(all_files, optional_endings)
if files_not_by_convention:
    start_msg = f"Package {zipped_file_name} is invalid. The following file(s) in the package are not following the naming convention: {os.linesep}"
    generate_error_message(error_file_name, start_msg, "", files_not_by_convention, [], [])
    exit(1)

optional_files = check_for_optional(all_files, optional_endings)

if optional_files:
    optional_list = set()
    for key, value in optional_files.items():
        optional_list.add(key)
        optional_list.add(value)
    start_msg = f"Package {zipped_file_name} does not contain any: {optional_list} files{os.linesep}"
    generate_error_message(error_file_name, start_msg, "", [], [], [])
    exit(1)

