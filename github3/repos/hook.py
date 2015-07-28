# -*- coding: utf-8 -*-
"""
github3.repos.hook
==================

This module contains only the RepositoryHook object for GitHub's Repository
Hook API.

"""
from __future__ import unicode_literals

from ..decorators import requires_auth
from ..hooks import Hook


class RepositoryHook(Hook):
    """The :class:`RepositoryHook <Hook>` object. This handles the information
    returned by GitHub about hooks set on a repository.

    Two RepositoyHook instances can be checked like so::

        h1 == h2
        h1 != h2

    And is equivalent to::

        h1.id == h2.id
        h1.id != h2.id

    See also: http://developer.github.com/v3/repos/hooks/
    """
    def _repr(self):
        return '<RepositoryHook [{0}]>'.format(self.name)

    @requires_auth
    def test(self):
        """Test this hook

        :returns: bool
        """
        url = self._build_url('tests', base_url=self._api)
        return self._boolean(self._post(url), 204, 404)
