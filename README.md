# Portfolio Backend API

Backend del portfolio profesional construido con **FastAPI**, **SQLAlchemy 2.x**, **PostgreSQL/PostGIS**, **Alembic** y arquitectura por capas.

## Stack

- Python 3.12+
- FastAPI + Pydantic v2
- SQLAlchemy 2.x + GeoAlchemy2 (PostGIS)
- Alembic
- Docker / docker-compose
- pytest

## Arquitectura

```
endpoint/router → service → repository → database
```

| Capa | Responsabilidad |
|------|-----------------|
| `api/v1/endpoints` | HTTP, validación de entrada, respuestas |
| `services` | Lógica de negocio |
| `repositories` | Acceso a datos |
| `models` | Entidades SQLAlchemy |
| `schemas` | DTOs Pydantic |
| `core` | Configuración, DB, errores, logging, seguridad |

## Requisitos

- Docker y Docker Compose (recomendado), o
- Python 3.12+ y PostgreSQL con PostGIS

## Inicio rápido con Docker

1. Copiar variables de entorno:

```bash
cp .env.example .env
```

2. Levantar servicios:

```bash
docker compose up --build
```

3. La API quedará disponible en:

- Swagger UI: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health
- Health DB: http://localhost:8000/api/v1/health/db

El contenedor `api` ejecuta automáticamente `alembic upgrade head` al iniciar.

## Desarrollo local (sin Docker)

1. Crear entorno virtual e instalar dependencias:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Configurar `.env` desde `.env.example`.

3. Asegurar PostgreSQL con PostGIS y ejecutar migraciones:

```bash
alembic upgrade head
```

4. Iniciar servidor:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Migraciones (Alembic)

Crear nueva migración:

```bash
alembic revision --autogenerate -m "descripcion del cambio"
```

Aplicar migraciones:

```bash
alembic upgrade head
```

Revertir última migración:

```bash
alembic downgrade -1
```

La migración inicial (`001`) habilita la extensión **PostGIS** y crea todas las tablas, incluyendo `project_locations` con geometría `POINT` SRID 4326.

## Tests

```bash
pytest
```

Los tests iniciales cubren healthcheck y validación de contacto sin requerir base de datos para todos los casos.

## Variables de entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `APP_NAME` | Nombre de la API | Portfolio API |
| `APP_VERSION` | Versión | 0.1.0 |
| `DEBUG` | Modo debug | false |
| `ENVIRONMENT` | Entorno | development |
| `API_V1_PREFIX` | Prefijo API | /api/v1 |
| `POSTGRES_HOST` | Host PostgreSQL | localhost |
| `POSTGRES_PORT` | Puerto PostgreSQL | 5432 |
| `POSTGRES_USER` | Usuario | portfolio |
| `POSTGRES_PASSWORD` | Contraseña | portfolio |
| `POSTGRES_DB` | Base de datos | portfolio |
| `DATABASE_URL` | URL completa (opcional) | — |
| `CORS_ORIGINS` | Orígenes CORS separados por coma | localhost:3000,5173 |
| `LOG_LEVEL` | Nivel de logging | INFO |
| `SECRET_KEY` | Clave para futura auth admin | change-me-in-production |

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/health` | Health de la app |
| GET | `/api/v1/health/db` | Health de PostgreSQL |
| GET | `/api/v1/projects` | Listar proyectos |
| GET | `/api/v1/projects/featured` | Proyectos destacados |
| GET | `/api/v1/projects/{slug}` | Detalle por slug |
| POST | `/api/v1/projects` | Crear proyecto |
| PUT | `/api/v1/projects/{id}` | Actualizar proyecto |
| DELETE | `/api/v1/projects/{id}` | Eliminar proyecto |
| GET | `/api/v1/technologies` | Listar tecnologías |
| POST | `/api/v1/technologies` | Crear tecnología |
| GET | `/api/v1/dashboards` | Listar dashboards |
| GET | `/api/v1/dashboards/{id}` | Detalle dashboard |
| POST | `/api/v1/dashboards` | Crear dashboard |
| GET | `/api/v1/notebooks` | Listar notebooks |
| GET | `/api/v1/notebooks/{id}` | Detalle notebook |
| POST | `/api/v1/notebooks` | Crear notebook |
| POST | `/api/v1/contact` | Enviar mensaje de contacto |

## Formato de respuesta

Éxito:

```json
{
  "success": true,
  "data": {},
  "message": "Operación realizada correctamente",
  "error": null
}
```

Error:

```json
{
  "success": false,
  "data": null,
  "message": "Error al procesar la solicitud",
  "error": {
    "code": "ERROR_CODE",
    "detail": "Detalle técnico o validación"
  }
}
```

## GIS (preparado)

- PostGIS habilitado desde la migración inicial.
- Modelo `ProjectLocation` con `geom` tipo `POINT` (EPSG:4326).
- Endpoints GIS específicos se pueden agregar en futuras iteraciones.

## Próximos pasos sugeridos

- Autenticación admin en `core/security.py`
- Filtros y paginación en listados
- Seeds de datos iniciales
- Endpoints GIS para ubicaciones de proyectos
