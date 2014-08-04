import json
import os


def returnDetails(cmp_name,n):
    '''(str)->(dict(int:[list]))
    This function takes in company name to be searched as argument, and returns
    the id of the employees as keys mapped to their basic info
    '''
    path="C:/Python27/Scripts/scraping/linkedin/" #Even on Windows use only forward slashes (Eg):"C:/Python27/Scripts/scraping/profoundis/"
    dom_filename="dom.txt"
    pattern_start='<code id="voltron_srp_main-content" style="display:none;"><!--' #This is the pattern that uniquely distinguishes HTML and JSON in the page source
    pattern_end='--></code>' #This is the delimiter which denotes the end of JSON
    details=[] #Details of employees
    d={} #Linkedin employee-id mapped to the details of the respective employees

    if(os.path.isfile(path+dom_filename)):
        f=open(dom_filename,"r")
        dom=f.read()
        json_content=dom[dom.find(pattern_start)+len(pattern_start):dom.find(pattern_end)]
        f.close()
        json_data=json.loads(json_content)
        for i in range(n):
            if(cmp_name.capitalize() in json_data["content"]["page"]["voltron_unified_search_json"]["search"]["results"][i]["person"]["fmt_headline"]):
                i_d=json_data["content"]["page"]["voltron_unified_search_json"]["search"]["results"][i]["person"]["id"]
                name=str(json_data["content"]["page"]["voltron_unified_search_json"]["search"]["results"][i]["person"]["fmt_name"])
                ind=str(json_data["content"]["page"]["voltron_unified_search_json"]["search"]["results"][i]["person"]["fmt_industry"])
                loc=str(json_data["content"]["page"]["voltron_unified_search_json"]["search"]["results"][i]["person"]["fmt_location"])
                details.append(name)
                details.append(ind)
                details.append(loc)
                snippets=json_data["content"]["page"]["voltron_unified_search_json"]["search"]["results"][i]["person"]["snippets"]
                if(len(snippets)>0):
                    for j in range(len(snippets)):
                        temp=snippets[j]["bodyList"]
                        temp=[str(s).replace('<strong class="highlight">','').replace('</strong>','').replace('&amp;','&') for s in temp]
                        for k in temp:
                            details.append(str(snippets[j]["fieldName"])+' -> '+k)
                    d[i_d]=details
                    details=[]
                else:
                    desig=str(json_data["content"]["page"]["voltron_unified_search_json"]["search"]["results"][i]["person"]["fmt_headline"]).replace('<strong class="highlight">','').replace('</strong>','').replace('&amp;','&')
                    details.append(desig)
                    d[i_d]=details
                    details=[]
    return d
