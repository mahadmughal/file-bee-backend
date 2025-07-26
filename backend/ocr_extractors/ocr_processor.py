from typing import Optional, Union, List
from django.core.files.uploadedfile import UploadedFile
import io

from .base_extractor import BaseTextExtractor
from .pdf_extractor import PDFTextExtractor
from .image_extractor import ImageOCRExtractor
from .text_extractor import PlainTextExtractor


class OCRProcessor:
    """
    Main OCR processor that manages all text extractors and routes files
    to the appropriate extractor based on MIME type.
    """

    def __init__(self):
        self.extractors: List[BaseTextExtractor] = [
            PDFTextExtractor(),
            ImageOCRExtractor(),
            PlainTextExtractor(),
        ]

    def extract_text(self, file: Union[UploadedFile, io.BytesIO], mimetype: str) -> Optional[str]:
        """
        Extract text from file using the appropriate extractor.
        
        Args:
            file: The file to extract text from
            mimetype: The MIME type of the file
            
        Returns:
            str: Extracted text or None if extraction failed
        """
        try:
            extractor = self._get_extractor_for_mimetype(mimetype)
            
            if not extractor:
                print(f"No extractor found for MIME type: {mimetype}")
                return None
            
            return extractor.extract_text(file)
            
        except Exception as e:
            print(f"Error in OCR processing: {e}")
            return None

    def extract_text_with_details(self, file: Union[UploadedFile, io.BytesIO], mimetype: str) -> Optional[dict]:
        """
        Extract text with additional details when available.
        
        Args:
            file: The file to extract text from
            mimetype: The MIME type of the file
            
        Returns:
            dict: Detailed extraction results or None if extraction failed
        """
        try:
            extractor = self._get_extractor_for_mimetype(mimetype)
            
            if not extractor:
                print(f"No extractor found for MIME type: {mimetype}")
                return None
            
            # Check if extractor supports detailed extraction
            if hasattr(extractor, 'extract_text_with_details'):
                return extractor.extract_text_with_details(file)
            elif hasattr(extractor, 'extract_text_with_metadata'):
                return extractor.extract_text_with_metadata(file)
            else:
                # Fallback to basic text extraction
                text = extractor.extract_text(file)
                return {'text': text} if text else None
                
        except Exception as e:
            print(f"Error in detailed OCR processing: {e}")
            return None

    def get_supported_mimetypes(self) -> List[str]:
        """
        Get all supported MIME types across all extractors.
        
        Returns:
            list: List of supported MIME types
        """
        supported_types = []
        
        for extractor in self.extractors:
            supported_types.extend(extractor.supported_mimetypes)
        
        # Remove duplicates and return
        return list(set(supported_types))

    def is_mimetype_supported(self, mimetype: str) -> bool:
        """
        Check if the given MIME type is supported by any extractor.
        
        Args:
            mimetype: The MIME type to check
            
        Returns:
            bool: True if supported, False otherwise
        """
        return self._get_extractor_for_mimetype(mimetype) is not None

    def _get_extractor_for_mimetype(self, mimetype: str) -> Optional[BaseTextExtractor]:
        """
        Find the appropriate extractor for the given MIME type.
        
        Args:
            mimetype: The MIME type to find an extractor for
            
        Returns:
            BaseTextExtractor: The appropriate extractor or None if not found
        """
        for extractor in self.extractors:
            if extractor.supports_mimetype(mimetype):
                return extractor
        
        return None

    def add_extractor(self, extractor: BaseTextExtractor) -> None:
        """
        Add a new text extractor to the processor.
        
        Args:
            extractor: The extractor to add
        """
        if isinstance(extractor, BaseTextExtractor):
            self.extractors.append(extractor)
        else:
            raise TypeError("Extractor must inherit from BaseTextExtractor")

    def remove_extractor(self, extractor_class: type) -> bool:
        """
        Remove an extractor by class type.
        
        Args:
            extractor_class: The class of the extractor to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        for i, extractor in enumerate(self.extractors):
            if isinstance(extractor, extractor_class):
                self.extractors.pop(i)
                return True
        
        return False

    def get_extractor_info(self) -> List[dict]:
        """
        Get information about all loaded extractors.
        
        Returns:
            list: List of extractor information dictionaries
        """
        info = []
        
        for extractor in self.extractors:
            info.append({
                'name': extractor.__class__.__name__,
                'supported_mimetypes': extractor.supported_mimetypes,
                'has_detailed_extraction': hasattr(extractor, 'extract_text_with_details') or 
                                          hasattr(extractor, 'extract_text_with_metadata')
            })
        
        return info