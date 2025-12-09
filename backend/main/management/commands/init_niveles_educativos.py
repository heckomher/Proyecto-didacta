from django.core.management.base import BaseCommand
from main.models import NivelEducativo

class Command(BaseCommand):
    help = 'Inicializa los niveles educativos básicos del sistema'

    def handle(self, *args, **options):
        niveles = [
            {'nombre': 'Educación Parvularia', 'descripcion': 'Pre-kínder y Kínder'},
            {'nombre': 'Educación Básica', 'descripcion': '1° a 8° Básico'},
            {'nombre': 'Educación Media', 'descripcion': '1° a 4° Medio'},
        ]
        
        creados = 0
        existentes = 0
        
        for nivel_data in niveles:
            nivel, created = NivelEducativo.objects.get_or_create(
                nombre=nivel_data['nombre'],
                defaults={'descripcion': nivel_data['descripcion']}
            )
            
            if created:
                creados += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Creado: {nivel.nombre}'))
            else:
                existentes += 1
                self.stdout.write(f'  Ya existe: {nivel.nombre}')
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Proceso completado: {creados} creados, {existentes} ya existían'))
