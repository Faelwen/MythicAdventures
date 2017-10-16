import html_cleaner
from bs4 import BeautifulSoup

import zipfile
import shutil
import csv
from lxml import etree
import html

module_file_name = "PFRPG-MythicAdventures.mod"
xml_definition_file = "definition.xml"
xml_database_file = "db.xml"
license_file = "cleanhtml/license.html"

file0_0 = "modulehtml/0-0 glossary.html"
file1_1 = "modulehtml/1-1 mythic_heroes.html"
file1_2 = "modulehtml/1-2 Creating a Mythic Character.html"
file1_3 = "modulehtml/1-3 Mythic Paths.html"
file1_3_1 = "modulehtml/1-3-1 archmage.html"
file1_3_2 = "modulehtml/1-3-2 champion.html"
file1_3_3 = "modulehtml/1-3-3 guardian.html"
file1_3_4 = "modulehtml/1-3-4 hierophant.html"
file1_3_5 = "modulehtml/1-3-5 marshal.html"
file1_3_6 = "modulehtml/1-3-6 trickster.html"
file1_4 = "modulehtml/1-4 Base Mythic Abilities.html"
file1_5 = "modulehtml/1-5 Gaining Tiers.html"
file1_6 = "modulehtml/1-6 Universal Path Abilities.html"

ability_mythic_heroes = "cleandata/mythic_heroes.csv"
ability_mythic_archmage = "cleandata/archmage.csv"
ability_mythic_champion = "cleandata/champion.csv"
ability_mythic_guardian = "cleandata/guardian.csv"
ability_mythic_hierophant = "cleandata/hierophant.csv"
ability_mythic_marshal = "cleandata/marshal.csv"
ability_mythic_trickster = "cleandata/trickster.csv"
ability_mythic_universal = "cleandata/universal_abilities.csv"

monster_data = "cleandata/mythic_monsters.xml"

FG_module_directory = "E:\\Fantasy Grounds\\DataDir\\modules"

module_name = "Mythic Adventures"
module_author = "Faelwen"
module_ruleset = "PFRPG"
library_tag_name = "MythicAdventures"
library_name = "Mythic Adventures"
library_category = "PFRPG Extras"

library_entries =   [{"Entry name":"---Legal Notice---",
                    "Entry tag":"AA.License",
                    "Link type":"librarylink",
                    "Window class":"referencetext",
                    "Record name": "License@" + module_name},
                    {"Entry name":"Glossary",
                    "Entry tag":"BA.Glossary",
                    "Link type":"librarylink",
                    "Window class":"referencetext",
                    "Record name": "lists.Glossary@" + module_name},
                    {"Entry name":"Mythic Heroes",
                    "Entry tag":"CA.MythicHeroes",
                    "Link type":"librarylink",
                    "Window class":"referencetext",
                    "Record name": "lists.MythicHeroes@" + module_name},
                    ]


def generate_xml_def_file():
    xml_def_root = etree.Element('root')
    xml_def_name = etree.SubElement(xml_def_root, "name")
    xml_def_name.text = module_name
    xml_def_author = etree.SubElement(xml_def_root, "author")
    xml_def_author.text = module_author
    xml_def_ruleset = etree.SubElement(xml_def_root, "ruleset")
    xml_def_ruleset.text = module_ruleset
    with open(xml_definition_file, 'w') as file:
        file.write(etree.tostring(xml_def_root,pretty_print=True,encoding="iso-8859-1",xml_declaration=True).decode("iso-8859-1"))


def generate_xml_db_file(xml_root):
    with open(xml_database_file, 'w', encoding="iso-8859-1") as file:
        xmldoc = html.unescape(etree.tostring(xml_root,pretty_print=True,encoding="iso-8859-1",xml_declaration=True).decode("iso-8859-1"))
        file.write(xmldoc)


def generate_module():
    with zipfile.ZipFile(module_file_name, 'w', zipfile.ZIP_DEFLATED) as file:
        file.write('db.xml')
        file.write('definition.xml')
        file.write('thumbnail.png')
    print("Module generated")


