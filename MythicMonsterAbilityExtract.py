from bs4 import BeautifulSoup
import re
import csv

html_file = 'data/mythic_monsters_abilities.html'
csv_file = 'data/mythic_monsters_abilities.csv'


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


def main():
    with open(html_file, 'r') as input_file:
        raw_html = input_file.read().replace('&minus;', '-').replace('&mdash', '--').replace('&ndash;','-').replace('&times;', 'x').replace('â€”', '-')
    soup = BeautifulSoup(raw_html, 'html.parser')
    with open(csv_file, 'w', newline='') as output_file:
        writer = csv.writer(output_file, delimiter ='\t', quotechar='"')
        for p in soup.find_all("p"):
            if not p.has_attr('id'):
                continue
            description = '<p>' + get_content(clean(p)) + '</p>'
            feat_ref = p['id']
            feat_name = p.text.split(':')[0].strip()
            tag = p
            while (True):
                tag = tag.next_sibling
                if tag == None:
                    break
                if tag.name == 'p':
                    if tag.has_attr("id"):
                        break
                    else:
                        description += get_content(clean(tag))

            writer.writerow([feat_ref, feat_name, description])


if __name__ == '__main__':
    main()