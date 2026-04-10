# Servicios SIG - Taller 2
## Sistema Completo de Visualización y Gestión de Datos Geoespaciales

Sistema integrado que combina PostgreSQL/PostGIS, GeoServer y una aplicación web Python/Flask con Folium para la visualización y gestión de datos geoespaciales de un departamento en Colombia.

## Servicios Disponibles

| Servicio | Puerto | URL | Credenciales |
|----------|--------|-----|--------------|
| **WebApp (Flask/Folium)** | 5000 | http://localhost:5000 | - |
| **GeoServer** | 8080 | http://localhost:8080/geoserver | admin/geoserver |
| **PostgreSQL/PostGIS** | 5432 | localhost:5432 | postgres/postgres |

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                      Usuario / Cliente                      │
└──────┬────────────────────┬────────────────────┬────────────┘
       │                    │                    │
       ▼                    ▼                    ▼
┌─────────────┐   ┌──────────────────┐   ┌──────────────────┐
│   WebApp    │   │   GeoServer      │   │  PostgreSQL      │
│  (Flask)    │   │   (WMS/WFS)      │   │  (PostGIS)       │
│             │   │                  │   │                  │
│ - Folium    │   │ - REST API       │   │ - geodatos DB    │
│ - Bootstrap │   │ - Web UI         │   │ - GDAL           │
│ - API REST  │   │ - Capas          │   │ - 2 Tablas       │
└──────┬──────┘   └────────┬─────────┘   └─────────┬────────┘
       │                   │                       │
       └───────────────────┴───────────────────────┘
                  Docker Network
```

## Estructura del Proyecto

```
Servicios_SIG_Taller/
├── docker-compose.yml           # Orquestación de servicios
├── Dockerfile.postgis           # Imagen personalizada PostGIS + GDAL
├── Dockerfile.webapp            # Imagen personalizada Python Flask
│
├── data/
│   └── geopackage/
│       └── amazonas.gpkg        # Datos geoespaciales fuente
|   └── shapefiles/                # (Opcional) Otros datos espaciales
│
├── init-scripts/
│   ├── 01-init-postgis.sh       # Habilita extensiones PostGIS
│   └── 02-import-geopackage.sh  # Importa datos del GeoPackage
│
├── webapp/
│   ├── app.py                   # Aplicación Flask principal
│   ├── requirements.txt         # Dependencias Python
│   ├── templates/
│   │   └── index.html           # Interfaz web
│   │   └── visor.html           # Mapa embebido│
│   ├── static/
│   │   └── css/style.css       # Estilos personalizados
│   └── README.md               # Documentación webapp
│
├── GUIA_COMPLETA.md            # Guía detallada paso a paso
├── VERIFICACION.md             # Guía rápida de verificación
└── README.md                   # Este archivo
```

## Datos Geoespaciales

### Tablas en PostgreSQL/PostGIS

| Tabla | Geometría | SRID | Registros | Descripción |
|-------|-----------|------|-----------|-------------|
| `dpto_amazonas` | MultiPolygon | 4686 | 1 | Límites del departamento |
| `puntos_administrativos` | PointZ | 900914 | 131 | Puntos administrativos |

### Características Espaciales

- **Extensiones PostGIS:** postgis, postgis_topology, fuzzystrmatch, postgis_tiger_geocoder
- **GDAL Version:** 3.2.2
- **Índices Espaciales:** GIST en todas las geometrías
- **Sistema de Coordenadas:** Múltiples SRID soportados

## Inicio Rápido

### Prerequisitos

- Docker (20.10+)
- Docker Compose (2.0+)
- 4GB RAM disponibles
- 10GB espacio en disco
- Puertos libres: 5000, 5432, 8080

### Instalación

```bash
# 1. Clonar o navegar al directorio del proyecto
cd Servicios_SIG_Taller

# 2. Construir las imágenes
docker-compose build

# 3. Iniciar todos los servicios
docker-compose up -d

# 4. Verificar que los servicios estén corriendo
docker-compose ps
```

### Verificar Instalación

```bash
# Ver logs de PostgreSQL para verificar importación de datos
docker logs postgis | grep "importadas"

# Verificar tablas en la base de datos
docker exec postgis psql -U postgres -d geodatos -c "\dt"

# Verificar conteo de registros
docker exec postgis psql -U postgres -d geodatos -c "
SELECT 'dpto_amazonas' as tabla, COUNT(*) FROM dpto_amazonas
UNION ALL
SELECT 'puntos_administrativos', COUNT(*) FROM puntos_administrativos;"
```

**Salida esperada:**
```
         tabla          | count
------------------------+-------
 dpto_amazonas          |     1
 puntos_administrativos |   131
```

## Acceso a los Servicios

### 1. Aplicación Web (WebApp)

**URL:** http://localhost:5000

**Características:**
- Mapa interactivo con Folium
- Visualización del departamento del Amazonas
- Marcadores de puntos administrativos con clustering
- Estadísticas en tiempo real
- API RESTful
- Interfaz responsiva con Bootstrap

**Endpoints API:**
- `GET /` - Interfaz web principal
- `GET /mapa` - Mapa embebido
- `GET /api/estadisticas` - Estadísticas generales
- `GET /api/departamento` - Datos del departamento
- `GET /api/puntos` - Lista de puntos administrativos
- `GET /health` - Health check

**Ejemplo de uso de API:**
```bash
# Obtener estadísticas
curl http://localhost:5000/api/estadisticas

