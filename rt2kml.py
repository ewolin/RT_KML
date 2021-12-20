#!/usr/bin/env python


# grab a list of RT tickets, associate with a station, and plot as KML

# example search:
# go to Feeds > Spreadsheet and download a .tsv
# https://igskgacgvmweb01.gs.doi.net/rt/Search/Results.html?Format=%27%3Cb%3E%3Ca%20href%3D%22__WebPath__%2FTicket%2FDisplay.html%3Fid%3D__id__%22%3E__id__%3C%2Fa%3E%3C%2Fb%3E%2FTITLE%3A%23%27%2C%0A%27%3Cb%3E%3Ca%20href%3D%22__WebPath__%2FTicket%2FDisplay.html%3Fid%3D__id__%22%3E__Subject__%3C%2Fa%3E%3C%2Fb%3E%2FTITLE%3ASubject%27%2C%0AStatus%2C%0AQueueName%2C%0AOwner%2C%0APriority%2C%0A%27__NEWLINE__%27%2C%0A%27__NBSP__%27%2C%0A%27%3Csmall%3E__Requestors__%3C%2Fsmall%3E%27%2C%0A%27__Created__%27%2C%0A%27%3Csmall%3E__CreatedRelative__%3C%2Fsmall%3E%27%2C%0A%27%3Csmall%3E__LastUpdatedRelative__%3C%2Fsmall%3E%27%2C%0A%27__CustomField.%7BANSS%20Stations%7D__%27%2C%0A%27__CustomField.%7BN4%20Stations%7D__%27%2C%0A%27__CustomField.%7BN4%2FANSS%20Equipment%20Affected%7D__%27&Order=DESC%7CASC%7CASC%7CASC&OrderBy=LastUpdated%7C%7C%7C&Query=(%20Queue%20%3D%20%27ANSS-backbone%27%20OR%20Queue%20%3D%20%27N4%20network%27%20)%20AND%20(%20%20Status%20%3D%20%27stalled%27%20OR%20Status%20%3D%20%27__Active__%27%20)&RowsPerPage=50&SavedChartSearchId=new&SavedSearchId=new


# to search all active and stalled tickets in ANSS, N4, or GSN queues:
# https://igskgacgvmweb01.gs.doi.net/rt/Search/Results.html?Format=%27%3Cb%3E%3Ca+href%3D%22__WebPath__%2FTicket%2FDisplay.html%3Fid%3D__id__%22%3E__id__%3C%2Fa%3E%3C%2Fb%3E%2FTITLE%3A%23%27%2C%0A%27%3Cb%3E%3Ca+href%3D%22__WebPath__%2FTicket%2FDisplay.html%3Fid%3D__id__%22%3E__Subject__%3C%2Fa%3E%3C%2Fb%3E%2FTITLE%3ASubject%27%2C%0AStatus%2C%0AQueueName%2C%0AOwner%2C%0APriority%2C%0A%27__NEWLINE__%27%2C%0A%27__NBSP__%27%2C%0A%27%3Csmall%3E__Requestors__%3C%2Fsmall%3E%27%2C%0A%27__Created__%27%2C%0A%27%3Csmall%3E__CreatedRelative__%3C%2Fsmall%3E%27%2C%0A%27%3Csmall%3E__LastUpdatedRelative__%3C%2Fsmall%3E%27%2C%0A%27__CustomField.%7BANSS+Stations%7D__%27%2C%0A%27__CustomField.%7BGSN+Stations%7D__%27%2C%0A%27__CustomField.%7BN4+Stations%7D__%27&Order=DESC%7CASC%7CASC%7CASC&OrderBy=LastUpdated%7C%7C%7C&Page=1&Query=(+Queue+%3D+%27ANSS-backbone%27+OR+Queue+%3D+%27GSN%27+OR+Queue+%3D+%27N4+Network%27+)+AND+(++Status+%3D+%27__Active__%27+OR+Status+%3D+%27stalled%27+)&RowsPerPage=50&SavedChartSearchId=new&SavedSearchId=

# search for current US and N4 stations using IRIS FDSNWS: 
# https://service.iris.edu/fdsnws/station/1/query?net=US,N4&sta=*&loc=*&cha=*&starttime=2021-07-01&level=station&format=text&includecomments=true&nodata=404

# or all networks currently maintained by ASL: 
# https://ds.iris.edu/gmap/#network=IU,IC,CU,US,N4,GS,NE,IW&starttime=2021-07-01&planet=earth

# IRIS KML: 
# https://ds.iris.edu/gmap/#network=US,N4&starttime=2021-07-01&planet=earth
# note: as of 2021-07-16 I had to manually edit the downloaded KML slightly
# header needs to look like this:
# <?xml version="1.0" encoding="UTF-8"?>
# <kml xmlns:atom="http://www.w3.org/2005/Atom" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns="http://www.opengis.net/kml/2.2">
# <Document> 
# with corresponding /Document and /kml tags at the end

