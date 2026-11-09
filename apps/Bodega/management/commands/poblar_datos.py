from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from apps.Bodega.models import Categoria, Figura


class Command(BaseCommand):
    help = 'Puebla la base de datos con 4 categorías automotrices, 8 repuestos y usuarios de prueba'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Actualizando catálogo a Repuestos Automotrices...'))

        # Limpiar datos anteriores de figuras para que solo queden repuestos
        Figura.objects.all().delete()
        Categoria.objects.all().delete()

        # 1. Usuarios de Prueba (Admin y Estándar)
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@repuestos.cl', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin1234')
            admin_user.save()

        cliente_user, created = User.objects.get_or_create(
            username='cliente',
            defaults={'email': 'cliente@repuestos.cl', 'is_staff': False, 'is_superuser': False}
        )
        if created:
            cliente_user.set_password('cliente1234')
            cliente_user.save()

        # 2. Crear 4 Categorías de Repuestos Automotrices
        datos_categorias = [
            ('Sistema de Frenos', 'Pastillas, discos ventilados, cálipers y sensores ABS.'),
            ('Motor y Distribución', 'Kits de distribución, bombas de agua, bujías y filtros.'),
            ('Suspensión y Dirección', 'Amortiguadores a gas, bandejas, axiales y terminales.'),
            ('Sistema Eléctrico e Iluminación', 'Alternadores, baterías, motores de partida y ópticos.'),
        ]

        categorias_objs = {}
        for nombre, desc in datos_categorias:
            cat = Categoria.objects.create(
                nombre=nombre,
                slug=slugify(nombre),
                descripcion=desc,
                activo=True,
            )
            categorias_objs[nombre] = cat
        self.stdout.write(self.style.SUCCESS('✔ 4 Categorías automotrices cargadas'))

        # 3. Crear 8 Repuestos Automotrices
        datos_repuestos = [
            ('Kit Pastillas de Freno Cerámicas Delanteras', 'Brembo', 'OEM P-83052 / Toyota Hilux - Corolla', 'Compuesto cerámico de bajo polvo y alta resistencia térmica. Incluye sensores de desgaste.', 48990, 15, True, 'Sistema de Frenos'),
            ('Par Discos de Freno Ventilados 280mm', 'Bosch', 'OEM 0986479 / Nissan NP300 - Sentra', 'Acero de alto carbono con recubrimiento anticorrosión UV.', 74990, 8, True, 'Sistema de Frenos'),
            ('Kit Correa Distribución + Tensor + Bomba', 'Gates', 'OEM TCKWP328 / Chevrolet Sail - Corsa 1.4', 'Correa reforzada en HNBR de larga duración para 60.000 km.', 89990, 6, True, 'Motor y Distribución'),
            ('Set 4 Bujías Iridium Power Laser', 'NGK', 'OEM BKR6EIX / Mazda 3 - Hyundai Accent', 'Electrodo central de iridio de 0.6mm para encendido óptimo y ahorro de combustible.', 36990, 20, False, 'Motor y Distribución'),
            ('Par Amortiguadores Delanteros Gas-Magnum', 'Monroe', 'OEM 334450 / Kia Rio - Morning', 'Válvula de desplazamiento variable con nitrógeno presurizado.', 95990, 10, True, 'Suspensión y Dirección'),
            ('Bandeja Suspensión Inferior con Rótula', 'TRW', 'OEM JTC1425 / Peugeot 208 - Partner', 'Forjada en acero de alta resistencia con bujes de caucho preinstalados.', 54990, 12, False, 'Suspensión y Dirección'),
            ('Alternador Trifásico 12V 110A Regulador Int.', 'Valeo', 'OEM TG11C042 / Renault Duster - Clio', 'Bobinado de cobre electrolítico 100% nuevo con polea libre.', 145000, 4, True, 'Sistema Eléctrico e Iluminación'),
            ('Batería Automotriz Libre Mantención 60Ah 550CCA', 'Hankook', 'Modelo MF55D23L / Multimarca', 'Rejilla de calcio-estaño con arranque en frío garantizado e indicador visual.', 69990, 14, True, 'Sistema Eléctrico e Iluminación'),
        ]

        for nombre, fabricante, escala, desc, precio, stock, destacado, cat_nombre in datos_repuestos:
            Figura.objects.create(
                nombre=nombre,
                categoria=categorias_objs[cat_nombre],
                fabricante=fabricante,
                escala=escala,
                descripcion=desc,
                precio=precio,
                stock=stock,
                estado='DISPONIBLE',
                destacado=destacado,
                activo=True,
            )
        self.stdout.write(self.style.SUCCESS('✔ 8 Repuestos Automotrices cargados correctamente'))