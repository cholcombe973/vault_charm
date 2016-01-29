import shutil
import os

from charmhelpers.core import hookenv
from charmhelpers.core.host import log
from charmhelpers.core.templating import render
from charms.reactive import when


@when('consul.available')
def setup_vault(consul):
    shutil.copyfile('vault', '/usr/local/bin/vault')
    pass


def setup_upstart_jobs():
    hookenv.log('setting up upstart jobs')
    working_dir = os.getcwd()
    charm_upstart_conf = "/var/lib/charm/{}/upstart.conf".format('vault')
    os.mkdir(os.path.dirname(charm_upstart_conf))
    context = {'decoder_path': '{}/hooks/vault'.format(working_dir), 'name': 'vault'}

    render('upstart.conf', charm_upstart_conf, context, perms=0o644)
    log('copying {} to /etc/init'.format(charm_upstart_conf))
    shutil.copy(charm_upstart_conf, '/etc/init/vault.conf')


def install():
    hookenv.log('Installing vault')
    setup_upstart_jobs()
