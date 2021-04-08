import os


DEFAULT_SPEC_DIR = "~/.local/orgtiger/spec.d"


class Spec(object):

    def __init__(self, spec_dir=DEFAULT_SPEC_DIR):
        self.spec_dir = spec_dir = os.path.expanduser(spec_dir)

    def validate_spec_dir(self):
        os.makedirs(self.spec_dir, exist_ok=True)




