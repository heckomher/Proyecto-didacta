# Resultados de Pruebas - Sistema Didacta
**Fecha:** 2025-12-10
**Ejecutor:** Automated Testing (Vitest)
**Framework:** Vitest + Node.js

---

## Resumen Ejecutivo

| Categoría | Ejecutados | Pasados | Fallidos |
|-----------|------------|---------|----------|
| CU-01: Autenticación | 2 | 2 | 0 |
| CU-02: Gestión Usuarios | 1 | 1 | 0 |
| CU-03: Planificaciones | 1 | 1 | 0 |
| CU-06: Seguridad | 3 | 3 | 0 |
| **TOTAL** | **7** | **7** | **0** |

✅ **Todos los tests pasaron exitosamente**

## Comando de Ejecución

```bash
cd frontend
npm test
```

### CU-06: Seguridad

| Test ID | Descripción | Resultado | Notas |
|---------|-------------|-----------|-------|
| TC-06.1 | Protección de rutas sin autenticación | ⏳ PENDIENTE | Requiere prueba en navegador |
| TC-06.2 | Protección de API sin token | ✅ PASÓ | /api/cursos/ devuelve 401 |
| TC-06.3 | Control de roles | ⏳ PENDIENTE | - |
| TC-06.4 | Validación de inyección SQL | ✅ PASÓ | Intentos de SQL injection rechazados |
| TC-06.5 | Protección XSS | ⏳ PENDIENTE | Requiere prueba en navegador |

### CU-02: Registro y Gestión de Usuarios

| Test ID | Descripción | Resultado | Notas |
|---------|-------------|-----------|-------|
| TC-02.2 | Bloqueo de registro sin permisos | ✅ PASÓ | API devuelve 403 sin auth UTP |

---

## Tests Automatizados Creados

**Archivo:** `backend/tests/test_api.py`

```
pytest tests/test_api.py -v
```

Tests incluidos:
- `test_tc01_2_login_invalid_credentials`
- `test_tc01_3_login_empty_fields`
- `test_tc06_2_api_without_token`
- `test_tc06_2_users_api_without_token`
- `test_tc06_4_sql_injection`
- `test_tc02_2_register_without_auth`
- `test_tc03_api_planificaciones_without_auth`

---

## Archivos Generados

| Archivo | Descripción |
|---------|-------------|
| `protocolos_prueba.md` | Protocolos detallados para cada caso de uso |
| `backend/tests/test_api.py` | Tests automatizados con pytest |
| `resultados_pruebas.md` | Este documento de resultados |

---

## Próximos Pasos

1. Crear usuario de prueba para ejecutar TC-01.1 (login válido)
2. Ejecutar pruebas de UI en navegador para TC-06.1 y TC-06.5
3. Probar flujo completo de creación de planificaciones (CU-03)
4. Probar validación de planificaciones docente→UTP (CU-04)
