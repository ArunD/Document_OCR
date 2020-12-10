import cv2
import numpy as np
from PIL import Image

from app_ocr.document_parsers.image_extraction import (get_image_from_file,
                                                       get_text_from_image)


class ImageParser:

    def parse(self, document):
        img = Image.open(document)
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        text = get_text_from_image([img])
        return text[0]
