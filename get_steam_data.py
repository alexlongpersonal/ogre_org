# this program attempts to access the game listed on a public steam profile
# by Alex Long

import urllib
import os
import re
import lxml.etree as ET
from game_classes import *
from game_functions import *


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
new_list =sorted(new_list, key=lambda l_game: l_game.name)
#print("Trying to get wikipedia links for game list")
#for game_itr in new_list: scrape_details(game_itr)
#scrape_details(new_list[8])

#calculate percentage found
num_found = 0
for game_itr in new_list:
  if (game_itr.wiki_link_found):
    num_found = num_found + 1

print("Found: {0} , percent: {1}".format(num_found, float(num_found)/ngames*100))


###############################################################################
#check to see if game list should be updated
#update file if number of games is different
#build data from file if number of games is the same
###############################################################################
filename= "steam_games_list_{0}.xml".format(steam_user_id)
file_exists = os.path.isfile(filename)
update_file = True
if file_exists:
  file_game_list, file_ngames = get_game_list_from_XML(filename)
  if (file_ngames == ngames):
    print("File has same number of games, not updating")
    update_file = False
    new_list = file_game_list
  else:
    print("File has different number of games, adding new games")
    # do something here that works


new_list =sorted(new_list, key=lambda l_game: l_game.name)
sort_found_link(new_list)

for game_itr in new_list:
  game_itr.print_info()

num_found = 0
for game_itr in new_list:
  if (game_itr.wiki_link_found):
    num_found = num_found + 1

print("Found: {0} , percent: {1}".format(num_found, float(num_found)/ngames*100))

if (update_file or (file_exists == False )):
  write_new_game_list(new_list, steam_user_id, filename) 
