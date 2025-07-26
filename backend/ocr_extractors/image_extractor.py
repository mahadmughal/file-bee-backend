import pytesseract
from PIL import Image
from typing import Optional, Union, List, Dict
from django.core.files.uploadedfile import UploadedFile
import io

from .base_extractor import BaseTextExtractor


class ImageOCRExtractor(BaseTextExtractor):
    """
    OCR text extractor for image files using Tesseract OCR.
    """

    def __init__(self):
        super().__init__()
        self.supported_mimetypes = [
            'image/jpeg',
            'image/jpg', 
            'image/png',
            'image/gif',
            'image/bmp',
            'image/tiff',
            'image/webp'
        ]
        
        # OCR configuration options for different scenarios
        self.ocr_configs = [
            ('--oem 3 --psm 6', 'Uniform block of text'),
            ('--oem 3 --psm 3', 'Fully automatic page segmentation'),
            ('--oem 3 --psm 1', 'Automatic page segmentation with OSD'),
            ('--oem 3 --psm 8', 'Single word'),
            ('--oem 3 --psm 7', 'Single text line'),
            ('--oem 3 --psm 4', 'Single column of text'),
        ]

    def supports_mimetype(self, mimetype: str) -> bool:
        """
        Check if this extractor supports the given mimetype.
        
        Args:
            mimetype: The MIME type to check
            
        Returns:
            bool: True if supported, False otherwise
        """
        return mimetype in self.supported_mimetypes

    def extract_text(self, file: Union[UploadedFile, io.BytesIO]) -> Optional[str]:
        """
        Extract text from image file using OCR with multiple configurations.
        
        Args:
            file: The image file to extract text from
            
        Returns:
            str: Extracted text or None if extraction failed
        """
        try:
            self._ensure_file_position(file)
            
            # Open and process the image
            image = Image.open(file)
            
            # Convert image to RGB if it's not already (required for some formats)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Try multiple OCR configurations for better results
            best_result = self._extract_with_multiple_configs(image)
            
            if best_result and best_result['text']:
                return self._clean_text(best_result['text'])
            
            return None
            
        except pytesseract.TesseractNotFoundError:
            print("Tesseract OCR not found. Please install Tesseract OCR.")
            return None
        except Exception as e:
            print(f"Error extracting text from image: {e}")
            return None

    def _extract_with_multiple_configs(self, image: Image.Image) -> Optional[Dict]:
        """
        Try multiple OCR configurations and return the best result.
        
        Args:
            image: PIL Image object
            
        Returns:
            dict: Best OCR result with text and confidence
        """
        best_result = {'text': '', 'confidence': 0, 'config': ''}
        
        for config, description in self.ocr_configs:
            try:
                # Extract text with current config
                text = pytesseract.image_to_string(image, config=config)
                text = text.strip()
                
                if text:
                    # Get confidence for this result
                    confidence = self._get_confidence(image, config)
                    
                    # Use result with highest confidence and reasonable length
                    if (confidence > best_result['confidence'] and 
                        len(text) > len(best_result['text']) * 0.8):
                        best_result = {
                            'text': text,
                            'confidence': confidence,
                            'config': config
                        }
                        
            except Exception as e:
                print(f"OCR config '{config}' failed: {e}")
                continue
        
        return best_result if best_result['text'] else None

    def _get_confidence(self, image: Image.Image, config: str) -> float:
        """
        Get confidence score for OCR result.
        
        Args:
            image: PIL Image object
            config: OCR configuration string
            
        Returns:
            float: Average confidence score
        """
        try:
            data = pytesseract.image_to_data(
                image, 
                config=config, 
                output_type=pytesseract.Output.DICT
            )
            
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            
            if confidences:
                return sum(confidences) / len(confidences)
            else:
                return 0.0
                
        except Exception:
            return 0.0

    def extract_text_with_details(self, file: Union[UploadedFile, io.BytesIO]) -> Optional[Dict]:
        """
        Extract text with additional details like confidence and bounding boxes.
        
        Args:
            file: The image file to extract text from
            
        Returns:
            dict: Detailed OCR results or None if extraction failed
        """
        try:
            self._ensure_file_position(file)
            image = Image.open(file)
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Use the best configuration found
            best_result = self._extract_with_multiple_configs(image)
            
            if not best_result:
                return None
            
            # Get detailed data using the best config
            data = pytesseract.image_to_data(
                image, 
                config=best_result['config'], 
                output_type=pytesseract.Output.DICT
            )
            
            return {
                'text': self._clean_text(best_result['text']),
                'confidence': best_result['confidence'],
                'config_used': best_result['config'],
                'word_details': self._extract_word_details(data)
            }
            
        except Exception as e:
            print(f"Error extracting detailed text from image: {e}")
            return None

    def _extract_word_details(self, data: Dict) -> List[Dict]:
        """
        Extract detailed information about each detected word.
        
        Args:
            data: Tesseract output data dictionary
            
        Returns:
            list: List of word details with bounding boxes and confidence
        """
        word_details = []
        
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 0:  # Only include words with confidence > 0
                word_details.append({
                    'text': data['text'][i],
                    'confidence': int(data['conf'][i]),
                    'left': int(data['left'][i]),
                    'top': int(data['top'][i]),
                    'width': int(data['width'][i]),
                    'height': int(data['height'][i])
                })
        
        return word_details

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR results.
        This can be extended with more sophisticated image processing.
        
        Args:
            image: PIL Image object
            
        Returns:
            Image.Image: Preprocessed image
        """
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Additional preprocessing can be added here:
        # - Resize for better resolution
        # - Grayscale conversion
        # - Noise reduction
        # - Contrast enhancement
        # - Deskewing
        
        return image