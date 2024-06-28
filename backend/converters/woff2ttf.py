import struct
import zlib
import os


class WoffToTtfConverter:

    def __init__(self, infile_path):
        """
        Initializes the converter with input and output file paths.

        Args:
            infile_path (str): Path to the input WOFF file.
            outfile_path (str): Path to the output TTF/OTF file.
        """
        self.infile_path = infile_path
        self.outfile_path = self.generate_output_file_path()

    def convert(self):
        """
        Converts the WOFF font file at `self.infile_path` to a TTF/OTF file at `self.outfile_path`.
        """

        with open(self.infile_path, mode='rb') as infile:
            with open(self.outfile_path, mode='wb') as outfile:
                self._convert_streams(infile, outfile)

    def _convert_streams(self, infile, outfile):
        WOFFHeader = {
            'signature': struct.unpack(">I", infile.read(4))[0],
            'flavor': struct.unpack(">I", infile.read(4))[0],
            'length': struct.unpack(">I", infile.read(4))[0],
            'numTables': struct.unpack(">H", infile.read(2))[0],
            'reserved': struct.unpack(">H", infile.read(2))[0],
            'totalSfntSize': struct.unpack(">I", infile.read(4))[0],
            'majorVersion': struct.unpack(">H", infile.read(2))[0],
            'minorVersion': struct.unpack(">H", infile.read(2))[0],
            'metaOffset': struct.unpack(">I", infile.read(4))[0],
            'metaLength': struct.unpack(">I", infile.read(4))[0],
            'metaOrigLength': struct.unpack(">I", infile.read(4))[0],
            'privOffset': struct.unpack(">I", infile.read(4))[0],
            'privLength': struct.unpack(">I", infile.read(4))[0],
        }

        outfile.write(struct.pack(">I", WOFFHeader['flavor']))
        outfile.write(struct.pack(">H", WOFFHeader['numTables']))
        maximum = list(filter(lambda x: x[1] <= WOFFHeader['numTables'], [
                      (n, 2**n) for n in range(64)]))[-1]
        searchRange = maximum[1] * 16
        outfile.write(struct.pack(">H", searchRange))
        entrySelector = maximum[0]
        outfile.write(struct.pack(">H", entrySelector))
        rangeShift = WOFFHeader['numTables'] * 16 - searchRange
        outfile.write(struct.pack(">H", rangeShift))

        offset = outfile.tell()

        TableDirectoryEntries = []
        for i in range(0, WOFFHeader['numTables']):
            TableDirectoryEntries.append({'tag': struct.unpack(">I", infile.read(4))[0],
                                          'offset': struct.unpack(">I", infile.read(4))[0],
                                          'compLength': struct.unpack(">I", infile.read(4))[0],
                                          'origLength': struct.unpack(">I", infile.read(4))[0],
                                          'origChecksum': struct.unpack(">I", infile.read(4))[0]})
            offset += 4*4

        for TableDirectoryEntry in TableDirectoryEntries:
            outfile.write(struct.pack(">I", TableDirectoryEntry['tag']))
            outfile.write(struct.pack(
                ">I", TableDirectoryEntry['origChecksum']))
            outfile.write(struct.pack(">I", offset))
            outfile.write(struct.pack(">I", TableDirectoryEntry['origLength']))
            TableDirectoryEntry['outOffset'] = offset
            offset += TableDirectoryEntry['origLength']
            if (offset % 4) != 0:
                offset += 4 - (offset % 4)

        for TableDirectoryEntry in TableDirectoryEntries:
            infile.seek(TableDirectoryEntry['offset'])
            compressedData = infile.read(TableDirectoryEntry['compLength'])
            if TableDirectoryEntry['compLength'] != TableDirectoryEntry['origLength']:
                uncompressedData = zlib.decompress(compressedData)
            else:
                uncompressedData = compressedData
            outfile.seek(TableDirectoryEntry['outOffset'])
            outfile.write(uncompressedData)
            offset = TableDirectoryEntry['outOffset'] + \
                TableDirectoryEntry['origLength']
            padding = 0
            if (offset % 4) != 0:
                padding = 4 - (offset % 4)
            outfile.write(bytearray(padding))

    def generate_output_file_path(self, target_extension=None):
        # Get the directory part of the original file path
        file_directory = os.path.dirname(self.infile_path)

        # Get the filename part of the original file path
        file_name = os.path.basename(self.infile_path)

        # Construct the output file path in the same directory with a different extension
        return (file_directory + '/' + file_name.split('.')[0] + '.' + 'ttf').replace('uploaded', 'converted')
