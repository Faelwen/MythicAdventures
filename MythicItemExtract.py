import html_cleaner

from bs4 import BeautifulSoup
import re
import csv
import urllib.request
import re
import sys

item_list = 'html/Magic Items.html'
csv_file = 'data/Magic Items.csv'


def extract_items(soup, writer):
    for p in soup.find_all('p', "stat-block-title"):
        name = p.string
        tag = p
        description = ""
        statblock = ""
        construction = ""
        is_statblock = True
        while True:
            tag = tag.next_sibling
            if tag == None:
                break
            if tag.name == 'p':
                if tag.has_attr("class"):
                    if tag["class"][0] == "stat-block-title":
                        break
                    elif tag["class"][0] == "stat-block":
                        description += '<p>' + html_cleaner.get_content(html_cleaner.clean(tag)) + '</p>'
                        is_statblock = False
                    elif tag["class"][0] == "stat-block-breaker":
                        description += '<h>Construction Requirements</h>'
                    elif tag["class"][0] == "stat-block-1":
                        if is_statblock:
                            statblock += tag.text
                        else:
                            construction += tag.text + ', '
                        description += '<p>' + html_cleaner.get_content(html_cleaner.clean(tag)) + '</p>'
        writer.writerow([name, description, construction.replace('\n', '')[:-2]])


def main():
    with open(item_list, 'r', encoding='utf-8') as spell_file, open(csv_file, 'w', newline='') as output_file:
        writer = csv.writer(output_file, delimiter ='\t', quotechar='"')
        raw_html = spell_file.read().replace('&minus;', '-').replace('&mdash', '--').replace('&ndash;','-').replace('&times;', 'x').replace('—', '--').replace('–', '–')
        soup = BeautifulSoup(raw_html, 'html.parser')
        extract_items(soup, writer)


if __name__ == '__main__':
    main()