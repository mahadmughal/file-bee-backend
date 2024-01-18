from PIL import Image
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

        if self.png_to_jpeg():
            image = image.convert('RGB')
            image.save(output_file_path, 'JPEG', quality=95)
        elif self.jpeg_to_bmp() or self.png_to_bmp():
            image = image.convert(mode="P", palette=Image.ADAPTIVE, colors=256)
            image = image.convert("RGB")
            image.save(output_file_path)
        elif self.jpeg_to_png():
            image.save(output_file_path, 'PNG')
        elif self.jpeg_to_webp() or self.png_to_webp():
            image.save(output_file_path, 'WEBP')
        elif self.webp_to_png():
            image = image.convert("RGB")
            image.save(output_file_path, 'PNG')
        elif self.webp_to_jpeg():
            image = image.convert("RGB")
            image.save(output_file_path, 'JPEG')
        elif self.webp_to_bmp():
            image = image.convert("RGB")
            image.save(output_file_path, 'BMP')

        return output_file_path

    def generate_output_path(self):
        # Get the directory part of the original file path
        file_directory = os.path.dirname(self.file.path)

        # Get the filename part of the original file path
        file_name = os.path.basename(self.file.path)

        # Construct the output file path in the same directory with a different extension
        return os.path.join(file_directory, file_name.split('.')[0] + '.' + self.target_mimetype.split('/')[-1]).replace('uploaded', 'converted')

    def png_to_jpeg(self):
        self.source_mimetype == 'image/png' and self.target_mimetype == 'image/jpeg'

    def png_to_bmp(self):
        self.source_mimetype == 'image/png' and self.target_mimetype == 'image/bmp'

    def png_to_webp(self):
        self.source_mimetype == 'image/png' and self.target_mimetype == 'image/webp'

    def jpeg_to_bmp(self):
        self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'image/bmp'

    def jpeg_to_png(self):
        self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'image/png'

    def jpeg_to_webp(self):
        self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'image/webp'

    def webp_to_png(self):
        self.source_mimetype == 'image/webp' and self.target_mimetype == 'image/png'

    def webp_to_jpeg(self):
        self.source_mimetype == 'image/webp' and self.target_mimetype == 'image/jpeg'

    def webp_to_bmp(self):
        self.source_mimetype == 'image/webp' and self.target_mimetype == 'image/bmp'



    # def generate_output_path(self):
        # return f"{self.file.path.split('.')[0]}.{self.target_mimetype.split('/')[-1]}".replace('uploaded', 'converted')

