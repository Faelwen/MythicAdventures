import html_cleaner

from bs4 import BeautifulSoup
import re
import csv
import urllib.request
import re
import sys

spell_list = 'data/missing_spells.html'
csv_file = 'data/missing_spells.csv'

def parse_spell(statblock):
        name = statblock[0]
        [school, level] = re.search('School (.*); Level (.*)', statblock[1]).groups()
        cast_time = statblock[2].split('Casting Time ')[1]
        components = statblock[3].split('Components ')[1]
        range = statblock[4].split('Range ')[1]
        target = statblock[5].split(' ', 1)[1]
        duration = statblock[6].split(' ', 1)[1]
        try:
            [save, sr] =  re.search('Saving Throw:? (.*); Spell Resistance:? (.*)', statblock[7]).groups()
        except:
            try:
                [save, sr] =  re.search('Save:? (.*); Spell Resistance:? (.*)', statblock[7]).groups()
            except:
                [save, sr] =  re.search('Save:? (.*); SR:? (.*)', statblock[7]).groups()
        return [name, school, level, cast_time, components, range, target, duration, save, sr]

def extract_spells(soup, writer):
    for p in soup.find_all('p', "stat-block-title"):
        name = p.string
        tag = p
        description = '<h>Normal Use</h>'
        statblock = [name]
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
                    description += '<p>' + html_cleaner.get_content(html_cleaner.clean(tag)) + '</p>'
        writer.writerow([name] + parse_spell(statblock) + [description])


def main():
    with open(spell_list, 'r', encoding='utf-8') as spell_file, open(csv_file, 'w', newline='') as output_file:
        writer = csv.writer(output_file, delimiter ='\t', quotechar='"')
        raw_html = spell_file.read().replace('&minus;', '-').replace('&mdash', '--').replace('&ndash;','-').replace('&times;', 'x').replace('—', '--').replace('–', '–')
        soup = BeautifulSoup(raw_html, 'html.parser')
        extract_spells(soup, writer)


if __name__ == '__main__':
    main()