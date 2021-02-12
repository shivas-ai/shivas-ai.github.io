
import os
import requests
import zipfile
import tarfile
import IPython

def download_file(packet_url, base_path="", extract=False, headers=None):
  if base_path != "":
    if not os.path.exists(base_path):
      os.mkdir(base_path)
  packet_file = os.path.basename(packet_url)
  with requests.get(packet_url, stream=True, headers=headers) as r:
      r.raise_for_status()
      with open(os.path.join(base_path,packet_file), 'wb') as f:
          for chunk in r.iter_content(chunk_size=8192):
              f.write(chunk)
  
  if extract:
    if packet_file.endswith(".zip"):
      with zipfile.ZipFile(os.path.join(base_path,packet_file)) as zfile:
        zfile.extractall(base_path)
    else:
      packet_name = packet_file.split('.')[0]
      with tarfile.open(os.path.join(base_path,packet_file)) as tfile:
        tfile.extractall(base_path)

def easy_paginate_colab(base_path,slide_images=[]):
  scripts = '''
    <script src="/static/components/requirejs/require.js"></script>
    <script>
      requirejs.config({
        paths: {
          base: '/static/base',
          "easyPaginate": "//raw.githubusercontent.com/shivas-ai/shivas-ai.github.io/main/assets/js/easypaginate/jquery.easyPaginate",
          jquery: '//ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min',
        },
      });
    </script>
  '''

  styles = '''
    <style>
      #easyPaginate {width:300px;}
      #easyPaginate img {display:block;margin-bottom:10px;}
      .easyPaginateNav a {padding:5px;}
      .easyPaginateNav a.current {font-weight:bold;text-decoration:none;}
    </style>
  '''

  custom_scripts = '''
    <script>
      console.log("Inside javascript....");
      requirejs(['jquery', 'easyPaginate'], function($, easyPaginate) {
          $("#easyPaginate").easyPaginate({
              paginateElement: 'img',
              elementsPerPage: 1
          });
      });
    </script>
  '''
  slides = '<div id="easyPaginate">'
  for img in slide_images:
    slides = slides + '<img src="'+base_path+img+'" width="1200" />'
  slides += '</div>'

  return display(IPython.core.display.HTML(scripts+styles+slides+custom_scripts))
