import os
import sys
import shutil
import tempfile

import pytest
from git import Repo

from  orgtiger.spec import DEFAULT_SPEC_DIR, Spec 


TEST_SPEC_BASEDIR = tempfile.mkdtemp()

def cleanup():
    shutil.rmtree(TEST_SPEC_BASEDIR)
    #os.path.isdir(TEST_SPEC_BASEDIR)

def test_makes_spec_instance():
    my_spec = Spec()
    assert isinstance(my_spec, Spec)
    assert my_spec.spec_dir == os.path.expanduser(DEFAULT_SPEC_DIR)
    
def test_validate_spec_dir(caplog):

    # spec_dir does not exist
    my_spec = Spec(spec_dir=os.path.join(TEST_SPEC_BASEDIR, 'spec.d'))
    assert not os.path.isdir(my_spec.spec_dir)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        my_spec.validate()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1 
    # https://docs.pytest.org/en/stable/logging.html
    #print(caplog.record_tuples)
    for record in caplog.records:
        assert record.levelname == "CRITICAL"
    caplog.clear()

    # spec_dir exists, but not a git repo
    os.makedirs(my_spec.spec_dir)
    return_value = my_spec.validate()
    assert not return_value
    for record in caplog.records:
        assert record.levelname == "ERROR"
    caplog.clear()

    # repo exist, but has uncommited changes
    with open(os.path.join(my_spec.spec_dir, 'emptyfile'), mode='w'): pass
    temp_repo = Repo.init(my_spec.spec_dir)
    temp_repo.index.add(os.path.join(my_spec.spec_dir, 'emptyfile'))
    temp_repo.index.commit('initial commit')
    with open(os.path.join(my_spec.spec_dir, 'emptyfile'), mode='a') as f:
        f.write('testing 1 2 3 ')
    return_value = my_spec.validate()
    assert isinstance(my_spec.repo, Repo)
    assert not return_value
    for record in caplog.records:
        assert record.levelname == "ERROR"
    caplog.clear()
  
    # spec_dir working tree is clean
    temp_repo.index.add(os.path.join(my_spec.spec_dir, 'emptyfile'))
    temp_repo.index.commit('edit emptyfile')
    return_value = my_spec.validate()
    assert return_value

    #assert False
    cleanup()

def test_generate_spec_dir(caplog):
    #assert os.path.isdir(my_spec.spec_dir)
    #assert isinstance(my_spec.repo, git.Repo)
    #print(TEST_SPEC_BASEDIR)
    return




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
