# Install both requests & Meraki Dashboard API Python modules:
# pip3 install --upgrade requests
# pip3 install --upgrade meraki

import csv, json
from datetime import datetime
import logging
import sys, os
from meraki import meraki


logger = logging.getLogger(__name__)

def configure_logging():

        logging.basicConfig(
            filename=os.pardir+'/logs/'+'{:%Y-%m-%d %H-%M-%S}.txt'.format(datetime.now()),
            level=logging.DEBUG,
            format='%(asctime)s: %(levelname)7s: [%(name)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

def main(netid, argfile, argmode):
    with open(os.path.join(os.pardir, "api/api_credentials.json"), "r") as creds:
        # Reads the api_credentials.json file for authentication
        keys = json.load(creds)

        # Defines the plain text API key generated in the Meraki portal
        apikey = keys[0]["apikey"]

    # Set default values for command line arguments
    netid = netid
    argfile = argfile
    argmode = argmode

    # Assign default mode to "check" unless "commit" specified
    if argmode != 'commit':
        argmode = 'check'

    fw_rules = []
    # Read CSV input file, and skip header row
    input_file = open(argfile)
    csv_reader = csv.reader(input_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    next(csv_reader, None)
    logger.info('Reading file {0}'.format(argfile))

    # Loop through each firewall rule from CSV file and build PUT data
    for row in csv_reader:
        rule = dict({'policy': row[0], 'protocol': row[1], 'srcCidr': row[2], 'srcPort': row[3], 'destCidr': row[4],
                     'destPort': row[5], 'comment': row[6],
                     'syslogEnabled': (row[7] == True or row[7] == 'True' or row[7] == 'true')})
        fw_rules.append(rule)
    print(fw_rules)
    old_rules = list(fw_rules)
    logger.info('Processed all {0} rules of file {1}'.format(len(fw_rules), argfile))

    # Check if last (default) rule exists, and if so, remove and check for default logging
    default_rule_exists = False
    default_logging = False
    last_rule = {'comment': 'Default rule', 'policy': 'allow', 'protocol': 'Any', 'srcPort': 'Any', 'srcCidr': 'Any',
                 'destPort': 'Any', 'destCidr': 'Any'}
    if all(item in fw_rules[-1].items() for item in last_rule.items()):
        default_rule_exists = True
        default_logging = (fw_rules.pop()['syslogEnabled'] == True)

    # Update MX L3 firewall rules
    if argmode == 'commit':
        meraki.updatemxl3fwrules(apikey, netid, fw_rules, default_logging)
        logger.info('Attempting update of firewall rules to network {0}'.format(netid))

        # Confirm whether changes were successfully made
        new_rules = meraki.getmxl3fwrules(apikey, netid)
        if default_rule_exists and new_rules[:-1] == old_rules[:-1]:
            logger.info('Update successful!')
        elif not (default_rule_exists) and new_rules[:-1] == old_rules:
            logger.info('Update successful!')
        else:
            logger.error('Uh oh, something went wrong...')
    else:
        logger.info('Simulating update of firewall rules to network {0}'.format(netid))


if __name__ == '__main__':
    # Configure logging to stdout
    configure_logging()
    # Define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # Set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # Tell the handler to use this format
    console.setFormatter(formatter)
    # Add the handler to the root logger
    logging.getLogger('').addHandler(console)

    with open(os.path.join(os.pardir,'api/')+'api_network_ids.csv', mode='r') as networkid:
        reader = csv.reader(networkid)
        next(reader, None) # Skips the row containing headers
        print("Warning you are about to push firewall rules to every network listed in 'api/api_network_ids.csv'.")
        argmode = input("Press enter to run in check mode, else type 'commit' to push changes: ")
        for row in reader:
            argfile = os.path.join(os.pardir,'data/')+row[0]+'.csv'
            main(row[0], argfile,argmode)

    # Output to logfile/console starting inputs
    start_time = datetime.now()
    logger.info('Started script at {0}'.format(start_time))


    # Finish output to logfile/console
    end_time = datetime.now()
    logger.info('Ended script at {0}'.format(end_time))
    logger.info(f'Total run time = {end_time - start_time}')