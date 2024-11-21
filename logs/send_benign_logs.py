import requests
import random
import time
from datetime import datetime, timedelta
import socket

# URL do servidor (substitua pelo endereço do seu servidor)
server_url = ""

# Headers comuns para parecer uma navegação legítima
common_headers = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
]

accept_headers = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "application/json, text/plain, */*",
    "image/avif,image/webp,image/apng,image/svg+xml,*/*;q=0.8",
    "*/*",
]

# Endpoints e métodos benignos
benign_endpoints = [
    {"endpoint": "/", "method": "GET"},  # Página inicial
    {"endpoint": "/admin", "method": "GET"},  # Painel administrativo
    {"endpoint": "/home", "method": "GET"},  # Página inicial do usuário autenticado
    {"endpoint": "/profile", "method": "GET"},  # Página de perfil do usuário
    {"endpoint": "/search", "method": "GET", "params": {"q": random.choice(["produtos", "carros", "cursos", "filmes"])}},  # Busca no site
    {"endpoint": "/contact", "method": "POST", "params": {"name": "John Doe", "message": "How can I help you?"}},  # Página de contato
    {"endpoint": "/products", "method": "GET"},  # Página de listagem de produtos
    {"endpoint": "/cart", "method": "GET"},  # Carrinho de compras
    {"endpoint": "/checkout", "method": "POST", "params": {"cart_id": "1234", "payment_method": "credit_card"}},  # Finalização de compras
    {"endpoint": "/api/data", "method": "GET", "params": {"type": "summary", "format": "json"}},  # API interna
]

# Função de tráfego legítimo (benigno)
def benign_request():
    """Gera requisições benignas simulando tráfego real no servidor e retorna o objeto requests."""
    # Escolhe um endpoint aleatório
    endpoint_data = random.choice(benign_endpoints)
    endpoint = endpoint_data["endpoint"]
    method = endpoint_data.get("method", "GET")
    params = endpoint_data.get("params", {})

    # Construir os headers
    headers = {
        "User-Agent": random.choice(common_headers),
        "Accept": random.choice(accept_headers),
    }

    url = f"{server_url}{endpoint}"

    # Enviar a requisição simulada
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=params)
        else:
            print(f"Método HTTP não suportado: {method}")
            return None
        return response
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar solicitação: {e}")
        return None

# Gerar tráfego contínuo
def generate_traffic(duration_minutes=5):
    end_time = datetime.now() + timedelta(minutes=duration_minutes)
    while datetime.now() < end_time:
        try:
            response = benign_request()
            if response:
                print(f"[Benign] Status: {response.status_code} - URL: {response.url}")
            
            # Pausa entre as solicitações (para parecer tráfego real)
            time.sleep(random.uniform(0.5, 2.0))
        except Exception as e:
            print(f"Erro ao enviar solicitação: {e}")

def get_local_ip():
    try:
        # Cria um socket temporário para determinar o IP local
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Conecta-se a um endereço público qualquer (não é feita uma conexão real)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]  # Obtém o endereço IP local associado
        return ip_address
    except Exception as e:
        print(f"Erro ao obter o IP local: {e}")
        return None
    
# Executar o gerador de tráfego
if __name__ == "__main__":
    local_ip = get_local_ip()
    if local_ip:
        print(f"IP local da rede: {local_ip}")
    else:
        print("Não foi possível obter o IP local.")
    server_url = f"http://{local_ip}/"  # Atualizar o URL do servidor com o IP local
    duration = 0.5  # Defina a duração em minutos
    print(f"Gerando tráfego por {duration} minutos...")
    generate_traffic(duration_minutes=duration)
    print("Tráfego gerado com sucesso.")
