# Install both requests & Meraki Dashboard API Python modules:
# pip3 install --upgrade requests
# pip3 install --upgrade meraki


import csv, json
from datetime import datetime
import os
from meraki import meraki

def main(netid, argfile):
    with open(os.path.join(os.pardir, "api/api_credentials.json"), "r") as creds:
        # Reads the api_credentials.json file for authentication
        keys = json.load(creds)

        # Defines the plain text API key generated in the Meraki portal
        apikey = keys[0]["apikey"]

    # Set default values for command line arguments
    netid = netid

    # Set the CSV output file and write the header row
    timenow = '{:%Y%m%d_%H%M%S}'.format(datetime.now())
    filename = 'mx_l3fw_rules_{0}.csv'.format(timenow)
    output_file = open(os.path.join(os.pardir, 'data/') + netid + '.csv', mode='w')
    field_names = ['policy', 'protocol', 'srcCidr', 'srcPort', 'destCidr', 'destPort', 'comment', 'logging']
    csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    csv_writer.writerow(field_names)

    # Read Dashboard configuration of MX L3 firewall rules
    fw_rules = meraki.getmxl3fwrules(apikey, netid)

    # Loop through each firewall rule and write to CSV
    for rule in fw_rules:
        csv_row = [rule['policy'], rule['protocol'], rule['srcCidr'], rule['srcPort'], rule['destCidr'],
                   rule['destPort'], rule['comment'], rule['syslogEnabled']]
        csv_writer.writerow(csv_row)

    output_file.close()
    print('Export completed to file {0}'.format(filename))


if __name__ == '__main__':
    with open(os.path.join(os.pardir, 'api/') + 'api_network_ids.csv', mode='r') as networkid:
        reader = csv.reader(networkid)
        next(reader, None)  # Skips the row containing headers
        for row in reader:
            argfile = os.path.join(os.pardir, 'data/') + row[0] + '.csv'
            main(row[0], argfile)