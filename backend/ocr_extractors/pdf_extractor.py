import fitz  # PyMuPDF
from typing import Optional, Union
from django.core.files.uploadedfile import UploadedFile
import io

from .base_extractor import BaseTextExtractor


class PDFTextExtractor(BaseTextExtractor):
    """
    Text extractor for PDF files using PyMuPDF.
    """

    def __init__(self):
        super().__init__()
        self.supported_mimetypes = ['application/pdf']

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
        Extract text from PDF file using PyMuPDF.
        
        Args:
            file: The PDF file to extract text from
            
        Returns:
            str: Extracted text or None if extraction failed
        """
        try:
            self._ensure_file_position(file)
            
            # Open PDF document
            pdf_document = fitz.open(stream=file.read(), filetype="pdf")
            
            text_parts = []
            
            # Extract text from each page
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                page_text = page.get_text()
                
                if page_text.strip():
                    text_parts.append(page_text)
            
            # Close the document
            pdf_document.close()
            
            # Combine all text
            full_text = "\n".join(text_parts)
            
            # Clean and return text
            cleaned_text = self._clean_text(full_text)
            
            return cleaned_text if cleaned_text else None
            
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None

    def get_page_count(self, file: Union[UploadedFile, io.BytesIO]) -> int:
        """
        Get the number of pages in the PDF.
        
        Args:
            file: The PDF file
            
        Returns:
            int: Number of pages or 0 if error
        """
        try:
            self._ensure_file_position(file)
            pdf_document = fitz.open(stream=file.read(), filetype="pdf")
            page_count = pdf_document.page_count
            pdf_document.close()
            return page_count
        except Exception:
            return 0

    def extract_text_from_page(self, file: Union[UploadedFile, io.BytesIO], page_number: int) -> Optional[str]:
        """
        Extract text from a specific page of the PDF.
        
        Args:
            file: The PDF file
            page_number: The page number (0-indexed)
            
        Returns:
            str: Extracted text from the page or None if extraction failed
        """
        try:
            self._ensure_file_position(file)
            pdf_document = fitz.open(stream=file.read(), filetype="pdf")
            
            if page_number >= pdf_document.page_count or page_number < 0:
                pdf_document.close()
                return None
            
            page = pdf_document[page_number]
            page_text = page.get_text()
            pdf_document.close()
            
            cleaned_text = self._clean_text(page_text)
            return cleaned_text if cleaned_text else None
            
        except Exception as e:
            print(f"Error extracting text from PDF page {page_number}: {e}")
            return None