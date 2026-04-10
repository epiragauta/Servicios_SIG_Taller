# Guía Completa: PostgreSQL/PostGIS con GeoServer e Importación de GeoPackage

## Tabla de Contenidos

1. [Prerequisitos](#prerequisitos)
2. [Descripción del Sistema](#descripción-del-sistema)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Instalación Paso a Paso](#instalación-paso-a-paso)
5. [Verificación de la Instalación](#verificación-de-la-instalación)
6. [Conexión y Uso](#conexión-y-uso)
7. [Consideraciones Importantes](#consideraciones-importantes)
8. [Solución de Problemas Comunes](#solución-de-problemas-comunes)
9. [Comandos Útiles](#comandos-útiles)
10. [Mantenimiento](#mantenimiento)

---

## Prerequisitos

### Software Requerido

| Software | Versión Mínima | Propósito |
|----------|---------------|-----------|
| **Docker** | 20.10+ | Motor de contenedores |
| **Docker Compose** | 2.0+ | Orquestación de servicios |
| **Git** | 2.0+ | Control de versiones (opcional) |

### Requisitos del Sistema

- **Sistema Operativo:** Windows 10/11, Linux, macOS
- **RAM:** Mínimo 4GB disponibles (recomendado 8GB)
- **Espacio en Disco:** Mínimo 10GB libres
- **Puertos Disponibles:** 5432 (PostgreSQL), 8080 (GeoServer)

### Verificar Prerequisitos

```bash
# Verificar Docker
docker --version
docker ps

# Verificar Docker Compose
docker-compose --version

# Verificar puertos disponibles (Linux/Mac)
netstat -tuln | grep -E '5432|8080'

# Verificar puertos disponibles (Windows PowerShell)
netstat -ano | findstr ":5432 :8080"
```

### Datos Requeridos

- **Archivo GeoPackage:** `data/geopackage/amazonas.gpkg`
  - Debe contener las capas: `dpto_amazonas` y `puntos_administrativos`
  - Formato: GeoPackage (.gpkg)
  - Ubicación: Relativa al directorio del proyecto

---

## Descripción del Sistema

### Arquitectura

```
┌──────────────────────────────────────────────────┐
│                   Usuario                        │
└────────────┬────────────────────┬────────────────┘
             │                    │
             ▼                    ▼
    ┌─────────────────┐  ┌─────────────────┐
    │   GeoServer     │  │   PostgreSQL    │
    │   Puerto: 8080  │  │   Puerto: 5432  │
    │                 │  │                 │
    │   - Web UI      │  │   - PostGIS     │
    │   - REST API    │  │   - GDAL        │
    │   - WMS/WFS     │  │   - geodatos DB │
    └────────┬────────┘  └────────┬────────┘
             │                    │
             └──────────┬─────────┘
                        │
                        ▼
             ┌──────────────────────┐
             │  Docker Network      │
             └──────────────────────┘
```

### Servicios

#### 1. PostgreSQL/PostGIS
- **Imagen Base:** `postgis/postgis:16-3.4`
- **Extensiones:** PostGIS, GDAL 3.2.2
- **Base de datos:** `geodatos`
- **Puerto:** 5432
- **Volúmenes:**
  - `postgres_data` → Persistencia de datos
  - `./data/geopackage` → Archivos GeoPackage
  - `./init-scripts` → Scripts de inicialización

#### 2. GeoServer
- **Imagen:** `docker.osgeo.org/geoserver:2.24.0`
- **Puerto:** 8080
- **Credenciales:** admin/geoserver
- **Memoria:** 2GB inicial, 4GB máxima
- **Volúmenes:**
  - `geoserver_data` → Configuraciones y capas
  - `./data` → Archivos Shapefiles

---

## Estructura del Proyecto

```
Servicios_SIG_Taller/
│
├── docker-compose.yml              # Orquestación de servicios
├── Dockerfile.postgis              # Imagen personalizada PostGIS + GDAL
│
├── data/
│   ├── geopackage/
│   │   └── amazonas.gpkg          # Archivo GeoPackage fuente
│   └── shapefiles/                # (Opcional) Otros datos espaciales
│
├── init-scripts/
│   ├── 01-init-postgis.sh         # Habilita extensiones PostGIS
│   └── 02-import-geopackage.sh    # Importa capas del GeoPackage
│
├── GUIA_COMPLETA.md               # Esta guía
└── VERIFICACION.md                # Guía rápida de verificación
```

---

## Instalación Paso a Paso

### Paso 1: Clonar o Descargar el Proyecto

```bash
# Si usas Git
cd /ruta/donde/quieres/el/proyecto
git clone <url-del-repositorio>
cd Servicios_SIG_Taller

# Si descargaste un ZIP
cd C:\ws\Universidad-JdC\Servicios_SIG_Taller
```

### Paso 2: Verificar Archivos Necesarios

```bash
# Verificar estructura de directorios
ls -la

# Verificar que existe el GeoPackage
ls -lh data/geopackage/amazonas.gpkg

# Verificar scripts de inicialización
ls -la init-scripts/
```

**Salida esperada:**
```
-rw-r--r-- 1 user user 1.5M Nov  7 11:02 data/geopackage/amazonas.gpkg
-rwxr-xr-x 1 user user  486 Nov  7 12:00 init-scripts/01-init-postgis.sh
-rwxr-xr-x 1 user user 1.8K Nov  7 12:00 init-scripts/02-import-geopackage.sh
```

### Paso 3: Verificar Permisos de Ejecución (Linux/Mac)

```bash
# Dar permisos de ejecución a los scripts
chmod +x init-scripts/*.sh

# Verificar permisos
ls -la init-scripts/
```

**Nota para Windows:** No es necesario este paso.

### Paso 4: Construir la Imagen de PostgreSQL con GDAL

```bash
# Construir la imagen personalizada
docker-compose build postgis
```

**Salida esperada:**
```
[+] Building 15.5s (7/7) FINISHED
 => [internal] load build definition from Dockerfile.postgis
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/postgis/postgis:16-3.4
 => [1/2] FROM docker.io/postgis/postgis:16-3.4
 => [2/2] RUN apt-get update && apt-get install -y gdal-bin python3-gdal
 => exporting to image
 => naming to docker.io/library/servicios_sig_taller-postgis:latest
```

**Tiempo estimado:** 1-5 minutos dependiendo de la conexión a internet.

### Paso 5: Iniciar los Servicios

```bash
# Iniciar todos los servicios en modo detached (background)
docker-compose up -d
```

**Salida esperada:**
```
[+] Running 4/4
 ✔ Network servicios_sig_taller_default      Created
 ✔ Volume "servicios_sig_taller_postgres_data"    Created
 ✔ Container postgis                           Started
 ✔ Container geoserver                         Started
```

**Tiempo estimado:** 30-60 segundos para que los servicios estén completamente listos.

### Paso 6: Monitorear la Inicialización

```bash
# Ver logs en tiempo real de PostgreSQL
docker logs -f postgis

# Presionar Ctrl+C para detener el seguimiento
```

**Eventos esperados (en orden):**

1. Inicialización de PostgreSQL
2. Creación de la base de datos `geodatos`
3. Ejecución de `01-init-postgis.sh`
   - "Habilitando extensión PostGIS..."
   - "PostGIS habilitado correctamente"
4. Ejecución de `02-import-geopackage.sh`
   - "Verificando disponibilidad de GDAL..."
   - "GDAL está disponible. Versión: GDAL 3.2.2"
   - "Importando capa: dpto_amazonas"
   - "Importando capa: puntos_administrativos"
   - "Todas las capas han sido importadas!"
5. PostgreSQL listo para aceptar conexiones

---

## Verificación de la Instalación

### Verificación 1: Estado de los Contenedores

```bash
docker ps
```

**Salida esperada:**
```
CONTAINER ID   IMAGE                               STATUS                   PORTS
a437b2a47ae9   servicios_sig_taller-postgis      Up 5 minutes (healthy)   0.0.0.0:5432->5432/tcp
ea441a37c90b   docker.osgeo.org/geoserver:2.24.0   Up 4 minutes             0.0.0.0:8080->8080/tcp
```

**Verificar:**
- Ambos contenedores con estado "Up"
- PostGIS con estado "(healthy)"
- Puertos mapeados correctamente

### Verificación 2: Logs de Inicialización

```bash
# Ver si los scripts se ejecutaron
docker logs postgis 2>&1 | grep -E "(PostGIS habilitado|Todas las capas han sido importadas)"
```

**Salida esperada:**
```
PostGIS habilitado correctamente en la base de datos geodatos
Todas las capas han sido importadas!
```

### Verificación 3: Tablas en la Base de Datos

```bash
# Listar todas las tablas
docker exec postgis psql -U postgres -d geodatos -c "\dt"
```

**Salida esperada (parcial):**
```
 Schema |           Name           | Type  |  Owner
--------+--------------------------+-------+----------
 public | dpto_amazonas            | table | postgres
 public | puntos_administrativos   | table | postgres
 public | spatial_ref_sys          | table | postgres
```

### Verificación 4: Contar Registros

```bash
docker exec postgis psql -U postgres -d geodatos -c "
SELECT 'dpto_amazonas' as tabla, COUNT(*) as registros FROM dpto_amazonas
UNION ALL
SELECT 'puntos_administrativos' as tabla, COUNT(*) as registros FROM puntos_administrativos;"
```

**Salida esperada:**
```
         tabla          | registros
------------------------+-----------
 dpto_amazonas          |         1
 puntos_administrativos |       131
```

### Verificación 5: Estructura de las Tablas

```bash
# Ver estructura de dpto_amazonas
docker exec postgis psql -U postgres -d geodatos -c "\d dpto_amazonas"
```

**Salida esperada:**
```
                     Table "public.dpto_amazonas"
   Column   |            Type             | Collation | Nullable | Default
------------+-----------------------------+-----------+----------+--------
 gid        | integer                     |           | not null | ...
 dpto_ccdgo | character varying(2)        |           |          |
 dpto_cnmbr | character varying(250)      |           |          |
 geom       | geometry(MultiPolygon,4686) |           |          |
Indexes:
    "dpto_amazonas_pkey" PRIMARY KEY, btree (gid)
    "dpto_amazonas_geom_geom_idx" gist (geom)
```

### Verificación 6: Geometrías Configuradas

```bash
docker exec postgis psql -U postgres -d geodatos -c "
SELECT f_table_name, f_geometry_column, type, srid
FROM geometry_columns
WHERE f_table_name IN ('dpto_amazonas', 'puntos_administrativos');"
```

**Salida esperada:**
```
    f_table_name       | f_geometry_column |    type     |  srid
-----------------------+-------------------+-------------+--------
 dpto_amazonas         | geom              | MULTIPOLYGON| 4686
 puntos_administrativos| geom              | POINTZ      | 900914
```

### Verificación 7: GeoServer Accesible

```bash
# Verificar que GeoServer responde
curl -I http://localhost:8080/geoserver/web/
```

**Salida esperada:**
```
HTTP/1.1 200 OK
```

**O acceder desde el navegador:**
```
http://localhost:8080/geoserver
```

**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `geoserver`

---

## Conexión y Uso

### Conexión desde PostgreSQL CLI

```bash
# Entrar a psql dentro del contenedor
docker exec -it postgis psql -U postgres -d geodatos

# Comandos útiles dentro de psql:
\dt                    # Listar tablas
\d nombre_tabla        # Describir tabla
\dx                    # Listar extensiones
\l                     # Listar bases de datos
\q                     # Salir
```

### Conexión desde QGIS

1. **Abrir QGIS**
2. **Añadir conexión PostGIS:**
   - Capa → Añadir Capa → Añadir Capa PostGIS
   - Clic en "Nueva"
3. **Configurar conexión:**
   ```
   Nombre: GeoServer Local
   Host: localhost
   Puerto: 5432
   Base de datos: geodatos
   Usuario: postgres
   Contraseña: postgres
   ```
4. **Probar conexión** → Aceptar
5. **Conectar** y seleccionar las capas:
   - `dpto_amazonas`
   - `puntos_administrativos`

### Conexión desde pgAdmin

1. **Abrir pgAdmin**
2. **Crear nuevo servidor:**
   - Clic derecho en "Servers" → Create → Server
3. **Pestaña General:**
   - Name: `PostgreSQL Local`
4. **Pestaña Connection:**
   ```
   Host: localhost
   Port: 5432
   Maintenance database: geodatos
   Username: postgres
   Password: postgres
   ```
5. **Guardar** y explorar:
   - Servers → PostgreSQL Local → Databases → geodatos → Schemas → public → Tables

### Conexión desde Python

```python
import psycopg2
from sqlalchemy import create_engine
import geopandas as gpd

# Opción 1: psycopg2
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="geodatos",
    user="postgres",
    password="postgres"
)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM dpto_amazonas;")
print(cursor.fetchone())
conn.close()

# Opción 2: GeoPandas
engine = create_engine(
    'postgresql://postgres:postgres@localhost:5432/geodatos'
)
gdf = gpd.read_postgis(
    "SELECT * FROM dpto_amazonas",
    engine,
    geom_col='geom'
)
print(gdf.head())
```

### Conexión desde GeoServer

1. **Acceder a GeoServer:**
   ```
   http://localhost:8080/geoserver
   ```

2. **Iniciar sesión:**
   - Usuario: `admin`
   - Contraseña: `geoserver`

3. **Crear un Almacén de Datos (Data Store):**
   - Ir a: Datos → Almacenes → Agregar nuevo Almacén
   - Seleccionar: "PostGIS - PostgreSQL"

4. **Configurar conexión:**
   ```
   Workspace: (crear uno nuevo o usar default)
   Data Source Name: postgis_geodatos

   Parámetros de conexión:
   - host: postgis
   - port: 5432
   - database: geodatos
   - schema: public
   - user: postgres
   - passwd: postgres
   ```

5. **Guardar** y publicar capas

6. **Publicar capas:**
   - La capa aparecerá en la lista
   - Clic en "Publicar" para cada capa
   - Configurar nombres y SRS
   - Guardar

---

## Consideraciones Importantes

### 1. Seguridad

 **ADVERTENCIA:** Las credenciales por defecto NO son seguras para producción.

**Para Producción:**

```yaml
# Modificar docker-compose.yml
environment:
  - POSTGRES_USER=mi_usuario_seguro
  - POSTGRES_PASSWORD=${DB_PASSWORD}  # Usar variable de entorno
  - GEOSERVER_ADMIN_PASSWORD=${GS_PASSWORD}
```

**Crear archivo `.env`:**
```bash
DB_PASSWORD=MiPasswordSeguro123!
GS_PASSWORD=OtroPasswordSeguro456!
```

**Añadir `.env` a `.gitignore`:**
```bash
echo ".env" >> .gitignore
```

### 2. Persistencia de Datos

**Volúmenes Docker:**
- `postgres_data`: Contiene TODOS los datos de PostgreSQL
- `geoserver_data`: Contiene configuraciones de GeoServer

**Backup de Volúmenes:**

```bash
# Backup de PostgreSQL
docker exec postgis pg_dump -U postgres geodatos > backup_geodatos_$(date +%Y%m%d).sql

# Backup de volumen
docker run --rm -v servicios_sig_taller_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres_data_backup.tar.gz /data
```

**Restaurar desde Backup:**

```bash
# Restaurar dump SQL
docker exec -i postgis psql -U postgres geodatos < backup_geodatos_20251107.sql
```

### 3. Rendimiento

**Ajustar Memoria de GeoServer:**

```yaml
# En docker-compose.yml
environment:
  - INITIAL_MEMORY=4G
  - MAXIMUM_MEMORY=8G
```

**Ajustar PostgreSQL:**

Crear archivo `postgresql.conf` personalizado y montarlo:

```yaml
volumes:
  - ./postgresql.conf:/etc/postgresql/postgresql.conf
```

**Configuraciones recomendadas:**
```
shared_buffers = 256MB
work_mem = 16MB
maintenance_work_mem = 128MB
effective_cache_size = 1GB
```

### 4. Reinicialización

**IMPORTANTE:** Los scripts de inicialización solo se ejecutan si la base de datos NO existe.

**Para reinicializar completamente:**

```bash
# 1. Detener servicios
docker-compose down

# 2. Eliminar volumen de PostgreSQL (¡BORRA TODOS LOS DATOS!)
docker volume rm servicios_sig_taller_postgres_data

# 3. Iniciar de nuevo
docker-compose up -d
```

### 5. Actualizaciones

**Actualizar Imágenes:**

```bash
# Detener servicios
docker-compose down

# Actualizar imágenes
docker-compose pull

# Reconstruir imagen personalizada
docker-compose build postgis

# Iniciar con nuevas imágenes
docker-compose up -d
```

### 6. SRID (Sistemas de Referencia)

**Tablas creadas con diferentes SRID:**
- `dpto_amazonas`: SRID 4686 (MAGNA-SIRGAS / Colombia Bogota zone)
- `puntos_administrativos`: SRID 900914 (Google Mercator)

**Reproyectar al consultar:**

```sql
-- Reproyectar puntos_administrativos a 4686
SELECT
    nombre_geo,
    ST_Transform(geom, 4686) as geom_4686
FROM puntos_administrativos;

-- Calcular distancia entre capas (requiere mismo SRID)
SELECT
    p.nombre_geo,
    ST_Distance(
        ST_Transform(p.geom, 4686),
        d.geom
    ) as distancia_metros
FROM puntos_administrativos p
CROSS JOIN dpto_amazonas d;
```

---

## Solución de Problemas Comunes

### Problema 1: Los contenedores no inician

**Síntoma:**
```bash
docker ps
# No aparecen contenedores o aparecen con estado "Exited"
```

**Diagnóstico:**
```bash
# Ver logs de error
docker-compose logs

# Ver logs específicos
docker logs postgis
docker logs geoserver
```

**Soluciones:**

1. **Puerto ya en uso:**
   ```bash
   # Linux/Mac
   sudo lsof -i :5432
   sudo lsof -i :8080

   # Windows
   netstat -ano | findstr ":5432"
   netstat -ano | findstr ":8080"
   ```

   **Solución:** Detener el servicio que usa el puerto o cambiar puerto en `docker-compose.yml`

2. **Memoria insuficiente:**
   ```bash
   # Ver uso de recursos
   docker stats
   ```

   **Solución:** Reducir memoria asignada a GeoServer o liberar RAM

3. **Docker no corriendo:**
   ```bash
   # Verificar estado de Docker
   systemctl status docker    # Linux
   docker info                # General
   ```

### Problema 2: Scripts de inicialización no se ejecutan

**Síntoma:**
```bash
docker logs postgis | grep "Skipping initialization"
# PostgreSQL Database directory appears to contain a database; Skipping initialization
```

**Causa:** El volumen de PostgreSQL ya existe de una ejecución anterior.

**Solución:**
```bash
# 1. Detener servicios
docker-compose down

# 2. Listar volúmenes
docker volume ls | grep postgres

# 3. Eliminar volumen (¡BORRA DATOS!)
docker volume rm servicios_sig_taller_postgres_data

# 4. Reiniciar
docker-compose up -d
```

### Problema 3: Las tablas no aparecen

**Síntoma:**
```bash
docker exec postgis psql -U postgres -d geodatos -c "\dt"
# No muestra dpto_amazonas ni puntos_administrativos
```

**Diagnóstico:**
```bash
# Ver logs de importación
docker logs postgis 2>&1 | grep -A 5 "import"
```

**Causas y soluciones:**

1. **Archivo GeoPackage no encontrado:**
   ```bash
   # Verificar que el archivo existe
   ls -lh data/geopackage/amazonas.gpkg

   # Verificar dentro del contenedor
   docker exec postgis ls -lh /geopackage/
   ```

   **Solución:** Verificar que el archivo existe en la ruta correcta

2. **Error en script de importación:**
   ```bash
   # Ver errores específicos
   docker logs postgis 2>&1 | grep -i "error"
   ```

3. **GDAL no instalado:**
   ```bash
   # Verificar GDAL en contenedor
   docker exec postgis which ogr2ogr
   docker exec postgis ogrinfo --version
   ```

   **Solución:** Reconstruir imagen con `docker-compose build postgis`

### Problema 4: No puedo conectarme desde fuera del contenedor

**Síntoma:**
```bash
psql -h localhost -U postgres -d geodatos
# psql: error: connection refused
```

**Diagnóstico:**
```bash
# Verificar que el puerto está mapeado
docker ps | grep postgis
# Debe mostrar: 0.0.0.0:5432->5432/tcp

# Verificar healthcheck
docker inspect postgis | grep -A 5 Health
```

**Soluciones:**

1. **Firewall bloqueando:**
   ```bash
   # Linux
   sudo ufw allow 5432/tcp

   # Windows
   # Abrir Windows Defender Firewall → Regla de entrada → Puerto 5432
   ```

2. **PostgreSQL no acepta conexiones remotas:**
   ```bash
   # Verificar pg_hba.conf (ya debería estar configurado)
   docker exec postgis cat /var/lib/postgresql/data/pg_hba.conf
   ```

3. **Contenedor no healthy:**
   ```bash
   # Esperar a que esté healthy
   docker ps

   # O verificar logs
   docker logs postgis
   ```

### Problema 5: GeoServer no carga (página en blanco)

**Síntoma:**
- Navegador muestra página en blanco en `http://localhost:8080/geoserver`
- O muestra error 404/503

**Diagnóstico:**
```bash
# Ver logs de GeoServer
docker logs geoserver

# Verificar que está corriendo
docker ps | grep geoserver
```

**Soluciones:**

1. **GeoServer aún está iniciando:**
   ```bash
   # GeoServer puede tardar 1-3 minutos en iniciar
   # Ver logs hasta que diga "Server startup"
   docker logs -f geoserver
   ```

   **Solución:** Esperar a que complete la inicialización

2. **Memoria insuficiente:**
   ```bash
   docker logs geoserver | grep -i "memory\|heap"
   ```

   **Solución:** Aumentar memoria en docker-compose.yml

3. **PostGIS no está listo:**
   ```bash
   # Verificar que PostGIS está healthy
   docker ps | grep postgis
   ```

   **Solución:** GeoServer espera a PostGIS por la dependencia en docker-compose

### Problema 6: Error "Permission denied" en scripts

**Síntoma:**
```bash
docker logs postgis | grep "Permission denied"
# /docker-entrypoint-initdb.d/01-init-postgis.sh: Permission denied
```

**Solución (Linux/Mac):**
```bash
# Dar permisos de ejecución
chmod +x init-scripts/*.sh

# Reconstruir
docker-compose down
docker volume rm servicios_sig_taller_postgres_data
docker-compose up -d
```

**Solución (Windows):**
```bash
# Verificar que los archivos tienen terminaciones de línea Unix (LF, no CRLF)
# Usar un editor como VSCode o Notepad++ para convertir
```

### Problema 7: Datos corruptos o inconsistentes

**Síntoma:**
```sql
SELECT * FROM dpto_amazonas;
-- ERROR: invalid memory alloc request size
```

**Solución:**
```bash
# 1. Hacer backup si es posible
docker exec postgis pg_dump -U postgres geodatos > backup.sql

# 2. Reinicializar completamente
docker-compose down
docker volume rm servicios_sig_taller_postgres_data
docker volume rm servicios_sig_taller_geoserver_data

# 3. Reiniciar
docker-compose up -d
```

### Problema 8: Actualización de Docker Compose

**Síntoma:**
```bash
docker-compose up
# WARNING: The version attribute is obsolete
```

**Solución:**
```yaml
# Editar docker-compose.yml y eliminar la primera línea:
# version: '3.8'  ← ELIMINAR ESTA LÍNEA

# El archivo debe empezar directamente con:
services:
  postgis:
    ...
```

---

## Comandos Útiles

### Gestión de Contenedores

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios (mantiene volúmenes)
docker-compose down

# Detener y eliminar volúmenes (¡BORRA DATOS!)
docker-compose down -v

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker logs -f postgis
docker logs -f geoserver

# Reiniciar un servicio
docker-compose restart postgis

# Ver estado y uso de recursos
docker stats

# Ver información de contenedores
docker ps -a
docker inspect postgis
```

### Gestión de Volúmenes

```bash
# Listar volúmenes
docker volume ls

# Inspeccionar un volumen
docker volume inspect servicios_sig_taller_postgres_data

# Backup de volumen
docker run --rm \
  -v servicios_sig_taller_postgres_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/postgres_backup.tar.gz /data

# Restaurar volumen desde backup
docker run --rm \
  -v servicios_sig_taller_postgres_data:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/postgres_backup.tar.gz --strip 1"

# Eliminar volúmenes huérfanos
docker volume prune
```

### Comandos PostgreSQL

```bash
# Conectar a la base de datos
docker exec -it postgis psql -U postgres -d geodatos

# Ejecutar comando SQL
docker exec postgis psql -U postgres -d geodatos -c "SELECT COUNT(*) FROM dpto_amazonas;"

# Ejecutar script SQL
docker exec -i postgis psql -U postgres -d geodatos < mi_script.sql

# Dump de base de datos
docker exec postgis pg_dump -U postgres geodatos > backup.sql

# Dump con formato custom (comprimido)
docker exec postgis pg_dump -U postgres -Fc geodatos > backup.dump

# Restaurar dump
docker exec -i postgis psql -U postgres geodatos < backup.sql

# Vacuuming (limpieza)
docker exec postgis psql -U postgres -d geodatos -c "VACUUM ANALYZE;"

# Ver conexiones activas
docker exec postgis psql -U postgres -c "SELECT * FROM pg_stat_activity;"
```

### Comandos GDAL/OGR

```bash
# Información del GeoPackage
docker exec postgis ogrinfo /geopackage/amazonas.gpkg

# Información detallada de una capa
docker exec postgis ogrinfo -al /geopackage/amazonas.gpkg dpto_amazonas

# Convertir GeoPackage a Shapefile
docker exec postgis ogr2ogr \
  /tmp/output.shp \
  /geopackage/amazonas.gpkg \
  dpto_amazonas

# Reproyectar capa
docker exec postgis ogr2ogr \
  -t_srs EPSG:4326 \
  /tmp/reproyectado.gpkg \
  /geopackage/amazonas.gpkg
```

### Consultas SQL Útiles

```sql
-- Listar todas las extensiones instaladas
SELECT * FROM pg_available_extensions WHERE name LIKE '%postgis%';

-- Versión de PostGIS
SELECT PostGIS_Version();

-- Listar todas las tablas con geometrías
SELECT * FROM geometry_columns;

-- Información de índices espaciales
SELECT schemaname, tablename, indexname
FROM pg_indexes
WHERE indexdef LIKE '%gist%';

-- Tamaño de las tablas
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Estadísticas de una geometría
SELECT
    ST_GeometryType(geom) as tipo,
    ST_SRID(geom) as srid,
    ST_Extent(geom) as bbox,
    COUNT(*) as total
FROM dpto_amazonas
GROUP BY ST_GeometryType(geom), ST_SRID(geom);

-- Validar geometrías
SELECT gid, ST_IsValid(geom), ST_IsValidReason(geom)
FROM dpto_amazonas
WHERE NOT ST_IsValid(geom);

-- Área de polígonos (en unidades del SRID)
SELECT
    dpto_cnmbr,
    ST_Area(geom) as area_original,
    ST_Area(ST_Transform(geom, 32618)) as area_metros2
FROM dpto_amazonas;
```

---

## Mantenimiento

### Mantenimiento Regular

**Semanal:**

```bash
# 1. Verificar espacio en disco
docker system df

# 2. Ver logs de errores
docker logs postgis 2>&1 | grep -i error
docker logs geoserver 2>&1 | grep -i error

# 3. Verificar conexiones
docker exec postgis psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"
```

**Mensual:**

```bash
# 1. Backup de base de datos
docker exec postgis pg_dump -U postgres -Fc geodatos > backup_$(date +%Y%m%d).dump

# 2. VACUUM y ANALYZE
docker exec postgis psql -U postgres -d geodatos -c "VACUUM ANALYZE;"

# 3. Verificar y reparar índices
docker exec postgis psql -U postgres -d geodatos -c "REINDEX DATABASE geodatos;"

# 4. Limpiar logs antiguos de Docker
docker system prune -a --volumes --filter "until=720h"
```

### Monitoreo

**Script de monitoreo básico:**

```bash
#!/bin/bash
# monitor.sh

echo "=== Estado de Contenedores ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo -e "\n=== Uso de Recursos ==="
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo -e "\n=== Espacio en Disco ==="
docker system df

echo -e "\n=== Registros en Tablas ==="
docker exec postgis psql -U postgres -d geodatos -c "
SELECT 'dpto_amazonas' as tabla, COUNT(*) as registros FROM dpto_amazonas
UNION ALL
SELECT 'puntos_administrativos', COUNT(*) FROM puntos_administrativos;"

echo -e "\n=== Conexiones Activas ==="
docker exec postgis psql -U postgres -c "
SELECT datname, count(*) as connections
FROM pg_stat_activity
GROUP BY datname;"
```

**Ejecutar monitoreo:**
```bash
chmod +x monitor.sh
./monitor.sh
```

### Actualización del Sistema

**Plan de actualización:**

1. **Preparación:**
   ```bash
   # Backup completo
   ./backup.sh

   # Documentar versiones actuales
   docker-compose images > versions_before.txt
   ```

2. **Actualización:**
   ```bash
   # Detener servicios
   docker-compose down

   # Actualizar imágenes
   docker-compose pull
   docker-compose build postgis

   # Iniciar con nuevas versiones
   docker-compose up -d
   ```

3. **Verificación:**
   ```bash
   # Verificar que todo funciona
   ./monitor.sh

   # Verificar versiones
   docker exec postgis psql -U postgres -c "SELECT version();"
   docker exec postgis psql -U postgres -c "SELECT PostGIS_Version();"
   ```

4. **Rollback (si es necesario):**
   ```bash
   # Detener servicios
   docker-compose down -v

   # Restaurar desde backup
   # ... (seguir procedimiento de restauración)
   ```

---

## Contacto y Soporte

### Recursos Adicionales

- **Documentación Docker:** https://docs.docker.com
- **Documentación PostGIS:** https://postgis.net/documentation
- **Documentación GeoServer:** https://docs.geoserver.org
- **GDAL/OGR:** https://gdal.org

### Logs para Reportar Problemas

Si necesitas reportar un problema, incluye:

```bash
# 1. Información del sistema
docker --version
docker-compose --version
uname -a  # o systeminfo en Windows

# 2. Estado de contenedores
docker ps -a

# 3. Logs relevantes
docker logs postgis > postgis.log 2>&1
docker logs geoserver > geoserver.log 2>&1

# 4. Configuración
cat docker-compose.yml
```

---

## Changelog

### v1.0 - 2025-11-07
- Configuración inicial de PostgreSQL/PostGIS con GeoServer
- Importación automática de GeoPackage
- Scripts de inicialización
- Documentación completa

---

**Última actualización:** 2025-11-07
**Versión:** 1.0
**Autor:** Sistema de Servicios SIG
