# -=- encoding: utf-8 -=-
#
# SFLvault - Secure networked password store and credentials manager.
#
# Copyright (C) 2008-2009  Savoir-faire Linux inc.
#
# Author: Alexandre Bourget <alexandre.bourget@savoirfairelinux.com>
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

__import__('pkg_resources').declare_namespace(__name__)

import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

import functools
import logging
import logging.config

import os
import sys

interpolation = { 'here': os.getcwd() }

settings = {}

def update_with_config_section(my_dict, config, section):
    for key in config._sections[section].keys():
        my_dict[key] = config.get(section, key, 0, interpolation)


class SFLvaultRequestHandler(SimpleXMLRPCRequestHandler):

    def __init__(self, request, client_address, server):
        self.client_address = client_address
        SimpleXMLRPCRequestHandler.__init__(self, request, client_address, server)

    def _dispatch(self, method, params):
        address = self.client_address

        request = {
            'REMOTE_ADDR': address[0],
            'PORT': address[1],
            'rpc_args': params,
            'settings': settings,
        }

        return self.server.instance._dispatch(request, method, params)

    rpc_paths = ('/vault', '/vault/rpc', '/',)

def main(config_file):

    logging.config.fileConfig(config_file)
    log = logging.getLogger(__name__)

    from sqlalchemy import engine_from_config
    #from controller.xmlrpc import SflVaultController

    from sflvault import model
    from sflvault.model import init_model
    from sflvault.lib.vault import SFLvaultAccess


    from datetime import datetime, timedelta
    import transaction

    import ConfigParser
    config = ConfigParser.ConfigParser({
        'sflvault.vault.session_timeout': 15,
        'sflvault.vault.setup_timeout': 300,
    })

    config.read(config_file)

    session_timeout = config.get('sflvault', 
                                 'sflvault.vault.session_timeout')


    setup_timeout = config.get('sflvault',
                               'sflvault.vault.setup_timeout')

    # Configure sqlalchemy
    update_with_config_section(settings, config, 'sflvault')
    engine = engine_from_config(settings,
                                'sqlalchemy.')
    init_model(engine)

    import sflvault.views
    from sflvault.views import XMLRPCDispatcher
    dispatcher = XMLRPCDispatcher()
    dispatcher.scan(sflvault.views)

    model.meta.metadata.create_all(engine)
    #Add admin user if not present
    if not model.query(model.User).filter_by(username='admin').first():
        log.info ("It seems like you are using SFLvault for the first time. An\
                'admin' user account will be added to the system.")
        u = model.User()
        u.waiting_setup = datetime.now() + timedelta(0,900)
        u.username = u'admin'
        u.created_time = datetime.now()
        u.is_admin = True
        #transaction.begin()
        model.meta.Session.add(u)
        transaction.commit()
        log.info("Added 'admin' user, you have 15 minutes to setup from your client")

    server = SimpleXMLRPCServer(("localhost", 8000),
                                requestHandler=SFLvaultRequestHandler,
                                allow_none=True)

    server.register_introspection_functions()
    server.register_instance(dispatcher)
    server.serve_forever()

if __name__ == '__main__':

    # FIXME: replace with argparse
    if len(sys.argv) == 2:
        config_file = sys.argv[1]
        main(config_file)