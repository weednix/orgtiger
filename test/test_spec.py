import os
import shutil
import tempfile

import pytest

from  orgtiger.spec import DEFAULT_SPEC_DIR, Spec 


TEST_SPEC_BASEDIR = tempfile.mkdtemp()

def cleanup():
    shutil.rmtree(TEST_SPEC_BASEDIR)

def test_makes_spec_instance():
    my_spec = Spec()
    assert isinstance(my_spec, Spec)
    assert my_spec.spec_dir == os.path.expanduser(DEFAULT_SPEC_DIR)
    
def test_create_spec_dir():
    my_spec = Spec(spec_dir=os.path.join(TEST_SPEC_BASEDIR, 'spec.d'))
    my_spec.validate_spec_dir()
    assert os.path.isdir(my_spec.spec_dir)
    print(TEST_SPEC_BASEDIR)
    cleanup()




#    checks that dir is a git repo working tree
#    checks that we fail with error message if dir exists

