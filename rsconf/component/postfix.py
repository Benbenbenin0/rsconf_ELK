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

        self.buildt.require_component('postgrey', 'spamd')
        j2_ctx = self.hdb.j2_ctx_copy()
        z = j2_ctx.setdefault('postfix', pkcollections.Dict())
        self.append_root_bash('rsconf_yum_install postfix')
        systemd.unit_prepare(self,j2_ctx, _CONF_D)
        self._setup_virtual_aliases(j2_ctx, z)
        self._setup_sasl(j2_ctx, z)
        # New install access
        self.install_access(mode='400', owner=j2_ctx.rsconf_db.root_u)
        kc = self.install_tls_key_and_crt(j2_ctx.rsconf_db.host, _CONF_D)
        z.update(
            tls_cert_file=kc.crt,
            tls_key_file=kc.key,
        )
        self.install_resource(
            'postfix/aliases',
            j2_ctx,
            '/etc/aliases',
        )
        self.append_root_bash_with_main(j2_ctx)
        systemd.unit_enable(self, j2_ctx)
        self.append_root_bash('rsconf_service_restart_at_end postfix')

    def _setup_sasl(self, j2_ctx, z):
        if not z.setdefault('sasl_users', []):
            return
        self.install_access(mode='400', owner=j2_ctx.rsconf_db.root_u)
        z.sasl_users_flattened = []
        for domain, u in z.sasl_users.items():
            for user, password in u.items():
                z.sasl_users_flattened.append(
                    pkcollections.Dict(
                        domain=domain,
                        user=user,
                        password=password,
                    ),
                )
        self.install_resource(
            'postfix/smtpd-sasldb.conf',
            j2_ctx,
            '/etc/sasl2/smtpd-sasldb.conf',
        )
        assert j2_ctx.postfix.sasl_users_flattened

    def _setup_virtual_aliases(self, j2_ctx, z):
        if not z.setdefault('virtual_aliases', []):
            return
        self.install_access(mode='440', owner=j2_ctx.rsconf_db.root_u, group='mail')
        z.virtual_alias_f = _CONF_D.join('virtual_alias')
        z.virtual_alias_domains_f = _CONF_D.join('virtual_alias_domains')
        self.install_resource(
            'postfix/virtual_alias_domains', j2_ctx, z.virtual_alias_domains_f)
        self.install_resource(
            'postfix/virtual_alias', j2_ctx, z.virtual_alias_f)
