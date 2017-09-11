# -*- coding: utf-8 -*-
u"""create base os configuration

:copyright: Copyright (c) 2017 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function
from rsconf import component
from pykern import pkcollections

class T(component.T):
    def internal_build(self):
        self.install_access(mode='400', owner=self.hdb.root_u)
        self.install_resource(
            'base_os/60-rsconf-base.conf',
            {},
            '/etc/sysctl.d/60-rsconf-base.conf',
        )
        self.append_root_bash_with_resource(
            'base_os/main.sh',
            {},
            'base_os_main',
        )
