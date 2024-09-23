import os
from pydub import AudioSegment
from io import BytesIO
from django.core.files.base import ContentFile
from backend.utils.s3_utils import s3_client


class AudioConverter:
    def __init__(self, source_mimetype, target_mimetype, file):
        self.source_mimetype = source_mimetype
        self.target_mimetype = target_mimetype
        self.file = file

    def convert(self):
        input_audio = self.get_file_from_s3()

        if self.is_mp3_to_oga():
            output = self.convert_mp3_to_oga(input_audio)
        elif self.is_mp3_to_wav():
            output = self.convert_mp3_to_wav(input_audio)
        elif self.is_mp3_to_flac():
            output = self.convert_mp3_to_flac(input_audio)
        elif self.is_mp3_to_mp2():
            output = self.convert_mp3_to_mp2(input_audio)
        elif self.is_wav_to_oga():
            output = self.convert_wav_to_oga(input_audio)
        elif self.is_wav_to_mp3():
            output = self.convert_wav_to_mp3(input_audio)
        elif self.is_wav_to_flac():
            output = self.convert_wav_to_flac(input_audio)
        elif self.is_wav_to_mp2():
            output = self.convert_wav_to_mp2(input_audio)
        elif self.is_flac_to_oga():
            output = self.convert_flac_to_oga(input_audio)
        elif self.is_flac_to_mp3():
            output = self.convert_flac_to_mp3(input_audio)
        elif self.is_flac_to_wav():
            output = self.convert_flac_to_wav(input_audio)
        elif self.is_flac_to_mp2():
            output = self.convert_flac_to_mp2(input_audio)
        elif self.is_mp2_to_oga():
            output = self.convert_mp2_to_oga(input_audio)
        elif self.is_mp2_to_mp3():
            output = self.convert_mp2_to_mp3(input_audio)
        elif self.is_mp2_to_wav():
            output = self.convert_mp2_to_wav(input_audio)
        elif self.is_mp2_to_flac():
            output = self.convert_mp2_to_flac(input_audio)

        return ContentFile(output)

    def convert_mp3_to_oga(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='mp3')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='oga')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def convert_mp3_to_wav(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='mp3')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='wav')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def convert_mp3_to_flac(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='mp3')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='flac')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def convert_mp3_to_mp2(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='mp3')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='mp2')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def convert_wav_to_oga(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='wav')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='oga')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def convert_wav_to_mp3(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='wav')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='mp3')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def convert_wav_to_flac(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='wav')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='flac')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def convert_wav_to_mp2(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='wav')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='mp2')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def convert_flac_to_oga(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='flac')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='oga')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def convert_flac_to_mp3(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='flac')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='mp3')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def convert_flac_to_wav(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='flac')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='wav')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def convert_flac_to_mp2(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='flac')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='mp2')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def convert_mp2_to_oga(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='mp3')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='oga')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def convert_mp2_to_mp3(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='mp2')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='mp3')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def convert_mp2_to_wav(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='mp2')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='wav')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def convert_mp2_to_flac(self, input_audio):
        audio = AudioSegment.from_file(input_audio, format='mp2')
        output_buffer = BytesIO()
        audio.export(output_buffer, format='flac')
        output_buffer.seek(0)

        return output_buffer.getvalue()

    def get_file_from_s3(self):
        file_content = s3_client.get_object(self.file.name)
        file_object = BytesIO(file_content)
        file_object.name = os.path.basename(os.path.basename(self.file.name))
        file_object.seek(0)

        return file_object

    def is_mp3_to_oga(self):
        return self.source_mimetype == 'audio/mpeg' and self.target_mimetype == 'audio/ogg'

    def is_mp3_to_wav(self):
        return self.source_mimetype == 'audio/mpeg' and self.target_mimetype == 'audio/wav'

    def is_mp3_to_flac(self):
        return self.source_mimetype == 'audio/mpeg' and self.target_mimetype == 'audio/flac'

    def is_mp3_to_mp2(self):
        return self.source_mimetype == 'audio/mpeg' and self.target_mimetype == 'audio/mp2'

    def is_wav_to_oga(self):
        return self.source_mimetype == 'audio/wav' and self.target_mimetype == 'audio/ogg'

    def is_wav_to_mp3(self):
        return self.source_mimetype == 'audio/wav' and self.target_mimetype == 'audio/mpeg'

    def is_wav_to_flac(self):
        return self.source_mimetype == 'audio/wav' and self.target_mimetype == 'audio/flac'

    def is_wav_to_mp2(self):
        return self.source_mimetype == 'audio/wav' and self.target_mimetype == 'audio/mp2'

    def is_flac_to_oga(self):
        return self.source_mimetype == 'audio/flac' and self.target_mimetype == 'audio/ogg'

    def is_flac_to_mp3(self):
        return self.source_mimetype == 'audio/flac' and self.target_mimetype == 'audio/mpeg'

    def is_flac_to_wav(self):
        return self.source_mimetype == 'audio/flac' and self.target_mimetype == 'audio/wav'

    def is_flac_to_mp2(self):
        return self.source_mimetype == 'audio/flac' and self.target_mimetype == 'audio/mp2'

    def is_mp2_to_oga(self):
        return self.source_mimetype == 'audio/mp2' and self.target_mimetype == 'audio/ogg'

    def is_mp2_to_mp3(self):
        return self.source_mimetype == 'audio/mp2' and self.target_mimetype == 'audio/mpeg'

    def is_mp2_to_wav(self):
        return self.source_mimetype == 'audio/mp2' and self.target_mimetype == 'audio/wav'

    def is_mp2_to_flac(self):
        return self.source_mimetype == 'audio/mp2' and self.target_mimetype == 'audio/flac'
