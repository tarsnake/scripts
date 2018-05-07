# Scripts
## config-updater.py:
is a Python script to be used in a Docker environment. The script will get the latest build and status from Travis
and will do a git pull (of your Home-Assistant config) when there is a newer build available and restart the Docker
container.

Run the script from crontab (example):

sudo crontab -e

and enter the following line:

*/10 * * * * /usr/bin/python /home/user/scripts/config_updater.py

This wil run the script every 10 minutes.
