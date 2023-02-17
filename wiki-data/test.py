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
deityList=[]
file_name = "deities.json"
#iterate through elements of each page 
for event, element in etree.iterparse(xmlM, tag="{http://www.mediawiki.org/xml/export-0.10/}text"):
    
    print("--------------------------------------------------------")
    try:
        #match a wiki page for a deity
        getInfo = element.text[element.text.find("{{Infobox deity"): 2000]
        deitySearchInfo = re.search('\|\s*type\s*=\s*(Greek|Roman|Hindu)', getInfo).string
        
        #check if regex made a match
        if len(deitySearchInfo) > 0:
            splitInfo = deitySearchInfo.split("\n")
            count += 1
            
            #parse wiki text in to readable format
            for each in splitInfo:
                
                if "| name" in each:
                    name = re.sub(r"\|\s*(name)\s*=", "", each)
                    name = re.sub(r"<ref>(.)*</ref>", "", name)
                    name = re.sub(r"{{(.)*}}>", "", name)
                    name = re.sub("'", "", name)
                    name = re.sub(r"<br\s*\/*>", "", name)
                    # print("Name: ",name)

                if "god_of "in each:
                    god = re.sub(r"\|\s*(god_of|goddess_of)\s*=\s*", "", each)
                    god = re.sub(r"<ref>(.)*</ref>", "", god)
                    god = re.sub(r"{{(.)*}}>", "", god)
                    god = re.sub(r"(\[\[|\]\]|''|''')", "", god)
                    god = re.sub("'", "", god)
                    god = re.sub(r"<br\s*\/*>", "", god)
                    # print("God: ", god)

                if "deity_of " in each:
                    god = re.sub(r"\|\s*(deity_of)\s*=\s*","", each)
                    god = re.sub(r"<ref>(.)*</ref>", "", god)
                    god = re.sub(r"{{(.)*}}", "", god)
                    god = re.sub(r"(\[\[|\]\]|''|''')", "", god)
                    god = re.sub("'", "", god)
                    god = re.sub(r"<br\s*\/*>", "", god)
                    # print("Deity: ", god)

                if "abode" in each:
                    abode = each.replace("[[", "").replace("]]", "").replace("\n","")
                    abode = re.sub(r"\|\s*(abode\s*=)\s*", "",abode)
                    abode = re.sub(r"<ref>(.)*</ref>", "", abode)
                    abode = re.sub(r"^\*", "", abode)
                    abode = re.sub(r"{{(.)*}}", "", abode)
                    abode = re.sub(r"{{(\w*\||\w*)*", "", abode)
                    abode = re.sub("'''", "", abode)
                    abode = re.sub(r"\(\)", "", abode)
                    abode = re.sub(r"<br\s*\/*>", "", abode)
                    # print("Abode: ", abode)

                if "symbol" in each:
                    symbol = re.sub(r"\|\s*(symbol(s?)\s*=)\s*", "",each)
                    symbol = re.sub(r"<ref>(.)*</ref>", "", symbol)
                    symbol = re.sub(r"{{(.)*}}", "", symbol)
                    symbol = re.sub(r"(\[\[|\]\]|'*)", "", symbol)
                    symbol = re.sub(r"<br\s*\/*>", "", symbol)
                    # print("Symbol: ", symbol)

                if "parents" in each:
                    parent = re.sub(r"\|\s*(parent(s?)\s*=)\s*", "", each)
                    parent = re.sub(r"<ref>(.)*</ref>", "", parent)
                    parent = re.sub(r"{{(.)*}}>", "", parent)
                    parent = re.sub(r"(\[\[|\]\]|'')", "", parent)
                    parent = re.sub(r"\(mythology\)w*", "", parent)
                    parent = re.sub(r"<br\s*\/*>", ",", parent)
                    parent = re.sub(r"<ref(\s*\w*\s*\=\s*\\*\"*\w*\\*\"*\s*\/*)>\s?(\w*\s?|,|\(|\))*", "", parent)
                    parent = re.sub(r"{*efn\||{*unbulleted list\||{*ubl\||\((\w*\s?)*\)|}}","", parent)
                    # print("Parent: ", parent)

                if "siblings" in each:
                    sibling = each.replace("\n","")
                    sibling = re.sub(r"\|\s*(siblings\s*=)\s*", "", sibling)
                    sibling = re.sub(r"(\[\[|\]\]|''|''')", "", sibling)
                    sibling = re.sub(r"<ref>(.)*</ref>", "", sibling)
                    sibling = re.sub(r"{{(.)*}}>", "", sibling)
                    sibling = re.sub(r"{*efn\||{*unbulleted list\||{*ubl\||\((\w*\s?)*\)|}}","", sibling)
                    sibling = re.sub(r"\|(w*|,|\s|\(|\)|\|)","", sibling )
                    sibling = re.sub(r"\(mythology\)w*", "", sibling)
                    sibling = re.sub(r"<br\s*\/*>", ",", sibling)
                    sibling = re.sub(r"{{Collapsible list", "", sibling)
                    sibling = re.sub(r"(\\\w*)","", sibling)
                    
                    # print("Siblings: ", sibling)
                
                if "children" in each:
                    children = re.sub(r"\|\s*(children\s*=)\s*", "", each)
                    children = re.sub(r"(\[\[|\]\]|''|''')", "", children)
                    # children = re.sub(r"<ref>(.)*</ref>", "", children)
                    children = re.sub(r"<ref(\s*\w*\s*\=\s*\\*\"*\w*\\*\"*\s*\/*)>\s?(\w*\s?|,|\(|\))*", "", children)
                    children = re.sub(r"{{(.)*}}>", "", children)
                    children = re.sub(r"\(mythology\)w*", "", children)
                    children = re.sub(r"<br\s*\/*>", ",", children)
                    children = re.sub(r"{*efn\||{*unbulleted list\||{*ubl\||\((\w*\s?)*\)|}}","", children)
                    children = re.sub(r"{*cite\s?book\s?\|(.*)","", children)
                    # print("Children: ", children)
            
            #CREATE deity profile in JSON
            my_json = {
                "name": name.strip(),
                "god": god.strip(),
                "abode": abode.strip(),
                "symbol": symbol.strip(),
                "parent": parent.strip(),
                "sibling": sibling.strip(),
                "children": children.strip()
            }
            # print(json.dumps(my_json, indent=4))
            
            #UPDATE deity to list of deities
            deityList.append(my_json)
            # print("list: ", deityList)
            #Create json file   
            
            # file = open("deity-profiles\\" + file_name, 'a')
            # json.dump(my_json, file, indent=2)
            # file.write(",")
            # file.close()

            # print(count, "Files Done")
            element.clear()
            #MAKE SURE BEGINNING AND END OF FILE HAS BRACKETS ex. "[{"key": "value1"}, {"key": "vale2"}]" AND REMOVE THE TRAILING COMMA BEFORE IMPORTING
            

    #catches error when an infobox for a deity isn't found    
    except Exception as e:
        print(e)
        # print("deity not found")
         
    element.clear()
    # file_name = "deities.json"
file = open("deity-profiles\\" + file_name, 'a')
json.dump(deityList, file, indent=1)
file.close()
# print(count, "Files Done")
  