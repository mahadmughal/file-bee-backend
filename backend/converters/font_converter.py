from fontTools.ttLib import TTFont
import os
from backend.converters.woff2ttf import WoffToTtfConverter
from io import BytesIO
from django.core.files.base import ContentFile
from backend.utils.s3_utils import s3_client


class FontConverter:
    def __init__(self, source_mimetype, target_mimetype, file):
        self.source_mimetype = source_mimetype
        self.target_mimetype = target_mimetype
        self.file = file

    def convert(self):
        font_file_object = self.get_file_from_s3()

        if self.is_otf_to_woff():
            output = self.convert_otf_to_woff(font_file_object)
        elif self.is_otf_to_woff2():
            output = self.convert_otf_to_woff2(font_file_object)
        elif self.is_ttf_to_woff():
            output = self.convert_ttf_to_woff(font_file_object)
        elif self.is_ttf_to_woff2():
            output = self.convert_ttf_to_woff2(font_file_object)
        elif self.is_woff_to_ttf():
            output = self.convert_woff_to_ttf(font_file_object)

        return ContentFile(output)

    def convert_otf_to_woff(self, input_file):
        font = TTFont(input_file)
        font.flavor = 'woff'
        woff_buffer = BytesIO()
        font.save(woff_buffer)
        woff_buffer.seek(0)

        return woff_buffer.getvalue()

    def convert_otf_to_woff2(self, input_file):
        font = TTFont(input_file)
        font.flavor = 'woff2'
        woff_buffer = BytesIO()
        font.save(woff_buffer)
        woff_buffer.seek(0)

        return woff_buffer.getvalue()

    def convert_ttf_to_woff(self, input_file):
        font = TTFont(input_file)
        font.flavor = 'woff2'
        woff_buffer = BytesIO()
        font.save(woff_buffer)
        woff_buffer.seek(0)

        return woff_buffer.getvalue()

    def convert_ttf_to_woff2(self, input_file):
        font = TTFont(input_file)
        font.flavor = 'woff2'
        woff_buffer = BytesIO()
        font.save(woff_buffer)
        woff_buffer.seek(0)

        return woff_buffer.getvalue()

    def convert_woff_to_ttf(self, input_file):
        converter = WoffToTtfConverter(input_file)
        output_file = converter.convert()

        return output_file

    def get_file_from_s3(self):
        file_content = s3_client.get_object(self.file.name)
        file_object = BytesIO(file_content)
        file_object.name = os.path.basename(os.path.basename(self.file.name))
        file_object.seek(0)

        return file_object

    def is_otf_to_woff(self):
        return self.source_mimetype == 'font/otf' and self.target_mimetype == 'font/woff'

    def is_otf_to_woff2(self):
        return self.source_mimetype == 'font/otf' and self.target_mimetype == 'font/woff2'

    def is_ttf_to_woff(self):
        return self.source_mimetype == 'font/ttf' and self.target_mimetype == 'font/woff'

    def is_ttf_to_woff2(self):
        return self.source_mimetype == 'font/ttf' and self.target_mimetype == 'font/woff2'

    def is_woff_to_ttf(self):
        return self.source_mimetype == 'font/woff' and self.target_mimetype == 'font/ttf'

    # TODO: not functional, have to confirm whether to remove this method.
    def generate_output_file_path(self, target_extension=None):
        file_directory = os.path.dirname(self.file.name)
        file_name = os.path.basename(self.file.path)
        target_extension = target_extension if target_extension else self.target_mimetype.split(
            '/')[-1]

        return (file_directory + '/' + file_name.split('.')[0] + '.' + target_extension).replace('uploaded', 'converted')
