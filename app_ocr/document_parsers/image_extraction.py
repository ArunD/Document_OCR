import cv2
import numpy as np
from PIL import Image
from pyocr import pyocr
import pyocr.builders
import sys

from app_ocr.document_parsers.converter import pdf_to_image


SHOW_IMAGES = False


def get_image_from_file(file, mimetype, dpi=200):
    pil_images = []
    cv_images = []
    if mimetype == 'application/pdf' or 'image' in mimetype:
        if mimetype == 'application/pdf':

            pil_images = pdf_to_image(pdf_path=file, dpi=dpi)

        else:
            # read file into pil image
            pil_images.append(Image.open(file))

        if len(pil_images) != 0:
            cv_images = list(map(lambda i: np.array(i), pil_images))
            # convert RGB to BGR
            cv_images = list(map(lambda i: i[:, :, ::-1].copy(), cv_images))
    return cv_images


def preprocess_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if SHOW_IMAGES:
        show_image("Original", image)

    # if noise removal is necessary
    # _, image = cv2.threshold(image, 170, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
    #
    # if SHOW_IMAGES:
    #     show_image("Threshold", image)

    return image


def get_text_from_image(images):
    text = []
    for i, img in enumerate(images):
        img = preprocess_image(img)

        tools = pyocr.get_available_tools()
        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            print("No OCR tool found")
            sys.exit(1)

        tool = tools[0]

        image_text = tool.image_to_string(
            Image.fromarray(img),
            lang='eng',
            builder=pyocr.builders.TextBuilder()
        )

        text.append(image_text)
    return text


def show_image(title, img):
    if img is not None:
        cv2.imshow(title, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
