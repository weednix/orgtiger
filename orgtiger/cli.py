#!/usr/bin/env python

import click
import boto3
from botocore.exceptions import ClientError

from orgcrawler.orgs import utils
from orgtiger.tiger import OrgTiger


DEFAULT_ROLE = 'OrganizationAccountAccessRole'


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--name', '-n',
    required=True,
    help='Name of the organization.')
@click.option('--role', '-r',
    #required=True,
    help='IAM role to assume for accessing AWS Organization Master account.')
def main(name, role):

    sts_client = boto3.client('sts')
    try:
        account_id = sts_client.get_caller_identity()['Account']
    except ClientError as e:    # pragma: no cover
        sys.exit('Could not find an AWS account: {}'.format(e.response['Error']['Code']))
    if not role:
        role = DEFAULT_ROLE
    try:
        master_id = utils.get_master_account_id(role)
    except ClientError as e:    # pragma: no cover
        sys.exit('Cant obtain master account id: {}'.format(e.response['Error']['Code']))
    try:
        my_tiger = OrgTiger(role, master_id)
    except Exception as e:
        print(e)
        exit(e)


    #my_orgtiger = OrgTiger(
    #    name=name,
    #    org_access_role=role,
    #)
    #my_orgtiger.org.load()
    #my_orgtiger.generate_spec_from_org()


if __name__ == '__main__':
    main()  # pragma no cover

