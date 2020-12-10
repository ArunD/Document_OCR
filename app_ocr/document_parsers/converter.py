import os
import subprocess
from pdf2image import convert_from_path


def pdf_to_image(pdf_path, image_path=None, dpi=200):
    return convert_from_path(pdf_path=pdf_path, dpi=dpi, output_folder=image_path, fmt='jpg')


def convert_office_to_pdf(office_path, pdf_path=None):
    cmd = ["libreoffice", "--headless", "--convert-to", "pdf", office_path]
    if pdf_path is not None:
        cmd += ["--outdir", pdf_path]
        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait(timeout=10)
    stdout, stderr = p.communicate()
    if stderr:
        print("Libre Office error: {}".format(stderr))
