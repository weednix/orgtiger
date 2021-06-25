import os
import sys
import inspect
import pkg_resources
import yaml
import git
from git.exc import InvalidGitRepositoryError, NoSuchPathError

import orgcrawler
from orgcrawler import orgs, utils
from orgcrawler.logger import Logger

from orgtiger.exceptions import (
   SPEC_VALIDATION_ERROR,
   SPEC_GENERATION_ERROR,
) 


DEFAULT_SPEC_DIR = "~/.local/orgtiger/spec.d"


class OrgTiger(object):

    def __init__(self, name=None, master_account_id=None, org_access_role=None,
		spec_dir=DEFAULT_SPEC_DIR):
        self.name = name
        if master_account_id is not None:
            self.org = orgs.Org(master_account_id, org_access_role)
        self.spec_dir = spec_dir = os.path.expanduser(spec_dir)
        self.log = Logger()

    def validate_spec_repo(self):
        logmsg = {
            'FILE': __file__.split('/')[-1],
            'CLASS': self.__class__.__name__,
            'METHOD': inspect.stack()[0][3],
        }
        try:
            self.spec_repo = git.Repo(self.spec_dir)
        except NoSuchPathError as e:
            logmsg['MESSAGE'] = "Spec dir '{}' does not exist.  Try running Spec.generate()".format(self.spec_dir)
            self.log.critical(logmsg)
            raise SPEC_VALIDATION_ERROR('Spec dir does not exist')
        except InvalidGitRepositoryError as e:
            logmsg['MESSAGE'] = "Spec dir {} is not a git repo.  Try running Spec.generate()".format(self.spec_dir)
            self.log.error(logmsg)
            return False
        if self.spec_repo.is_dirty():
            logmsg['MESSAGE'] = "Spec dir {} has uncommited changes.".format(self.spec_dir)
            self.log.error(logmsg)
            return False
        return True
        
    def generate_spec_repo(self):
        logmsg = {
            'FILE': __file__.split('/')[-1],
            'CLASS': self.__class__.__name__,
            'METHOD': inspect.stack()[0][3],
        }

        def _new_repo():
            self.spec_repo = git.Repo.init(self.spec_dir)
            with open(os.path.join(self.spec_dir, 'README.rst'), mode='a') as f:
                f.write('Orgtiger Spec Files')
                f.write('===================')
            self.spec_repo.index.add(os.path.join(self.spec_dir, 'README.rst'))
            self.spec_repo.index.commit('initial commit')

        try:
            self.spec_repo = git.Repo(self.spec_dir)
        except NoSuchPathError as e:
            logmsg['MESSAGE'] = "Creating spec dir '{}'".format(self.spec_dir)
            self.log.info(logmsg)
            os.makedirs(self.spec_dir)
            _new_repo()
        except InvalidGitRepositoryError as e:
            if os.path.isdir(self.spec_dir) and not os.listdir(self.spec_dir):
                _new_repo()
            elif os.path.isdir(self.spec_dir) and os.listdir(self.spec_dir):
                logmsg['MESSAGE'] = "Cannot initialize git repo in spec dir. '{}' is not empty".format(self.spec_dir)
                self.log.critical(logmsg)
                raise SPEC_GENERATION_ERROR('proposed spec_dir is not empty')
            elif os.path.isfile(self.spec_dir):
                logmsg['MESSAGE'] = "Cannot initialize git repo in spec dir. '{}' is not a directory".format(self.spec_dir)
                self.log.critical(logmsg)
                raise SPEC_GENERATION_ERROR('proposed spec_dir is a file')

    def generate_spec_from_org(self):
        logmsg = {
            'FILE': __file__.split('/')[-1],
            'CLASS': self.__class__.__name__,
            'METHOD': inspect.stack()[0][3],
        }
        self.org.load()
        self.generate_spec_repo()
        org_spec = self.org.dump()
        print(utils.yamlfmt(org_spec))
        spec_file = os.path.join(self.spec_dir, 'org_spec.yaml')
        with open(spec_file, mode='a') as f:
            f.write('---')
            f.write(utils.yamlfmt(org_spec))
        self.spec_repo.index.add(spec_file)
        self.spec_repo.index.commit('generate_spec_from_org')
        logmsg['MESSAGE'] = "Generating spec from existing AWS Organization in '{}'".format(spec_file)
        self.log.info(logmsg)
