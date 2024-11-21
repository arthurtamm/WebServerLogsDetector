## Sistema de Detecção de Ameaças Cibernéticas em Servidores Web

### Descrição do Projeto

Este projeto tem como objetivo desenvolver um sistema capaz de identificar e classificar ameaças cibernéticas em servidores web a partir de dados coletados. O sistema realiza diversas etapas:

- **Coleta de Dados**: Captura logs detalhados de acesso ao servidor web.
- **Pré-processamento**: Limpa e prepara os dados, removendo valores anômalos e gerando atributos relevantes.
- **Análise de Dados**: Implementa métodos de classificação para identificar requisições normais ou maliciosas.
- **Geração de Alertas**: Armazena os dados processados e gera alertas em tempo real, com uma interface web para visualização dos relatórios e atividades suspeitas.

### Estrutura do Repositório

O repositório possui os seguintes diretórios:

- `data/`
    - `logs.csv`: Dados brutos de treinamento.
    - `train.csv`: Dados processados para o treinamento do modelo.

- `logs/`
    - `send_benign_logs.py`: Script para enviar logs não maliciosos ao servidor.
    - `send_malicious_logs.py`: Script para enviar logs maliciosos ao servidor.

- `logs-frontend/`
    - Código do frontend da aplicação em React.

- `models/`
    - `random_forest`: Modelo treinado em formato pickle.

- `src/`
    - `preprocess.py`: Script de pré-processamento dos dados brutos.
    - `train.py`: Script para treinar o modelo de classificação.
    - `monitor.py`: Script que monitora os logs em tempo real e envia a classificação para o frontend.

- `venv/`
Ambiente virtual com as dependências do projeto.

### Configuração do Ambiente

#### 1. Criar e Ativar o Ambiente Virtual

Crie um ambiente virtual para o projeto:

```bash
python3 -m venv venv
```

Ative o ambiente virtual:

- No Linux/Mac:
```bash
source venv/bin/activate
```
- No Windows:
```bash
venv\Scripts\activate
```

#### 2. Instalar as Dependências

Instale as dependências necessárias usando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Preparação dos Dados e Treinamento do Modelo

#### 1. Pré-processamento dos Dados
Navegue até o diretório `src/` e execute o script `preprocess.py`:

```bash
cd src/
python preprocess.py
```

Este script irá:

- Ler os dados brutos de `data/logs.csv`.
- Aplicar transformações e extrações de features.
- Salvar os dados processados em `data/train.csv`.


#### 2. Treinamento do Modelo
Ainda no diretório `src/`, execute o script `train.py`:

```bash
python train.py
```

Este script irá:

- Ler os dados processados de `data/train.csv`.
- Treinar um modelo Random Forest com os dados.
- Salvar o modelo treinado em `models/random_forest`.

### Executando a Aplicação

#### 1. Iniciar o Frontend
Navegue até o diretório `logs-frontend/` e inicie o frontend da aplicação:

```bash
cd logs-frontend/
npm install
npm start
```
O frontend será executado em `http://localhost:3000`.

#### 2. Iniciar o Monitor de Logs

Em outro terminal, ative o ambiente virtual e execute o script `monitor.py`:

```bash
source venv/bin/activate  # Caso ainda não esteja ativado
cd src/
python monitor.py
```

O monitor:

- Observa o arquivo de log do Apache (`/var/log/apache2/access.log`).
- Processa novos logs em tempo real.
- Classifica os logs como maliciosos ou benignos.
- Envia os resultados para o frontend via WebSocket.

#### 3. Gerar Logs para Teste
Em outro terminal, escolha um dos scripts para gerar logs:

**a) Gerar Logs Benignos**

```bash
cd logs/
python send_benign_logs.py
```

**a) Gerar Logs Maliciosos**

```bash
cd logs/
python send_malicious_logs.py
```

Este script envia requisições simuladas maliciosas para o servidor.

`Dica`: Execute primeiro um dos geradores e, depois que este terminar de rodar, execute o outro para testar a classificação de ambos os tipos de logs.

### Testando a Aplicação

- Acesse o frontend em `http://localhost:3000`.
- Observe que os logs aparecem em tempo real com suas respectivas classificações.
- Verifique como o sistema classifica os logs gerados (benignos ou maliciosos).

### Considerações Importantes

- **Prioridade do Recall**: O modelo foi treinado priorizando o recall em relação à precisão. Isso significa que o sistema busca minimizar falsos negativos (logs maliciosos classificados como benignos). Portanto, é possível que alguns logs benignos sejam classificados como maliciosos.

- **Configuração do Servidor**: Certifique-se de que o servidor Apache está em execução e que o caminho do arquivo de log (`/var/log/apache2/access.log`) está correto. Caso contrário, ajuste o caminho no script `monitor.py`.

- **Endereço IP Local**: Os scripts de geração de logs (`send_benign_logs.py` e `send_malicious_logs.py`) detectam o IP local automaticamente. Verifique se o IP obtido corresponde ao do servidor onde o Apache está rodando.

#### Estrutura dos Dados
### Dados Brutos (`logs.csv`)

**Colunas**:

- `method`: Método HTTP da requisição (GET, POST, etc.).
- `URL`: URL acessada.
- `content`: Conteúdo da requisição (corpo).
- `accept`: Cabeçalho Accept da requisição.
- `host`: Host da requisição.
- `classification`: Classe da requisição (maliciosa ou não).


### Dados Processados (train.csv)

**Colunas**:

- `classification`: Classe da requisição (maliciosa ou não).

- `sql_injection`: Indica presença de padrões de SQL Injection.

- `xss_attack`: Indica presença de padrões de XSS.

- `path_traversal`: Indica presença de tentativas de Path Traversal.

- `hex_encoding`: Indica presença de codificações hexadecimais suspeitas.

- `param_count`: Número de parâmetros na URL.

- `accept_present`: Indica se o cabeçalho Accept está presente.

- `content_length`: Tamanho do conteúdo da requisição.

- `param_count_content`: Número de parâmetros no conteúdo.

- `method_GET`, `method_POST`, `method_PUT`: Codificação One-Hot dos métodos HTTP.