from fontTools.ttLib import TTFont
import os
from backend.converters.woff2ttf import WoffToTtfConverter


class FontConverter:
    def __init__(self, source_mimetype, target_mimetype, file):
        self.source_mimetype = source_mimetype
        self.target_mimetype = target_mimetype
        self.file = file

    def convert(self):
        if self.is_otf_to_woff():
            self.convert_otf_to_woff()
        elif self.is_otf_to_woff2():
            self.convert_otf_to_woff2()
        elif self.is_ttf_to_woff():
            self.convert_ttf_to_woff()
        elif self.is_ttf_to_woff2():
            self.convert_ttf_to_woff2()
        elif self.is_woff_to_ttf():
            self.convert_woff_to_ttf()

        return self.output_path()

    def convert_otf_to_woff(self):
        f = TTFont(self.file.path)
        f.flavor = 'woff'
        f.save(self.output_path())

    def convert_otf_to_woff2(self):
        f = TTFont(self.file.path)
        f.flavor = 'woff2'
        f.save(self.output_path())

    def convert_ttf_to_woff(self):
        f = TTFont(self.file.path)
        f.flavor = 'woff'
        f.save(self.output_path())

    def convert_ttf_to_woff2(self):
        f = TTFont(self.file.path)
        f.flavor = 'woff2'
        f.save(self.output_path())

    def convert_woff_to_ttf(self):
        converter = WoffToTtfConverter(self.file.path)
        converter.convert()

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

    def output_path(self):
        self.output_path = self.generate_output_file_path()
        return self.output_path

    def generate_output_file_path(self, target_extension=None):
        # Get the directory part of the original file path
        file_directory = os.path.dirname(self.file.name)

        # Get the filename part of the original file path
        file_name = os.path.basename(self.file.path)
        target_extension = target_extension if target_extension else self.target_mimetype.split(
            '/')[-1]

        # Construct the output file path in the same directory with a different extension
        return (file_directory + '/' + file_name.split('.')[0] + '.' + target_extension).replace('uploaded', 'converted')
