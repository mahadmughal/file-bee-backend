from PIL import Image
from reportlab.pdfgen import canvas
from pdf2docx import Converter
import fitz  # PyMuPDF
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import subprocess
import os


class DocumentConverter:
    def __init__(self, source_mimetype, target_mimetype, file):
        self.file = file
        self.source_mimetype = source_mimetype
        self.target_mimetype = target_mimetype

    def convert(self):
        if self.is_pdf_to_docx():
            output_file_path = self.generate_output_file_path('docx')
            self.convert_pdf_to_docx(self.file.name, output_file_path)
            return output_file_path
        elif self.is_pdf_to_doc():
            output_file_path = self.generate_output_file_path('docx')
            self.convert_pdf_to_doc(self.file.name, output_file_path)
            return output_file_path
        elif self.is_docx_to_pdf():
            output_file_path = self.generate_output_file_path('pdf')
            self.convert_docx_to_pdf(self.file.name, output_file_path)
            return output_file_path

    def convert_pdf_to_doc(self, pdf_path, doc_path):
        # Step 1: Extract text from PDF
        pdf_document = fitz.open(pdf_path)
        text = ""
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text += page.get_text()

        # Step 2: Create DOC file using python-docx
        doc = Document()
        doc.add_paragraph(text)

        # Save the DOC file
        doc.save(doc_path)

    def convert_docx_to_pdf(self, docx_path, pdf_path):
        try:
            subprocess.run(['unoconv', '-f', 'pdf', '-o', pdf_path, docx_path])
            print(f"Conversion successful. PDF saved at: {pdf_path}")
        except Exception as e:
            print(f"Error converting file: {e}")

    def convert_pdf_to_docx(self, pdf_path, docx_path):
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()

    def generate_output_file_path(self, target_extension=None):
        # Get the directory part of the original file path
        file_directory = os.path.dirname(self.file.name)

        # Get the filename part of the original file path
        file_name = os.path.basename(self.file.path)
        target_extension = target_extension if target_extension else self.target_mimetype.split(
            '/')[-1]

        # Construct the output file path in the same directory with a different extension
        return (file_directory + '/' + file_name.split('.')[0] + '.' + target_extension).replace('uploaded', 'converted')

    def is_pdf_to_docx(self):
        return self.source_mimetype == 'application/pdf' and self.target_mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    def is_pdf_to_doc(self):
        return self.source_mimetype == 'application/pdf' and self.target_mimetype == 'application/msword'

    def is_docx_to_pdf(self):
        return self.source_mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' and self.target_mimetype == 'application/pdf'
