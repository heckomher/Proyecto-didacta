# Definicion del plan de pruebas y diseño de protocolos de pruebas

Estado: Listo
Responsable: Nicolas, jhon Sánchez
Descripción: Diseño de protocolo de pruebas

Plan de pruebas

| **Caso de Uso / Área** | **Escenario Crítico / Riesgo** | **Alcance del Test** | **Tipo(s) de Prueba** | **Responsable(s)** |
| --- | --- | --- | --- | --- |
| CU-01: Autenticación e inicio de sesión | Autenticación fallida | Módulo de autenticación / login | Pruebas funcionales | Héctor |
| CU-02: Registro y gestión de usuarios | Accesos no autorizados / permisos mal asignados | Módulo de usuarios | Pruebas funcionales | Jhon |
| CU-03: Creación de planificaciones | Integración fallida entre frontend / backend / BD | Módulo de creación de planificaciones | Pruebas de integración | Nicolás |
| CU-04: Validación de planificaciones (Docente → UTP) | Pérdida o corrupción de datos en envío/revisión | Módulo de revisión y validación | Pruebas de integración | Héctor |
| CU-05: Gestión del calendario dinámico | Sobrecarga del sistema, lentitud o fallos bajo carga | Calendario + base de datos de eventos | Pruebas de estrés / rendimiento | Héctor |
| CU-06: Seguridad y manejo de sesiones | Vulnerabilidades (inyección, sesiones, XSS, accesos indebidos) | Seguridad general del sistema | Pruebas de seguridad | Jhon |
| Área transversal: Integración entre todos los módulos | Fallos en la interacción entre componentes (frontend/backend/BD) | Todo el sistema | Pruebas de integración | Nicolás |
| Área transversal: Rendimiento y disponibilidad global | Caídas o degradación bajo carga alta o concurrencia | Todo el sistema bajo carga | Pruebas de estrés / rendimiento | Héctor |
| Área transversal: Usabilidad para usuarios Docente/UTP | Interfaz poco intuitiva, errores de UX, dificultad de uso | Frontend / interfaz de usuario | Pruebas de usabilidad | Nicolás |