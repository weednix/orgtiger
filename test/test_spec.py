import os
import sys
import shutil
import tempfile

import pytest
import git

from  orgtiger.spec import DEFAULT_SPEC_DIR, Spec 


TEST_SPEC_BASEDIR = tempfile.mkdtemp()

def cleanup():
    shutil.rmtree(TEST_SPEC_BASEDIR)

def test_makes_spec_instance():
    my_spec = Spec()
    assert isinstance(my_spec, Spec)
    assert my_spec.spec_dir == os.path.expanduser(DEFAULT_SPEC_DIR)
    
# https://docs.pytest.org/en/stable/logging.html
def test_validate_spec_dir(caplog):
    my_spec = Spec(spec_dir=os.path.join(TEST_SPEC_BASEDIR, 'spec.d'))
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        my_spec.validate()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1 

    #print(caplog.record_tuples)
    for record in caplog.records:
        #print(record.levelname)
        assert record.levelname == "ERROR"


    #assert os.path.isdir(my_spec.spec_dir)
    #assert isinstance(my_spec.repo, git.Repo)
    #print(TEST_SPEC_BASEDIR)

    #assert False
    cleanup()



'''
if no spec dir:
  error: specdir not found.  provide hint about spec generator tool.
  exit

if spec dir, but not a git repo:
  warn: spec dir not under version contoll

if spec dir and git repo
  info: report current branch, last commit date

  if working tree is dirty
    warn: uncommitted changes in spec dir
'''

'''
using spec.generate()

if specdir exists and is not empty:
  error: specdir exists and is not empty
  exit
else:
  attept to create spec dir. passive fail if exists  
  initialize git repo

'''
