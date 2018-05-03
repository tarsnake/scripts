from docker import Client
from travispy import TravisPy
import os
import git

# Create a Travis access token with the following scopes:
# read:org
# user:email
# repo_deployment
# repo:status
# write:repo_hook

# config start

file = '/tmp/last_build.txt'

git_dir = '/home/hass/home-assistant'
g = git.cmd.Git(git_dir)

github_token = '<your github token>'
t = TravisPy.github_auth(github_token)
repo = t.repo('<your github repo name>')

ha_container_name = '<home-assistant containername>'
# config end

t = TravisPy.github_auth(github_token)
cli = Client(base_url='unix://var/run/docker.sock')

build_status = t.build(repo.last_build_id).state
latest_build = t.build(repo.last_build_id).number

try:
    fo = open(file, 'r+')
    current_build = fo.read(10)
    fo.close()
except:
    fo = open(file, 'wb')
    fo.write(0 + '\n')

if int(current_build) < int(latest_build) and build_status = 'passed':
    print('Current build is: ' + current_build + 'Newer build '+ latest_build + ' available, pulling reposistory')
    g.pull()
    print('Restarting container ' + ha_container_name)
    cli.restart(container=ha_container_name)
    print ('Update file ' + file)
    fo = open(file, 'wb')
    fo.write(latest_build + '\n')
    fo.close()
else:
   print("No newer build available, nothing to do")