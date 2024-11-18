import pandas as pd
import random

# Funções de geração para cada tipo de ataque
def generate_sql_injection():
    methods = ["GET", "POST"]
    urls = [
        "/publico/login.jsp?username=admin' OR '1'='1' --&password=pass",
        "/products/search.jsp?query=DROP TABLE users;--",
        "/account/view.jsp?id=5 UNION SELECT * FROM users",
    ]
    contents = [
        "username=admin' OR '1'='1' --",
        "item_id=5 UNION SELECT credit_card_number FROM users",
        "product_name='; DROP TABLE orders;--",
    ]
    accepts = ["*/*", "text/html,application/xhtml+xml,application/xml;q=0.9"]
    hosts = ["192.168.100.121", "192.168.100.122"]

    return {
        "Method": random.choice(methods),
        "URL": random.choice(urls),
        "content": random.choice(contents),
        "Accept": random.choice(accepts),
        "host": random.choice(hosts),
        "classification": 1,
    }

def generate_xss_attack():
    methods = ["GET", "POST"]
    urls = [
        "/search?q=<script>alert('XSS')</script>",
        "/publico/submit_form.jsp?input=<img src='x' onerror='alert(1)'>",
        "/comments/add.jsp?comment=<svg onload=alert(1)>",
    ]
    contents = [
        "comment=<script>alert('attack')</script>",
        "data=<img src=x onerror=alert('XSS')>",
        "<iframe src=javascript:alert('XSS')>",
    ]
    accepts = ["*/*", "text/html,application/xhtml+xml,application/xml;q=0.9"]
    hosts = ["192.168.100.121", "192.168.100.122"]

    return {
        "Method": random.choice(methods),
        "URL": random.choice(urls),
        "content": random.choice(contents),
        "Accept": random.choice(accepts),
        "host": random.choice(hosts),
        "classification": 1,
    }

def generate_path_traversal():
    methods = ["GET"]
    urls = [
        "/images/../../../../etc/passwd",
        "/account/view.jsp?user=../../admin/config",
        "/public/docs/../../../windows/system32/drivers/etc/hosts",
    ]
    contents = ["path=../../../../etc/shadow", "file=../../../boot.ini", "doc=../../confidential.pdf"]
    accepts = ["*/*", "text/html,application/xhtml+xml,application/xml;q=0.9"]
    hosts = ["192.168.100.121", "192.168.100.122"]

    return {
        "Method": random.choice(methods),
        "URL": random.choice(urls),
        "content": random.choice(contents),
        "Accept": random.choice(accepts),
        "host": random.choice(hosts),
        "classification": 1,
    }

def generate_hex_encoding():
    methods = ["GET"]
    urls = [
        "/login.jsp?username=%27%20OR%20%271%27%3D%271",
        "/publico/update.jsp?name=admin%27--",
        "/admin/edit.jsp?data=%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E",
    ]
    contents = [
        "id=%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "data=%3Cscript%3Ealert(%27XSS%27)%3C%2Fscript%3E",
        "product=%27%20OR%20%271%27%3D%271",
    ]
    accepts = ["*/*", "text/html,application/xhtml+xml,application/xml;q=0.9"]
    hosts = ["192.168.100.121", "192.168.100.122"]

    return {
        "Method": random.choice(methods),
        "URL": random.choice(urls),
        "content": random.choice(contents),
        "Accept": random.choice(accepts),
        "host": random.choice(hosts),
        "classification": 1,
    }

# Gerar exemplos de logs
def generate_attack_logs(num_samples=10):
    logs = []
    for _ in range(num_samples):
        attack_type = random.choice(["sql_injection", "xss_attack", "path_traversal", "hex_encoding"])
        if attack_type == "sql_injection":
            logs.append(generate_sql_injection())
        elif attack_type == "xss_attack":
            logs.append(generate_xss_attack())
        elif attack_type == "path_traversal":
            logs.append(generate_path_traversal())
        elif attack_type == "hex_encoding":
            logs.append(generate_hex_encoding())
    return pd.DataFrame(logs)

# Gerar e exibir exemplos de logs maliciosos
malicious_logs = generate_attack_logs(10000)
# print(malicious_logs)
malicious_logs.to_csv("malicious_logs.csv", index=False)