def copy_to_Fantasy_Grounds():
    shutil.copy(module_file_name, FG_module_directory)
    print("Module copied to Fantasy Grounds")


def populate_library_entries(xml_library_entries):
    for entry in library_entries:
        xml_library_entry =  etree.SubElement(xml_library_entries, entry["Entry tag"])
        xml_library_entry_linktype = etree.SubElement(xml_library_entry, entry["Link type"], type="windowreference")
        xml_library_entry_linktype_class = etree.SubElement(xml_library_entry_linktype, "class")
        xml_library_entry_linktype_class.text = entry["Window class"]
        xml_library_entry_linktype_recordname = etree.SubElement(xml_library_entry_linktype, "recordname")
        xml_library_entry_linktype_recordname.text = entry["Record name"]
        xml_library_entry_name = etree.SubElement(xml_library_entry, "name", type="string")
        xml_library_entry_name.text = entry["Entry name"]


def populate_license(xml_root):
    xml_license = etree.SubElement(xml_root, "License", static="true")
    xml_license_link = etree.SubElement(xml_license,"librarylink", type="windowreference")
    xml_license_link_class = etree.SubElement(xml_license_link, "class")
    xml_license_link_class.text = "referencetext"
    xml_license_link_recordname = etree.SubElement(xml_license_link, "recordname")
    xml_license_link_recordname.text = ".."
    xml_license_name = etree.SubElement(xml_license,"name", type="string")
    xml_license_name.text = "License"
    xml_license_text = etree.SubElement(xml_license,"text", type="formattedtext")
    with open(license_file, 'r') as file:
        license_text = file.read()
    xml_license_text.text = license_text


def populate_mythic_abilities(file, node, ability_type):
    node_abilities = etree.SubElement(node, "Abilities")
    with open(file, 'r') as inputfile:
        csvreader = csv.reader(inputfile, delimiter='\t', quotechar="'")
        for row in csvreader:
            [ref, name, description] = row
            soup = BeautifulSoup(description, 'html.parser')
            clean_description = ""
            for tag in soup:
                clean_description += str(html_cleaner.clean(soup))
            node_abilities_ref = etree.SubElement(node_abilities, ref)
            node_abilities_ref_name = etree.SubElement(node_abilities_ref, "name", type="string")
            node_abilities_ref_name.text = name
            node_abilities_ref_type = etree.SubElement(node_abilities_ref, "type", type="string")
            node_abilities_ref_type.text = ability_type
            node_abilities_ref_text = etree.SubElement(node_abilities_ref, "text", type="formattedtext")
            node_abilities_ref_text.text = clean_description
            node_abilities_ref_benefit = etree.SubElement(node_abilities_ref, "benefit", type="formattedtext")
            node_abilities_ref_benefit.text = clean_description


def populate_library_page(htmlfile, node, tagname, name):
    node_ref =  etree.SubElement(node, tagname)
    node_ref_name = etree.SubElement(node_ref, "name", type="string")
    node_ref_text = etree.SubElement(node_ref, "text", type="formattedtext")
    node_ref_name.text = name
    with open(htmlfile, 'r') as inputfile:
        node_ref_text.text = inputfile.read()
    return node_ref


