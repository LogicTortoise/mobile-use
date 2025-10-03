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
                # Note: Using older-style API without document preprocessor
                cls._ocr_model = PaddleOCR(
                    lang='ch'  # Chinese + English support
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
            # Note: cls parameter is handled via use_angle_cls in initialization
            result = ocr_model.ocr(image)

            # Extract text - handle different result formats
            if result:
                # PaddleOCR 3.2+ returns a list with dict containing 'rec_texts'
                # For single image, use first element
                page_result = result[0] if isinstance(result, list) and len(result) > 0 else result

                # New format: dict with 'rec_texts' key
                if isinstance(page_result, dict) and 'rec_texts' in page_result:
                    texts = page_result['rec_texts']
                    if texts:
                        text = ' '.join(str(t) for t in texts)
                        return text
                # Old format: list of [bbox, (text, confidence)]
                elif page_result and isinstance(page_result, list):
                    texts = []
                    for line in page_result:
                        if line and len(line) > 1 and isinstance(line[1], (list, tuple)):
                            texts.append(str(line[1][0]))

                    if texts:
                        text = ' '.join(texts)
                        return text

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
