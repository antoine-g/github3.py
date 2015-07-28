import github3
from github3 import orgs
from tests.utils import (BaseCase, load)


class TestOrganization(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestOrganization, self).__init__(methodName)
        self.org = orgs.Organization(load('org'))

    def setUp(self):
        super(TestOrganization, self).setUp()
        self.org = orgs.Organization(self.org.as_dict(), self.g)
        self.api = 'https://api.github.com/orgs/github3py/'

    def test_create_hook(self):
        self.response('hook', 201)
        self.post(self.api + 'hooks')
        self.conf = {
            'data': {
                'name': 'Hookname',
                'config': {
                    'foo': 'bar'
                }
            }
        }

        self.assertRaises(github3.GitHubError, self.org.create_hook,
                          None, None)

        self.login()
        h = self.org.create_hook(**self.conf['data'])
        assert isinstance(h, orgs.OrganizationHook)
        self.mock_assertions()

    def test_equality(self):
        assert self.org == orgs.Organization(load('org'))


class TestHook(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestHook, self).__init__(methodName)
        self.hook = orgs.OrganizationHook(load('hook'))
        self.api = ("https://api.github.com/orgs/github3py/"
                    "hooks/292492")

    def setUp(self):
        super(TestHook, self).setUp()
        self.hook = orgs.OrganizationHook(self.hook.as_dict(), self.g)

    def test_equality(self):
        h = orgs.OrganizationHook(load('hook'))
        assert self.hook == h
        h._uniq = 1
        assert self.hook != h

    def test_repr(self):
        assert repr(self.hook) == '<OrganizationHook [readthedocs]>'

    def test_delete(self):
        self.response('', 204)
        self.delete(self.api)

        self.assertRaises(github3.GitHubError, self.hook.delete)
        self.not_called()

        self.login()
        assert self.hook.delete()
        self.mock_assertions()

    def test_edit(self):
        self.response('hook', 200)
        self.patch(self.api)
        data = {
            'config': {'push': 'http://example.com'},
            'events': ['push'],
            'add_events': ['fake_ev'],
            'rm_events': ['fake_ev'],
            'active': True,
        }
        self.conf = {'data': data.copy()}
        self.conf['data']['remove_events'] = data['rm_events']
        del(self.conf['data']['rm_events'])

        self.assertRaises(github3.GitHubError, self.hook.edit, **data)

        self.login()
        self.not_called()

        assert self.hook.edit(**data)
        self.mock_assertions()

    def test_edit_failed(self):
        self.response('', 404)
        self.patch(self.api)
        self.conf = {}

        self.login()
        assert self.hook.edit() is False
        self.mock_assertions()

    def test_ping(self):
        self.response('', 204)
        self.post(self.api + '/pings')
        self.conf = {}

        self.assertRaises(github3.GitHubError, self.hook.ping)
        self.not_called()

        self.login()
        assert self.hook.ping()
        self.mock_assertions()
