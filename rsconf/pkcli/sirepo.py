# -*- coding: utf-8 -*-
u"""sirepo configuration commands

:copyright: Copyright (c) 2017 Bivio Software, Inc.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function

def create_beaker_secret(path):
    """Generate flask beaker secret

    Args:
        path (str): where to write the secret

    Returns:
        path: what was created
    """
    import random, string, sys
    from pykern import pkio

    y = string.digits + string.letters + string.punctuation
    x = ''.join(random.choice(y) for _ in range(64))
    with open(path, 'wb') as f:
        f.write(x)
    return path
