import unittest
import sys
import os
import shutil

sys.path.append(os.path.abspath('.'))
from src import WebAppManifest


class WebAppManifestTest(unittest.TestCase):

    
    SAMPLES_DIR = './samples/'
    OUTPUT_DIR = './test/tmp/'


    def test_files_are_created_from_png(self):
        WebAppManifest(
            output_dir=WebAppManifestTest.OUTPUT_DIR,
            icon_path='./samples/demo.png',
            name='Demo App',
            short_name='Demo',
            lang='EN-US',
            description='This is just a demo',
            theme_color='#00aeff',
            background_color='#ffffff')
        self.assertTrue(os.path.exists(WebAppManifestTest.OUTPUT_DIR+'favicon.ico'))
        self.assertTrue(os.path.exists(WebAppManifestTest.OUTPUT_DIR+'apple-touch-icon.png'))
        self.assertTrue(os.path.exists(WebAppManifestTest.OUTPUT_DIR+'icon-192.png'))
        self.assertTrue(os.path.exists(WebAppManifestTest.OUTPUT_DIR+'icon-512.png'))
        self.assertFalse(os.path.exists(WebAppManifestTest.OUTPUT_DIR+'icon.svg'))
        self.assertTrue(os.path.exists(WebAppManifestTest.OUTPUT_DIR+'snippet.htm'))
        

    def test_files_are_created_from_svg(self):
        WebAppManifest(
            output_dir=WebAppManifestTest.OUTPUT_DIR,
            icon_path='./samples/demo.svg',
            name='Demo App',
            short_name='Demo',
            lang='EN-US',
            description='This is just a demo',
            theme_color='#00aeff',
            background_color='#ffffff')
        self.assertTrue(os.path.exists(WebAppManifestTest.OUTPUT_DIR+'favicon.ico'))
        self.assertTrue(os.path.exists(WebAppManifestTest.OUTPUT_DIR+'apple-touch-icon.png'))
        self.assertTrue(os.path.exists(WebAppManifestTest.OUTPUT_DIR+'icon-192.png'))
        self.assertTrue(os.path.exists(WebAppManifestTest.OUTPUT_DIR+'icon-512.png'))
        self.assertTrue(os.path.exists(WebAppManifestTest.OUTPUT_DIR+'icon.svg'))
        self.assertTrue(os.path.exists(WebAppManifestTest.OUTPUT_DIR+'snippet.htm'))
        

    def setUp(self):
        shutil.rmtree(WebAppManifestTest.OUTPUT_DIR, ignore_errors=True)


    def tearDown(self):
        shutil.rmtree(WebAppManifestTest.OUTPUT_DIR)


if __name__ == '__main__':
    unittest.main()
