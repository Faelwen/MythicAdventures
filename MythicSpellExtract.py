from bs4 import BeautifulSoup
import re
import csv

html_file = 'test/Protection from Chaos_Evil_Good_Law.htm'
csv_file = 'data/mythic_feats.csv'


def get_content(tag):
    result = ""
    for element in tag.contents:
        result += str(element)
    return result


def clean(soup):
    # strip all attributes
    for tag in soup.find_all(True):
    	tag.attrs = {}

    # replace <h?> by <h>
    for h1 in soup.find_all("h1"):
    	h1.name = "h"
    for h2 in soup.find_all("h2"):
    	h2.name = "h"
    for h3 in soup.find_all("h3"):
    	h3.name = "h"

    # remove <caption> and content
    for tag in soup.find_all('caption'):
        tag.decompose()

    # put content of <th> in bold, replace <th> by <td>
    for th in soup.find_all("th"):
        th.string.wrap(soup.new_tag("b"))
        th.name = "td"

    #replace <em> with <i>
    for em in soup.find_all('em'):
    	em.name = "i"

    #replace <strong> with <b>
    for strong in soup.find_all('strong'):
    	strong.name = "b"

    # remove <a> links
    for a in soup.find_all("a"):
    	a.unwrap()

    return soup


with open(html_file, 'r') as input_file:
    raw_html = input_file.read().replace('&minus;', '-').replace('&mdash', '--').replace('&ndash;','-').replace('&times;', 'x').replace('—', '-')
soup = BeautifulSoup(raw_html, 'html.parser')

for p in soup.find_all('p', "stat-block-title"):
    print(p)
    tag = p
    while (True):
        tag = tag.next_sibling
        if tag == None:
            break
        if tag.name == 'p':
            #print(tag)
