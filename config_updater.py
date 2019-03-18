# modified from https://github.com/wpeterw/scripts

from docker import Client
import os
import git
import requests

# ##############################################################################################################
#                                                                                                              #
# Python script to check for a new build of your HomeAssistant config, pull repo and restart docker container  #
#                                                                                                              #
################################################################################################################


# grab env variables

envfile = '/media/data/docker/.env'
with open(envfile) as f:
    for line in f:
        k, v = line.split('=')
        os.environ[k] = v.strip()

# config start

# file to store latest build number from Travis
file = os.environ['USERDIR'] + '/docker/tmp/last_build.txt'

# git
git_dir = os.environ['USERDIR'] + '/docker/homeassistant:/config'
g = git.cmd.Git(git_dir)

# travis
github_token = os.environ['GHTOKEN']
travis_url = 'https://api.travis-ci.org/repos/your/repo/builds'

# docker
ha_container_name = 'homeassistant'
cli = Client(base_url='unix://var/run/docker.sock')
# config end

r = requests.get(url = travis_url)
build_info = (r.json()[0])
build_status = build_info['result']
latest_build = build_info['number']
initial_build = '0'

# read latest buildnumber from file, if file does not exist create it with buildnumber = 0
try:
    fo = open(file, 'r+')
    current_build = fo.read(10)
    fo.close()
except:
    fo = open(file, 'wb')
    fo.write(initial_build + '\n')
    fo.close()
    current_build = initial_build

# check buildnumber and status against current buildnumber, pull, restart container or do nothing
if int(current_build) < int(latest_build) and build_status == 0:
    print('Current build is: ' + current_build + 'Newer build '+ latest_build + ' available, pulling reposistory')
    g.pull()
    print('Restarting container ' + ha_container_name)
    cli.restart(container=ha_container_name)
    print ('Update file ' + file)
    fo = open(file, 'wb')
    fo.write(latest_build + '\n')
    fo.close()
else:
   print("No newer build available or build failed,  nothing to do")

