# Classificador de Frutas com CNN

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Lite-orange?logo=tensorflow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-Deep%20Learning-red?logo=keras&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-013243?logo=numpy&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ARM%20Emulation-2496ED?logo=docker&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)

## Descricao do Projeto

Este projeto implementa um classificador de imagens de frutas utilizando Redes Neurais Convolucionais (CNN). O modelo foi treinado com Keras e convertido para TensorFlow Lite (TFLite) para execucao em sistemas embarcados.

O projeto utiliza Docker para simular um ambiente Linux ARM (arquitetura ARM v7), permitindo testar o modelo em condicoes similares a dispositivos embarcados como Raspberry Pi, sistemas IoT e outros dispositivos ARM.

## Estrutura do Projeto

```
fruit_classifier_cnn/
│
├── predict.py                      # Script de predicao
├── tutorial.txt                    # Tutorial de uso
│
├── trained_model/                  # Modelos treinados
│   ├── modelo_fruits.keras         # Modelo original Keras
│   ├── modelo_fruits.tflite        # Modelo TFLite padrao
│   ├── modelo_fruits_compat.tflite # Modelo TFLite compativel ARM
│   ├── labels.json                 # Labels originais
│   └── labels_traduzidas.json      # Labels em portugues
│
└── training/                       # Notebook de treinamento
    └── fruit_classifier_cnn.ipynb
```

## Requisitos

### No Windows (Host)

- Docker Desktop instalado e configurado
- Windows PowerShell

### No Container (Linux ARM)

As dependencias serao instaladas automaticamente seguindo o tutorial abaixo.

## Como Usar

### Passo 1: Comando Magico (Resetar Emulador)

Se voce reiniciou o PC ou o Docker, rode isso antes de tudo para garantir que o Windows entenda o sistema ARM.

```powershell
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
```

**O que este comando faz:** Configura o QEMU para permitir que o Docker execute containers ARM em sistemas x86/x64.

### Passo 2: Limpar e Criar o Container (Com a Nova Pasta)

Como mudou o caminho, vamos apagar o container antigo (se existir) e criar um novo apontando para a pasta do projeto.

```powershell
# 1. Remove o container antigo
docker rm -f tflite_arm

# 2. Cria o novo mapeando sua pasta do Desktop para dentro do Linux
docker run -it --platform linux/arm/v7 --name tflite_arm -v "C:\Users\Jonas\Desktop\fruit_classifier_cnn:/home/fruit_project" debian:bullseye /bin/bash
```

**Explicacao:**
- `--platform linux/arm/v7`: Especifica arquitetura ARM v7 (sistemas embarcados)
- `--name tflite_arm`: Nome do container
- `-v "C:\Users\Jonas\Desktop\fruit_classifier_cnn:/home/fruit_project"`: Mapeia a pasta do Windows para dentro do container Linux
- `debian:bullseye`: Imagem base Debian (leve e compativel)

**Nota:** A pasta interna no container se chama `/home/fruit_project`.

### Passo 3: Instalar Dependencias (Copie e Cole)

Ja que estamos em um container novo, precisamos instalar o ambiente. Copie tudo abaixo e cole no terminal do Linux (`root@...:/#`):

```bash
apt-get update && \
apt-get install -y python3 python3-pip python3-venv build-essential python3-numpy python3-pil && \
python3 -m venv --system-site-packages tflite_venv && \
source tflite_venv/bin/activate && \
pip install --no-build-isolation --no-deps tflite-runtime==2.7.0
```

**O que este comando faz:**
- Atualiza lista de pacotes do Debian
- Instala Python 3, pip, ambiente virtual e bibliotecas necessarias (NumPy, PIL)
- Cria ambiente virtual Python
- Ativa o ambiente virtual
- Instala TensorFlow Lite Runtime (versao leve para inferencia)

### Passo 4: Rodar a Predicao

Dentro do terminal do Linux (que voce abriu no Passo 2):

```bash
# 1. Ative o ambiente (se nao aparecer (tflite_venv) antes do prompt)
source tflite_venv/bin/activate

# 2. Entre na pasta do projeto
cd /home/fruit_project

# 3. Rode o script de predicao
python3 predict.py
```

### Resultado Esperado

O script ira analisar a imagem especificada (por padrao `banana.png`) e retornar:

```
Predicao: Banana
Confianca: 98.75%

Top 3 predicoes:
1. Banana: 98.75%
2. Manga: 0.89%
3. Morango: 0.36%
```

## Testando Outras Imagens

Para testar com outras imagens, edite o arquivo `predict.py` e altere a linha:

```python
image_path = 'banana.png'
```

Para uma das imagens disponiveis:
- `banana.png`
- `maca.png`
- `Morango.png`
- `manga.png` (dentro da pasta `images/`)

Ou adicione suas proprias imagens na pasta do projeto.

## Por Que Docker com ARM?

O Docker configurado com `--platform linux/arm/v7` simula um ambiente Linux de arquitetura ARM, comum em:

- Raspberry Pi
- Sistemas embarcados IoT
- Dispositivos moveis
- Cameras inteligentes
- Sistemas industriais

Isso permite testar e validar que o modelo TFLite funciona corretamente em dispositivos com recursos limitados antes de fazer o deploy real.

## Tecnologias Utilizadas

- **Python 3**: Linguagem principal
- **TensorFlow Lite**: Framework de inferencia otimizado
- **Keras**: Treinamento do modelo original
- **NumPy**: Processamento numerico
- **PIL (Pillow)**: Processamento de imagens
- **Docker**: Containerizacao e emulacao ARM
- **QEMU**: Emulador de arquitetura ARM

## Observacoes Importantes

### Sessoes Futuras

Se voce fechar o terminal ou sair do container, para voltar:

```powershell
# Inicia o container novamente
docker start tflite_arm

# Conecta ao container
docker exec -it tflite_arm /bin/bash

# Ativa o ambiente virtual
source tflite_venv/bin/activate

# Navega para a pasta do projeto
cd /home/fruit_project
```

### Solucao de Problemas

**Erro: "exec user process caused: exec format error"**
- Execute novamente o Passo 1 (comando magico do QEMU)

**Erro: "No such file or directory" ao rodar predict.py**
- Verifique se esta na pasta correta: `cd /home/fruit_project`
- Verifique se o ambiente virtual esta ativo: `source tflite_venv/bin/activate`

**Container nao inicia**
- Remova e recrie: `docker rm -f tflite_arm` e execute novamente o Passo 2

## Licenca

Projeto educacional para demonstracao de classificacao de imagens em sistemas embarcados.
