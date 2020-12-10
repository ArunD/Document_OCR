import extract_msg
import glob
import io
import json
import os
import tempfile

from app_ocr.document_parsers.docx_parser import DocxParser
from app_ocr.document_parsers.image_parser import ImageParser
from app_ocr.document_parsers.pdf_parser import PdfParser


class MailParser:

    def __init__(self, tmp_dir):
        self.tmp_dir = tmp_dir
        self.docx_parser = DocxParser(tmp_dir)
        self.pdf_parser = PdfParser(tmp_dir)
        self.mail_data = {}

    def parse(self, document):
        doc_path = os.path.join(self.tmp_dir, document.name)
        #with open(doc_path, 'wb') as indoc:
        #    indoc.write(document.read())

        msg = extract_msg.Message(doc_path)
        self._parse_mail_info(msg)
        self._parse_attachments(msg)
        self._purge_tmp_dir(document.name)
        text = ''
        for key in self.mail_data:
            if self.mail_data[key] and key != 'attachments':
                text += key + ':' + self.mail_data[key] + '\n'
        for attachment in self.mail_data['attachments']:
            text += 30 * '#' + '\n'
            text += attachment['filename'] + '\n'
            text += attachment['text'] + '\n'
        return text

    def _parse_mail_info(self, msg):
        self.mail_data['from'] = msg.sender
        self.mail_data['to'] = msg.to
        self.mail_data['cc'] = msg.cc
        self.mail_data['subject'] = msg.subject
        self.mail_data['date'] = msg.date
        self.mail_data['attachments'] = []
        self.mail_data['body'] = msg.body

    def _parse_attachments(self, msg):
        for attachment in msg.attachments:
            _, ext = os.path.splitext(attachment.longFilename)
            if ext == '.pdf':
                parser = PdfParser(self.tmp_dir)
            elif ext == '.docx':
                parser = DocxParser(self.tmp_dir)
            elif ext in ['.jpg', '.jpeg', '.png']:
                parser = ImageParser()
            else:
                continue
            document = io.BytesIO(attachment.data)
            document.name = attachment.longFilename
            text = parser.parse(document)
            self.mail_data['attachments'].append(
                {
                    'filename': attachment.longFilename,
                    'text': text
                }
            )

    def _purge_tmp_dir(self, filename):
        base = filename.split('.msg')[0]
        files_to_remove = glob.glob(os.path.join(self.tmp_dir, base) + '*')
        for filename in files_to_remove:
            os.remove(filename)
