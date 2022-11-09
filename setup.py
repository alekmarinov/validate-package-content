import os
import setuptools

setuptools.setup(name='ValidatePackageContent',
    version='1.0',
    description='Validates zip package content according to predefined rules',
    url='https://github.com/...',
    packages=setuptools.find_packages(where='src'),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={ '': ['validation_rules.json'] },
    entry_points={
        'console_scripts': [
            'validate-package-content = validate_package_content.cli:main'
        ]
    }
)
