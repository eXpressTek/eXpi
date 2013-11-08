from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

#env.hosts = ['pi@garage']
#env.hosts = ['pi@172.16.19.54','pi@172.16.19.57']

def test():
    with settings(warn_only=True):
        result = local('./manage.py test my_app', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")

def enableSPI():
    run("sudo modprobe spi-bcm2708");
    run("sudo perl -p -i.bak -e 's/^blacklist spi-bcm2708$/#blacklist spi-bcm2708/g' /etc/modprobe.d/raspi-blacklist.conf");

def nfsClient():
    run("sudo apt-get install nfs-client --yes --quiet");
    run("sudo mkdir -p /mnt/nas03");
    run("sudo service rpcbind start");
    run("sudo mount xtifrnas03:/mnt/nas03 /mnt/nas03");

def update():
    run("sudo rpi-update");
    run("sudo apt-get update --yes --quiet");
    run("sudo apt-get install --yes --quiet");
#    local("git add -p && git commit")

def restart():
    run("sudo shutdown -r now");

def commit():
    local("git add -p && git commit")

def push():
    local("git push")

def prepare_deploy():
    test()
    commit()
    push()

def deploy():
    code_dir = '/srv/django/myproject'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone user@vcshost:/path/to/repo/.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        run("touch app.wsgi")

