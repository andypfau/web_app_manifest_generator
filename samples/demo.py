import shutil
import sys
import os

sys.path.append(os.path.abspath('.'))
from src import WebAppManifest


if __name__ == '__main__':
    WebAppManifest(
        
        # all generated files will be put here; the directory will be created automatically
        output_dir='./samples/output/',

        # this is our icon file; .svg is recommended, .png also works
        icon_path='./samples/demo.svg',

        # parameters of the app
        name='My Faboulous App',
        short_name='MFA',
        lang='EN-US',
        description='This is just a fabulous app',
        theme_color='#33aadd',
        background_color='#222222',
        create_html_sample=True,
        create_html_snippet=True,
    )
