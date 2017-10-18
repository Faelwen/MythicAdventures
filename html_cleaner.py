from bs4 import BeautifulSoup
import os

input_dir = "mythicitems"
output_dir = "cleanhtml"



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
        print(th)
        if th.string != None:
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
    for file in os.listdir(input_dir):
        #replace caracters not supported in ASCII
        with open("{0}/{1}".format(input_dir, file), 'r') as html_file:
        	raw_html = html_file.read().replace('&minus;', '-').replace('&mdash', '--').replace('&ndash;','-').replace('&times;', 'x').replace('—', '-')
        soup = BeautifulSoup(raw_html, 'html.parser')
        clean_soup = clean(soup)

        with open("{0}/{1}".format(output_dir, file), 'w') as clean_html_file:
            clean_html_file.write(str(clean_soup))


if __name__ == '__main__':
    main()




