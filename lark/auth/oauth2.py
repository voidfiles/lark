from __future__ import absolute_import
from functools import partial
import logging

from flask import g

__all__ = ('bind_redis',)


log = logging.getLogger(__name__)


def bind_rcon(func, r_con):
    return partial(func, r_con)


def bind_redis(provider, r_con, user=None, client=None,
               token=None, grant=None, current_user=None):

    if user:
        provider.usergetter(bind_rcon(user.get_for_oauth2, r_con))

    if client:
        provider.clientgetter(bind_rcon(client.get_for_oauth2, r_con))

    if token:
        provider.tokengetter(bind_rcon(token.get_for_oauth2, r_con))
        provider.tokensetter(bind_rcon(token.set_for_oauth2, r_con))

    if grant:
        if not current_user:
            raise ValueError(('`current_user` is required'
                              'for Grant Binding'))
        provider.grantgetter(bind_rcon(grant.get_for_oauth2, r_con))
        provider.grantsetter(bind_rcon(grant.set_for_oauth2, r_con))