# use fastkml conda environment
import configparser
import pandas as pd
from fastkml import kml
from fastkml import styles


#from dqatools import dqaclient
import dqaclient
from io import StringIO

import datetime as dt

import matplotlib.pyplot as plt


import json
import rt

# DQA has metrics up to 3 days ago
threedaysago = dt.datetime.utcnow() - dt.timedelta(days=3)
# get a 7-day average:
tendaysago = dt.datetime.utcnow() - dt.timedelta(days=10)

dqa_dead = dqaclient.call_dqa(metric='DeadChannelMetric:4-8',begin=(tendaysago.strftime("%Y-%m-%d")))
names = ['Date', 'Net', 'Sta', 'Loc', 'Cha', 'Metric', 'MetricVal']
df_dead = pd.read_csv(StringIO(dqa_dead), parse_dates=[0], names=names,
                      sep='\s+', dtype={'Loc':str})


dqa_avail = dqaclient.call_dqa(metric='AvailabilityMetric',begin=(tendaysago.strftime("%Y-%m-%d")))
df_avail = pd.read_csv(StringIO(dqa_avail), parse_dates=[0], names=names,
                       sep='\s+', dtype={'Loc':str})

# read downloaded search results from RT
#df = pd.read_csv('Results.tsv', sep='\t')
#df = pd.read_csv('Results_US-N4.tsv', sep='\t')

#df = pd.read_csv('Results_ASLStations.tsv', sep='\t')


#############
config = configparser.ConfigParser()
config.read('config.ini')
tracker= rt.Rt('https://igskgacgvmweb01.gs.doi.net/rt/REST/1.0', config['RT']['user'], config['RT']['pwd'] ,verify_cert=False)

tracker.login()
print('logged into RT')

#meh = tracker.search(raw_query="( Queue = 'ANSS-backbone' OR Queue = 'GSN' OR Queue = 'N4 Network' ) AND (  Status = '__Active__' OR Status = 'stalled' )", Queue=rt.ALL_QUEUES, order='-Created') 
meh = tracker.search(raw_query="( Queue = 'ANSS-backbone' OR Queue = 'GSN' OR Queue = 'N4 Network' OR Queue = 'Aftershock' ) AND (  Status = '__Active__' OR Status = 'stalled' )", Queue=rt.ALL_QUEUES, order='-Created') 

#print(meh)

#print(len(meh))


df = pd.read_json(json.dumps(meh))
#############

#df[df['CustomField.{ANSS Stations}'] == 'AGMN' ]
df[df['CF.{ANSS Stations}'] == 'AGMN' ]
# when using rt package (NOT spreadsheet), need to use CF instead




# read downloaded KML from IRIS

#kml_file = 'US_2021-07.kml'
#kml_file = 'US-N4_2021-07.kml'
#kml_file = 'ASLStations_2021-07.kml'
kml_file = 'ASLStations_2021-10.kml'
myfile = open(kml_file, 'r')
kmldoc = myfile.read()
myfile.close()

k = kml.KML()
#k.from_string(kmldoc)
k.from_string(kmldoc.encode('utf-8'))


features = list(k.features())
doc = features[0]

#netname = 'US'
netname = 'US-N4'
doc.name='ASL_RTtickets'
#doc.name=f'{netname}_RTtickets'

#icon_href = 'http://ds.iris.edu/static/img/markers/circle-dot-10x10-33CC33.27295a36c313.png'
icon_href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
#icon_href = 'http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png'
#icon_href = '/Users/ewolin/code/RT_KML/circle.png'

for j in doc.features():
    color = '#ff00ffff' # yellow
    sta = j.name.split('.')[-1]
    net = j.name.split('.')[0]
    #print(j.name, net, sta)
    if net == "N4":
        df_small = df[df['CF.{N4 Stations}'] == sta ]
    elif net in [ "IU", "CU", "IC" ] :
        df_small = df[df['CF.{GSN Stations}'] == sta ]
    elif net in [ "IW", "NE"] : 
        df_small = df[ df['CF.{ANSS Stations}'] == f'{net}-{sta}']
    elif net == "GS":
        df_small = df[ df['Subject'].str.contains(sta)] 
    else:
        df_small = df[ df['CF.{ANSS Stations}'] == sta ]
        

    #print(df_small)

    avg_dead = df_dead[df_dead['Sta'] == sta]['MetricVal'].mean()
    avg_avail = df_avail[df_avail['Sta'] == sta]['MetricVal'].mean()
    #print(avg_dead, 'avg_dead')
    if avg_dead < 1.0:
        color = '#ff0000ff' #red
    elif avg_avail < 90:
        color = '#ff0000ff' #red

    dead_color='black'
    if avg_dead < 0.99:
        dead_color = 'red'
    elif avg_dead >= 0.99:
        dead_color = 'green'

    avail_color='black'
    if avg_avail < 90:
        avail_color='red'
    elif avg_avail >= 90:
        avail_color='green'

    if len(df_small) == 0 and avg_dead > 0.99 and avg_avail > 90:
        color = 'green'


