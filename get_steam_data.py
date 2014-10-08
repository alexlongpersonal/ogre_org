# this program attempts to access the game listed on a public steam profile
# by Alex Long

import urllib
import os
import re
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

game_list = []
for g_s in g_str_list:
  app_ID = app_reg.findall(g_s)[0]
  name = name_reg.findall(g_s)[0]
  game_list.append(game(name, app_ID))



'''
#try to get wikipedia link for game list
print("Trying to get wikipedia links for game list")
for game in game_list: scrape_details(game)
'''

###############################################################################
#check to see if game list should be updated
#update file if number of games is different
###############################################################################
filename= "steam_games_list_{0}.txt".format(steam_user_id)
file_exists = os.path.isfile(filename)
update_file = True
ngame = len(game_list)
if file_exists:
  ngame_reg = re.compile('ngames:(.*?)$')
  f_check = open(filename,'r')
  for line in f_check:
    if ngame_reg.search(line):
      print("File has same number of games, not updating")
      old_ngame = ngame_reg.findall(line)[0]
      update_file = False
      f_check.close()
      break
  f_check.close() 

###############################################################################
#build game list data from file
###############################################################################

if (update_file == False):
  game_list = []
  f_check = open(filename,'r')
  r_name = re.compile('<name: (.*?)>')
  r_app = re.compile('<app_ID: (.*?)>')
  r_found = re.compile('<wiki_found: (.*?)>')
  r_wiki = re.compile('<wiki_link: (.*?)>')
  for line in f_check:
    if r_name.search(line):
      name = r_name.findall(line)[0]
      app_ID = r_app.findall(line)[0]
      found_l = r_found.findall(line)[0] 
      wiki_l = r_wiki.findall(line)[0]
      game_list.append(game(name, app_ID, found_l,wiki_l))

game_list =sorted(game_list, key=lambda game: game.name)
sort_found_link(game_list)


for g in game_list:
  g.print_info() 


###############################################################################


if (update_file or (file_exists != True )):
  print("Writing game data to file")
  f_out = open(filename, 'w')
  f_out.write("user: {0} ngames: {1}\n".format(steam_user_id, ngame))
  for game in game_list:
    f_out.write(str(game))
  f_out.close()




#f_check = open(filename, 'r')
#game_data = f_check.readline()
#game_data = game_data.split()
#if (game_data[3] == ngame):
#  print("Skipping file write--games list unchanged")
