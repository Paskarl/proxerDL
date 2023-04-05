import argparse
import json
import re
import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup
import urllib


class proxerDL:
    
    def __init__(self) -> None:
       
        self.cookies = {'proxer_loggedin':'true', 'joomla_user_state':'logged_in', 'XSRF-TOKEN':'eyJpdiI6Imh3cDVTbktsa2RLU0lqZHN2TWtzOVE9PSIsInZhbHVlIjoiK05sXC9NMFQ2VXdWbWR2YkZCcXdZRHBpUkJXZ092UWMzanlNaGdZZ1dLbWZcL1JsT1wvUXp5bWt5QkFEajNBXC9PVm0iLCJtYWMiOiIyYmVhNTU5ODUwYmMzZmQwNTllMzE5OTM4ZmU5OGZhNzE1ZGViZWIzZmIzOGI5YjBkNTA1YjMyMzcxMTdiZGYwIn0%3D', 'proxer_player_session':'eyJpdiI6InRBR3pPNzYzbVhvTUdNaTJ1Tmp5a0E9PSIsInZhbHVlIjoia2tcL25zQWFhMFM4T1Y3UjN3ZDVBM1UzeEJ4ZGVQeTZnbVA3VUJYcldEc0phYkZQbGtLSFRxQ0VSNU1ldXRkYVkiLCJtYWMiOiIyYTQyNmZhYzY2NDEwY2U4OWIxYzM4NzM3N2UwNmEyMWQ1MzQxNzEzNTdjYTcyZjg2ZTc5NjY1YTM3ODcxYWJiIn0%3D', 'CookieScriptConsent':'{"action":"reject","categories":"[]","CMP":"CPnub35Pnub35F2ADBENCaCgAAAAAAAAAAAAAAAAAAAA.YAAAAAAAAAAA","key":"b29ca758-3105-4fde-a46e-6fb840e3e277"}', 'e0da4f913f5f05ed7a3f6dc5f0488c7b':'7tjktjvhurce0bicbbl04o9j7k', 'stream_choose':'proxer-stream', 'tmode':'ht', 'joomla_remember_me_0109a16d4ebeb98d2073bff41fd9c5dd':'9QjxjlGu1CLNOMxa.LcCKzlQfflZWiOsgeb2k', 'style':'gray', 'stream_donatecall3':'1', 'default_design':'gray', 'joomla_remember_me_0c0d7e49ef22a3e1275ace60581e72ff':'484IoNJwWxFK44P2.Ndnnkf7X1Yn0zgC0iO74'}
        coockieConsent = {"action":"reject","categories":"[]","CMP":"CPpalVSPpalVSF2ADBENCaCgAAAAAAAAAAAAAAAAAAAA.YAAAAAAAAAAA","key":"6fa4718a-c72a-4da9-a357-231cdf252463"}
        json_coockie = json.dumps(coockieConsent)
        #self.cookies = {'proxer_loggedin':'true', 'joomla_user_state':'logged_in', 'e0da4f913f5f05ed7a3f6dc5f0488c7b':'fup0j35noesb38l3ovpakgc0r4', 'CookieScriptConsent':json_coockie}
        self.s = requests.Session()
        self.url = ""

    def download(self, url, name, location):
        
        r = requests.get(url, allow_redirects=True, stream=True)
        total = int(r.headers.get('content-length', 0))
        name = name + ".mp4"
        complete_name = os.path.join(self.folderTitle + "\\" + name)
        with open(complete_name, "wb") as file, tqdm(
                desc=name,
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in r.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
                
                
    def bulk_download(self, id):
        cwd = os.getcwd()
        self.get_content(id, 1)
        self.folderTitle = self.folderTitle.replace(":", "")
        path = os.path.join(cwd, self.folderTitle)


        try:
            os.mkdir(path)
        except:
            os.rmdir(path)
            os.mkdir(path)
        amnt_episodes = self.get_amount_episodes(id) 
        img_url = self.get_cover_image(id)
        urllib.request.urlretrieve(img_url, path + "\\poster.jpg")
        for episode in range(1, amnt_episodes + 1):
            
            self.get_content(id, episode)
            url = self.get_download_url()
            self.download(url, self.episode_name, str(path))
        
            
    def get_content(self, id, episode):
        while True:
            try:
                self.url = "https://proxer.me/watch/" + str(id) + "/" + str(episode) + "/engsub"
                        
                r = self.s.get(self.url, cookies=self.cookies)

                soup = BeautifulSoup(r.content, "html.parser")
            
                data = soup.find_all('script', type='text/javascript')
                self.episode_name = str(soup.find("span", {"class": "wName"}))
                self.episode_name = self.episode_name.replace('<span class="wName">', '')
                self.episode_name = self.episode_name.replace("</span>", "")
                self.episode_name = self.episode_name.replace(":", "")
                self.folderTitle = self.episode_name.replace(":", "")
                self.episode_name = self.episode_name + " s01e" + str(episode)
       # print(self.episode_name)

                anime_id_data = str(data[5])
                match = re.search(r'"code":"\w+"', anime_id_data)
                
                if match:
                    code_text = match.group()
                    #print(f"Der Code-Text wurde gefunden: {code_text}")
                    self.anime_id = code_text.replace('"code":', '')
                    self.anime_id = self.anime_id.replace('"', "")
                    #print(self.anime_id)
                else:
                    print("Kein Code-Text gefunden.")
                    #print(match)
            except:
                print("You may have to Enter the Capcha to continue, please check your browser or wait 5 seconds and press any key")
                input()
                continue
            break
                
           
    def get_cover_image(self, id):
       url = 'https://proxer.me/info/' + str(id)
       r = self.s.get(url, cookies=self.cookies)
       soup = BeautifulSoup(r.content, "html.parser")
       coverImg = soup.find_all("img")
       for x in coverImg:
           if("cover" in x["src"]):
                img_url = x["src"]
                return img_url.replace("//", "https://")
      
       return 0
   
    def get_amount_episodes(self, id):
       url = 'https://proxer.me/info/' + str(id) + '/list'
       r = self.s.get(url, cookies=self.cookies)
       soup = BeautifulSoup(r.content, "html.parser")
       mydivs = soup.find_all("tr")
       amount = len(mydivs) - 1
       print("Anzahl der Folgen: " + str(amount))
       
       
       return amount
   
    def get_download_url(self):
        
        base_url = "https://stream.proxer.me/embed-" + self.anime_id + ".html"
        while True:
            try:
                r = self.s.get(base_url, cookies=self.cookies)
                soup = BeautifulSoup(r.content, "html.parser")
                source = soup.find("source")
                unparsed_url = str(source)
                match = re.search(r"https?://\S+", unparsed_url)
                if match:
                    code_text = match.group()
                    #print(f"Die URL wurde gefunden: {code_text}")
                    code_text = code_text.replace('"', "")
                    return code_text
                else:
                    base_url = "https://stream-service.proxer.me/embed-" + self.anime_id + ".html"
            
                    
                    r = self.s.get(base_url, cookies=self.cookies)
                    soup = BeautifulSoup(r.content, "html.parser")
                    source = soup.find("source")
                    unparsed_url = str(source)
                    match = re.search(r"https?://\S+", unparsed_url)
                
                    if match:
                        code_text = match.group()
                    # print(f"Die URL wurde gefunden: {code_text}")
                        code_text = code_text.replace('"', "")
                        return code_text

            except:
                print("Error getting Payload. Wait a few seconds and then press any key")
                input()
                continue
            break


                
       
      




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Proxer Downlaoder')
    parser.add_argument('-i', '--id')
    args = parser.parse_args()
    
    if args.id:
        
        downloadObj = proxerDL()
        downloadObj.bulk_download(args.id)
    else:
        print("No Args provided! Please Enter -i with an Anime ID")
        
        
        
        
        
        # X-Plex-Token=UnfTg2my49m9TiE2Xe_i
        
        
       #GET http://[IP address]:32400/library/sections/all/refresh?X-Plex-Token=[PlexToken]