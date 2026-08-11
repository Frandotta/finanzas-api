# API de Finanzas Personales

API REST para gestión de finanzas personales, con autenticación de usuarios, categorización de ingresos/gastos y reportes de balance. Desarrollada como proyecto de portfolio con la intencion de demostrar habilidades de backend.

## Stack tecnológico

- **Python 3.14**
- **FastAPI** — framework para construir la API
- **Uvicorn** — servidor ASGI
- **PostgreSQL 18** — base de datos
- **SQLAlchemy** — ORM
- **Pydantic** — validación de datos
- **passlib + bcrypt** — encriptación de contraseñas
- **python-jose** — generación y validación de tokens JWT
- **python-dotenv** — manejo de variables de entorno

## Características

- Registro y login de usuarios con autenticación JWT
- Contraseñas encriptadas con bcrypt 
- Categorías de ingresos/gastos personalizables
- Registro de transacciones asociadas a cada usuario
- Reporte de balance (ingresos vs gastos) calculado
- Autorización a nivel de datos: cada usuario solo accede a su propia información

## Cómo correrlo localmente

### Requisitos previos
- Python 3.11+
- PostgreSQL instalado y corriendo

### Instalación

1. Cloná el repositorio:
```bash
git clone https://github.com/Frandotta/finanzas-api.git
cd finanzas-api
```

2. Creá y activá un entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

3. Instalá las dependencias:
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic passlib bcrypt==4.0.1 python-jose python-dotenv
```

4. Creá una base de datos en PostgreSQL llamada `finanzas` (o el nombre que prefieras).

5. Creá un archivo `.env` en la raíz del proyecto con:
DATABASE_URL=postgresql://usuario:password@localhost/finanzas
SECRET_KEY=una_clave_secreta_random_y_larga

Para generar una `SECRET_KEY` random, podés correr:
```python
import secrets
print(secrets.token_hex(32))
```

6. Levantá el servidor:
```bash
uvicorn main:app --reload
```

7. Abrí la documentación interactiva en `http://127.0.0.1:8000/docs`

## Endpoints disponibles

| Método | Ruta | Protegido | Descripción |
|--------|------|-----------|-------------|
| GET | `/ping` | No | Healthcheck de la API |
| POST | `/registro` | No | Crea un usuario nuevo |
| POST | `/login` | No | Inicia sesión y devuelve un JWT |
| POST | `/categorias` | Sí | Crea una categoría (ingreso o gasto) |
| GET | `/categorias` | Sí | Lista todas las categorías |
| POST | `/transacciones` | Sí | Crea una transacción |
| GET | `/transacciones` | Sí | Lista las transacciones del usuario logueado |
| GET | `/reportes/resumen` | Sí | Devuelve total de ingresos, gastos y balance del usuario |

Los endpoints protegidos requieren el header `Authorization: Bearer <token>`, obtenido desde `/login`.

## Decisiones de diseño

- **Separación en capas** (`models`, `routers`, `auth`, `database`): cada archivo tiene una responsabilidad clara, facilitando mantenimiento y testing.
- **JWT vía `HTTPBearer`**: en vez de `OAuth2PasswordBearer`, se usa un esquema de autenticación simple basado en Bearer token, para un login custom body JSON.
- **Autorización a nivel de datos**: todas las consultas de transacciones filtran explícitamente por el usuario autenticado, evitando que un usuario acceda a datos de otro.
- **Variables de entorno**: credenciales de base de datos y clave de firma JWT nunca están hardcodeadas en el código.

##  Futuras mejoras 

- `PUT /transacciones/{id}` y `DELETE /transacciones/{id}`
- `GET /reportes/por-categoria` (gastos agrupados por categoría)
- Tests automatizados con pytest
- Deploy en Render con documentación pública en `/docs`


Francisco Dottavio — Analista de Sistemas (UNNOBA)
[LinkedIn](www.linkedin.com/in/franciscodottavio) · [GitHub](https://github.com/Frandotta)