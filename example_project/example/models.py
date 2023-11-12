from django.db import models


class Blob(models.Model):
    """An example model."""

    blob = models.BinaryField(null=True, blank=True)

    def __str__(self):
        if not self.blob:
            return None
        return self.blob.hex()[:64]

    class Meta:
        verbose_name = "blob"
        verbose_name_plural = "blobs"
