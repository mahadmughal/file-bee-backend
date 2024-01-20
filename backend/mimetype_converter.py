from PIL import Image
from reportlab.pdfgen import canvas
import os
import pdb

class MimetypeConverter:
    def __init__(self, source_mimetype, target_mimetype, file):
        self.source_mimetype = source_mimetype
        self.target_mimetype = target_mimetype
        self.file = file

    def convert(self):
        image = Image.open(self.file.name)
        output_file_path = self.generate_output_path()

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
        elif self.is_png_to_pdf():
            self.convert_image_to_pdf(image, output_file_path)
        elif self.is_jpeg_to_pdf():
            self.convert_image_to_pdf(image, output_file_path)
        elif self.is_webp_to_pdf():
            self.convert_image_to_pdf(image, output_file_path)

        return output_file_path

    def generate_output_path(self):
        # Get the directory part of the original file path
        file_directory = os.path.dirname(self.file.path)

        # Get the filename part of the original file path
        file_name = os.path.basename(self.file.path)

        # Construct the output file path in the same directory with a different extension
        return os.path.join(file_directory, file_name.split('.')[0] + '.' + self.target_mimetype.split('/')[-1]).replace('uploaded', 'converted')

    def is_png_to_jpeg(self):
        return self.source_mimetype == 'image/png' and self.target_mimetype == 'image/jpeg'

    def is_png_to_bmp(self):
        return self.source_mimetype == 'image/png' and self.target_mimetype == 'image/bmp'

    def is_png_to_webp(self):
        return self.source_mimetype == 'image/png' and self.target_mimetype == 'image/webp'

    def is_jpeg_to_bmp(self):
        return self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'image/bmp'

    def is_jpeg_to_png(self):
        return self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'image/png'

    def is_jpeg_to_webp(self):
        return self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'image/webp'

    def is_webp_to_png(self):
        return self.source_mimetype == 'image/webp' and self.target_mimetype == 'image/png'

    def is_webp_to_jpeg(self):
        return self.source_mimetype == 'image/webp' and self.target_mimetype == 'image/jpeg'

    def is_webp_to_bmp(self):
        return self.source_mimetype == 'image/webp' and self.target_mimetype == 'image/bmp'

    def is_png_to_pdf(self):
        return self.source_mimetype == 'image/png' and self.target_mimetype == 'application/pdf'

    def is_jpeg_to_pdf(self):
        return self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'application/pdf'

    def is_webp_to_pdf(self):
        return self.source_mimetype == 'image/webp' and self.target_mimetype == 'application/pdf'

    def convert_image_to_pdf(self, input_image, output_file_path):
        print('converting png image to pdf file ...')
        pdf_canvas = canvas.Canvas(output_file_path, pagesize=input_image.size)
        pdf_canvas.drawInlineImage(self.file.name, 0, 0, width=input_image.width, height=input_image.height)
        pdf_canvas.save()



    # def generate_output_path(self):
        # return f"{self.file.path.split('.')[0]}.{self.target_mimetype.split('/')[-1]}".replace('uploaded', 'converted')

