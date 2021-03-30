"""orgtiger setup"""

from orgtiger import __version__
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aws-orgs',
    version=__version__,
    description='Tools to manage AWS Organization resources',
    long_description=long_description,
    url='https://github.com/ucopacme/aws-orgs',
    author=['Ashley Gould', 'Santhosh Katakam', 'Sophia Rice-Smith'],
    author_email=['agould@ucop.edu','santh[ubhai12@gmail.com'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='aws organizations',
    packages=find_packages(exclude=['scratch', 'notes']),
    install_requires=[
        'boto3', 
        'docopt', 
        'PyYAML', 
        'passwordgenerator',
        'cerberus',
        'orgcrawler',
    ],
    package_data={
        'orgtiger': [
            'data/*',
            'spec_init_data/*',
            'spec_init_data/spec.d/*',
        ],
    },
    entry_points={
        'console_scripts': [
            'awsorgs=awsorgs.orgs:main',
            'awsaccounts=awsorgs.accounts:main',
        #    'awsauth=awsorgs.auth:main',
            'awsloginprofile=awsorgs.loginprofile:main',
            'awsorgs-accessrole=awsorgs.tools.accessrole:main',
            'awsorgs-spec-init=awsorgs.tools.spec_init:main',
        ],
    },

)
