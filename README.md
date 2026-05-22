# Password Generator Pro

Generador de contrasenas seguras con analisis de entropia y evaluacion de fortaleza en tiempo real.

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-18%20passed-brightgreen.svg)](tests/)

---

## Descripcion

**Problema que resuelve:** Las herramientas de generacion online envian datos por red o usan generadores no criptograficos.

**Como lo resuelve:** Genera contrasenas localmente con el modulo `secrets` de Python (CSPRNG del sistema operativo), evalua su fortaleza calculando entropia en bits, y permite copiar al portapapeles sin tocar la red.

**Para quien es:** Desarrolladores, administradores de sistemas, y cualquier persona que necesite generar contrasenas seguras.

---

## Instalacion

```bash
git clone https://github.com/hyperiumia/password-generator.git
cd password-generator
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Uso

```bash
python main.py
python main.py -n 5 -l 24
python main.py --pronounceable -l 20
python main.py -l 32 --copy
```

### Parametros

| Parametro | Descripcion | Default |
|-----------|-------------|---------|
| `-n, --count` | Numero de contrasenas | 1 |
| `-l, --length` | Longitud | 16 |
| `--no-upper` | Excluir mayusculas | False |
| `--no-lower` | Excluir minusculas | False |
| `--no-digits` | Excluir numeros | False |
| `--no-symbols` | Excluir simbolos | False |
| `--pronounceable` | Modo pronunciable | False |
| `--copy` | Copiar al portapapeles | False |

---

## Decisiones Tecnicas

| Decision | Alternativas | Eleccion | Razon |
|----------|-------------|----------|-------|
| Generador | random, secrets | secrets | CSPRNG seguro del SO |
| CLI | argparse, click | argparse | Sin dependencias |
| Terminal | print, rich | rich | Visualizacion profesional |
| Clipboard | pyperclip, subprocess | pyperclip | Cross-platform |

Ver `docs/adr/001-secrets-vs-random.md` para analisis detallado.

---

## Estructura del Proyecto

```
password-generator/
  main.py              # Punto de entrada
  src/
    generator.py       # Motor criptografico
    analyzer.py        # Evaluacion de entropia
    cli.py             # Interfaz CLI
    config.py          # Constantes
  tests/
    test_generator.py  # 11 tests
    test_analyzer.py   # 7 tests
  docs/adr/
  README.md
  requirements.txt
  .gitignore
  LICENSE
```

---

## Tests

```bash
pytest tests/ -v
# 18 passed in 0.07s
```

---

## Stack

Python 3.12 | secrets | rich | pyperclip | pytest

---

## Posibles Mejoras

- GUI con CustomTkinter
- Generacion de passphrase (diccionario EFF)
- Exportar contrasenas encriptadas (AES-256)
- Modo batch desde archivo YAML

---

## Licencia

MIT License

---

## Autor

**Patricio Tirado** - [Hyperium IA](https://www.hyperiumia.com)

[![GitHub](https://img.shields.io/badge/GitHub-hyperiumia-black.svg?style=flat&logo=github)](https://github.com/hyperiumia)
[![Website](https://img.shields.io/badge/Web-hyperiumia.com-FF6B00.svg?style=flat&logo=google-chrome&logoColor=white)](https://www.hyperiumia.com)