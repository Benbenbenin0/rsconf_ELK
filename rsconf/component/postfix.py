# -*- coding: utf-8 -*-
u"""create postfix configuration

:copyright: Copyright (c) 2017 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function
from pykern import pkcollections
from pykern import pkio
from rsconf import component

_CONF_D = pkio.py_path('/etc/postfix')

class T(component.T):

    def internal_build(self):
        from rsconf import systemd
        from rsconf.component import docker_registry

        self.buildt.require_component('postgrey', 'spamd')
        j2_ctx = self.hdb.j2_ctx_copy()
        self.append_root_bash('rsconf_yum_install postfix')
        systemd.unit_prepare(self, _CONF_D)
        self.install_access(mode='400', owner=j2_ctx.rsconf_db.root_u)
        kc = self.install_tls_key_and_crt(j2_ctx.rsconf_db.host, _CONF_D)
        j2_ctx.setdefault('postfix', pkcollections.Dict()).update(
            tls_cert_file=kc.crt,
            tls_key_file=kc.key,
        )
        #TODO(robnagler) docker_image should be automatically prefixed
        j2_ctx.bop.docker_image = docker_registry.absolute_image(
            j2_ctx, j2_ctx.bop.docker_image)
        j2_ctx.spamd.docker_image = docker_registry.absolute_image(
            j2_ctx, j2_ctx.spamd.docker_image)
        self.append_root_bash_with_main(j2_ctx)
        systemd.unit_enable(self)
