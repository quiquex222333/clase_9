import pytest
from playwright.sync_api import expect

@pytest.mark.ui
@pytest.mark.smoke
def test_login_smoke(page):
    page.goto("https://www.saucedemo.com/")
    page.fill("[data-test='username']", "standard_user")
    page.fill("[data-test='password']", "secret_sauce")
    page.click("[data-test='login-button']")

    # Validación de éxito (lista de productos visible)
    expect(page.locator(".inventory_list")).to_be_visible()
