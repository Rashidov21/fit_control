"""
Utility functions for QR code generation.
"""
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image


def generate_qr_code_image(url):
    """Generate QR code image from URL."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return ContentFile(buffer.read(), name='qr_code.png')
