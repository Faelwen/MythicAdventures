from bs4 import BeautifulSoup
import re
import csv

html_files = ["html/mythic_heroes.html", "html/archmage.html"]
csv_files = ["data/mythic_abilities.csv", "data/archmage.csv"]

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


def clean_b(soup):
    soup.find('b').unwrap()
    return soup


def clean_p(soup):
    soup.unwrap()
    return soup


def extract_mythic_abilities(html_file, csv_file):
    print(html_file)
    print(csv_file)
    with open(html_file, 'r') as input_file:
        raw_html = input_file.read().replace('&minus;', '-').replace('&mdash', '--').replace('&ndash;','-').replace('&times;', 'x').replace('—', '-')
    soup = BeautifulSoup(raw_html, 'html.parser')

    with open(csv_file, 'w', newline='') as output_file:
        writer = csv.writer(output_file, delimiter ='\t', quotechar='"')
        for p in soup.find_all("p"):
            if p.has_attr('id'):
                print(p)
                p = clean(p)
                if p.b == None:
                    p.i.unwrap()
                else:
                    p.b.unwrap()
                ability = ""
                for tag in p.contents:
                    ability += str(tag)
                [name, description] = ability.split(':', 1)
                description = '<p>' + description.strip() + '</p>'
                ref = re.sub('[^0-9a-zA-Z]+', '-', name)[:-1]
                writer.writerow([ref, name, description])


def main():
    for html_file, csv_file in zip(html_files, csv_files):
        extract_mythic_abilities(html_file, csv_file)


if __name__ == '__main__':
    main()
