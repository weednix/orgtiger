import os
import sys
import inspect

from orgcrawler.logger import Logger

from git import Repo
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
            self.repo = Repo(self.spec_dir)
        except NoSuchPathError as e:
            logmsg['MESSAGE'] = "Spec dir '{}' does not exist.  Try running Spec.generate()".format(self.spec_dir)
            self.log.critical(logmsg)
            sys.exit(1)
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
        os.makedirs(self.spec_dir, exist_ok=True)
        #self.repo = git.Repo(self.spec_dir)
        #try:
        #    self.repo = git.Repo(self.spec_dir)
        #except:
        #    pass




