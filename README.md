# RT_KML
Grab tickets from RT, DQA metrics, etc. and show in a Google Earth KML to assist with maintenance planning and quality control.

To generate a KML with station status info, links to tickets, etc.:
1. Be on the USGS network or VPN
2. Create a copy of config.ini.example named config.ini with your RT login info
3. Run rt2kml.py to create ASL_RTtickets.kml
4. Open network link file ASL_Station_Status.kml to get an auto-refreshing KML

Must be on USGS network or VPN for this to work!

Also requires a conda environment with rt (https://github.com/CZ-NIC/python-rt) and fastkml (install from conda-forge).


to run as a cron job every 30 min: 
```
crontab -e
SHELL=/bin/bash
BASH_ENV=~/.conda_profile
*/30 * * * * cd /path/to/repo; /path/to/python/env/ rt2kml.py; cd
```
