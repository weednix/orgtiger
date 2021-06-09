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
from orgtiger.tiger import OrgTiger


def test_makes_orgtiger_instance():
    my_orgtiger = OrgTiger()
    assert isinstance(my_orgtiger, OrgTiger)
    

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
def test_orgtiger_dumps_an_existing_org():
    MockOrganization().simple()
    my_orgtiger = OrgTiger(name='moch_org', org_access_role=ORG_ACCESS_ROLE, master_account_id=MASTER_ACCOUNT_ID)
    my_orgtiger.org.load()
    org_spec = my_orgtiger.org.dump()
    #org_spec = my_orgtiger.org.dump_accounts()
    print(utils.yamlfmt(org_spec))
    assert false
