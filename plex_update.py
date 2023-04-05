import requests


url = "http://192.168.178.69:32400/library/sections/all/refresh?X-Plex-Token=UnfTg2my49m9TiE2Xe_i"

test = requests.get(url)

print(test)


#ayo das geht!


#http://192.168.178.69:32400/activites/?X-Plex-Token=UnfTg2my49m9TiE2Xe_i