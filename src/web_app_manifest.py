import os
import io
import shutil
import logging
from PIL import Image


class WebAppManifest:


    @staticmethod
    def create(
            icon_filename: str,
            working_dir: str = './',
            server_dir: str = './',
            name: str = None,
            short_name: str = None,
            lang: str = 'EN-US',
            start_url: str = None,
            description: str = None,
            display: str = 'browser',
            theme_color: str = None,
            background_color: str = None):

        create_svg = WebAppManifest._create_icons(working_dir, icon_filename)
        WebAppManifest._create_html_snippet(working_dir, server_dir, create_svg)
        WebAppManifest._create_manifest(working_dir, server_dir, name, short_name,
            lang, start_url, description, display, theme_color, background_color)


    @staticmethod
    def _create_icons(working_dir: str, icon_filename: str) -> bool:

        ext = os.path.splitext(icon_filename)[1].lower()
        if ext == '.png':
            logging.debug('Using PNG converter')
            convert = WebAppManifest._convert_png
            save_svg = False
        elif ext == '.svg':
            logging.debug('Using SVG converter')
            convert = WebAppManifest._convert_svg
            save_svg = True
        else:
            raise RuntimeError(f'Unsupported file extension for image: "{ext}"')

        convert(working_dir+icon_filename, working_dir+'favicon.ico',  32)
        convert(working_dir+icon_filename, working_dir+'apple-touch-icon.png', 180)
        convert(working_dir+icon_filename, working_dir+'icon-192.png', 192)
        convert(working_dir+icon_filename, working_dir+'icon-512.png', 512)
        if save_svg:
            fn = working_dir+icon_filename
            logging.info(f'Creating <{fn}>')
            shutil.copy(fn, working_dir+'icon.svg')
        
        return save_svg
    

    @staticmethod
    def _create_html_snippet(working_dir: str, server_dir: str, save_svg: bool):

        html = ''
        html += f'<link rel="icon" href="{server_dir}favicon.ico" sizes="any">\n'
        if save_svg:
            html += f'<link rel="icon" href="{server_dir}icon.svg" type="image/svg+xml">\n'
        html += f'<link rel="apple-touch-icon" href="{server_dir}apple-touch-icon.png">\n'
        html += f'<link rel="manifest" href="{server_dir}manifest.webmanifest">\n'
        
        fn = working_dir+'snippet.htm'
        logging.info(f'Creating <{fn}>')
        with open(fn, 'w') as fp:
            fp.write(html)


    @staticmethod
    def _create_manifest(working_dir: str, server_dir: str, name: str, short_name: str, lang: str,
            start_url: str, description: str, display: str, theme_color: str, background_color: str):
        
        manifest = ''
        manifest += f'// manifest.webmanifest\n'
        manifest += '{\n'
        if name is not None:
            manifest += f'  "name": "{name}",\n'
        if short_name is not None:
            manifest += f'  "short_name": "{short_name}",\n'
        if lang is not None:
            manifest += f'  "lang": "{lang}",\n'
        if start_url is not None:
            manifest += f'  "start_url": "{start_url}",\n'
        if description is not None:
            manifest += f'  "description": "{description}",\n'
        if display is not None:
            manifest += f'  "display": "{display}",\n'
        if theme_color is not None:
            manifest += f'  "theme_color": "{theme_color}",\n'
        if background_color is not None:
            manifest += f'  "background_color": "{background_color}",\n'
        manifest += '  "icons": [\n'
        manifest += '    { "src": "'+server_dir+'icon-192.png", "type": "image/png", "sizes": "192x192" },\n'
        manifest += '    { "src": "'+server_dir+'icon-512.png", "type": "image/png", "sizes": "512x512" }\n'
        manifest += '  ]\n'
        manifest += '}\n'
        
        fn = working_dir+'manifest.webmanifest'
        logging.info(f'Creating <{fn}>')
        with open(fn, 'w') as fp:
            fp.write(manifest)



    @staticmethod
    def _convert_png(input_filename, output_filename, size):

        png = Image.open(input_filename)
        logging.info(f'Creating <{output_filename}> ({size}<{size})')
        png.resize((size, size)).save(output_filename)


    @staticmethod
    def _convert_svg(input_filename, output_filename, size):

        ext = os.path.splitext(output_filename)[1].lower()
        from cairosvg import svg2png
        with open(input_filename, 'r') as fp:
            svg = fp.read()
        logging.info(f'Creating <{output_filename}> ({size}<{size})')
        if ext == '.png':
            svg2png(bytestring=svg, write_to=output_filename,
                    output_width=size, output_height=size)
        elif ext == '.ico':
            png_bin = svg2png(bytestring=svg,
                             output_width=size, output_height=size)
            png = Image.open(io.BytesIO(png_bin))
            png.resize((size, size)).save(output_filename)
