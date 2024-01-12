from PIL import Image
import os
import pdb

def convert(source_mimetype, target_mimetype, file):
    image = Image.open(file.path)
    output_file_path = f"{file.name.split('.')[0]}.{target_mimetype.split('/')[1]}".replace('uploaded', 'converted')
    
    if source_mimetype == 'image/png' and target_mimetype == 'image/jpeg':
        image.save(output_file_path, 'JPEG', quality=95)
    elif source_mimetype == 'image/jpeg' and target_mimetype == 'image/png':
        image.save(output_file_path, 'PNG')
    
    return output_file_path