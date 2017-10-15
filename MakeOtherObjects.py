import zipfile
import shutil
import csv
from lxml import etree
import html
import re

input_file = "cleandata/Magic Items - Others.csv"
output_file = "data/Magic Items - Others.xml"

def ref_name(name):
    return re.sub('[^0-9a-zA-Z]+', '-', name.strip()).lower()

def main():
    xml_root = etree.Element('equipment', static="true")
    with open(input_file, 'r') as finput, open(output_file, 'w', encoding="iso-8859-1") as foutput:
        csvreader = csv.reader(finput, delimiter="\t", quotechar='"')
        for row in csvreader:
            [name, cost, slot, cl, weight, aura, description, craft] = row
            ref = ref_name(name)
            xml_ref = etree.SubElement(xml_root, ref)
            xml_ref_aura = etree.SubElement(xml_ref, "aura", type="string")
            xml_ref_cl = etree.SubElement(xml_ref, "cl", type="number")
            xml_ref_cost = etree.SubElement(xml_ref, "cost", type="string")
            xml_ref_description = etree.SubElement(xml_ref, "description", type="formattedtext")
            xml_ref_name = etree.SubElement(xml_ref, "name", type="string")
            xml_ref_prerequisites = etree.SubElement(xml_ref, "prerequisites", type="string")
            xml_ref_subtype = etree.SubElement(xml_ref, "subtype", type="string")
            xml_ref_type = etree.SubElement(xml_ref, "type", type="string")
            xml_ref_weight = etree.SubElement(xml_ref, "weight", type="number")
            xml_ref_aura.text = aura
            xml_ref_cl.text = cl
            xml_ref_cost.text = cost
            xml_ref_description.text = description
            xml_ref_name.text = name
            xml_ref_prerequisites.text = craft
            xml_ref_subtype.text = "" if slot == "none" else slot
            xml_ref_type.text = "Mythic Item"
            xml_ref_weight.text = weight
        xmldoc = html.unescape(etree.tostring(xml_root,pretty_print=True,encoding="iso-8859-1",xml_declaration=True).decode("iso-8859-1"))
        foutput.write(xmldoc)


if __name__ == '__main__':
    main()
