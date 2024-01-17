from PIL import Image
import cv2

class MimetypeConverter:
    def __init__(self, source_mimetype, target_mimetype, file):
        self.source_mimetype = source_mimetype
        self.target_mimetype = target_mimetype
        self.file = file

    def convert(self):
        image = Image.open(self.file.path)
        output_file_path = self.generate_output_path()

        if self.source_mimetype == 'image/png' and self.target_mimetype == 'image/jpeg':
            image = image.convert('RGB')
            image.save(output_file_path, 'JPEG', quality=95)
        elif (self.source_mimetype == 'image/jpeg' or self.source_mimetype == 'image/png') and self.target_mimetype == 'image/bmp':
            image = image.convert(mode="P", palette=Image.ADAPTIVE, colors=256)
            image = image.convert("RGB")
            image.save(output_file_path)
        elif self.source_mimetype == 'image/jpeg' and self.target_mimetype == 'image/png':
            image.save(output_file_path, 'PNG')
        elif (self.source_mimetype == 'image/jpeg' or self.source_mimetype == 'image/png') and self.target_mimetype == 'image/webp':
            image.save(output_file_path, 'WEBP')

        return output_file_path

    def generate_output_path(self):
        return f"{self.file.name.split('.')[0]}.{self.target_mimetype.split('/')[1]}".replace('uploaded', 'converted')

# Example usage:
# source_mimetype = 'image/png'
# target_mimetype = 'image/jpeg'
# file = YourFileObjectHere  # Replace with your actual file object

# converter = ImageConverter(source_mimetype, target_mimetype, file)
# output_path = converter.convert()
