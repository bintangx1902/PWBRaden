from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    penduduk = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    alamat = models.TextField()

    def __str__(self):
        return self.first_name + ' | ' + str(self.penduduk)


class JenisAspiration(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Aspiration(models.Model):
    title = models.CharField(max_length=255, default='')
    penduduk = models.ForeignKey(User, on_delete=models.CASCADE)
    jenis_aspirasi = models.ForeignKey(JenisAspiration, on_delete=models.CASCADE)
    aspirasi = models.TextField(null=False)
    lokasi = models.CharField(max_length=255)
    instansi_tujuan = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, default='unread')
    date_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return self.pk

    def __str__(self):
        return self.title + ' | ' + str(self.penduduk) + ' | ' + self.status
