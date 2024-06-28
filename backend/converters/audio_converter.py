import os
from pydub import AudioSegment


class AudioConverter:
    def __init__(self, source_mimetype, target_mimetype, file):
        self.source_mimetype = source_mimetype
        self.target_mimetype = target_mimetype
        self.file = file

    def convert(self):
        if self.is_mp3_to_oga():
            self.convert_mp3_to_oga()
        elif self.is_mp3_to_wav():
            self.convert_mp3_to_wav()
        elif self.is_mp3_to_flac():
            self.convert_mp3_to_flac()

        return self.output_path

    def convert_mp3_to_oga(self):
        audio = AudioSegment.from_file(self.file.path, format='mp3')
        audio.export(self.output_path(), format='oga')

    def convert_mp3_to_wav(self):
        audio = AudioSegment.from_file(self.file.path, format='mp3')
        audio.export(self.output_path(), format='wav')

    def convert_mp3_to_flac(self):
        audio = AudioSegment.from_file(self.file.path, format='mp3')
        audio.export(self.output_path(), format='flac')

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

    def is_mp3_to_oga(self):
        return self.source_mimetype == 'audio/mpeg' and self.target_mimetype == 'audio/ogg'

    def is_mp3_to_wav(self):
        return self.source_mimetype == 'audio/mpeg' and self.target_mimetype == 'audio/wav'

    def is_mp3_to_flac(self):
        return self.source_mimetype == 'audio/mpeg' and self.target_mimetype == 'audio/flac'
