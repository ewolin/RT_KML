#!/bin/bash

open -a "Google Chrome" "https://igskgacgvmweb01.gs.doi.net/rt/Search/Results.html?Format=%27%3Cb%3E%3Ca+href%3D%22__WebPath__%2FTicket%2FDisplay.html%3Fid%3D__id__%22%3E__id__%3C%2Fa%3E%3C%2Fb%3E%2FTITLE%3A%23%27%2C%0A%27%3Cb%3E%3Ca+href%3D%22__WebPath__%2FTicket%2FDisplay.html%3Fid%3D__id__%22%3E__Subject__%3C%2Fa%3E%3C%2Fb%3E%2FTITLE%3ASubject%27%2C%0AStatus%2C%0AQueueName%2C%0AOwner%2C%0APriority%2C%0A%27__NEWLINE__%27%2C%0A%27__NBSP__%27%2C%0A%27%3Csmall%3E__Requestors__%3C%2Fsmall%3E%27%2C%0A%27__Created__%27%2C%0A%27%3Csmall%3E__CreatedRelative__%3C%2Fsmall%3E%27%2C%0A%27%3Csmall%3E__LastUpdatedRelative__%3C%2Fsmall%3E%27%2C%0A%27__CustomField.%7BANSS+Stations%7D__%27%2C%0A%27__CustomField.%7BGSN+Stations%7D__%27%2C%0A%27__CustomField.%7BN4+Stations%7D__%27&Order=DESC%7CASC%7CASC%7CASC&OrderBy=LastUpdated%7C%7C%7C&Page=1&Query=(+Queue+%3D+%27ANSS-backbone%27+OR+Queue+%3D+%27GSN%27+OR+Queue+%3D+%27N4+Network%27+)+AND+(++Status+%3D+%27__Active__%27+OR+Status+%3D+%27stalled%27+)&RowsPerPage=50&SavedChartSearchId=new&SavedSearchId="


echo "page opened, hit Feeds > Spreadsheet to download a tsv file!"
sleep 10;


mv $HOME/Downloads/Results.tsv Results_ASLStations.tsv
