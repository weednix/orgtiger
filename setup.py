"""orgtiger setup"""

from orgtiger import __version__
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='orgtiger',
    version=__version__,
    description='Tools to manage AWS Organization resources',
    long_description=long_description,
    url='https://github.com/weednix/orgtiger',
    author='Ashley Gould, Santhosh Katakam, Sophia Rice-Smith',
    author_email='agould@ucop.edu,santhubhai12@gmail.com, ssrice@ucdavis.edu',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Build Tools ',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

    ],
    keywords='aws organizations setup tool',
    project_urls={
        'Documentation': 'https://github.com/weednix/orgtiger',
        'Source':'https://github.com/weednix/orgtiger',
    },
    packages=find_packages(exclude=['scratch', 'notes']),
    install_requires=[
        'boto3', 
        'click', 
        'PyYAML', 
        'cerberus',
        'orgcrawler',
        'pytest',
        'GitPython',
        'jinja2',
        'pytest',
        'pytest-cov',
        'moto',
        'flake8'
    ],
    package_data={
        'orgtiger': [],
    },
    entry_points={
        'console_scripts': [
        ],
    },

)
