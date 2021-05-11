import orgcrawler
import orgcrawler.orgs

from orgtiger.spec import Spec


class OrgTiger(object):

    def __init__(self, name=None, master_account_id=None, org_access_role=None):
        self.name = name
        if master_account_id is not None:
            self.org = orgcrawler.orgs.Org(master_account_id, org_access_role)
        self.spec = Spec()

    def generate():
        return
        
