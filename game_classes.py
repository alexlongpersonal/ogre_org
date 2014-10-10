# game_classes.py

import urllib
import re

class game:
  def __init__(self, name, app_ID, wiki_found=False, wiki_str=""):
    self.name =  name
    self.app_ID = app_ID 
    self.wiki_string = wiki_str
    if (wiki_found == "False"): 
      self.wiki_link_found = False
    elif (wiki_found == "True"):
      self.wiki_link_found = True
    else:
      self.wiki_link_found = wiki_found
    self.release_date = 1900
    self.developer = ""
    self.publisher = ""
    self.data_filled = False
  def __str__(self):
    return "<name: {0}>  <app_ID: {1}> <wiki_found: {2}> <wiki_link: {3}>\n" \
              .format(self.name, self.app_ID, self.wiki_link_found, self.wiki_string)
  def __repr__(self):
    return str(self)
  def print_info(self):
    print("name: {0}   app_ID: {1}  wiki_found: {2}  wiki_link: {3}" \
              .format(self.name, self.app_ID, self.wiki_link_found, self.wiki_string))
  def get_data_from_wiki(self):
    if(self.wiki_found == False):
      print("Can't get data, no wikipedia link!")
    elif(self.data_filled == True):
      print("Data already filled in, skipping {0}".format(self.name))
    else:
      rd_reg = re.compile('\{\"appid\".*?\}')
      
      base_wiki_api_url = 'http://en.wikipedia.org/w/index.php?action=raw&title='
      wiki_app_url = '{0}{1}'.format(base_wiki_api_url, self.wiki_string)
      headers = {'User-Agent' : 'Mozilla/5.0'}
      
      
    
