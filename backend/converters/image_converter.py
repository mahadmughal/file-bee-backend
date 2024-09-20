from PIL import Image
from reportlab.pdfgen import canvas
import os
from io import BytesIO
from django.core.files.base import ContentFile
from backend.utils.s3_utils import s3_client


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
            image.save(output)
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
        elif self.is_png_to_pdf():
            output = self.convert_image_to_pdf(image)
        elif self.is_jpeg_to_pdf():
            output = self.convert_image_to_pdf(image)
        elif self.is_webp_to_pdf():
            output = self.convert_image_to_pdf(image)

        return ContentFile(output.getvalue())

    def convert_image_to_pdf(self, input_image):
        print('Converting image to PDF...')
        buffer = BytesIO()
        pdf_canvas = canvas.Canvas(buffer, pagesize=input_image.size)
        pdf_canvas.drawInlineImage(
            input_image, 0, 0, width=input_image.width, height=input_image.height)
        pdf_canvas.save()

        return buffer

    # TODO: not functional, have to confirm whether to remove this method.
    def generate_output_file_path(self, target_extension=None):
        file_directory = os.path.dirname(self.file.name)
        file_name = os.path.basename(self.file.name)
        target_extension = target_extension if target_extension else self.target_mimetype.split(
            '/')[-1]

        return (file_directory + '/' + file_name.split('.')[0] + '.' + target_extension).replace('uploaded', 'converted')

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
