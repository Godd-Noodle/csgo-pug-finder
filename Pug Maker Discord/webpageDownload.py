import urllib.request, urllib.error, urllib.parse


faceituser = "PaddyVac" 
url_start = "https://faceitstats.com/player,"


webpage = "https://faceitstats.com/player,"
response = urllib.request.urlopen(webpage +faceituser)
    
webcontentfs = str(response.read())

index = webcontentfs.find("https://steamcommunity.com/profiles/")
i_e = webcontentfs[index:].find('"')

steamurl = webcontentfs[index:index+i_e]

response = urllib.request.urlopen(steamurl)
    
webcontentsteam = str(response.read())
    
    
    
p_s = webcontentsteam.find(str('<div class="profile_summary">'))
p_e = webcontentsteam.find(str('<div class="profile_summary_footer">'))


level_s = webcontentfs.find("level: <strong>")

level = webcontentfs[level_s:level_s+20]

level_filter = filter(str.isdigit, level)
faceitLevel = "".join(level_filter)
found = webcontentsteam[p_s:p_e].find("Godd_Noodle#3075")

print(found)
print(faceitLevel)



#outF = open("faceit.txt", "w")
#outF.writelines(webcontent)
#outF.close()
