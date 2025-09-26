import allure
import pytest
from playwright.sync_api import expect

@allure.feature("Login")
@allure.story("Happy path")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.ui
@pytest.mark.smoke
def test_login_smoke(page):
    with allure.step("Abrir aplicación"):
        page.goto("https://www.saucedemo.com/")

    with allure.step("Ingresar credenciales"):
        page.fill("[data-test='username']", "standard_user")
        page.fill("[data-test='password']", "secret_sauce")

    with allure.step("Iniciar sesión"):
        page.click("[data-test='login-button']")

    # Validación de éxito (lista de productos visible)
    with allure.step("Validar lista de productos"):
        expect(page.locator(".inventory_list")).to_be_visible()

    with allure.step("dato forzado"):
        assert 1 == 1, "esto esta forzado"


    allure.attach(page.screenshot(), name="pantalla_final", attachment_type=allure.attachment_type.PNG)
