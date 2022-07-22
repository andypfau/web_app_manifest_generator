import unittest
import sys
import os
import shutil


sys.path.append(os.path.abspath('.'))
from src import WebAppManifest


class WebAppManifestTest(unittest.TestCase):

    
    SAMPLES_DIR = './samples/'
    TMP_DIR = './samples/tmp/'


    def test_files_are_created_from_png(self):
        self.prepare(copy_png=True)
        try:
            WebAppManifest.create(
                working_dir=WebAppManifestTest.TMP_DIR,
                icon_filename='demo.png',
                name='Demo App',
                short_name='Demo',
                lang='EN-US',
                description='This is just a demo',
                theme_color='#00aeff',
                background_color='#ffffff')
            self.assertTrue(os.path.exists(WebAppManifestTest.TMP_DIR+'favicon.ico'))
            self.assertTrue(os.path.exists(WebAppManifestTest.TMP_DIR+'apple-touch-icon.png'))
            self.assertTrue(os.path.exists(WebAppManifestTest.TMP_DIR+'icon-192.png'))
            self.assertTrue(os.path.exists(WebAppManifestTest.TMP_DIR+'icon-512.png'))
            self.assertFalse(os.path.exists(WebAppManifestTest.TMP_DIR+'icon.svg'))
            self.assertTrue(os.path.exists(WebAppManifestTest.TMP_DIR+'snippet.htm'))
        finally:
            self.cleanup()
        

    def test_files_are_created_from_svg(self):
        self.prepare(copy_svg=True)
        try:
            WebAppManifest.create(
                working_dir=WebAppManifestTest.TMP_DIR,
                icon_filename='demo.svg',
                name='Demo App',
                short_name='Demo',
                lang='EN-US',
                description='This is just a demo',
                theme_color='#00aeff',
                background_color='#ffffff')
            self.assertTrue(os.path.exists(WebAppManifestTest.TMP_DIR+'favicon.ico'))
            self.assertTrue(os.path.exists(WebAppManifestTest.TMP_DIR+'apple-touch-icon.png'))
            self.assertTrue(os.path.exists(WebAppManifestTest.TMP_DIR+'icon-192.png'))
            self.assertTrue(os.path.exists(WebAppManifestTest.TMP_DIR+'icon-512.png'))
            self.assertTrue(os.path.exists(WebAppManifestTest.TMP_DIR+'icon.svg'))
            self.assertTrue(os.path.exists(WebAppManifestTest.TMP_DIR+'snippet.htm'))
        finally:
            self.cleanup()
        

    def prepare(self, /, copy_png: bool = False, copy_svg: bool = False):
        os.makedirs(WebAppManifestTest.TMP_DIR, exist_ok=True)
        if copy_png:
            shutil.copy(WebAppManifestTest.SAMPLES_DIR+'demo.png', WebAppManifestTest.TMP_DIR+'demo.png')
        if copy_svg:
            shutil.copy(WebAppManifestTest.SAMPLES_DIR+'demo.svg', WebAppManifestTest.TMP_DIR+'demo.svg')


    def cleanup(self):
        shutil.rmtree(WebAppManifestTest.TMP_DIR)


if __name__ == '__main__':
    unittest.main()
