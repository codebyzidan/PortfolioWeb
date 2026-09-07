"""
Validator upload file bersama untuk seluruh aplikasi.

Satu sumber aturan (DRY): semua ImageField & FileField pada proyek memakai
validator di sini, sehingga kebijakan ukuran/ekstensi konsisten dan mudah
diubah di satu tempat.
"""

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.deconstruct import deconstructible

MAX_IMAGE_SIZE_MB = 2
MAX_DOCUMENT_SIZE_MB = 5

MAX_IMAGE_SIZE = MAX_IMAGE_SIZE_MB * 1024 * 1024
MAX_DOCUMENT_SIZE = MAX_DOCUMENT_SIZE_MB * 1024 * 1024


@deconstructible
class FileSizeValidator:
    """Memastikan ukuran file yang di-upload tidak melebihi batas."""

    def __init__(self, max_bytes: int) -> None:
        self.max_bytes = max_bytes

    def __call__(self, uploaded_file) -> None:
        if uploaded_file.size > self.max_bytes:
            raise ValidationError(
                f"Ukuran file maksimal {self.max_bytes // (1024 * 1024)} MB."
            )

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, FileSizeValidator) and self.max_bytes == other.max_bytes
        )


_validate_image_extension = FileExtensionValidator(
    allowed_extensions=("jpg", "jpeg", "png", "webp"),
    message="Format gambar harus JPG, PNG, atau WebP.",
)

_validate_document_extension = FileExtensionValidator(
    allowed_extensions=("pdf", "doc", "docx"),
    message="Format dokumen harus PDF, DOC, atau DOCX.",
)


def validate_image_upload(uploaded_file) -> None:
    """Validasi gabungan gambar: ekstensi diizinkan + batas ukuran."""
    _validate_image_extension(uploaded_file)
    FileSizeValidator(MAX_IMAGE_SIZE)(uploaded_file)


def validate_document_upload(uploaded_file) -> None:
    """Validasi gabungan dokumen: ekstensi diizinkan + batas ukuran."""
    _validate_document_extension(uploaded_file)
    FileSizeValidator(MAX_DOCUMENT_SIZE)(uploaded_file)