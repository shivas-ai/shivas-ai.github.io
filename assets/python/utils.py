
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
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tfile, base_path)

def easy_paginate_colab(base_path,slide_images=[]):
  scripts = '''
    <script src="/static/components/requirejs/require.js"></script>
    <script>
      requirejs.config({
        paths: {
          base: '/static/base',
          "easyPaginate": "//storage.googleapis.com/public_js_modules/easypaginate/jquery.easyPaginate",
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
