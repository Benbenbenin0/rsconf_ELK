# -*- coding: utf-8 -*-
u"""create postgrey configuration

:copyright: Copyright (c) 2017 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function
from rsconf import component
from pykern import pkcollections


class T(component.T):
    def internal_build(self):
        from rsconf import systemd
        from rsconf import docker_registry

        self.buildt.require_component('docker')
        j2_ctx = pkcollections.Dict(self.hdb)
        run_d = systemd.docker_unit_prepare(self)
        j2_ctx.postgrey_dbdir = run_d.join('db')
        j2_ctx.postgrey_etc = run_d.join('etc')
        run = run_d.join('run')
        systemd.docker_unit_enable(
            self,
            image=docker_registry.absolute_image(j2_ctx, j2_ctx.postgrey_docker_image),
            env=pkcollections.Dict(),
            cmd=str(run),
        )
        self.install_access(mode='700', owner=self.hdb.rsconf_db_run_u)
        self.install_directory(run_d)
        self.install_directory(j2_ctx.postgrey_dbdir)
        self.install_directory(j2_ctx.postgrey_etc)
        self.install_resource('postgrey/run.sh', j2_ctx, run)
        self.install_resource(
            'postgrey/postgrey_whitelist_recipients',
            j2_ctx,
            j2_ctx.postgrey_dbdir.join('postgrey_whitelist_recipients'),
        )
        self.install_resource(
            'postgrey/postgrey_whitelist_clients.local',
            j2_ctx,
            j2_ctx.postgrey_dbdir.join('postgrey_whitelist_clients.local'),
        )
