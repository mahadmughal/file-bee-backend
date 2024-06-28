from backend.converters.image_converter import ImageConverter
from backend.converters.document_converter import DocumentConverter
from backend.converters.font_converter import FontConverter
from backend.converters.audio_converter import AudioConverter
import os


class MimetypeConverter:
    def __init__(self, source_mimetype, target_mimetype, file):
        self.source_mimetype = source_mimetype
        self.target_mimetype = target_mimetype
        self.file = file

    def convert(self):
        if self.source_mimetype.startswith("image"):
            image_converter = ImageConverter(
                self.source_mimetype, self.target_mimetype, self.file)
            return image_converter.convert()
        elif self.source_mimetype.startswith("font"):
            font_converter = FontConverter(
                self.source_mimetype, self.target_mimetype, self.file)
            return font_converter.convert()
        elif self.source_mimetype.startswith("audio"):
            audio_converter = AudioConverter(
                self.source_mimetype, self.target_mimetype, self.file)
            return audio_converter.convert()
        else:
            document_converter = DocumentConverter(
                self.source_mimetype, self.target_mimetype, self.file)
            return document_converter.convert()

    def generate_output_file_path(self, target_extension=None):
        # Get the directory part of the original file path
        file_directory = os.path.dirname(self.file.name)

        # Get the filename part of the original file path
        file_name = os.path.basename(self.file.path)
        target_extension = target_extension if target_extension else self.target_mimetype.split(
            '/')[-1]

        # Construct the output file path in the same directory with a different extension
        return (file_directory + '/' + file_name.split('.')[0] + '.' + target_extension).replace('uploaded', 'converted')

    # def generate_output_file_path(self):
        # return f"{self.file.path.split('.')[0]}.{self.target_mimetype.split('/')[-1]}".replace('uploaded', 'converted')
