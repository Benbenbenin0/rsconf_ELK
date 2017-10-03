# -*- coding: utf-8 -*-
u"""create docker configuration

:copyright: Copyright (c) 2017 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function
from rsconf import component
from pykern import pkcollections
from pykern import pkio

_CONF_DIR = pkio.py_path('/etc/docker')
_DAEMON_JSON = _CONF_DIR.join('daemon.json')

class T(component.T):
    def internal_build(self):
        self.buildt.require_component('base_users')
        #TODO(robnagler) if /etc/docker changes restart daemon
        #  coordinate with main.sh which may have just started daemon
        self.append_root_bash(
            "rsconf_service_prepare '{}' '{}'".format(
                self.name,
                _DAEMON_JSON,
            ),
        )
        j2_ctx = pkcollections.Dict(self.hdb)
        j2_ctx.update(
            docker_volume_group='docker',
        )
        self.install_access(mode='700', owner=j2_ctx.rsconf_db_root_u)
        self.install_directory(_CONF_DIR)
        self.install_access(mode='400', owner=j2_ctx.rsconf_db_root_u)
        self.install_resource(
            'docker/daemon.json',
            j2_ctx,
            _DAEMON_JSON,
        )
        if docker_registry.is_self_signed():
        if self.hdb.get('docker_registry_host')
            self._docker_registry_crt()
        self.append_root_bash_with_resource(
            'docker/main.sh',
            j2_ctx,
            'docker_main',
        )
        #TODO(robnagler) add live-restore?
        # live restore: https://docs.docker.com/engine/admin/live-restore
        # "live-restore": true,
        # live-restore does interrupt network due to proxies, --net=host
