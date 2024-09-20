from django.core.files.base import ContentFile
from backend.utils.s3_utils import s3_client
from pdf2docx import Converter
import fitz  # PyMuPDF
from docx import Document
from io import BytesIO
import tempfile
import subprocess
import os


class DocumentConverter:
    def __init__(self, source_mimetype, target_mimetype, file):
        self.file = file
        self.source_mimetype = source_mimetype
        self.target_mimetype = target_mimetype

    def convert(self):
        file_object = self.get_doc_from_s3()

        if self.is_pdf_to_docx():
            output = self.convert_pdf_to_docx(file_object)
        elif self.is_pdf_to_doc():
            output = self.convert_pdf_to_doc(file_object)
        # elif self.is_docx_to_pdf():
        #     output = self.convert_docx_to_pdf(file_object)

        return ContentFile(output)

    def convert_pdf_to_doc(self, pdf_file):
        pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text += page.get_text()

        doc = Document()
        doc.add_paragraph(text)

        doc_buffer = BytesIO()
        doc.save(doc_buffer)

        doc_content = doc_buffer.getvalue()
        doc_buffer.close()

        return doc_content

    # TODO: not functional, have to rectify this method.
    def convert_docx_to_pdf(self, doc_object):
        try:
            subprocess.run(['unoconv', '-f', 'pdf', '-o', pdf_path, docx_path])
            print(f"Conversion successful. PDF saved at: {pdf_path}")
        except Exception as e:
            print(f"Error converting file: {e}")

    def convert_pdf_to_docx(self, pdf_file_object):
        # Create temporary files for input and output
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf_file, \
                tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_docx_file:

            # Write the contents of pdf_file_object to the temporary PDF file
            pdf_file_object.seek(0)
            temp_pdf_file.write(pdf_file_object.read())
            temp_pdf_file.close()

            try:
                # Convert PDF to DOCX
                cv = Converter(temp_pdf_file.name)
                cv.convert(temp_docx_file.name)
                cv.close()

                # Read the contents of the DOCX file
                with open(temp_docx_file.name, 'rb') as docx_file:
                    docx_content = docx_file.read()

                return docx_content

            except Exception as e:
                print(f"Error converting PDF to DOCX: {e}")
                return None

            finally:
                # Clean up temporary files
                os.unlink(temp_pdf_file.name)
                os.unlink(temp_docx_file.name)

    def get_doc_from_s3(self):
        file_content = s3_client.get_object(self.file.name)
        file_object = BytesIO(file_content)
        file_object.name = os.path.basename(os.path.basename(self.file.name))
        file_object.seek(0)

        return file_object

    # TODO: not functional, have to confirm whether to remove this method.
    def generate_output_file_path(self, target_extension=None):
        file_directory = os.path.dirname(self.file.name)
        file_name = os.path.basename(self.file.name)
        target_extension = target_extension if target_extension else self.target_mimetype.split(
            '/')[-1]

        return (file_directory + '/' + file_name.split('.')[0] + '.' + target_extension).replace('uploaded', 'converted')

    def is_pdf_to_docx(self):
        return self.source_mimetype == 'application/pdf' and self.target_mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    def is_pdf_to_doc(self):
        return self.source_mimetype == 'application/pdf' and self.target_mimetype == 'application/msword'

    def is_docx_to_pdf(self):
        return self.source_mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' and self.target_mimetype == 'application/pdf'
