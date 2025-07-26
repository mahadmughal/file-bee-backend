from typing import Optional, Union
from django.core.files.uploadedfile import UploadedFile
import io
import chardet

from .base_extractor import BaseTextExtractor


class PlainTextExtractor(BaseTextExtractor):
    """
    Text extractor for plain text files and other text-based formats.
    """

    def __init__(self):
        super().__init__()
        self.supported_mimetypes = [
            'text/plain',
            'text/csv',
            'text/html',
            'text/xml',
            'application/xml',
            'text/markdown',
            'text/rtf',
            'application/rtf'
        ]

    def supports_mimetype(self, mimetype: str) -> bool:
        """
        Check if this extractor supports the given mimetype.
        
        Args:
            mimetype: The MIME type to check
            
        Returns:
            bool: True if supported, False otherwise
        """
        return mimetype in self.supported_mimetypes or mimetype.startswith('text/')

    def extract_text(self, file: Union[UploadedFile, io.BytesIO]) -> Optional[str]:
        """
        Extract text from plain text files with automatic encoding detection.
        
        Args:
            file: The text file to extract text from
            
        Returns:
            str: Extracted text or None if extraction failed
        """
        try:
            self._ensure_file_position(file)
            
            # Read file content as bytes
            file_content = file.read()
            
            if not file_content:
                return None
            
            # Detect encoding
            encoding = self._detect_encoding(file_content)
            
            # Decode content
            try:
                text = file_content.decode(encoding)
            except UnicodeDecodeError:
                # Fallback to utf-8 with error handling
                text = file_content.decode('utf-8', errors='replace')
            
            # Clean and return text
            cleaned_text = self._clean_text(text)
            return cleaned_text if cleaned_text else None
            
        except Exception as e:
            print(f"Error extracting text from file: {e}")
            return None

    def _detect_encoding(self, file_content: bytes) -> str:
        """
        Detect file encoding using chardet library.
        
        Args:
            file_content: Raw file content as bytes
            
        Returns:
            str: Detected encoding or 'utf-8' as fallback
        """
        try:
            # Use chardet to detect encoding
            result = chardet.detect(file_content)
            
            if result and result['encoding']:
                # Use detected encoding if confidence is reasonable
                if result['confidence'] > 0.7:
                    return result['encoding']
            
            # Common encoding fallbacks
            encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings_to_try:
                try:
                    file_content.decode(encoding)
                    return encoding
                except UnicodeDecodeError:
                    continue
            
            # Final fallback
            return 'utf-8'
            
        except Exception:
            return 'utf-8'

    def extract_text_with_metadata(self, file: Union[UploadedFile, io.BytesIO]) -> Optional[dict]:
        """
        Extract text along with metadata like encoding and file stats.
        
        Args:
            file: The text file to extract text from
            
        Returns:
            dict: Text and metadata or None if extraction failed
        """
        try:
            self._ensure_file_position(file)
            file_content = file.read()
            
            if not file_content:
                return None
            
            # Detect encoding
            encoding_info = chardet.detect(file_content)
            used_encoding = encoding_info['encoding'] if encoding_info['confidence'] > 0.7 else 'utf-8'
            
            # Decode content
            try:
                text = file_content.decode(used_encoding)
            except UnicodeDecodeError:
                text = file_content.decode('utf-8', errors='replace')
                used_encoding = 'utf-8 (with error handling)'
            
            # Clean text
            cleaned_text = self._clean_text(text)
            
            return {
                'text': cleaned_text,
                'encoding': used_encoding,
                'encoding_confidence': encoding_info.get('confidence', 0) if encoding_info else 0,
                'size_bytes': len(file_content),
                'size_characters': len(text),
                'line_count': len(text.splitlines()),
                'word_count': len(text.split())
            } if cleaned_text else None
            
        except Exception as e:
            print(f"Error extracting text with metadata: {e}")
            return None