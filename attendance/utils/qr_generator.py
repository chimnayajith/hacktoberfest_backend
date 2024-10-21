import qrcode
from io import BytesIO
from django.core.files import File

def generate_qr_code(data):
    qr_image = qrcode.make(data)
    
    qr_io = BytesIO()
    qr_image.save(qr_io, format='PNG')
    
    qr_io.seek(0)
    return File(qr_io, name=f'{data}.png')
