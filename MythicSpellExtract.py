from bs4 import BeautifulSoup
import re
import csv
import urllib.request
import re
import sys

spell_list = 'data/spell-links.txt'
csv_file = 'data/mythic_spells.csv'


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


def extract_mythic_spells(soup, writer):
    for p in soup.find_all('p', "stat-block-title"):
        tag = p
        name = tag.string
        print(name)
        description = "<h>Mythic Enhanced</h>"
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
                        tag.b.string = "Mythic " + tag.b.string
                        tag.b.name = 'h'
                    description += '<p>' + get_content(clean(tag)) + '</p>'
        try:
            raw_html = urllib.request.urlopen('http://paizo.com' + link).read().decode('utf-8').replace('&minus;', '-').replace('&mdash', '--').replace('&ndash;','-').replace('&times;', 'x').replace('—', '-')
            soup_normal_spell = BeautifulSoup(raw_html, 'html.parser')
            row = [name] + extract_normal_spell(soup_normal_spell) + [link]
        except:
            row = [name, sys.exc_info()]
        writer.writerow(row)


def extract_normal_spell(soup):
    p = soup.find('p', 'stat-block-title')
    statblock = []
    statblock.append(p.text)
    description = "<h>Normal Use</h>"
    tag = p
    while True:
        tag = tag.next_sibling
        if tag == None:
            break
        if tag.name == 'p':
            if tag.has_attr("class"):
                if tag["class"][0] == "stat-block-title":
                    break
                elif tag["class"][0] == "stat-block-1":
                   statblock.append(tag.text)
            else:
               description += '<p>' + get_content(clean(tag)) + '</p>'
    return parse_spell(statblock)


def parse_spell(statblock):
    try:
        name = statblock[0]
        [school, level] = re.search('School (.*); Level (.*)', statblock[1]).groups()
        cast_time = statblock[2].split('Casting Time ')[1]
        components = statblock[3].split('Components ')[1]
        range = statblock[4].split('Range ')[1]
        target = statblock[5].split(' ', 1)[1]
        duration = statblock[6].split(' ', 1)[1]
        [save, sr] =  re.search('Saving Throw:? (.*); Spell Resistance:? (.*)', statblock[7]).groups()
    except:
        print("Error !!!")
        [name, school, level, cast_time, components, range, target, duration, save, sr] = [sys.exc_info(), statblock, " ",  " ", " ", " ", " ", " ", " ", " "]
    return [name, school, level, cast_time, components, range, target, duration, save, sr]


def main():
    with open(spell_list, 'r') as spell_file, open(csv_file, 'w', newline='') as output_file:
        writer = csv.writer(output_file, delimiter ='\t', quotechar='"')
        for link in spell_file:
            raw_html = urllib.request.urlopen(link.strip()).read().decode('utf-8').replace('&minus;', '-').replace('&mdash', '--').replace('&ndash;','-').replace('&times;', 'x').replace('—', '-')
            soup = BeautifulSoup(raw_html, 'html.parser')
            extract_mythic_spells(soup, writer)


if __name__ == '__main__':
    main()