# game_classes.py

import urllib2
import re


wiki_title = {}

def get_link_found(game):
  return game.wiki_link_found

def sort_found_link(game_list):
  game_list.sort(key=get_link_found, reverse=True)
  return game_list
  


def scrape_details(game):
  base_wiki_api_url = 'http://en.wikipedia.org/w/index.php?action=raw&title='
  
  # replace name with underscored version of itself
  wiki_string = ""
  name_vec = game.name.split()
  for i,word in enumerate(name_vec):
    if (i==0):
      wiki_string = word
    else:
      wiki_string = "{0}_{1}".format(wiki_string, word)

  # set up request data
  wiki_app_url = '{0}{1}'.format(base_wiki_api_url, wiki_string)
  headers = { 'User-Agent' : 'Mozilla/5.0' }

  # try to get the data from the wikipedia page
  print("name: {0} , trying url: {1}".format(game.name, wiki_app_url))
  html_app_data = ""
  req = urllib2.Request(wiki_app_url, None, headers)
  try:
    html_app_data = urllib2.urlopen(req).readlines()
  except urllib2.URLError as e:
    print("URL Error, reason: {0}, code: {1}".format(e.reason, e.code))
 
  game_reg = re.compile('\{\{infobox video game', re.IGNORECASE) 
  for i,line in enumerate(html_app_data):
    line = line.strip()
    #print(line)
    if (game_reg.search(line)):
      game.wiki_link_found = True
      game.wiki_string = wiki_string
      print("wikipedia entry found! name: {0}".format(wiki_string))
      break
  
  if (game.wiki_link_found == False):
    #print("ERROR: Wikipedia entry not found: {0}".format(wiki_string))  
    #print("Trying name and video game")
    wiki_string = "{0}_{1}".format(wiki_string, "(video_game)")
    wiki_app_url = '{0}{1}'.format(base_wiki_api_url, wiki_string)

    print("name: {0} , trying url: {1}".format(game.name, wiki_app_url))
    req = urllib2.Request(wiki_app_url, None, headers)
    try:
      html_app_data = urllib2.urlopen(req).readlines()
    except urllib2.URLError as e:
      print("URL Error, reason: {0}, code: {1}".format(e.reason, e.code))
   
    for i,line in enumerate(html_app_data):
      line = line.strip()
      #print(line)
      if (line == "{{Infobox video game"):
        game.wiki_link_found = True
        game.wiki_string = wiki_string
        print("Second attempt wikipedia entry found! name: {0}".format(wiki_string))
        break


class game:
  def __init__(self, name, app_ID, wiki_found=False, wiki_str=""):
    self.name =  name
    self.app_ID = app_ID 
    self.wiki_string = wiki_str
    self.wiki_link_found = wiki_found
    self.release_date = 1900
    self.developer = ""
  def __str__(self):
    return "<name: {0}>  <app_ID: {1}> <wiki_found: {2}> <wiki_link: {3}>\n" \
              .format(self.name, self.app_ID, self.wiki_link_found, self.wiki_string)
  def __repr__(self):
    return str(self)
  def print_info(self):
    print("name: {0}   app_ID: {1}  wiki_found: {2}  wiki_link: {3}" \
              .format(self.name, self.app_ID, self.wiki_link_found, self.wiki_string))
