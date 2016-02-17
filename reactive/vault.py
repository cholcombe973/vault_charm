import shutil
import os

from charmhelpers.core import hookenv
from charmhelpers.core.host import log, mkdir
from charmhelpers.core.templating import render
from charms.reactive import when, when_not, hook
from charms.reactive import is_state, set_state, remove_state

from charmhelpers.core.host import (
    adduser,
    service_stop,
    service_restart,
    service_running,
    service_start,
)


@when('consul.available')
@when_not('vault.running')
def setup_vault(consul):
    render(
        source='config.hcl',
        target='/etc/vault/config.hcl',
        context={
            'private_address': hookenv.unit_get('private-address') 
        }
    )
    service_restart('vault')
    set_state('vault.running')


@when('vault.running')
@when_not('vault.initialized')
def initialize_vault():
    log("Running initialize_vault now")
    set_state('vault.initialized')


def setup_upstart_jobs():
    hookenv.log('setting up upstart jobs')
    context = {
        'vault_path': '/usr/local/bin/vault',
        'name': 'vault',
        'vault_options': '--config=/etc/vault/config.hcl'
    }
    render('upstart.conf', '/etc/init/vault.conf', context, perms=0o644)
    service_stop('vault')


@hook('stop')
def stop():
    service_stop('vault')
    remove_state('vault.running')


@hook('install')
def install():
    hookenv.log('Installing vault')
    shutil.copyfile('{}/files/vault-0.5.0'.format(hookenv.charm_dir()), '/tmp/vault')
    mkdir('/usr/local/bin')
    shutil.move('/tmp/vault', '/usr/local/bin/vault')
    setup_upstart_jobs()
    hookenv.open_port(8200)
