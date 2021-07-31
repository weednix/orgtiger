import os
import sys
import shutil
import tempfile

import pytest
from git import Repo
from moto import (
    mock_organizations,
    mock_sts,
    mock_iam,
)

from orgcrawler import orgs
from orgcrawler.mock.org import (
    MockOrganization,
    ORG_ACCESS_ROLE,
    MASTER_ACCOUNT_ID,
)

from  orgtiger.spec import (
    DEFAULT_SPEC_DIR,
    SPEC_VALIDATION_ERROR,
    SPEC_GENERATION_ERROR,
    Spec,
)


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
    with pytest.raises(SPEC_VALIDATION_ERROR) as pytest_wrapped_e:
        my_spec.validate()
    assert pytest_wrapped_e.type == SPEC_VALIDATION_ERROR
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

def test_generate_repo(caplog):
    my_spec = Spec(spec_dir=os.path.join(TEST_SPEC_BASEDIR, 'spec.d'))
    my_spec.generate_repo()
    return_value = my_spec.validate()
    assert return_value
    cleanup()

    os.makedirs(my_spec.spec_dir)
    my_spec.generate_repo()
    return_value = my_spec.validate()
    assert return_value
    cleanup()

    os.makedirs(my_spec.spec_dir)
    with open(os.path.join(my_spec.spec_dir, 'emptyfile'), mode='w'): pass
    with pytest.raises(SPEC_GENERATION_ERROR) as pytest_wrapped_e:
        my_spec.generate_repo()
    assert pytest_wrapped_e.type == SPEC_GENERATION_ERROR
    cleanup()

    os.makedirs(TEST_SPEC_BASEDIR)
    with open(my_spec.spec_dir, mode='w'): pass
    with pytest.raises(SPEC_GENERATION_ERROR) as pytest_wrapped_e:
        my_spec.generate_repo()
    assert pytest_wrapped_e.type == SPEC_GENERATION_ERROR
    cleanup()

    #assert False

@mock_sts
@mock_organizations
def test_generate_spec_from_org():
    MockOrganization().simple()
    my_org = orgs.Org(MASTER_ACCOUNT_ID, ORG_ACCESS_ROLE)
    my_org.load()
    my_spec = Spec(spec_dir=os.path.join(TEST_SPEC_BASEDIR, 'spec.d'))
    my_spec.generate_repo()
    my_spec.generate_spec_from_org(my_org)
    assert os.path.isfile(os.path.join(my_spec.spec_dir, 'common.yaml'))








"""

test generation of common.yaml.  This action may need to live in tiger object

file exists
file passes cerubus parsing (must contain the following parameters):
    minimum_version
    master_account_id
    default_ou
    default_sc_policy
params match default or supplied values 

https://jinja.palletsprojects.com/en/2.11.x/intro/#basic-api-usage
"""
