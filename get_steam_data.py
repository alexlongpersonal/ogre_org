# this program attempts to access the game listed on a public steam profile
# by Alex Long

import urllib
import os
import re
from game_classes import *
from game_functions import *


steam_user_id = 'metaljoints'
force_write = True

#get the game list from steam
steam_game_list, steam_ngames = get_steam_game_list(steam_user_id)


#try to get wikipedia link for game list
steam_game_list =sorted(steam_game_list, key=lambda l_game: l_game.name)



###############################################################################
#check to see if game list should be updated
#update file if number of games is different
#build data from file if number of games is the same
###############################################################################
filename= "steam_games_list_{0}.xml".format(steam_user_id)
file_exists = os.path.isfile(filename)
update_file = True
new_list = []
if file_exists:
  file_game_list, file_ngames = get_game_list_from_XML(filename)
  if (file_ngames == steam_ngames):
    print("File has same number of games, not updating")
    update_file = False
    new_list = file_game_list
  else:
    print("File has different number of games, adding new games")
    for s_gitr in steam_game_list:
      found = False
      for f_gitr in file_game_list:
        if (int(s_gitr.app_ID) == int(f_gitr.app_ID)):
          found = True
      if (found==False):
        print("Adding game: {0}".format(s_gitr.name))
        file_game_list.append(s_gitr) 
    new_list = file_game_list
else:
  new_list = steam_game_list

new_list =sorted(new_list, key=lambda l_game: l_game.name)
#new_list =sorted(new_list, key=lambda l_game: l_game.release_date, reverse=True)
#sort_found_link(new_list)

for game_itr in new_list:
  game_itr.print_info()

print_percent_found(new_list)


# Try to get steam data using app ID
print("Trying to get game info from Steam for game list")
for g_itr in new_list:
  g_itr.get_data_from_steam()

print("Trying to get wikipedia links for game list")
for game_itr in new_list: find_wikipedia_url(game_itr)


#write XML file
if (update_file or (file_exists == False ) or force_write):
  write_new_game_list(new_list, steam_user_id, filename) 
