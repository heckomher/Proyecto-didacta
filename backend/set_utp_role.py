#!/usr/bin/env python
"""Script para asignar rol UTP a un usuario"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from main.models import User

# Cambia 'admin' por tu nombre de usuario
username = input("Ingresa el nombre de usuario: ")

try:
    user = User.objects.get(username=username)
    user.role = 'UTP'
    user.save()
    print(f"✓ Usuario '{username}' actualizado con rol UTP")
    print(f"  - Email: {user.email}")
    print(f"  - Rol: {user.role}")
    print(f"  - Superuser: {user.is_superuser}")
except User.DoesNotExist:
    print(f"✗ Usuario '{username}' no encontrado")
    print("\nUsuarios disponibles:")
    for u in User.objects.all():
        print(f"  - {u.username} (Rol: {u.role})")
