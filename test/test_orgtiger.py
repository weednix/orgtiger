import pytest
from  orgtiger.tiger import OrgTiger


def test_makes_orgtiger_instance():
    my_orgtiger = OrgTiger()
    assert isinstance(my_orgtiger, OrgTiger)
    
