from PIL import Image
from reportlab.pdfgen import canvas
from pdf2docx import Converter
import fitz  # PyMuPDF
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import subprocess
import os
import pdb

class MimetypeConverter:
    def __init__(self, source_mimetype, target_mimetype, file):
        self.source_mimetype = source_mimetype
        self.target_mimetype = target_mimetype
        self.file = file

    def convert(self):
        if self.source_mimetype.startswith("image"):
            return self.convert_image()
        else:
            return self.convert_file()

    def convert_image(self):
        image = Image.open(self.file.name)
        output_file_path = self.generate_output_file_path()

        if self.is_png_to_jpeg():
            image = image.convert('RGB')
            image.save(output_file_path, 'JPEG', quality=95)
        elif self.is_jpeg_to_bmp() or self.is_png_to_bmp():
            image = image.convert(mode="P", palette=Image.ADAPTIVE, colors=256)
            image = image.convert("RGB")
            image.save(output_file_path)
        elif self.is_jpeg_to_png():
            image.save(output_file_path, 'PNG')
        elif self.is_jpeg_to_webp() or self.is_png_to_webp():
            image.save(output_file_path, 'WEBP')
        elif self.is_webp_to_png():
            image = image.convert("RGB")
            image.save(output_file_path, 'PNG')
        elif self.is_webp_to_jpeg():
            image = image.convert("RGB")
            image.save(output_file_path, 'JPEG')
        elif self.is_webp_to_bmp():
            image = image.convert("RGB")
            image.save(output_file_path, 'BMP')
        elif self.is_gif_to_png():
            image.save(output_file_path, 'PNG')
        elif self.is_gif_to_jpeg():
            image = image.convert("RGB")
            image.save(output_file_path, 'JPEG')
        elif self.is_gif_to_webp():
            image.save(output_file_path, 'WEBP')
        elif self.is_gif_to_bmp():
            image.save(output_file_path, 'BMP')
        elif self.is_png_to_pdf():
            self.convert_image_to_pdf(image, output_file_path)
        elif self.is_jpeg_to_pdf():
            self.convert_image_to_pdf(image, output_file_path)
        elif self.is_webp_to_pdf():
            self.convert_image_to_pdf(image, output_file_path)

        return output_file_path

    def convert_file(self):
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


    def generate_output_file_path(self, target_extension=None):
        # Get the directory part of the original file path
        file_directory = os.path.dirname(self.file.name)

        # Get the filename part of the original file path
        file_name = os.path.basename(self.file.path)
        target_extension = target_extension if target_extension else self.target_mimetype.split('/')[-1]

        # Construct the output file path in the same directory with a different extension
        return (file_directory + '/' + file_name.split('.')[0] + '.' + target_extension).replace('uploaded', 'converted')

    def is_png_to_jpeg(self):
        return self.source_mimetype == 'image/png' and self.target_mimetype == 'image/jpeg'

    def is_png_to_bmp(self):
        return self.source_mimetype == 'image/png' and self.target_mimetype == 'image/bmp'

    def is_png_to_webp(self):
        return self.source_mimetype == 'image/png' and self.target_mimetype == 'image/webp'

    def is_png_to_pdf(self):
        return self.source_mimetype == 'image/png' and self.target_mimetype == 'application/pdf'

    def is_jpeg_to_bmp(self):
        return self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'image/bmp'

    def is_jpeg_to_png(self):
        return self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'image/png'

    def is_jpeg_to_webp(self):
        return self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'image/webp'

    def is_jpeg_to_pdf(self):
        return self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'application/pdf'

    def is_webp_to_png(self):
        return self.source_mimetype == 'image/webp' and self.target_mimetype == 'image/png'

    def is_webp_to_jpeg(self):
        return self.source_mimetype == 'image/webp' and self.target_mimetype == 'image/jpeg'

    def is_webp_to_bmp(self):
        return self.source_mimetype == 'image/webp' and self.target_mimetype == 'image/bmp'

    def is_webp_to_pdf(self):
        return self.source_mimetype == 'image/webp' and self.target_mimetype == 'application/pdf'

    def is_gif_to_png(self):
        return self.source_mimetype == 'image/gif' and self.target_mimetype == 'image/png'

    def is_gif_to_jpeg(self):
        return self.source_mimetype == 'image/gif' and self.target_mimetype == 'image/jpeg'

    def is_gif_to_webp(self):
        return self.source_mimetype == 'image/gif' and self.target_mimetype == 'image/webp'

    def is_gif_to_bmp(self):
        return self.source_mimetype == 'image/gif' and self.target_mimetype == 'image/bmp'

    def is_pdf_to_docx(self):
        return self.source_mimetype == 'application/pdf' and self.target_mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    def is_pdf_to_doc(self):
        return self.source_mimetype == 'application/pdf' and self.target_mimetype == 'application/msword'

    def is_docx_to_pdf(self):
        return self.source_mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' and self.target_mimetype == 'application/pdf'

    def convert_image_to_pdf(self, input_image, output_file_path):
        print('converting png image to pdf file ...')
        pdf_canvas = canvas.Canvas(output_file_path, pagesize=input_image.size)
        pdf_canvas.drawInlineImage(self.file.name, 0, 0, width=input_image.width, height=input_image.height)
        pdf_canvas.save()

    def convert_pdf_to_docx(self, pdf_path, docx_path):
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()

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








    # def generate_output_file_path(self):
        # return f"{self.file.path.split('.')[0]}.{self.target_mimetype.split('/')[-1]}".replace('uploaded', 'converted')

