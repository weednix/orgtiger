import os
import sys
import logging

import git
from git.exc import InvalidGitRepositoryError


DEFAULT_SPEC_DIR = "~/.local/orgtiger/spec.d"


class Spec(object):

    def __init__(self, spec_dir=DEFAULT_SPEC_DIR):
        self.spec_dir = spec_dir = os.path.expanduser(spec_dir)
        #self.log = logging.Logger(__name__)

    def validate(self):
        if not os.path.isdir(self.spec_dir):
            #self.log.error("Spec dir does not exist.  Try running Spec.generate()")
            sys.exit("Spec dir does not exist.  Try running Spec.generate()")
        try:
            self.repo = git.Repo(self.spec_dir)
        except InvalidGitRepositoryError as e:
            sys.exit("Spec dir is not a git repo.  Try running Spec.generate()")

    def generate(self):
        os.makedirs(self.spec_dir, exist_ok=True)
        #self.repo = git.Repo(self.spec_dir)
        #try:
        #    self.repo = git.Repo(self.spec_dir)
        #except:
        #    pass




