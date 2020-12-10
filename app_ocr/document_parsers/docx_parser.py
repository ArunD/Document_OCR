import os
from subprocess import Popen
from app_ocr.document_parsers.pdf_parser import PdfParser


COMMAND = 'libreoffice --headless --convert-to pdf --outdir {outdir} {filename}'


class DocxParser:

    def __init__(self, tmp_dir):
        self.tmp_dir = tmp_dir
        self.pdf_parser = PdfParser(tmp_dir)

    def parse(self, document):

        doc_path = os.path.join(self.tmp_dir, document.name)
        #with open(doc_path, 'wb') as indoc:
        #    indoc.write(document.read())
        self._docx_to_pdf(document.name)
        pdf_name = os.path.splitext(document.name)[0] + '.pdf'
        doc_path = os.path.join(self.tmp_dir, pdf_name)
        pdf_document = open(doc_path, 'rb')
        text = self.pdf_parser.parse(pdf_document)
        return text

    def _docx_to_pdf(self, doc_name):
        filename = doc_name.replace(' ', '\ ')
        command = COMMAND.format(outdir=self.tmp_dir, filename=filename)
        process = Popen(command, cwd=self.tmp_dir, shell=True)
        process.communicate()
