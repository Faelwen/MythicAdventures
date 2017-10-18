import html_cleaner
from bs4 import BeautifulSoup
import re
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
file2_1 = "modulehtml/2-1 mythic-feats.html"
file2_2 = "modulehtml/2-2 types of feats.html"
file2_3 = "modulehtml/2-3 Feat Descriptions.html"
file2_4 = "modulehtml/2-4 List of Feats.html"
file3_0 = "modulehtml/3-0 intro.xml"
file3_1 = "modulehtml/3-1 mythic_spells.html"
file3_2 = "modulehtml/3-2 mythic_spell_list.html"
file3_3 = "modulehtml/3-3 spell_index.html"
file4_0 = "modulehtml/4-0 index.xml"
file4_1 = "modulehtml/4-1 intro.html"
file4_2 = "modulehtml/4-2 story structure.html"
file4_3 = "modulehtml/4-3 mythic themes.html"
file4_4 = "modulehtml/4-4 designing encounters.html"
file4_5 = "modulehtml/4-5 mythic trials.html"
file4_6 = "modulehtml/4-6 mythic boons.html"
file4_7 = "modulehtml/4-7 recurring mythic villains.html"
file4_8 = "modulehtml/4-8 mythic flaws.html"
file4_9 = "modulehtml/4-9 ideas.html"
file6_0 = "modulehtml/6-0 index.xml"
file6_1 = "modulehtml/6-1 mythic monsters.html"
file6_2 = "modulehtml/6-2 monster index.xml"
file6_3 = "modulehtml/6-3 monster origins.html"
file6_4 = "modulehtml/6-4 monster ranks.html"
file6_5 = "modulehtml/6-5 reading.html"
file6_6 = "modulehtml/6-6 monster advancement.html"

ability_mythic_heroes = "cleandata/mythic_heroes.csv"
ability_mythic_archmage = "cleandata/archmage.csv"
ability_mythic_champion = "cleandata/champion.csv"
ability_mythic_guardian = "cleandata/guardian.csv"
ability_mythic_hierophant = "cleandata/hierophant.csv"
ability_mythic_marshal = "cleandata/marshal.csv"
ability_mythic_trickster = "cleandata/trickster.csv"
ability_mythic_universal = "cleandata/universal_abilities.csv"
feats_data = "cleandata/mythic_feats.csv"
spell_data = "cleandata/all_spells.csv"
monster_data = "cleandata/mythic_monsters.xml"
weapon_data = "cleandata/mythic weapon.xml"
armor_data = "cleandata/mythic_armor.xml"
artifact_weapon_data = "cleandata/artifacts_weapon.xml"
artifact_armor_data = "cleandata/artifacts_armor.xml"
magic_items_data = "cleandata/Magic Items - Others.xml"

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
                    "Window class":"referencetextwide",
                    "Record name": "License@" + module_name},
                    {"Entry name":"Glossary",
                    "Entry tag":"BA.Glossary",
                    "Link type":"librarylink",
                    "Window class":"referencetextwide",
                    "Record name": "lists.Glossary@" + module_name},
                    {"Entry name":"Mythic Heroes",
                    "Entry tag":"CA.MythicHeroes",
                    "Link type":"librarylink",
                    "Window class":"referencetextwide",
                    "Record name": "lists.MythicHeroes@" + module_name},
                    {"Entry name":"Mythic Feats",
                    "Entry tag":"DA.MythicFeats",
                    "Link type":"librarylink",
                    "Window class":"referencetextwide",
                    "Record name": "lists.MythicFeats@" + module_name},
                    {"Entry name":"Mythic Spells",
                    "Entry tag":"EA.MythicSpells",
                    "Link type":"librarylink",
                    "Window class":"referenceindex",
                    "Record name": "lists.MythicSpells.intro@" + module_name},
                    {"Entry name":"Running a Mythic Game",
                    "Entry tag":"EA.RunningAMythicGame",
                    "Link type":"librarylink",
                    "Window class":"referenceindex",
                    "Record name": "lists.RunningAMythicGame.intro@" + module_name},
                    {"Entry name":"Mythic Magic Items",
                    "Entry tag":"FA.MythicMagicItems",
                    "Link type":"librarylink",
                    "Window class":"referencetext",
                    "Record name": "lists.MythicMagicItems@" + module_name},
                    {"Entry name":"Mythic Monsters",
                    "Entry tag":"GA.MythicMonsters",
                    "Link type":"librarylink",
                    "Window class":"referenceindex",
                    "Record name": "lists.MythicMonsters.intro@" + module_name},
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


def populate_mythic_heroes(library_node):
    xml_mythic_heroes = populate_library_page(file1_1, library_node, "MythicHeroes", "Mythic Heroes")
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


