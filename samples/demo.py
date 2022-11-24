# fix Python paths
import sys, os
sys.path.append(os.path.abspath('.'))

import shutil
from src import WebAppManifest


# prepare file structure for this demo
os.makedirs('./samples/output/', exist_ok=True)
shutil.copy2('./samples/demo.svg', './samples/output/')
shutil.copy2('./samples/demo.png', './samples/output/')


# create the actual web manifest
WebAppManifest.create(
    working_dir='./samples/output/',
    icon_filename='demo.png',
    name='My Faboulous App',
    short_name='MFA',
    lang='EN-US',
    description='This is just a fabulous app',
    theme_color='#00aeff',
    background_color='#ffffff',
    create_html_sample=True)
