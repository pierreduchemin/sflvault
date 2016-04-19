# -=- encoding: utf-8 -=-
#
# SFLvault - Secure networked password store and credentials manager.
#
# Copyright (C) 2016 Savoir-faire Linux inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

dependencies = [
    "pycrypto",
    "decorator",
    "urwid",
    "pexpect",
    "keyring>=2.0,<8.0"
]

setup(
    name='sflvault',
    version="0.8.0",
    description='Networked credentials store and authentication manager - Client',
    author='Alexandre Bourget',
    url='http://www.sflvault.org',
    license='GPLv3',
    install_requires=dependencies,
    packages=find_packages(),
    entry_points="""
    [console_scripts]
    sflvault = sflvault.client.commands:main

    [sflvault.services]
    ssh = sflvault.client.services:ssh
    ssh+pki = sflvault.client.services:ssh_pki
    content = sflvault.client.services:content
    sflvault = sflvault.client.services:sflvault
    vnc = sflvault.client.services:vnc
    mysql = sflvault.client.services:mysql
    psql = sflvault.client.services:postgres
    postgres = sflvault.client.services:postgres
    postgresql = sflvault.client.services:postgres
    su = sflvault.client.services:su
    sudo = sflvault.client.services:sudo

    """,
)
