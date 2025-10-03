"""OCR functionality using PaddleOCR"""
import numpy as np
from module.logger import logger
from module.base.utils import crop


class OCR:
    """OCR text recognition"""

    _ocr_model = None

    @classmethod
    def _init_ocr(cls):
        """Initialize PaddleOCR model (lazy loading)"""
        if cls._ocr_model is None:
            try:
                from paddleocr import PaddleOCR
                logger.info('Initializing PaddleOCR model...')
                # Suppress PaddleOCR logging
                import logging as paddle_logging
                paddle_logging.getLogger('ppocr').setLevel(paddle_logging.ERROR)

                # Initialize PaddleOCR with compatible parameters
                cls._ocr_model = PaddleOCR(
                    use_angle_cls=True,
                    lang='en'
                )
                logger.info('PaddleOCR initialized successfully')
            except Exception as e:
                logger.error(f'Failed to initialize PaddleOCR: {e}')
                raise

        return cls._ocr_model

    def __init__(self, area=None):
        """
        Initialize OCR

        Args:
            area (tuple): Area to perform OCR on (x1, y1, x2, y2)
        """
        self.area = area

    def ocr(self, image, area=None):
        """
        Perform OCR on image

        Args:
            image (np.ndarray): Image to perform OCR on
            area (tuple): Area to crop before OCR (x1, y1, x2, y2)

        Returns:
            str: Recognized text
        """
        # Use specified area or default area
        if area is None:
            area = self.area

        # Crop image if area specified
        if area is not None:
            image = crop(image, area)

        # Initialize OCR model
        ocr_model = self._init_ocr()

        # Perform OCR
        try:
            result = ocr_model.ocr(image, cls=True)

            # Extract text
            if result and result[0]:
                texts = [line[1][0] for line in result[0]]
                text = ' '.join(texts)
                return text
            else:
                return ''
        except Exception as e:
            logger.warning(f'OCR failed: {e}')
            return ''

    def ocr_single_line(self, image, area=None):
        """
        Perform OCR expecting single line of text

        Args:
            image (np.ndarray): Image to perform OCR on
            area (tuple): Area to crop before OCR

        Returns:
            str: Recognized text (single line)
        """
        text = self.ocr(image, area)
        # Return first line if multiple lines detected
        if '\n' in text:
            text = text.split('\n')[0]
        return text.strip()
