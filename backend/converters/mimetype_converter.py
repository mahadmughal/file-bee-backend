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
