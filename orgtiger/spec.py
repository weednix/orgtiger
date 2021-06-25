import os
import sys
import inspect
import pkg_resources


import yaml
from jinja2 import Template
from git import Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError
from cerberus import Validator, schema_registry

from orgcrawler import orgs
from orgcrawler.logger import Logger
from orgtiger.schemas import (
    COMMON_SCHEMA,
)

DEFAULT_SPEC_DIR = "~/.local/orgtiger/spec.d"

class SPEC_VALIDATION_ERROR(Exception):
    """Base class for spec validation errors"""

class SPEC_GENERATION_ERROR(Exception):
    """Base class for spec generation errors"""

class Spec(object):

    def __init__(self, spec_dir=DEFAULT_SPEC_DIR):
        self.spec_dir = spec_dir = os.path.expanduser(spec_dir)
        self.log = Logger()

    def validate(self):
        logmsg = {
            'FILE': __file__.split('/')[-1],
            'CLASS': self.__class__.__name__,
            'METHOD': inspect.stack()[0][3],
        }
        try:
            self.repo = Repo(self.spec_dir)
        except NoSuchPathError as e:
            logmsg['MESSAGE'] = "Spec dir '{}' does not exist.  Try running Spec.generate()".format(self.spec_dir)
            self.log.critical(logmsg)
            raise SPEC_VALIDATION_ERROR('Spec dir does not exist')
        except InvalidGitRepositoryError as e:
            logmsg['MESSAGE'] = "Spec dir {} is not a git repo.  Try running Spec.generate()".format(self.spec_dir)
            self.log.error(logmsg)
            return False
        if self.repo.is_dirty():
            logmsg['MESSAGE'] = "Spec dir {} has uncommited changes.".format(self.spec_dir)
            self.log.error(logmsg)
            return False
        return True
        

    def generate_repo(self):
        logmsg = {
            'FILE': __file__.split('/')[-1],
            'CLASS': self.__class__.__name__,
            'METHOD': inspect.stack()[0][3],
        }
        try:
            self.repo = Repo(self.spec_dir)
        except NoSuchPathError as e:
            logmsg['MESSAGE'] = "Creating spec dir '{}'".format(self.spec_dir)
            self.log.info(logmsg)
            os.makedirs(self.spec_dir)
            self._init_new_repo()
        except InvalidGitRepositoryError as e:
            if os.path.isdir(self.spec_dir) and not os.listdir(self.spec_dir):
                self._init_new_repo()
            elif os.path.isdir(self.spec_dir) and os.listdir(self.spec_dir):
                logmsg['MESSAGE'] = "Cannot initialize git repo in spec dir. '{}' is not empty".format(self.spec_dir)
                self.log.critical(logmsg)
                raise SPEC_GENERATION_ERROR('proposed spec_dir is not empty')
            elif os.path.isfile(self.spec_dir):
                logmsg['MESSAGE'] = "Cannot initialize git repo in spec dir. '{}' is not a directory".format(self.spec_dir)
                self.log.critical(logmsg)
                raise SPEC_GENERATION_ERROR('proposed spec_dir is a file')

    def _init_new_repo(self):
        self.repo = Repo.init(self.spec_dir)
        with open(os.path.join(self.spec_dir, 'README.rst'), mode='a') as f:
            f.write('Orgtiger Spec Files')
            f.write('===================')
        self.repo.index.add(os.path.join(self.spec_dir, 'README.rst'))
        self.repo.index.commit('initial commit')


    def generate_spec_from_org(self, org=None):
        logmsg = {
            'FILE': __file__.split('/')[-1],
            'CLASS': self.__class__.__name__,
            'METHOD': inspect.stack()[0][3],
        }
        if org is not None and isinstance(org, orgs.Org):
            self._init_common(org)
            self._init_sc_policies(org)


    def _init_common(self, org):
        logmsg = {
            'FILE': __file__.split('/')[-1],
            'CLASS': self.__class__.__name__,
            'METHOD': inspect.stack()[0][3],
        }
        local_template_file = 'templates/common.yaml.j2'
        template_file = os.path.abspath(pkg_resources.resource_filename(__name__, local_template_file))
        logmsg['MESSAGE'] = "processing template file '{}'".format(template_file)
        print(logmsg['MESSAGE'])
        with open(template_file) as t:
            spec_file = Template(t.read()).render(master_account_id = org.master_account_id)
        print(spec_file)
        with open(os.path.join(self.spec_dir, 'common.yaml'), 'w') as f:
            f.write(spec_file)


    def _init_sc_policies(self, org):
        logmsg = {
            'FILE': __file__.split('/')[-1],
            'CLASS': self.__class__.__name__,
            'METHOD': inspect.stack()[0][3],
        }
        local_template_file = 'templates/service_control_polices.yaml.j2'
        template_file = os.path.abspath(pkg_resources.resource_filename(__name__, local_template_file))
        logmsg['MESSAGE'] = "processing template file '{}'".format(template_file)
        print(logmsg['MESSAGE'])
        with open(template_file) as t:
            spec_file = Template(t.read()).render(sc_polices = org.policies)
        print(spec_file)
        with open(os.path.join(self.spec_dir, 'service_control_polices.common.yaml'), 'w') as f:
            f.write(spec_file)

