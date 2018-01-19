# -*- coding: utf-8 -*-
u"""Database

:copyright: Copyright (c) 2017 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function
from pykern import pkcollections
from pykern import pkconfig
from pykern import pkio
from pykern import pkjinja
from pykern import pkyaml
from pykern.pkdebug import pkdc, pkdp, pkdpretty
import random
import string


VISIBILITY_LIST = ('global', 'channel', 'host')
VISIBILITY_DEFAULT = VISIBILITY_LIST[1]
VISIBILITY_GLOBAL = VISIBILITY_LIST[0]

ZERO_YML = '0*.yml'

SRV_SUBDIR = 'srv'
DEFAULT_ROOT_SUBDIR = 'run'
DB_SUBDIR = 'db'
SECRET_SUBDIR = 'secret'
HOST_SUBDIR = 'host'
LEVELS = ('default', 'channel', 'host')
# Secrets are long so keep them simple
_RANDOM_STRING = string.ascii_letters + string.digits

class T(pkcollections.Dict):

    def __init__(self, *args, **kwargs):
        super(T, self).__init__(*args, **kwargs)
        self.root_d = pkio.py_path(cfg.root_d)
        self.db_d = self.root_d.join(DB_SUBDIR)
        self.base = pkcollections.Dict()
        for d in self.db_d, self.db_d.join(SECRET_SUBDIR):
            for f in pkio.sorted_glob(d.join(ZERO_YML)):
                v = pkyaml.load_str(
                    pkjinja.render_file(
                        f,
                        self.base,
                        strict_undefined=True,
                    ),
                )
                _merge_dict(self.base, v)

    def host_db(self, channel, host):
        res = pkcollections.Dict()
        v = pkcollections.Dict(
            rsconf_db=pkcollections.Dict(
                # Common defaults we allow overrides for
                host_run_d='/var/lib',
                run_u='vagrant',
                root_u='root',
            )
        )
        _merge_dict(res, v)
        #TODO(robnagler) optimize by caching default and channels
        for l in LEVELS:
            v = self.base[l]
            if l != 'default':
                v = v.get(channel)
                if not v:
                    continue
                if l == 'host':
                    v = v.get(host)
                    if not v:
                        continue
            _merge_dict(res, v)
        db_d = self.root_d.join(DB_SUBDIR)
        srv_d = self.root_d.join(SRV_SUBDIR)
        v = pkcollections.Dict(
            rsconf_db=pkcollections.Dict(
                channel=channel,
                db_d=db_d,
                host=host.lower(),
                secret_d=db_d.join(SECRET_SUBDIR),
                srv_d=srv_d,
                srv_host_d=srv_d.join(HOST_SUBDIR),
            )
        )
        _merge_dict(res, v)
        flat = pkcollections.Dict()
        pkconfig.flatten_values(flat, res)
        res.update(flat)
        _update_paths(res)
        return res

    def channel_hosts(self):
        res = pkcollections.OrderedMapping()
        for c in pkconfig.VALID_CHANNELS:
            res[c] = sorted(
                self.base.host.get(c, pkcollections.Dict()).keys(),
            )
        return res


def secret_path(hdb, filename, visibility=None):
    if visibility:
        assert visibility in VISIBILITY_LIST, \
            '{}: invalid visibility, must be {}'.format(
                visibility,
                VISIBILITY_LIST,
            )
    else:
        visibility = VISIBILITY_DEFAULT
    p = [] if visibility == VISIBILITY_GLOBAL else [hdb['rsconf_db'][visibility]]
    p.append(filename)
    res = hdb.rsconf_db.secret_d.join(*p)
    pkio.mkdir_parent_only(res)
    return res


def random_string(path=None, length=32):
    import random
    import string

    chars = string.ascii_lowercase + string.digits + string.ascii_uppercase
    res = ''.join(random.choice(chars) for _ in range(length))
    if path:
        with open(str(path), 'wb') as f:
            f.write(res)
    return res


@pkconfig.parse_none
def _cfg_root(value):
    """Parse root directory"""
    #TODO(robnagler) encapsulate this sirepo.server is the same thing
    from pykern import pkio, pkinspect
    import os, sys

    if value:
        assert os.path.isabs(value), \
            '{}: must be absolute'.format(value)
        value = pkio.py_path(value)
        assert value.check(dir=1), \
            '{}: must be a directory and exist'.format(value)
    else:
        assert pkconfig.channel_in('dev'), \
            'must be configured except in DEV'
        fn = pkio.py_path(sys.modules[pkinspect.root_package(_cfg_root)].__file__)
        root = pkio.py_path(pkio.py_path(fn.dirname).dirname)
        # Check to see if we are in our ~/src/radiasoft/<pkg> dir. This is a hack,
        # but should be reliable.
        if not root.join('setup.py').check():
            # Don't run from an install directorya
            root = pkio.py_path('.')
        value = root.join(DEFAULT_ROOT_SUBDIR)
    return value


def _merge_dict(base, new):
    for k in list(new.keys()):
        new_v = new[k]
        if not k in base:
            base[k] = new_v
            continue
        base_v = base[k]
        if isinstance(new_v, dict) or isinstance(base_v, dict):
            if new_v is None or base_v is None:
                # Just replace, because new_v overrides type in case of None
                base[k] = new_v
            elif isinstance(new_v, dict) and isinstance(base_v, dict):
                _merge_dict(base_v, new_v)
            else:
                raise AssertionError(
                    '{}: type mismatch between new value ({}) and base ({})'.format(
                        k, new_v, base_v))
            continue
        if isinstance(new_v, list) or isinstance(base_v, list):
            if new_v is None or base_v is None:
                # Just replace, because new_v overrides type in case of None
                pass
            elif isinstance(new_v, list) and isinstance(base_v, list):
                # prepend the new values
                new_v.extend(base_v)
            else:
                raise AssertionError(
                    '{}: type imsmatch between new value ({}) and base ({})'.format(
                        k, new_v, base_v))
            base[k] = new_v


def _update_paths(base):
    for k in list(base.keys()):
        if k.endswith('_d'):
            base[k] = pkio.py_path(base[k])
        elif isinstance(base[k], dict):
            _update_paths(base[k])


cfg = pkconfig.init(
    root_d=(None, _cfg_root, 'Top of rsconf tree'),
)
