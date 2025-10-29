import requests
import pytest

DOMIN = "https://www.wildberries.ru"
#https://www.wildberries.ru/catalog/235347993/detail.aspx
class TestWB:

    def test_get_cart(self):
        resp = requests.get(f"{DOMIN}/catalog/235347993/detail.aspx")
        print(resp.status_code)
        assert resp.status_code in [200, 201], f"Ошибка входа! Код: {resp.status_code}"

some_client = TestWB() 
print(678)
