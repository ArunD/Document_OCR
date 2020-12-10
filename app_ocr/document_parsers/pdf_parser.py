import os
import glob
import unicodedata
import html2text
import re
import xml.etree.ElementTree as ET
from collections import OrderedDict
from subprocess import Popen

from app_ocr.document_parsers.image_extraction import get_image_from_file, get_text_from_image

PDF_TO_HTML = 'pdftohtml -zoom 1.75 -s {filename}'
IMAGE_REGEX = '\[background image\]\(.*?\)'


class PdfParser:

    def __init__(self, tmp_dir):
        self.tmp_dir = tmp_dir

    def parse(self, document):
        if os.path.isabs(document.name):
            doc_path = document.name
        else:
            doc_path = os.path.join(self.tmp_dir, document.name)
        if not os.path.isfile(doc_path):
            with open(doc_path, 'wb') as indoc:
                indoc.write(document.read())
        self._pdf_to_html(document.name)
        text = self._html_to_text('.'.join(document.name.split('.')[:-1]) + '-html.html')
        text = unicodedata.normalize('NFKD', text)
        #self._purge_tmp_dir(document.name)
        return text

    def _pdf_to_html(self, filename):
        filename = filename.replace(' ', '\ ')
        command = PDF_TO_HTML.format(filename=filename)
        if type(self.tmp_dir) != str:
            tmp_dir_path = self.tmp_dir.name
        else:
            tmp_dir_path = self.tmp_dir
        process = Popen(command, cwd=tmp_dir_path, shell=True)  # check what pipe means
        process.communicate()

    def _html_to_text(self, filename):
        with open(os.path.join(self.tmp_dir, filename), 'r', encoding="utf-8") as f:
            html_string = f.read()
        trimmed = map(lambda x: x.strip(), html_string.split('<!DOCTYPE html>'))
        filtered = list(filter(lambda x: len(x) > 0, trimmed))
        unique = OrderedDict()
        for index, page in enumerate(filtered):
            unique[page] = page
        pdf_text = []
        for index, page in unique.items():
            page_text = html2text.html2text(page)
            images = re.findall(IMAGE_REGEX, page_text)
            
            for image_string in images:
                
                image_name = image_string[image_string.find('(') + 1: image_string.find(')')]
                
                image_path = os.path.join(self.tmp_dir, image_name)
                image_list = get_image_from_file(image_path, 'image/png', 150)
                
                image_text = get_text_from_image(image_list)
                page_text = page_text.replace(image_string, image_text[0])
            pdf_text.append(page_text)
            pdf_text.append(30 * '#')
        pdf_text = '\n'.join(filter(lambda x: x.strip() != '', pdf_text))
        return pdf_text

    def _purge_tmp_dir(self, filename):
        base = filename.split('.pdf')[0]
        files_to_remove = glob.glob(os.path.join(self.tmp_dir, base) + '*')
        for filename in files_to_remove:
            os.remove(filename)
