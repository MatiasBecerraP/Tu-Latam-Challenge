import requests

def test_api():
    url = "https://api-gateway-url.amazonaws.com/endpoint"  # URL de tu API
    response = requests.get(url)
    assert response.status_code == 200  # Confirma que la API está respondiendo correctamente
    assert len(response.json()) > 0  # Confirma que la API está devolviendo datos
