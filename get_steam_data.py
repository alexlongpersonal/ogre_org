# this program attempts to access the game listed on a public steam profile
# by Alex Long

import urllib
import os
import re
from game_classes import *
from game_functions import *


steam_user_id = 'metaljoints'

#get the game list from steam
steam_game_list, steam_ngames = get_steam_game_list(steam_user_id)


#try to get wikipedia link for game list
steam_game_list =sorted(steam_game_list, key=lambda l_game: l_game.name)


#print("Trying to get wikipedia links for game list")
#for game_itr in steam_game_list: scrape_details(game_itr)
#print_percent_found(steam_game_list)

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
#sort_found_link(new_list)

for game_itr in new_list:
  game_itr.print_info()

print_percent_found(new_list)

new_list[steam_ngames-2].get_data_from_wiki()




if (update_file or (file_exists == False )):
  write_new_game_list(new_list, steam_user_id, filename) 
