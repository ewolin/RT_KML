# RT_KML
Grab tickets from RT, DQA metrics, etc. and show in a Google Earth KML to assist with maintenance planning and quality control.

To generate a KML with station status info, links to tickets, etc.:
1. Be on the USGS network or VPN
2. Create a copy of config.ini.example named config.ini with your RT login info
3. Run rt2kml.py to create ASL_RTtickets.kml
4. Open network link file ASL_Station_Status.kml to get an auto-refreshing KML
Must be on USGS network or VPN for this to work!