def populate_feats(feat_node, library_node):
    xml_mythic_feats = populate_library_page(file2_1, library_node, "MythicFeats", "Mythic Feats")
    xml_mythic_feats_types = populate_library_page(file2_2, xml_mythic_feats, "TypesOfFeats", "Types of Feats")
    xml_mythic_feats_description = populate_library_page(file2_3, xml_mythic_feats, "FeatDescription", "Feat Description")

    xml_mythic_feats_list = etree.SubElement(xml_mythic_feats, "ListOfFeats")
    xml_mythic_feats_list_name = etree.SubElement(xml_mythic_feats_list, "name", type="string")
    xml_mythic_feats_list_name.text = "List of Feats"
    xml_mythic_feats_list_index = etree.SubElement(xml_mythic_feats_list, "index")

    with open(feats_data, 'r') as inputfile:
        csvreader = csv.reader(inputfile, delimiter='\t', quotechar="'")
        for row in csvreader:
            [ref, name, description, prereq, benefit, special] = row
            parsename = re.search('(.*)\((.*)\)', name)
            name2 = parsename.group(1) if parsename != None else "Mythic"
            feattype = parsename.group(2) if parsename != None else "Mythic"
            xml_ref = etree.SubElement(feat_node, ref)
            xml_ref_name = etree.SubElement(xml_ref, "name", type="string")
            xml_ref_type = etree.SubElement(xml_ref, "type", type="string")
            xml_ref_prerequisites = etree.SubElement(xml_ref, "prerequisites", type="string")
            xml_ref_benefit = etree.SubElement(xml_ref, "benefit", type="formattedtext")
            xml_ref_source = etree.SubElement(xml_ref, "source", type="string")
            xml_ref_special = etree.SubElement(xml_ref, "special", type="formattedtext")
            xml_ref_text = etree.SubElement(xml_ref, "text", type="formattedtext")
            xml_ref_name.text = name
            xml_ref_type.text = feattype
            xml_ref_prerequisites.text = prereq.replace("<p>","").replace("</p>","")
            xml_ref_benefit.text = "<frame>" + description + "</frame>" + benefit
            xml_ref_special.text = special
            xml_ref_source.text = "Mythic Adventures"
            xml_ref_text.text = "<frame>" + description + "</frame>" + benefit

            xml_mythic_feats_list_index_ref = etree.SubElement(xml_mythic_feats_list_index, ref)
            xml_mythic_feats_list_index_ref_listlink = etree.SubElement(xml_mythic_feats_list_index_ref, "listlink", type="windowreference")
            xml_mythic_feats_list_index_ref_listlink_class = etree.SubElement(xml_mythic_feats_list_index_ref_listlink, "class")
            xml_mythic_feats_list_index_ref_listlink_recordname = etree.SubElement(xml_mythic_feats_list_index_ref_listlink, "recordname")
            xml_mythic_feats_list_index_ref_listlink_class.text = "referencefeat"
            xml_mythic_feats_list_index_ref_listlink_recordname.text = "reference.feats.{0}".format(ref)
            xml_mythic_feats_list_index_refname = etree.SubElement(xml_mythic_feats_list_index_ref, "name", type="string")
            xml_mythic_feats_list_index_refname.text = name2


def populate_spells(spell_node, library_node):
    library_node_mythicspells = etree.SubElement(library_node, "MythicSpells")
    with open(file3_0, 'r') as inputfile:
        library_node_mythicspells.text = inputfile.read()
    library_node_mythicspells_mythicspellsintro = populate_library_page(file3_1, library_node_mythicspells, "MythicSpellsIntroduction", "Mythic Spells Introduction")
    library_node_mythicspells_mythicspellslists = populate_library_page(file3_2, library_node_mythicspells, "MythicSpellsLists", "Mythic Spells Lists")
    library_node_mythicspells_mythicspellsindex = populate_library_page(file3_3, library_node_mythicspells, "MythicSpellsIndex", "Mythic Spells Index")

    with open(spell_data, 'r') as inputfile:
        csvreader = csv.reader(inputfile, delimiter='\t', quotechar="'")
        for row in csvreader:
            [ref, name, school, level, time, components, s_range, target, duration, resist, sr, description] = row
            xml_ref = etree.SubElement(spell_node, ref)
            xml_ref_name = etree.SubElement(xml_ref, "name", type="string")
            xml_ref_school = etree.SubElement(xml_ref, "school", type="string")
            xml_ref_level = etree.SubElement(xml_ref, "level", type="string")
            xml_ref_components = etree.SubElement(xml_ref, "components", type="string")
            xml_ref_castingtime = etree.SubElement(xml_ref, "castingtime", type="string")
            xml_ref_range = etree.SubElement(xml_ref, "range", type="string")
            xml_ref_effect = etree.SubElement(xml_ref, "effect", type="string")
            xml_ref_duration = etree.SubElement(xml_ref, "duration", type="string")
            xml_ref_save = etree.SubElement(xml_ref, "save", type="string")
            xml_ref_sr = etree.SubElement(xml_ref, "sr", type="string")
            xml_ref_description = etree.SubElement(xml_ref, "description", type="formattedtext")
            xml_source = etree.SubElement(xml_ref, "source", type="string")
            xml_ref_name.text = name
            xml_ref_school.text = school
            xml_ref_level.text = level
            xml_ref_components.text = components
            xml_ref_castingtime.text = time
            xml_ref_range.text = s_range
            xml_ref_effect.text = target
            xml_ref_duration.text = duration
            xml_ref_save.text = resist
            xml_ref_sr.text = sr
            xml_ref_description.text = description