# Obtener puntos administrativos
curl http://localhost:5000/api/puntos | jq
```

### 2. GeoServer

**URL:** http://localhost:8080/geoserver
**Usuario:** admin
**Contraseña:** geoserver

**Configuración inicial:**
1. Ir a "Stores" → "Add new Store"
2. Seleccionar "PostGIS"
3. Configurar conexión:
   - host: `postgis`
   - port: `5432`
   - database: `geodatos`
   - user: `postgres`
   - password: `postgres`

### 3. PostgreSQL/PostGIS

**Conexión desde herramientas externas:**

```bash
# psql
psql -h localhost -U postgres -d geodatos

# QGIS
# Host: localhost
# Port: 5432
# Database: geodatos
# Username: postgres
# Password: postgres
```

**Python:**
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="geodatos",
    user="postgres",
    password="postgres"
)
```

## 🔧 Comandos Útiles

### Gestión de Servicios

```bash
# Iniciar todos los servicios
docker-compose up -d

# Detener todos los servicios
docker-compose down

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker logs -f webapp
docker logs -f postgis
docker logs -f geoserver

# Reiniciar un servicio
docker-compose restart webapp

# Ver estado de los servicios
docker-compose ps
```

### Gestión de Datos

```bash
# Backup de la base de datos
docker exec postgis pg_dump -U postgres geodatos > backup_$(date +%Y%m%d).sql

# Restaurar backup
docker exec -i postgis psql -U postgres geodatos < backup_20251107.sql

# Acceder a psql interactivo
docker exec -it postgis psql -U postgres -d geodatos

# Ver información del GeoPackage
docker exec postgis ogrinfo /geopackage/amazonas.gpkg
```

### Reinicialización Completa

```bash
# ESTO BORRARÁ TODOS LOS DATOS

# 1. Detener servicios
docker-compose down

# 2. Eliminar volúmenes
docker volume rm servicios_sig_taller_postgres_data
docker volume rm servicios_sig_taller_geoserver_data

# 3. Reiniciar desde cero
docker-compose up -d
```

## Desarrollo

### Modificar la Aplicación Web

Los cambios en el código de la webapp se reflejan automáticamente gracias al volume mount:

```bash
# Editar archivos en ./webapp/
# Los cambios se recargan automáticamente (Flask debug mode)

# Si modificas requirements.txt:
docker-compose stop webapp
docker-compose build webapp
docker-compose up -d webapp
```

### Agregar Nuevas Funcionalidades

**Ejemplo: Nuevo endpoint en la API**

```python
# Editar webapp/app.py

@app.route('/api/mi-nuevo-endpoint')
def mi_nuevo_endpoint():
    """Nueva funcionalidad"""
    # Tu código aquí
    return jsonify({'mensaje': 'Hola'})
```

Los cambios se aplican automáticamente en modo desarrollo.

## Monitoreo

### Script de Monitoreo

```bash
#!/bin/bash
# monitor.sh

echo "=== Estado de Servicios ==="
docker-compose ps

echo -e "\n=== Uso de Recursos ==="
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo -e "\n=== Datos en PostgreSQL ==="
docker exec postgis psql -U postgres -d geodatos -c "
SELECT 'dpto_amazonas' as tabla, COUNT(*) FROM dpto_amazonas
UNION ALL
SELECT 'puntos_administrativos', COUNT(*) FROM puntos_administrativos;"

echo -e "\n=== Health Checks ==="
curl -s http://localhost:5000/health | jq
curl -s -I http://localhost:8080/geoserver | head -1
```

## Solución de Problemas

### WebApp no inicia

```bash
# Ver logs
docker logs webapp

# Verificar conectividad con PostgreSQL
docker exec webapp ping -c 3 postgis

# Reconstruir imagen
docker-compose build --no-cache webapp
docker-compose up -d webapp
```

### PostgreSQL no importa datos

```bash
# Verificar logs de inicialización
docker logs postgis | grep -A 10 "import"

# Si dice "Skipping initialization", reinicializar:
docker-compose down
docker volume rm servicios_sig_taller_postgres_data
docker-compose up -d
```

### GeoServer no conecta con PostgreSQL

1. Verificar que PostgreSQL esté healthy:
   ```bash
   docker ps | grep postgis
   ```

2. En GeoServer, usar `postgis` como host (no `localhost`)

3. Verificar credenciales: `postgres` / `postgres`

## Documentación

- **[GUIA_COMPLETA.md](GUIA_COMPLETA.md)** - Guía detallada con prerequisitos, instalación paso a paso, troubleshooting
- **[VERIFICACION.md](VERIFICACION.md)** - Guía rápida de verificación
- **[webapp/README.md](webapp/README.md)** - Documentación específica de la aplicación web

## Seguridad

**IMPORTANTE:** Las credenciales por defecto NO son seguras para producción.

**Para producción:**

1. Crear archivo `.env`:
```bash
DB_PASSWORD=TuPasswordSeguro123!
GS_PASSWORD=OtroPasswordSeguro456!
```

2. Actualizar `docker-compose.yml`:
```yaml
environment:
  - POSTGRES_PASSWORD=${DB_PASSWORD}
  - GEOSERVER_ADMIN_PASSWORD=${GS_PASSWORD}
```

3. Agregar `.env` a `.gitignore`

## Contribuir

1. Fork el repositorio
2. Crear rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Agrega nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## Licencia

Este proyecto es parte del curso de Servicios SIG - Universidad Juan de Castellanos.

## Autor

Universidad Juan de Castellanos - Servicios SIG Taller 2

---

**Última actualización:** 2025-11-07
**Versión:** 1.0.0

## Recursos Adicionales

- [PostGIS Documentation](https://postgis.net/documentation/)
- [GeoServer Documentation](https://docs.geoserver.org/)
- [Folium Documentation](https://python-visualization.github.io/folium/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