def populate_mythic_heroes(xml_lists):
    xml_mythic_heroes = populate_library_page(file1_1, xml_lists, "MythicHeroes", "Mythic Heroes")
    xml_creating_character = populate_library_page(file1_2, xml_mythic_heroes, "CreatingAMythicCharacter", "Creating a Mythic Character")
    xml_mythic_paths = populate_library_page(file1_3, xml_mythic_heroes, "MythicPaths", "Mythic Paths")
    xml_mythic_paths_archmage = populate_library_page(file1_3_1, xml_mythic_paths, "Archmage", "Archmage")
    xml_mythic_paths_champion = populate_library_page(file1_3_2, xml_mythic_paths, "Champion", "Champion")
    xml_mythic_paths_guardian = populate_library_page(file1_3_3, xml_mythic_paths, "Guardian", "Guardian")
    xml_mythic_paths_hierophant = populate_library_page(file1_3_4, xml_mythic_paths, "Hierophant", "Hierophant")
    xml_mythic_paths_marshal = populate_library_page(file1_3_5, xml_mythic_paths, "Marshal", "Marshal")
    xml_mythic_paths_trickster = populate_library_page(file1_3_6, xml_mythic_paths, "Trickster", "Trickster")
    xml_mythic_abilities = populate_library_page(file1_4, xml_mythic_heroes, "BaseMythicAbilities", "Base Mythic Abilities")
    xml_mythic_tiers = populate_library_page(file1_5, xml_mythic_heroes, "GainingTiers", "Gaining Tiers")
    xml_mythic_univ = populate_library_page(file1_6, xml_mythic_heroes, "UniversalPathAbilities", "Universal Path Abilities")

    populate_mythic_abilities(ability_mythic_heroes, xml_mythic_abilities, "Base Mythic Ability")
    populate_mythic_abilities(ability_mythic_archmage, xml_mythic_paths_archmage, "Archmage Ability")
    populate_mythic_abilities(ability_mythic_champion, xml_mythic_paths_champion, "Champion Ability")
    populate_mythic_abilities(ability_mythic_guardian, xml_mythic_paths_guardian, "Guardian Ability")
    populate_mythic_abilities(ability_mythic_hierophant, xml_mythic_paths_hierophant, "Hireophant Ability")
    populate_mythic_abilities(ability_mythic_marshal, xml_mythic_paths_marshal, "Marshal Ability")
    populate_mythic_abilities(ability_mythic_trickster, xml_mythic_paths_trickster, "Trikster Ability")
    populate_mythic_abilities(ability_mythic_universal, xml_mythic_univ, "Mythic Universal Path Ability")


def populate_feats():
    pass


def populate_spells():
    pass


def populate_running():
    pass


def populate_items():
    pass


def populate_monsters(xml_reference):
    xml_npc = etree.SubElement(xml_reference, "npcdata", static="true")
    with open(monster_data, 'r') as inputfile:
        xml_npc.text = inputfile.read()


def generate_xml_structure(xml_root):
    xml_libraries = etree.SubElement(xml_root, "library", static="true")
    xml_library = etree.SubElement(xml_libraries, library_tag_name)
    xml_library_name = etree.SubElement(xml_library, "name", type="string")
    xml_library_name.text = library_name
    xml_library_categoryname = etree.SubElement(xml_library, "categoryname", type="string")
    xml_library_categoryname.text = library_category
    xml_library_entries = etree.SubElement(xml_library, "entries")
    xml_reference = etree.SubElement(xml_root, "reference", static="true")
    xml_ref_armor = etree.SubElement(xml_reference,"armor")
    xml_ref_equipment = etree.SubElement(xml_reference,"equipment")
    xml_ref_feats = etree.SubElement(xml_reference,"feats")
    xml_ref_npcdata = etree.SubElement(xml_reference,"npcdata")
    xml_ref_skills = etree.SubElement(xml_reference,"skills")
    xml_ref_spells = etree.SubElement(xml_reference,"spells")
    xml_ref_weapon = etree.SubElement(xml_reference,"weapon")
    xml_lists = etree.SubElement(xml_root, "lists", static="true")

    populate_library_entries(xml_library_entries)
    populate_license(xml_root) # Legal notice
    populate_library_page(file0_0, xml_lists, "Glossary", "Glossary") # Glossary
    populate_mythic_heroes(xml_lists) #Chapter 1
    populate_feats() #Chapter 2
    populate_spells() #Chapter 3
    populate_running() #Chapter 4
    populate_items() #Chapter 5
    populate_monsters(xml_reference) #Chapter 6



def main():
    xml_root = etree.Element('root', version="2.0")
    generate_xml_structure(xml_root)
    generate_xml_db_file(xml_root)
    generate_xml_def_file()
    generate_module()
    copy_to_Fantasy_Grounds()


if __name__ == '__main__':
    main()