from abc import ABC, abstractmethod
from typing import Optional, Union
from django.core.files.uploadedfile import UploadedFile
import io


class BaseTextExtractor(ABC):
    """
    Abstract base class for text extraction from various file types.
    All OCR extractors should inherit from this class.
    """

    def __init__(self):
        self.supported_mimetypes = []

    @abstractmethod
    def extract_text(self, file: Union[UploadedFile, io.BytesIO]) -> Optional[str]:
        """
        Extract text from the given file.
        
        Args:
            file: The file to extract text from
            
        Returns:
            str: Extracted text or None if extraction failed
        """
        pass

    @abstractmethod
    def supports_mimetype(self, mimetype: str) -> bool:
        """
        Check if this extractor supports the given mimetype.
        
        Args:
            mimetype: The MIME type to check
            
        Returns:
            bool: True if supported, False otherwise
        """
        pass

    def _ensure_file_position(self, file: Union[UploadedFile, io.BytesIO]) -> None:
        """
        Ensure the file pointer is at the beginning of the file.
        
        Args:
            file: The file to reset
        """
        try:
            file.seek(0)
        except (AttributeError, io.UnsupportedOperation):
            pass

    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text.
        
        Args:
            text: Raw extracted text
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = " ".join(text.split())
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text