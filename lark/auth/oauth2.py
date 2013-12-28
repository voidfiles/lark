from __future__ import absolute_import
from functools import partial
import logging


__all__ = ('bind_models',)


log = logging.getLogger(__name__)


def bind_models(provider, user=None, client=None,
                token=None, grant=None, current_user=None):

    if user:
        provider.usergetter(user.get_for_oauth2)

    if client:
        provider.clientgetter(client.get_for_oauth2)

    if token:
        provider.tokengetter(token.get_for_oauth2)
        provider.tokensetter(token.set_for_oauth2)

    if grant:
        if not current_user:
            raise ValueError(('`current_user` is required'
                              'for Grant Binding'))
        provider.grantgetter(grant.get_for_oauth2)
        provider.grantsetter(partial(grant.set_for_oauth2, current_user))
