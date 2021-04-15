# ws-freemusicarchive

Script que realiza Web Scraping do site Free Music Archive que retorna lista por genero e busca as licenças desta lista, também possui um script que retorna um reusmo quantidade de musicas por tipo de Licença.

## Instruções

1. Python;
2. Requirements;
3. Estrutura de pastas;
4. Execute;

## Python

```bash
virtualenv -p python3 env
source env/bin/activate
```

## Requirements

```bash
pip install -r requirements.txt
```

## Estrutura de pastas

```bash
mkdir -p json/
```

## Execute

```lang-py
python listmusics.py
```
