import pandas as pd
import json
import csv
import sys
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize

print (" Argument: {}". format ( sys . argv [1]))
filename = sys.argv[1]

table               = []
age_of_correction   = 65535
true_age            = 0
last_tow            = 0
previous_age        = 0
nb_sbas             = 0
iconSize            = 0.8
iconColor           = []
header              = ['tow','age of corrections']

kmlOutput = open (filename + "_1Hz.kml","w")
kmlOutput.write('<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n');
kmlOutput.write('<Document><Folder><name>GNSS</name>\n');

with open (filename,"r") as f:
    table  = [json.loads(line) for line in f]

    for json_data in table:
        # obs processing
        if json_data['msg_type'] == 30583:
            nb_sbas = False
            if json_data['sid']['code'] == 2:
                nb_sbas = True
        # age of corrections
        elif json_data['msg_type'] == 528:
            if json_data['tow']%1000 < 10:
                age_of_correction = json_data['age']
                if age_of_correction != 65535:
                    true_age = age_of_correction
                else:
                    true_age = previous_age + (json_data['tow']-last_tow)/100

                previous_age = true_age
                last_tow     = json_data['tow']
        # PVT
        elif json_data['msg_type'] == 522:
            if json_data['tow']%1000 < 10:

                new_record  = pd.DataFrame([[json_data['tow']/1000, true_age, columns=header)
                new_record.to_csv(filename + '_output.csv', columns=header, mode='a', header=False, index=False)

                if (nb_sbas and true_age>50):
                    iconColor = 'cc0073ff'  # Orange
                elif  (nb_sbas and true_age<51):
                    iconColor = 'cc00ff00'  # green
                else:
                    iconColor = 'FF000000'  # Black

                kmlOutput.write("<Placemark><Style><IconStyle><scale>{0}</scale><color>{1}</color></IconStyle></Style>\n".format(iconSize, iconColor));
                kmlOutput.write("<Point><coordinates>{0:3.6f},{1:3.6f},{2:4.2f}</coordinates></Point>\n".format(json_data['lon'],json_data['lat'],json_data['height']))
                kmlOutput.write('<description><![CDATA[<table width="180"><tr><td><p style="line-height:18px;"><font face="Arial"><b>TOW:</b>{0:6.2f} s</font></p></td></tr></table>]]></description></Placemark>\n'.format(json_data['tow']/1000))

kmlOutput.write("</Folder></Document></kml>\n");
kmlOutput.close()