## plot availability and dead channel metric
#    df_test = df_avail[df_avail['Sta'] == sta]
#    df_uniq_lc = df_test[['Loc','Cha']].drop_duplicates()
#    for l,c in zip(df_uniq_lc['Loc'], df_uniq_lc['Cha']):
#        print(l,c)
#        df_select = df_test[(df_test['Loc'] == l) & (df_test['Cha'] == c)]
#        print(df_select)
#        plt.plot(df_select['Date'], df_select['MetricVal'])
#        plt.gca().set_ylim(-5,105)
#        plt.gcf().autofmt_xdate()
        

    icon = styles.IconStyle(scale=len(df_small)+1, icon_href=icon_href, color=color)
    for style in j.styles():
        #print('--',style)
        for s in style.styles():
            #print('----',s)
            s.text = f"<h1> {net}.{sta}</h1>" 
            s.text += f"<table width =\"600\"><tr><h2> Active or Stalled RT Tickets:</h2></tr>" 
            if len(df_small) == 0:
                s.text += "<tr>No open or stalled tickets</tr>"
            else:
                s.text += f"<tr><td width=10%>Ticket #</td><td width=60%>Subject</td><td width=30%>Last Updated</td></tr> "
                for index, row in df_small.iterrows():
                    sub = row['Subject']
                    tid = row['id'].split('/')[-1]
#                    lup = row['LastUpdatedRelative']
                    lup = row['LastUpdated']
                    href = f'https://igskgacgvmweb01.gs.doi.net/rt/Ticket/Display.html?id={tid}' 
                    s.text += f"<tr><td width=10%>{tid}</td><td width=60%><a href='{href}'> {sub}</a></td><td width=30%>{lup}</td></tr> "
            s.text += "</table>"
            all_href = f'https://igskgacgvmweb01.gs.doi.net/rt/Search/Simple.html?q={sta}'
            s.text += f"\n<a href='{all_href}'> Search RT for all tickets containing {sta}</a>"
            #s.text += "</td></tr></table>"
            s.text += f'<h2> Past 7 days:</h2>' 
            s.text += f'<p style=\"color:{avail_color};\"> Availability: {avg_avail:.2f}%</p>'
            s.text += f'<p style=\"color:{dead_color};\"> Non-dead BB channels: {avg_dead*100:.2f}% </p>'
            dashboard_url = f"https://igskgacgvmwebx1.gs.doi.net/dashboard/station/{net}/{sta}"
            dqa_url = f"https://igskgacgvmweb01.gs.doi.net/dqa/N4/summary/?network={net}&station={sta}"
            sis_url = f"https://anss-sis.scsn.org/sis/find/?lookup={sta}"
            mda_url = f"https://ds.iris.edu/mda/{net}/{sta}"
            if net in ["IU", "US"]:
                ch = "BH"
            else:
                ch = "HH"
            spectro_url = f"http://service.iris.edu/mustang/noise-spectrogram/1/query?net={net}&sta={sta}&loc=00&cha={ch}Z&quality=M&output=power&format=plot&plot.color.palette=YlGnBu&plot.color.invert=true&plot.horzaxis=time&plot.time.matchrequest=true&plot.time.tickunit=auto&plot.time.invert=false&plot.powerscale.show=true&plot.powerscale.range=-180,-110&plot.powerscale.orientation=horz&nodata=404"
            s.text += f"\n<a href='{dashboard_url}'> DQA Dashboard for {net} {sta}</a><br>"
            s.text += f"\n<a href='{dqa_url}'> DQA page for {net} {sta}</a><br>"
            s.text += f"\n<a href='{mda_url}'> IRIS MDA page for {net} {sta}</a><br>"
            s.text += f"\n<a href='{sis_url}'> SIS page for {net} {sta}</a><br>"
            s.text += f"\n<a href='{spectro_url}'> Noise-spectrogram for {net} {sta} 00 {ch}Z</a><br>"
#            s.text += "<h1 style=\"color:blue;\">This is a heading</h1> \
#<p style=\"color:red;\">This is a paragraph.</p>" 
        j._styles[0].append_style(icon)

    if len(df_small) == 0 and avg_dead > 0.99 and avg_avail > 90:
        j.visibility = 0



outfile = open(f'{doc.name}.kml', 'w')
outfile.write(k.to_string(prettyprint=True))
outfile.close()
print(f"wrote {doc.name}.kml")
