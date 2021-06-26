import os
import sys
import shutil
import tempfile

import git
import pytest
from moto import (
    mock_organizations,
    mock_sts,
    mock_iam,
)

from orgcrawler import orgs, utils
from orgcrawler.mock.org import (
    MockOrganization,
    ORG_ACCESS_ROLE,
    MASTER_ACCOUNT_ID,
)
from orgtiger.tiger import (
    OrgTiger,
    DEFAULT_SPEC_DIR,
)

from orgtiger.exceptions import (
    SPEC_VALIDATION_ERROR,
    SPEC_GENERATION_ERROR,
)


TEST_SPEC_BASEDIR = tempfile.mkdtemp()


def cleanup():
    shutil.rmtree(TEST_SPEC_BASEDIR)


def test_makes_orgtiger_instance():
    my_orgtiger = OrgTiger(ORG_ACCESS_ROLE)
    assert isinstance(my_orgtiger, OrgTiger)
    assert my_orgtiger.spec_dir == os.path.expanduser(DEFAULT_SPEC_DIR)
    

@mock_sts
@mock_organizations
def test_orgtiger_has_org_attribute():
    my_orgtiger = OrgTiger(name='moch_org', org_access_role=ORG_ACCESS_ROLE, master_account_id=MASTER_ACCOUNT_ID)
    assert my_orgtiger.name == 'moch_org'
    assert isinstance(my_orgtiger.org, orgs.Org)


@mock_sts
@mock_organizations
def test_orgtiger_loads_an_existing_org():
    MockOrganization().simple()
    my_orgtiger = OrgTiger(name='moch_org', org_access_role=ORG_ACCESS_ROLE, master_account_id=MASTER_ACCOUNT_ID)
    my_orgtiger.org.load()
    assert my_orgtiger.org.id is not None
    assert my_orgtiger.org.root_id is not None
    assert len(my_orgtiger.org.accounts) > 0
    assert len(my_orgtiger.org.org_units) > 0
    assert len(my_orgtiger.org.policies) > 0


@mock_sts
@mock_organizations
def test_validate_spec_dir(caplog):
    MockOrganization().simple()
    my_orgtiger = OrgTiger(
        name='moch_org',
        org_access_role=ORG_ACCESS_ROLE,
        master_account_id=MASTER_ACCOUNT_ID,
        spec_dir=os.path.join(TEST_SPEC_BASEDIR, 'spec.d'),
    )

    # spec_dir does not exist
    assert not os.path.isdir(my_orgtiger.spec_dir)
    with pytest.raises(SPEC_VALIDATION_ERROR) as pytest_wrapped_e:
        my_orgtiger.validate_spec_repo()
    assert pytest_wrapped_e.type == SPEC_VALIDATION_ERROR
    # https://docs.pytest.org/en/stable/logging.html
    #print(caplog.record_tuples)
    for record in caplog.records:
        assert record.levelname == "CRITICAL"
    caplog.clear()

    # spec_dir exists, but not a git repo
    os.makedirs(my_orgtiger.spec_dir)
    return_value = my_orgtiger.validate_spec_repo()
    assert not return_value
    for record in caplog.records:
        assert record.levelname == "ERROR"
    caplog.clear()

    # repo exist, but has uncommited changes
    with open(os.path.join(my_orgtiger.spec_dir, 'emptyfile'), mode='w'): pass
    temp_repo = git.Repo.init(my_orgtiger.spec_dir)
    temp_repo.index.add(os.path.join(my_orgtiger.spec_dir, 'emptyfile'))
    temp_repo.index.commit('initial commit')
    with open(os.path.join(my_orgtiger.spec_dir, 'emptyfile'), mode='a') as f:
        f.write('testing 1 2 3 ')
    return_value = my_orgtiger.validate_spec_repo()
    assert isinstance(my_orgtiger.spec_repo, git.Repo)
    assert not return_value
    for record in caplog.records:
        assert record.levelname == "ERROR"
    caplog.clear()
  
    # spec_dir working tree is clean
    temp_repo.index.add(os.path.join(my_orgtiger.spec_dir, 'emptyfile'))
    temp_repo.index.commit('edit emptyfile')
    return_value = my_orgtiger.validate_spec_repo()
    assert return_value

    #assert False
    cleanup()


@mock_sts
@mock_organizations
def test_generate_repo(caplog):
    MockOrganization().simple()
    my_orgtiger = OrgTiger(
        name='moch_org',
        org_access_role=ORG_ACCESS_ROLE,
        master_account_id=MASTER_ACCOUNT_ID,
        spec_dir=os.path.join(TEST_SPEC_BASEDIR, 'spec.d'),
    )
    my_orgtiger.generate_spec_repo()
    return_value = my_orgtiger.validate_spec_repo()
    assert return_value
    cleanup()

    os.makedirs(my_orgtiger.spec_dir)
    my_orgtiger.generate_spec_repo()
    return_value = my_orgtiger.validate_spec_repo()
    assert return_value
    cleanup()

    os.makedirs(my_orgtiger.spec_dir)
    with open(os.path.join(my_orgtiger.spec_dir, 'emptyfile'), mode='w'): pass
    with pytest.raises(SPEC_GENERATION_ERROR) as pytest_wrapped_e:
        my_orgtiger.generate_spec_repo()
    assert pytest_wrapped_e.type == SPEC_GENERATION_ERROR
    cleanup()


@mock_sts
@mock_organizations
def test_generate_spec_from_org(caplog):
    MockOrganization().simple()
    my_orgtiger = OrgTiger(
        name='moch_org',
        org_access_role=ORG_ACCESS_ROLE,
        master_account_id=MASTER_ACCOUNT_ID,
        spec_dir=os.path.join(TEST_SPEC_BASEDIR, 'spec.d'),
    )
    my_orgtiger.org.load()
    my_orgtiger.generate_spec_from_org()
    assert os.path.isfile(os.path.join(my_orgtiger.spec_dir, 'org_spec.yaml'))
    #cleanup()







"""
@mock_sts
@mock_organizations
def test_orgtiger_dumps_an_existing_org():
    MockOrganization().simple()
    my_orgtiger = OrgTiger(name='moch_org', org_access_role=ORG_ACCESS_ROLE, master_account_id=MASTER_ACCOUNT_ID)
    my_orgtiger.org.load()
    org_spec = my_orgtiger.org.dump()
    #org_spec = my_orgtiger.org.dump_accounts()
    print(utils.yamlfmt(org_spec))
    assert false

@mock_sts
@mock_organizations
def test_generate_spec_from_org():
    MockOrganization().simple()
    my_org = orgs.Org(MASTER_ACCOUNT_ID, ORG_ACCESS_ROLE)
    my_org.load()
    my_spec = Spec(spec_dir=os.path.join(TEST_SPEC_BASEDIR, 'spec.d'))
    my_spec.generate_spec_repo()
    my_spec.generate_spec_from_org(my_org)
    assert os.path.isfile(os.path.join(my_spec.spec_dir, 'common.yaml'))
"""
