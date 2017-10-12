from bs4 import BeautifulSoup
import re
import csv
import urllib.request

html_file = 'test/Animate Dead.htm'
csv_file = 'data/mythic_spells.csv'
url_test = 'http://paizo.com/pathfinderRPG/prd/coreRulebook/spells/animateDead.html#animate-dead'


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


def get_link(tag):
    return tag.a["href"]


def get_content(tag):
    result = ""
    for element in tag.contents:
        result += str(element)
    return result


def extract_mythic_spells(soup):
    for p in soup.find_all('p', "stat-block-title"):
        tag = p
        name = tag.string
        description = ""
        while (True):
            tag = tag.next_sibling
            if tag == None:
                break
            if tag.name == 'p':
                if tag.has_attr("class"):
                    if tag["class"][0] == "stat-block-title":
                        break
                    elif tag["class"][0] == "stat-block-1":
                        link = get_link(tag)
                else:
                    if tag.b != None:
                        tag.b.name = 'h'
                    description += '<p>' + get_content(clean(tag)) + '</p>'
        print("{0} - {1} - {2}".format(name, link, description))


##with open(html_file, 'r') as input_file:
##    raw_html = input_file.read().replace('&minus;', '-').replace('&mdash', '--').replace('&ndash;','-').replace('&times;', 'x').replace('—', '-')
##soup = BeautifulSoup(raw_html, 'html.parser')

raw_html = urllib.request.urlopen(url_test).read().decode('utf-8').replace('&minus;', '-').replace('&mdash', '--').replace('&ndash;','-').replace('&times;', 'x').replace('—', '-')
soup = BeautifulSoup(raw_html, 'html.parser')