def populate_running(xml_lists):
    library_node_running = etree.SubElement(xml_lists, "RunningAMythicGame")
    with open(file4_0, 'r') as inputfile:
        library_node_running.text = inputfile.read()
    populate_library_page(file4_1, library_node_running, "Introduction", "Introduction")
    populate_library_page(file4_2, library_node_running, "MythicStoryStructure", "Mythic Story Structure")
    populate_library_page(file4_3, library_node_running, "MythicThemes", "Mythic Themes")
    populate_library_page(file4_4, library_node_running, "DesigningEncounters", "Designing Encounters")
    populate_library_page(file4_5, library_node_running, "MythicTrials", "Mythic Trials")
    populate_library_page(file4_6, library_node_running, "MythicBoons", "Mythic Boons")
    populate_library_page(file4_7, library_node_running, "RecurringMythicVillains", "Recurring Mythic Villains")
    populate_library_page(file4_8, library_node_running, "MythicFlaws", "Mythic Flaws")
    populate_library_page(file4_9, library_node_running, "IdeasforMythicAdventures", "Ideas for Mythic Adventures")


def populate_items(xml_ref_weapon, xml_ref_armor, xml_ref_magicitems):
    with open(weapon_data, 'r') as inputfile:
        xml_ref_weapon.text = inputfile.read()
    with open(armor_data, 'r') as inputfile:
        xml_ref_armor.text = inputfile.read()
    with open(artifact_weapon_data, 'r') as inputfile:
        xml_ref_weapon.text += inputfile.read()
    with open(artifact_armor_data, 'r') as inputfile:
        xml_ref_armor.text += inputfile.read()
    with open(magic_items_data, 'r') as inputfile:
        xml_ref_magicitems.text = inputfile.read()


def populate_monsters(monster_node, library_node):
    xml_npc = etree.SubElement(monster_node, "npcdata", static="true")
    with open(monster_data, 'r') as inputfile:
        xml_npc.text = inputfile.read()

    library_node_list = etree.SubElement(library_node, "MythicMonsters")
    with open(file6_0, 'r') as inputfile:
        library_node_list.text = inputfile.read()
    populate_library_page(file6_1, library_node_list, "Introduction", "Introduction")

    with open(file6_2, 'r') as inputfile:
        library_node_list.text += inputfile.read()

    populate_library_page(file6_2, library_node_list, "MythicMonsterIndex", "Mythic Monster Index")
    populate_library_page(file6_3, library_node_list, "MythicMonsterOrigins", "Mythic Monster Origins")
    populate_library_page(file6_4, library_node_list, "MythicRank", "Mythic Rank")
    populate_library_page(file6_5, library_node_list, "ReadingaMythicMonsterStatBlock", "Reading a Mythic Monster Stat Block")
    populate_library_page(file6_6, library_node_list, "MythicMonsterAdvancement", "Mythic Monster Advancement")


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
    xml_ref_magicitems = etree.SubElement(xml_reference,"magicitems")
    xml_ref_feats = etree.SubElement(xml_reference,"feats")
    xml_ref_skills = etree.SubElement(xml_reference,"skills")
    xml_ref_spells = etree.SubElement(xml_reference,"spells")
    xml_ref_weapon = etree.SubElement(xml_reference,"weapon")
    xml_lists = etree.SubElement(xml_root, "lists", static="true")

    populate_library_entries(xml_library_entries)
    populate_license(xml_root) # Legal notice
    populate_library_page(file0_0, xml_lists, "Glossary", "Glossary") # Glossary
    populate_mythic_heroes(xml_lists) #Chapter 1
    populate_feats(xml_ref_feats, xml_lists) #Chapter 2
    populate_spells(xml_ref_spells, xml_lists) #Chapter 3
    populate_running(xml_lists) #Chapter 4
    populate_items(xml_ref_weapon, xml_ref_armor, xml_ref_magicitems) #Chapter 5
    populate_monsters(xml_reference, xml_lists) #Chapter 6



def main():
    xml_root = etree.Element('root', version="2.0")
    generate_xml_structure(xml_root)
    generate_xml_db_file(xml_root)
    generate_xml_def_file()
    generate_module()
    copy_to_Fantasy_Grounds()


if __name__ == '__main__':
    main()