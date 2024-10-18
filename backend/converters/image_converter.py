from PIL import Image
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.files.base import ContentFile
from backend.utils.s3_utils import s3_client
from docx import Document
from docx.shared import Inches
from reportlab.lib.utils import ImageReader


class ImageConverter:
    def __init__(self, source_mimetype, target_mimetype, file):
        self.file = file
        self.source_mimetype = source_mimetype
        self.target_mimetype = target_mimetype

    def convert(self):
        image = self.get_image_from_s3()
        output = BytesIO()

        if self.is_png_to_jpeg():
            image = image.convert('RGB')
            image.save(output, 'JPEG', quality=95)
        elif self.is_jpeg_to_bmp() or self.is_png_to_bmp():
            image = image.convert(mode="P", palette=Image.ADAPTIVE, colors=256)
            image = image.convert("RGB")
            image.save(output, 'BMP')
        elif self.is_jpeg_to_png():
            image.save(output, 'PNG')
        elif self.is_jpeg_to_webp() or self.is_png_to_webp():
            image.save(output, 'WEBP')
        elif self.is_webp_to_png():
            image = image.convert("RGB")
            image.save(output, 'PNG')
        elif self.is_webp_to_jpeg():
            image = image.convert("RGB")
            image.save(output, 'JPEG')
        elif self.is_webp_to_bmp():
            image = image.convert("RGB")
            image.save(output, 'BMP')
        elif self.is_gif_to_png():
            image.save(output, 'PNG')
        elif self.is_gif_to_jpeg():
            image = image.convert("RGB")
            image.save(output, 'JPEG')
        elif self.is_gif_to_webp():
            image.save(output, 'WEBP')
        elif self.is_gif_to_bmp():
            image.save(output, 'BMP')
        elif self.is_gif_to_pdf():
            output = self.convert_gif_to_pdf(image)
        elif self.is_png_to_pdf():
            output = self.convert_image_to_pdf(image)
        elif self.is_jpeg_to_pdf():
            output = self.convert_image_to_pdf(image)
        elif self.is_webp_to_pdf():
            output = self.convert_image_to_pdf(image)
        elif self.is_png_to_doc() or self.is_png_to_docx():
            output = self.convert_image_to_document(image, 'PNG')
        elif self.is_jpeg_to_doc() or self.is_jpeg_to_docx():
            output = self.convert_image_to_document(image, 'JPEG')
        elif self.is_webp_to_doc() or self.is_webp_to_docx():
            input_image = self.convert_webp_to_png(image)
            output = self.convert_image_to_document(input_image, 'PNG')

        return ContentFile(output.getvalue())

    def convert_webp_to_png(self, input_image):
        png_image = BytesIO()
        input_image.save(png_image, format='PNG')
        png_image.seek(0)
        input_image = Image.open(png_image)

        return input_image

    def convert_image_to_pdf(self, input_image):
        print('Converting image to PDF...')
        buffer = BytesIO()
        pdf_canvas = canvas.Canvas(buffer, pagesize=input_image.size)
        pdf_canvas.drawInlineImage(
            input_image, 0, 0, width=input_image.width, height=input_image.height)
        pdf_canvas.save()

        return buffer

    def convert_image_to_document(self, input_image, input_image_extension):
        doc = Document()

        width, height = input_image.size
        aspect_ratio = width / height

        max_width = Inches(6)

        doc_width = max_width
        doc_height = max_width / aspect_ratio

        byte_stream = BytesIO()
        input_image.save(byte_stream, format=input_image_extension)
        byte_stream.seek(0)

        doc.add_picture(byte_stream, width=doc_width, height=doc_height)
        doc_stream = BytesIO()
        doc.save(doc_stream)
        doc_stream.seek(0)

        return doc_stream

    def convert_gif_to_pdf(self, input_image):
        width, height = input_image.size

        # Create a new PDF with ReportLab
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=(width, height))

        # Loop over all frames in the GIF
        for frame in range(0, input_image.n_frames):
            input_image.seek(frame)
            # Convert each frame to RGB (PDF doesn't support transparency)
            rgb_frame = Image.new('RGB', input_image.size, (255, 255, 255))
            rgb_frame.paste(input_image, (0, 0),
                            input_image.convert('RGBA'))

            # Save the frame as a temporary PNG
            temp_buffer = BytesIO()
            rgb_frame.save(temp_buffer, format='PNG')
            temp_buffer.seek(0)

            # Add the frame to the PDF
            img_reader = ImageReader(temp_buffer)
            c.drawImage(img_reader, 0, 0, width, height)
            c.showPage()

        c.save()

        pdf_buffer.seek(0)

        return pdf_buffer

    def get_image_from_s3(self):
        file_content = s3_client.get_object(self.file.name)

        return Image.open(BytesIO(file_content))

    def is_png_to_jpeg(self):
        return self.source_mimetype == 'image/png' and self.target_mimetype == 'image/jpeg'

    def is_png_to_bmp(self):
        return self.source_mimetype == 'image/png' and self.target_mimetype == 'image/bmp'

    def is_png_to_webp(self):
        return self.source_mimetype == 'image/png' and self.target_mimetype == 'image/webp'

    def is_png_to_pdf(self):
        return self.source_mimetype == 'image/png' and self.target_mimetype == 'application/pdf'

    def is_png_to_doc(self):
        return self.source_mimetype == 'image/png' and self.target_mimetype == 'application/msword'

    def is_png_to_docx(self):
        return self.source_mimetype == 'image/png' and self.target_mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    def is_jpeg_to_bmp(self):
        return self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'image/bmp'

    def is_jpeg_to_png(self):
        return self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'image/png'

    def is_jpeg_to_webp(self):
        return self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'image/webp'

    def is_jpeg_to_pdf(self):
        return self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'application/pdf'

    def is_jpeg_to_doc(self):
        return self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'application/msword'

    def is_jpeg_to_docx(self):
        return self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    def is_webp_to_png(self):
        return self.source_mimetype == 'image/webp' and self.target_mimetype == 'image/png'

    def is_webp_to_jpeg(self):
        return self.source_mimetype == 'image/webp' and self.target_mimetype == 'image/jpeg'

    def is_webp_to_bmp(self):
        return self.source_mimetype == 'image/webp' and self.target_mimetype == 'image/bmp'

    def is_webp_to_pdf(self):
        return self.source_mimetype == 'image/webp' and self.target_mimetype == 'application/pdf'

    def is_webp_to_doc(self):
        return self.source_mimetype == 'image/webp' and self.target_mimetype == 'application/msword'

    def is_webp_to_docx(self):
        return self.source_mimetype == 'image/webp' and self.target_mimetype == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

    def is_gif_to_png(self):
        return self.source_mimetype == 'image/gif' and self.target_mimetype == 'image/png'

    def is_gif_to_jpeg(self):
        return self.source_mimetype == 'image/gif' and self.target_mimetype == 'image/jpeg'

    def is_gif_to_webp(self):
        return self.source_mimetype == 'image/gif' and self.target_mimetype == 'image/webp'

    def is_gif_to_bmp(self):
        return self.source_mimetype == 'image/gif' and self.target_mimetype == 'image/bmp'

    def is_gif_to_pdf(self):
        return self.source_mimetype == 'image/gif' and self.target_mimetype == 'application/pdf'
