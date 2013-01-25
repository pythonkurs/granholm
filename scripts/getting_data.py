#!/usr/bin/env python

import requests
from lxml import etree

def main():
    '''
    Import NY subway escalator outage data, print the fraction of those that are in 'REPAIR'
    '''
    # Download and initialize up XML-tree and variables
    r = requests.get('http://www.grandcentral.org/developers/data/nyct/nyct_ene.xml')
    root = etree.XML(r.content)
    num_of_repair = 0.0
    total_num = 0.0
    # Iterate through outages in XML file
    for reason_elem in root.findall('outage/reason'):
        total_num += 1
        if reason_elem.text == 'REPAIR':
            num_of_repair += 1
    # Calculate fraction and print
    repair_fraction = num_of_repair/total_num
    print 'The fraction of escalator outages with reason \"REPAIR\": %.3f' % (repair_fraction)

if __name__ == '__main__':
    main()
