import os
import sys
import inspect

from orgcrawler.logger import Logger

import git
from git.exc import InvalidGitRepositoryError, NoSuchPathError


DEFAULT_SPEC_DIR = "~/.local/orgtiger/spec.d"


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
            self.repo = git.Repo(self.spec_dir)
        except NoSuchPathError as e:
            logmsg['ERROR'] = "Spec dir '{}' does not exist.  Try running Spec.generate()".format(self.spec_dir)
            self.log.error(logmsg)
            sys.exit(1)
        except InvalidGitRepositoryError as e:
            self.log.error("Spec dir {} is not a git repo.  Try running Spec.generate()", self.spec_dir)

    def generate(self):
        os.makedirs(self.spec_dir, exist_ok=True)
        #self.repo = git.Repo(self.spec_dir)
        #try:
        #    self.repo = git.Repo(self.spec_dir)
        #except:
        #    pass




