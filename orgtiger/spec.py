import os
import sys
import inspect

from orgcrawler.logger import Logger

from git import Repo
from git.exc import InvalidGitRepositoryError, NoSuchPathError


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
        

    def generate(self):
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
            else:
                logmsg['MESSAGE'] = "Cannot initialize git repo in spec dir '{}'".format(self.spec_dir)
                self.log.critical(logmsg)
                raise SPEC_GENERATION_ERROR('Cannot initialize git repo')

    def _init_new_repo(self):
        self.repo = Repo.init(self.spec_dir)
        with open(os.path.join(self.spec_dir, 'README.rst'), mode='a') as f:
            f.write('Orgtiger Spec Files')
            f.write('===================')
        self.repo.index.add(os.path.join(self.spec_dir, 'README.rst'))
        self.repo.index.commit('initial commit')





