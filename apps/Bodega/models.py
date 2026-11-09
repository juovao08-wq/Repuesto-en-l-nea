from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Sistema o Categoría Automotriz")
    slug = models.SlugField(max_length=120, unique=True, blank=True, help_text="URL amigable")
    descripcion = models.TextField(blank=True, verbose_name="Descripción del Sistema")
    activo = models.BooleanField(default=True, verbose_name="¿Activo?")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoría de Repuesto"
        verbose_name_plural = "Categorías de Repuestos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Figura(models.Model):
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'En Stock en Bodega'),
        ('PREVENTA', 'Por Encargo / Importación'),
        ('SUSPENDIDO', 'Agotado / Descontinuado'),
    ]

    nombre = models.CharField(max_length=200, verbose_name="Nombre del Repuesto / Pieza")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="figuras", verbose_name="Sistema Automotriz")
    fabricante = models.CharField(max_length=100, verbose_name="Marca / Fabricante OEM")
    escala = models.CharField(max_length=50, blank=True, verbose_name="Código OEM / Compatibilidad")
    descripcion = models.TextField(verbose_name="Especificaciones Técnicas y Modelos Compatibles")
    precio = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(0)], verbose_name="Precio Unitario (CLP)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Unidades en Bodega")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DISPONIBLE', verbose_name="Estado en Bodega")
    imagen = models.ImageField(upload_to="figuras/", blank=True, null=True, verbose_name="Fotografía del Repuesto")
    destacado = models.BooleanField(default=False, verbose_name="¿Oferta Destacada?")
    activo = models.BooleanField(default=True, verbose_name="¿Disponible para Venta?")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Repuesto Automotriz"
        verbose_name_plural = "Repuestos Automotrices"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} - {self.fabricante}"

    @property
    def en_stock(self):
        return self.stock > 0

    @property
    def precio_formateado(self):
        return f"${self.precio:,.0f}".replace(",", ".")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            contador = 1
            while Figura.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug
        super().save(*args, **kwargs)