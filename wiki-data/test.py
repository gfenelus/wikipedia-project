from lxml import etree
import json
import re

#xmlB is the unzipped wikidump xml
#the other files are for testing with smaller sets of wikipedia data
xmlB = "wiki-pages\\bigData.xml"
xmlM = 'deities.xml'
xmlS = "wikiSmall.xml"
xmlH = "hindu-deities2.xml"
count = 0
pageCount = 0
deityList=[]
file_name = "C:\wikipedia-project\wiki-data\deity-profiles\deities.json"
sub_list = []
curly_bracket_pattern = re.compile(r"{{(.)*}}")

ref_pattern = re.compile(r"<ref>(.)*</ref>")
strict_ref_pattern = re.compile(r"<ref(\s*\w*\s*\=\s*\\*\"*\w*\\*\"*\s*\/*)>\s?(\w*\s?|,|\(|\))*")
br_pattern = re.compile(r"<br\s*\/*>")
double_bracket_quotes_pattern = re.compile(r"(\[\[|\]\]|''|''')")
double_bracket_pattern = re.compile(r"(\[\[|\]\]|'*)")
wiki_list_pattern = re.compile(r"{*efn\||{*unbulleted list\||{*ubl\||\((\w*\s?)*\)|}}")
mythology_pattern = re.compile(r"\(mythology\)w*")
citation_pattern = re.compile(r"{*cite\s?book\s?\|(.*)")
c_list_pattern = re.compile(r"{{Collapsible list|{{plainlist\|*")
title_pattern = re.compile(r"\|\s*(title|caption)\s*=")
abodes_pattern = re.compile(r"\|\s*(abode|abodes)\s*=")
siblings_pattern = re.compile(r"Other siblings|Half-siblings")


#create empty json list
with open(file_name, 'w') as initFile:
    json.dump(deityList, initFile)

# function to add to JSON
def write_json(my_json):
    with open(file_name,'r+') as file:
        file_data = json.load(file)
        file_data.append(my_json)
        file.seek(0)
        json.dump(file_data, file, indent=0)

#iterate through elements of each page 
for event, element in etree.iterparse(xmlB, tag="{http://www.mediawiki.org/xml/export-0.10/}text"):
    pageCount += 1
    #prints a notification for every 100,000th page
    if pageCount%100000 == 0:
        print("pages parsed: ", pageCount)

    try:
        #match a wiki page for a deity
        getInfo = element.text[element.text.find("{{Infobox deity"): 2000]
        deitySearchInfo = re.search('\|\s*type\s*=\s*(Greek|Roman|Hindu)', getInfo).string
        
        #check if regex made a match
        if len(deitySearchInfo) > 0:
            splitInfo = deitySearchInfo.split("\n")
            count += 1
            print("deities found: ", count)

            #parse wiki text in to readable format
            for each in splitInfo:
                if "| type" in each:
                    type = re.sub(r"\|\s*(type)\s*=", "", each) 

                if "| name" in each:
                    name = re.sub(r"\|\s*(name)\s*=", "", each)
                    name = re.sub("'", "", name)
                    name = re.sub(ref_pattern, "", name)
                    name = re.sub(curly_bracket_pattern, "", name)
                    name = re.sub(br_pattern, "", name)

                if "god_of "in each:
                    god = re.sub(r"\|\s*(god_of|goddess_of)\s*=\s*", "", each)
                    god = re.sub("'", "", god)
                    god = re.sub(ref_pattern, "", god)
                    god = re.sub(curly_bracket_pattern, "", god)
                    god = re.sub(double_bracket_quotes_pattern, "", god)
                    god = re.sub(br_pattern, "", god)

                if "deity_of " in each:
                    god = re.sub(r"\|\s*(deity_of)\s*=\s*","", each)
                    god = re.sub("'", "", god)
                    god = re.sub(ref_pattern, "", god)
                    god = re.sub(curly_bracket_pattern, "", god)
                    god = re.sub(double_bracket_quotes_pattern, "", god)
                    god = re.sub(br_pattern, "", god)

                if "abode" in each:
                    abode = each.replace("[[", "").replace("]]", "").replace("\n","")
                    abode = re.sub(abodes_pattern, "",abode)
                    abode = re.sub("'''", "", abode)
                    abode = re.sub(r"^\*", "", abode)
                    abode = re.sub(r"{{(\w*\||\w*)*", "", abode)
                    abode = re.sub(r"\(\)", "", abode)
                    abode = re.sub(ref_pattern, "", abode)
                    abode = re.sub(curly_bracket_pattern, "", abode)
                    abode = re.sub(br_pattern, "", abode)

                if "symbol" in each:
                    symbol = re.sub(r"\|\s*(symbol(s?)\s*=)\s*", "",each)
                    symbol = re.sub(ref_pattern, "", symbol)
                    symbol = re.sub(curly_bracket_pattern, "", symbol)
                    symbol = re.sub(double_bracket_pattern, "", symbol)
                    symbol = re.sub(br_pattern, "", symbol)

                if "parents" in each:
                    parent = re.sub(r"\|\s*(parent(s?)\s*=)\s*", "", each)
                    parent = re.sub(ref_pattern, "", parent)
                    parent = re.sub(curly_bracket_pattern, "", parent)
                    parent = re.sub(double_bracket_quotes_pattern, "", parent)
                    parent = re.sub(mythology_pattern, "", parent)
                    parent = re.sub(br_pattern, ",", parent)
                    parent = re.sub(strict_ref_pattern, "", parent)
                    parent = re.sub(wiki_list_pattern,"", parent)
                    parent = re.sub(c_list_pattern,"", parent)

                if "siblings" in each:
                    sibling = each.replace("\n","")
                    sibling = re.sub(r"\|\s*(siblings\s*=)\s*", "", sibling)
                    sibling = re.sub(r"(\\\w*)","", sibling)
                    sibling = re.sub(title_pattern,"", sibling)
                    sibling = re.sub(double_bracket_quotes_pattern, "", sibling)
                    sibling = re.sub(ref_pattern, "", sibling)
                    sibling = re.sub(curly_bracket_pattern, "", sibling)
                    sibling = re.sub(wiki_list_pattern,"", sibling)
                    sibling = re.sub(mythology_pattern, "", sibling)
                    sibling = re.sub(br_pattern, ",", sibling)
                    sibling = re.sub(c_list_pattern, "", sibling)
                    sibling = re.sub(siblings_pattern, "", sibling)
                    
                
                if "children" in each:
                    children = re.sub(r"\|\s*(children\s*=)\s*", "", each)
                    children = re.sub(double_bracket_quotes_pattern, "", children)
                    children = re.sub(strict_ref_pattern, "", children)
                    children = re.sub(curly_bracket_pattern, "", children)
                    children = re.sub(mythology_pattern, "", children)
                    children = re.sub(br_pattern, ",", children)
                    children = re.sub(wiki_list_pattern,"", children)
                    children = re.sub(citation_pattern,"", children)
                    children = re.sub(title_pattern,"", children)
                    children = re.sub(c_list_pattern,"", children)
           
            #CREATE deity profile in JSON
            my_json = {
                "type": type.strip(),
                "name": name.strip(),
                "god": god.strip(),
                "abode": abode.strip(),
                "symbol": symbol.strip(),
                "parent": parent.strip(),
                "sibling": sibling.strip(),
                "children": children.strip()
            }
            write_json(my_json)            
            element.clear()           
    #catches error when an infobox for a deity isn't found    
    except Exception as e:
        # print(e)
        pass        
    element.clear()
    

  