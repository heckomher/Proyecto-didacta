/**
 * Tests automatizados para el sistema Didacta
 * Ejecutar con: npm test
 */

const BASE_URL = 'http://localhost/api';

describe('CU-01: Autenticación', () => {

    test('TC-01.2: Login fallido con credenciales inválidas', async () => {
        const response = await fetch(`${BASE_URL}/auth/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: 'test_invalido', password: 'wrong123' })
        });

        expect(response.status).toBe(401);
        const data = await response.json();
        expect(data).toHaveProperty('detail');
    });

    test('TC-01.3: Login con campos vacíos', async () => {
        const response = await fetch(`${BASE_URL}/auth/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: '', password: '' })
        });

        expect([400, 401]).toContain(response.status);
    });
});

describe('CU-06: Seguridad', () => {

    test('TC-06.2: API cursos sin token devuelve 401', async () => {
        const response = await fetch(`${BASE_URL}/cursos/`);
        expect(response.status).toBe(401);
    });

    test('TC-06.2b: API usuarios sin token devuelve 401', async () => {
        const response = await fetch(`${BASE_URL}/auth/users/`);
        expect(response.status).toBe(401);
    });

    test('TC-06.4: SQL Injection rechazada', async () => {
        const response = await fetch(`${BASE_URL}/auth/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: "' OR '1'='1", password: "' OR '1'='1" })
        });

        // No debe permitir acceso con SQL injection
        expect(response.status).toBe(401);
    });
});

describe('CU-02: Gestión de Usuarios', () => {

    test('TC-02.2: Registro sin autenticación bloqueado', async () => {
        const response = await fetch(`${BASE_URL}/auth/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: 'test_user',
                password: 'test123',
                password2: 'test123',
                email: 'test@test.com',
                role: 'DOCENTE'
            })
        });

        expect([401, 403]).toContain(response.status);
    });
});

describe('CU-03: Planificaciones', () => {

    test('TC-03: Planificaciones requiere autenticación', async () => {
        const response = await fetch(`${BASE_URL}/planificaciones-anuales/`);
        expect(response.status).toBe(401);
    });
});
