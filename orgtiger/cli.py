#!/usr/bin/env python

import click

from orgtiger.tiger import OrgTiger

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--name', '-n',
    required=True,
    help='Name of the organization.')
@click.option('--role', '-r',
    required=True,
    help='IAM role to assume for accessing AWS Organization Master account.')
def main(name, role):
    my_orgtiger = OrgTiger(
        name=name,
        org_access_role=role,
    )
    my_orgtiger.org.load()
    my_orgtiger.generate_spec_from_org()


if __name__ == '__main__':
    main()  # pragma no cover

