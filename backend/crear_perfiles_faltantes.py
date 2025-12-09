#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from main.models import User, Docente, EquipoDirectivo

# Crear perfiles de Docente faltantes
usuarios_docente = User.objects.filter(role='DOCENTE')
for usuario in usuarios_docente:
    if not hasattr(usuario, 'perfil_docente'):
        Docente.objects.create(
            usuario=usuario,
            rut=f'pending-{usuario.id}',
            especialidad='Sin especialidad'
        )
        print(f'Perfil de Docente creado para: {usuario.username} ({usuario.nombre} {usuario.apellido})')
    else:
        print(f'Perfil de Docente ya existe para: {usuario.username}')

# Crear perfiles de Equipo Directivo faltantes
usuarios_directivo = User.objects.filter(role='EQUIPO_DIRECTIVO')
for usuario in usuarios_directivo:
    if not hasattr(usuario, 'perfil_directivo'):
        EquipoDirectivo.objects.create(
            usuario=usuario,
            cargo='Sin cargo',
            departamento='Sin departamento'
        )
        print(f'Perfil de Directivo creado para: {usuario.username} ({usuario.nombre} {usuario.apellido})')
    else:
        print(f'Perfil de Directivo ya existe para: {usuario.username}')

print('\nResumen:')
print(f'Total usuarios DOCENTE: {User.objects.filter(role="DOCENTE").count()}')
print(f'Total perfiles Docente: {Docente.objects.count()}')
print(f'Total usuarios EQUIPO_DIRECTIVO: {User.objects.filter(role="EQUIPO_DIRECTIVO").count()}')
print(f'Total perfiles Directivo: {EquipoDirectivo.objects.count()}')
