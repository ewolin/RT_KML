# RT_KML
Grab tickets from RT, DQA metrics, etc. and show in a Google Earth KML to assist with maintenance planning and quality control.

To generate a KML with station status info, links to tickets, etc.:
1. Be on the USGS network or VPN
2. Create a copy of config.ini.example named config.ini with your RT login info
3. Run rt2kml.py to create ASL_RTtickets.kml
4. Open network link file ASL_Station_Status.kml to get an auto-refreshing KML

Must be on USGS network or VPN for the DQA and RT queries to work!
After that you can view the KML and ticket subjects off-line if needed.

Also requires a conda environment with rt (https://github.com/CZ-NIC/python-rt) and fastkml (install from conda-forge).


to run as a cron job every 30 min: 
```
crontab -e
SHELL=/bin/bash
BASH_ENV=~/.conda_profile
*/30 * * * * cd /path/to/repo; /path/to/python/env/ rt2kml.py; cd
```

![example_image](https://user-images.githubusercontent.com/6301484/136247866-e947db4f-4fb1-4157-9fe6-46f6b6dbdf55.jpg)


To dos:

- [ ] Add DQA timing quality metric to list of critical issues (turns a dot red)
- [ ] Get channel metadata - for better handling of links to spectrograms, PSDs, etc and smart handling of strong-motion-only sites
- [ ] Code cleanup: make it easier to set symbol size/color, and maybe more flexibility in adding/selecting/weighting metrics?
