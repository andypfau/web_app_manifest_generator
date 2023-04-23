import os
import io
import shutil
import logging
from PIL import Image


def convert_png(input_path: str, output_path: str, size_px: int):

    png = Image.open(input_path)
    logging.info(f'Creating <{output_path}> ({size_px}<{size_px})')
    png.resize((size_px, size_px)).save(output_path)


def convert_svg(input_path: str, output_path: str, size_px: int):

    ext = os.path.splitext(output_path)[1].lower()
    from cairosvg import svg2png
    with open(input_path, 'r') as fp:
        svg = fp.read()
    logging.info(f'Creating <{output_path}> ({size_px}<{size_px})')
    if ext == '.png':
        svg2png(bytestring=svg, write_to=output_path,
                output_width=size_px, output_height=size_px)
    elif ext == '.ico':
        png_bin = svg2png(bytestring=svg,
                            output_width=size_px, output_height=size_px)
        png = Image.open(io.BytesIO(png_bin))
        png.resize((size_px, size_px)).save(output_path)


def open_file(path: str):
    import subprocess, os, platform
    if platform.system() == 'Windows':
        os.startfile(path)
    else: # Linux
        subprocess.call(('xdg-open', path))



class WebAppManifest:

    def __init__(self,
            icon_path: str,
            output_dir: str = './',
            server_dir: str = './',
            name: str = None,
            short_name: str = None,
            lang: str = 'EN-US',
            start_url: str = None,
            description: str = None,
            display: str = 'browser',
            theme_color: str = None,
            background_color: str = None,
            create_html_snippet: bool = True,
            create_html_sample: bool = False,
            open_html_sample: bool = True):
        """Create web manifest files. Just call the constructor to run.

        Args:
            icon_path (str): path to the icon file, can be .png or .svg
            output_dir (str, optional): the directory where the files are created; the directory will be created automatically. Defaults to './'.
            server_dir (str, optional): the intended directory on the server. Defaults to './'.
            name (str, optional): full name of the app. Defaults to None.
            short_name (str, optional): short name of the app. Defaults to None.
            lang (str, optional): natural language of the app. Defaults to 'EN-US'.
            start_url (str, optional): the home URL of the app. Defaults to None.
            description (str, optional): a description for the app. Defaults to None.
            display (str, optional): preferred display mode ('fullscreen', 'standalone', 'minimal-ui', 'browser'). Defaults to 'browser'.
            theme_color (str, optional): CSS theme color. Defaults to None.
            background_color (str, optional): CSS background color. Defaults to None.
            create_html_snippet (bool, optional): whether to create a HTML snippet or not. Defaults to True.
            create_html_sample (bool, optional): wheter to create a full HTML sample page or not. Defaults to False.

        For more info, check <https://developer.mozilla.org/en-US/docs/Web/Manifest>.
        """

        self.icon_path = icon_path
        self.output_dir = output_dir
        self.server_dir = server_dir
        self.name = name
        self.short_name = short_name
        self.lang = lang
        self.start_url = start_url
        self.description = description
        self.display = display
        self.theme_color = theme_color
        self.background_color = background_color
        
        self.server_dir = self.server_dir.replace('\\', '/')
        if not self.server_dir.endswith('/'):
            self.server_dir += '/'

        os.makedirs(output_dir, exist_ok=True)
        have_svg = self._create_icons()
        if create_html_snippet:
            self._create_html_sample(have_svg, full_sample=False)
        if create_html_sample:
            self._create_html_sample(have_svg, full_sample=True)
            if open_html_sample:
                open_file(os.path.join(self.output_dir, 'sample.htm'))

        self._create_manifest()


    def _create_icons(self) -> bool:

        ext = os.path.splitext(self.icon_path)[1].lower()
        if ext == '.png':
            logging.debug('Using PNG converter')
            convert = convert_png
            have_svg = False
        elif ext == '.svg':
            logging.debug('Using SVG converter')
            convert = convert_svg
            have_svg = True
        else:
            raise RuntimeError(f'Unsupported file extension for image: "{ext}"')

        convert(self.icon_path, os.path.join(self.output_dir, 'favicon.ico'),  32)
        convert(self.icon_path, os.path.join(self.output_dir, 'apple-touch-icon.png'), 180)
        convert(self.icon_path, os.path.join(self.output_dir, 'icon-192.png'), 192)
        convert(self.icon_path, os.path.join(self.output_dir, 'icon-512.png'), 512)
        
        if have_svg:
            svg_path = os.path.join(self.output_dir, 'icon.svg')
            if os.path.isfile(svg_path):
                logging.info(f'<{svg_path}> already exists, skipping')
            else:
                logging.info(f'Creating <{svg_path}>')
                shutil.copy(self.icon_path, svg_path)
        else:
            logging.warn('No .svg-file provided, no vector graphics are used')
        
        return have_svg
    

    def _create_html_sample(self, have_svg: bool, full_sample: bool):

        html = ''
        
        if full_sample:
            html += '<!DOCTYPE html>\n'
            html += '<html lang="en">\n'
            html += '<head>\n'
            html += '<meta charset="utf-8" />\n'
            html += '<style type="text/css">\n'
            html += '*{\n'
            html += f'font-family:sans-serif;\n'
            if self.background_color is not None:
                html += f'background-color:{self.background_color};\n'
            html += '}\n'
            if self.theme_color is not None:
                html += 'p{\n'
                html += f'border: solid 1ex {self.theme_color}; padding: 1em;\n'
                html += '}\n'
            html += '</style>\n'
            html += f'<title>{self.name}</title>\n'
            html += '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n'
            html += '<meta name="mobile-web-app-capable" content="yes">\n'
            html += '<meta name="apple-mobile-web-app-capable" content="yes">\n'
            html += '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'

        html += f'<link rel="icon" href="{self.server_dir}favicon.ico" type="image/x-icon">\n'
        if have_svg:
            html += f'<link rel="icon" href="{self.server_dir}icon.svg" type="image/svg+xml">\n'
        html += f'<link rel="apple-touch-icon" href="{self.server_dir}apple-touch-icon.png">\n'
        html += f'<link rel="manifest" href="{self.server_dir}manifest.webmanifest">\n'
        
        if full_sample:
            html += '</head><body>\n'
            html += f'<h1>{self.name}</h1>\n'
            html += f'<p>{self.description}</p>\n'
            html += '</html>\n'
        
        if full_sample:
            filename = 'sample.htm'
        else:
            filename = 'snippet.htm'
        output_path = os.path.join(self.output_dir, filename)
        
        logging.info(f'Creating <{output_path}>')
        with open(output_path, 'w') as fp:
            fp.write(html)


    def _create_manifest(self):
        
        manifest = ''
        manifest += '{\n'
        if self.name is not None:
            manifest += f'  "name": "{self.name}",\n'
        if self.short_name is not None:
            manifest += f'  "short_name": "{self.short_name}",\n'
        if self.lang is not None:
            manifest += f'  "lang": "{self.lang}",\n'
        if self.start_url is not None:
            manifest += f'  "start_url": "{self.start_url}",\n'
        if self.description is not None:
            manifest += f'  "description": "{self.description}",\n'
        if self.display is not None:
            manifest += f'  "display": "{self.display}",\n'
        if self.theme_color is not None:
            manifest += f'  "theme_color": "{self.theme_color}",\n'
        if self.background_color is not None:
            manifest += f'  "background_color": "{self.background_color}",\n'
        manifest += '  "icons": [\n'
        manifest += '    { "src": "'+self.server_dir+'icon-192.png", "type": "image/png", "sizes": "192x192" },\n'
        manifest += '    { "src": "'+self.server_dir+'icon-512.png", "type": "image/png", "sizes": "512x512" }\n'
        manifest += '  ]\n'
        manifest += '}\n'
        
        output_path = os.path.join(self.output_dir, 'manifest.webmanifest')
        logging.info(f'Creating <{output_path}>')
        with open(output_path, 'w') as fp:
            fp.write(manifest)
