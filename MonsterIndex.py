from lxml import etree
import html

monster_ref_file = "data/monsterref.txt"
output_file = "modulehtml/6-2 monster index.xml"

xml_root = etree.Element('MythicMonsterIndex')
xml_def_name = etree.SubElement(xml_root, "name", type="string")
xml_def_name.text = "Mythic Monster Index"
xml_def_index = etree.SubElement(xml_root, "index")

with open(monster_ref_file, 'r') as inputfile:
    for line in inputfile:
        [name, ref] = line.strip().split('\t')
        xml_ref = etree.SubElement(xml_def_index, ref)
        xml_name = etree.SubElement(xml_ref, "name", type="string")
        xml_name.text = name
        xml_list = etree.SubElement(xml_ref, "listlink", type="windowreference")
        xml_class =  etree.SubElement(xml_list, "class")
        xml_class.text = "npc"
        xml_recordname =  etree.SubElement(xml_list, "recordname")
        xml_recordname.text = "reference.npcdata.{0}".format(ref)

with open(output_file, 'w') as outputfile:
    xmldoc = html.unescape(etree.tostring(xml_root,pretty_print=True,encoding="iso-8859-1",xml_declaration=False).decode("iso-8859-1"))
    outputfile.write(xmldoc)

