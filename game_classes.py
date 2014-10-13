# game_classes.py

import urllib
import re
import lxml.etree as ET
import urllib2

class game:
  def __init__(self, name, app_ID, wiki_found=False, wiki_str="None", rd=1900, dev="Unlisted", pub="Unlisted" ):
    self.name =  name
    self.app_ID = app_ID 
    self.wiki_string = wiki_str
    if (wiki_str == ""):
      wiki_string = "None"
    if (wiki_found == "False"): 
      self.wiki_link_found = False
    elif (wiki_found == "True"):
      self.wiki_link_found = True
    else:
      self.wiki_link_found = wiki_found
    self.release_date = rd
    self.developer = dev
    self.publisher = pub
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
    if(self.wiki_link_found == False):
      print("Can't get data, no wikipedia link!")
    elif(self.data_filled == True):
      print("Data already filled in, skipping {0}".format(self.name))
    else:
      base_wiki_api_url = 'http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&titles='
      data_reg = re.compile('\{\{Infobox video game(.*?)\}\}', re.DOTALL)
      dev_reg = re.compile('\{\{Infobox video game(.*?)\}\}', re.DOTALL)
      #rd_reg_alt = re.compile('\{\"appid\".*?\}')
      #rd_reg_alt = re.compile('\{\"appid\".*?\}')
      
      wiki_app_url = '{0}{1}'.format(base_wiki_api_url, self.wiki_string)
      headers = {'User-Agent' : 'Mozilla/5.0'}
      html_app_data = ""
      
      req = urllib2.Request(wiki_app_url, None, headers)
      data = []
      redirect = False
      try:
        data = urllib2.urlopen(req)
        html_app_data = data.read()
        if (data.geturl() != wiki_app_url):
          redirect =True
      except urllib2.URLError as e:
        print("URL Error, reason: {0}, code: {1}".format(e.reason, e.code))

      r_root = ET.fromstring(html_app_data)
      e_data = r_root.find('query') 
      e_data = e_data.find('pages') 
      e_data = e_data.find('page') 
      e_data = e_data.find('revisions') 
      e_data = e_data.find('rev')

      print(e_data.text)
      game_data = data_reg.findall(e_data.text)[0]
      game_data = game_data.lstrip()
      game_data = game_data.rstrip()
      game_data = game_data.splitlines()
      print(game_data )
