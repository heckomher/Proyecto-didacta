"""
Tests automatizados para el sistema Didacta
Ejecutar con: pytest tests/test_api.py -v
"""
import pytest
import requests

BASE_URL = "http://localhost/api"


class TestAuthentication:
    """TC-01: Autenticación e inicio de sesión"""
    
    def test_tc01_2_login_invalid_credentials(self):
        """TC-01.2: Login fallido con credenciales inválidas"""
        response = requests.post(
            f"{BASE_URL}/auth/login/",
            json={"username": "test_invalido", "password": "wrong123"}
        )
        assert response.status_code == 401
        assert "detail" in response.json()
    
    def test_tc01_3_login_empty_fields(self):
        """TC-01.3: Login con campos vacíos"""
        response = requests.post(
            f"{BASE_URL}/auth/login/",
            json={"username": "", "password": ""}
        )
        assert response.status_code in [400, 401]


class TestSecurity:
    """TC-06: Seguridad y manejo de sesiones"""
    
    def test_tc06_2_api_without_token(self):
        """TC-06.2: Protección de API sin token"""
        response = requests.get(f"{BASE_URL}/cursos/")
        assert response.status_code == 401
    
    def test_tc06_2_users_api_without_token(self):
        """TC-06.2b: Protección de usuarios API sin token"""
        response = requests.get(f"{BASE_URL}/auth/users/")
        assert response.status_code == 401
    
    def test_tc06_4_sql_injection(self):
        """TC-06.4: Validación de inyección SQL"""
        response = requests.post(
            f"{BASE_URL}/auth/login/",
            json={"username": "' OR '1'='1", "password": "' OR '1'='1"}
        )
        # No debe permitir acceso con SQL injection
        assert response.status_code == 401


class TestUserManagement:
    """TC-02: Registro y gestión de usuarios"""
    
    def test_tc02_2_register_without_auth(self):
        """TC-02.2: Bloqueo de registro sin autenticación"""
        response = requests.post(
            f"{BASE_URL}/auth/register/",
            json={
                "username": "test_user",
                "password": "test123",
                "password2": "test123",
                "email": "test@test.com",
                "role": "DOCENTE"
            }
        )
        # Debe requerir autenticación UTP para registrar
        assert response.status_code in [401, 403]


class TestPlanifications:
    """TC-03 y TC-04: Creación y validación de planificaciones"""
    
    def test_tc03_api_planificaciones_without_auth(self):
        """Verificar que planificaciones requiere autenticación"""
        response = requests.get(f"{BASE_URL}/planificaciones-anuales/")
        assert response.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
