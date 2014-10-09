# this program attempts to access the game listed on a public steam profile
# by Alex Long

import urllib
import os
import re
import lxml.etree as ET
from game_classes import *


steam_user_id = 'metaljoints'
steam_user_url = 'http://steamcommunity.com/id/{0}'.format(steam_user_id)
all_games_url = '{0}/games/?tab=all'.format(steam_user_url)

print("Getting game list for Steam user {0}".format(steam_user_id))
steam_url_obj = urllib.urlopen(all_games_url)
html_all_games = steam_url_obj.readlines()

###############################################################################
# find the long string of games and data from raw HTML
###############################################################################
raw_games_str = ""

for i,line in enumerate(html_all_games):
  lvec = line.split()
  if (len(lvec) > 2 ):
    if (lvec[1] =='rgGames'):
      raw_game_str = line

###############################################################################
# parse games and app ID from raw string
# (this string is defining a java class)
###############################################################################

#regular expressions
g_reg = re.compile('\{\"appid\".*?\}')
app_reg = re.compile('\"appid\":(.*?),')
name_reg = re.compile('\"name\":\"(.*?)\"') 
 
g_str_list = g_reg.findall(raw_game_str)

new_list = []
for g_s in g_str_list:
  app_ID = app_reg.findall(g_s)[0]
  name = name_reg.findall(g_s)[0]
  new_list.append(game(name, app_ID))

ngames = len(new_list)




#try to get wikipedia link for game list
#new_list =sorted(new_list, key=lambda game: game.name)
#print("Trying to get wikipedia links for game list")
#for game in new_list: scrape_details(game)
#scrape_details(new_list[8])

###############################################################################
#check to see if game list should be updated
#update file if number of games is different
#build data from file if number of games is the same
###############################################################################
filename= "steam_games_list_{0}.xml".format(steam_user_id)
file_exists = os.path.isfile(filename)
update_file = True
old_game_list = []
if file_exists:
  r_tree = ET.parse(filename)
  r_root = r_tree.getroot()
  r_info = r_root[0]
  old_ngames = int(r_info[1].text)
  if (old_ngames == ngames):
    print("File has same number of games, not updating")
    update_file = False

  if (update_file == False):
    r_game_list = r_root[1]
    for g_itr in r_game_list.findall('game'):
      name = g_itr.get("name")
      app_ID = g_itr.find("app_ID").text
      found_l = g_itr.find("wiki_link_found").text
      wiki_l = g_itr.find("wiki_string").text
      old_game_list.append(game(name, app_ID, found_l,wiki_l))
    new_list = old_game_list

new_list =sorted(new_list, key=lambda game: game.name)
sort_found_link(new_list)

for g in new_list:
  g.print_info()


###############################################################################
#write XML file
###############################################################################
if (update_file or (file_exists != True )):
  print("Writing game data to XML file")
  root = ET.Element("root")
  info = ET.SubElement(root, "info")
  user = ET.SubElement(info, "user_ID")
  user.text = steam_user_id
  ngame_elem = ET.SubElement(info, "num_games")
  ngame_elem.text = "{0}".format(ngames)

  games = ET.SubElement(root, "game_list")

  for g in new_list:
    game_elem = ET.SubElement(games, "game")
    game_elem.set("name", g.name)
    app_elem = ET.SubElement(game_elem, "app_ID")
    found_elem = ET.SubElement(game_elem, "wiki_link_found")
    wiki_elem = ET.SubElement(game_elem, "wiki_string")
    app_elem.text = g.app_ID
    found_elem.text = str(g.wiki_link_found)
    wiki_elem.text = g.wiki_string

  tree = ET.ElementTree(root)
  tree.write(filename, pretty_print=True )
