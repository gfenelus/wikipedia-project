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
#iterate through elements of each page 
for event, element in etree.iterparse(xmlB, tag="{http://www.mediawiki.org/xml/export-0.10/}text"):
    
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
                    name = re.sub("\|\s*(name)\s*=", "", each)
                    name = re.sub("<ref>(.)*</ref>", "", name)
                    name = re.sub(r"{{(.)*}}>", "", name)
                    name = re.sub("'", "", name)
                    name = re.sub("<br/>", "", name)
                    # print("Name: ",name)

                if "god_of "in each:
                    god = re.sub("\|\s*(god_of|goddess_of)\s*=\s*", "", each)
                    god = re.sub("<ref>(.)*</ref>", "", god)
                    god = re.sub(r"{{(.)*}}>", "", god)
                    god = re.sub(r"(\[\[|\]\]|''|''')", "", god)
                    god = re.sub("'", "", god)
                    god = re.sub("<br/>", "", god)
                    # print("God: ", god)

                if "deity_of " in each:
                    god = re.sub("\|\s*(deity_of)\s*=\s*","", each)
                    god = re.sub("<ref>(.)*</ref>", "", god)
                    god = re.sub(r"{{(.)*}}", "", god)
                    god = re.sub(r"(\[\[|\]\]|''|''')", "", god)
                    god = re.sub("'", "", god)
                    god = re.sub("<br/>", "", god)
                    # print("Deity: ", god)

                if "abode" in each:
                    abode = each.replace("| abode            =", "").replace("[[", "").replace("]]", "").replace("\n","")
                    abode = re.sub("\|\s*(abode\s*=)\s*", "",abode)
                    abode = re.sub("<ref>(.)*</ref>", "", abode)
                    abode = re.sub("^\*", "", abode)
                    abode = re.sub("{{(.)*}}", "", abode)
                    abode = re.sub("{{(\w*\||\w*)*", "", abode)
                    abode = re.sub("'''", "", abode)
                    abode = re.sub("\(\)", "", abode)
                    abode = re.sub("<br/>", "", abode)
                    # print("Abode: ", abode)

                if "symbol" in each:
                    # symbol = each.replace("| symbol           =", "").replace("[[", "").replace("]]", "").replace("\n","")
                    symbol = re.sub("\|\s*(symbol(s?)\s*=)\s*", "",each)
                    symbol = re.sub("<ref>(.)*</ref>", "", symbol)
                    symbol = re.sub(r"{{(.)*}}", "", symbol)
                    symbol = re.sub(r"(\[\[|\]\]|'')", "", symbol)
                    # print("Symbol: ", symbol)

                if "parents" in each:
                    parent = each.replace("| parents          =", "").replace("[[", "").replace("]]", "").replace("\n","")
                    parent = re.sub("\|\s*(parent(s?)\s*=)\s*", "",parent)
                    parent = re.sub("<ref>(.)*</ref>", "", parent)
                    parent = re.sub(r"{{(.)*}}>", "", parent)
                    # print("Parent: ", parent)

                if "siblings" in each:
                    # sibling = each.replace("[[", "").replace("]]", "").replace("\n","").replace("{{", "").replace("|", "").replace("}}", "")
                    sibling = re.sub(r"\|\s*(siblings\s*=)\s*", "", each)
                    sibling = re.sub(r"(\[\[|\]\]|''|''')", "", sibling)
                    sibling = re.sub("<ref>(.)*</ref>", "", sibling)
                    sibling = re.sub(r"{{(.)*}}>", "", sibling)
                    # print("Siblings: ", sibling)
                
                if "children" in each:
                    # children = each.replace("| children         =", "").replace("[[", "").replace("]]", "").replace("\n", "").replace("{{", "").replace("|", "").replace("}}", "")
                    children = re.sub(r"\|\s*(children\s*=)\s*", "", each)
                    children = re.sub(r"(\[\[|\]\]|''|''')", "", children)
                    children = re.sub("<ref>(.)*</ref>", "", children)
                    children = re.sub(r"{{(.)*}}>", "", children)

                    # print("Children: ", children)

            my_json = {
                "name": name.strip(),
                "god": god,
                "abode": abode,
                "symbol": symbol,
                "parent": parent,
                "sibling": sibling,
                "children": children
            }
            # print(json.dumps(my_json, indent=4))
         
            #Create json file   
            file_name = name + ".json"
            file = open(file_name, 'w')
            json.dump(my_json, file)
            file.close()
            print(count, "Files Done")
            element.clear()
    
    #catches error when an infobox for a deity isn't found    
    except Exception as e:
        # print(e)
        print("deity not found") 
    element.clear()
