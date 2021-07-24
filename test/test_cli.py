import pytest
from click.testing import CliRunner
from moto import (
    mock_organizations,
    mock_sts,
    mock_iam,
)

from orgtiger import cli

#from orgcrawler import orgs, utils
from orgcrawler.mock.org import (
    MockOrganization,
    ORG_ACCESS_ROLE,
    MASTER_ACCOUNT_ID,
)
#from orgtiger.tiger import (
#    OrgTiger,
#    DEFAULT_SPEC_DIR,
#)
#
#from orgtiger.exceptions import (
#    SPEC_VALIDATION_ERROR,
#    SPEC_GENERATION_ERROR,
#)



@pytest.mark.parametrize('options_list', [
    (['--name', 'blee', '--role', 'blee']),
])
def test_no_account(options_list):
    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        options_list,
    )
    assert result.exit_code == 1

@mock_sts
@mock_organizations
@mock_iam
@pytest.mark.parametrize('options_list', [
    (['--name', 'blee', '--role', ORG_ACCESS_ROLE]),
])
def test_has_account(options_list):
    MockOrganization().simple()
    runner = CliRunner()
    result = runner.invoke(
        cli.main,
        options_list,
    )
    print(result)
    assert result.exit_code == 0




