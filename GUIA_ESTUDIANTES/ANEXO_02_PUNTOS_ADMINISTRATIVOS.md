# Anexo 2: Carga de Puntos Administrativos desde Shapefile

## Objetivos de Aprendizaje

Al completar este anexo, habrás:

- Descargado y descomprimido un shapefile en el contenedor PostGIS
- Cargado shapefile a PostGIS con `shp2pgsql`
- Creado tabla de puntos intersectados con límite departamental
- Creado vista con buffer de 5000 metros alrededor de puntos
- Publicado 3 nuevas capas en GeoServer (WMS y WFS)
- Integrado las capas al visor geográfico

---

## A2.1 Contexto

En este anexo agregarás una nueva capa de **puntos administrativos** al proyecto. Trabajarás con:

1. **Shapefile fuente:** `Administrativo_P.zip` (puntos de toda Colombia)
2. **Capa completa:** Todos los puntos administrativos
3. **Capa filtrada:** Solo puntos dentro del departamento de Chocó
4. **Capa de buffer:** Polígonos de 5000m alrededor de cada punto en Chocó

**Flujo de trabajo:**
```
Administrativo_P.zip (GitHub)
    ↓ Descarga
data/shapefiles/ (local)
    ↓ Volumen Docker
/data/ (contenedor postgis)
    ↓ shp2pgsql
puntos_administrativos (PostGIS)
    ↓ ST_Intersects
puntos_admin_depto (PostGIS)
    ↓ ST_Buffer
puntos_admin_buffer5000 (PostGIS vista)
    ↓ Publicar
GeoServer (3 capas)
    ↓ Integrar
Visor web (app.js)
```

---

## A2.2 Paso 1: Descargar Shapefile

### Descargar archivo desde GitHub

**URL del archivo:**
```
https://github.com/epiragauta/Servicios_SIG_Taller/blob/guia-estudiantes/data/shapefiles/Administrativo_P.zip
```

**Opción 1: Desde navegador**

1. Visitar la URL en el navegador
2. Click en botón "Download raw file" o "Descargar"
3. Guardar en: `C:\ws\ujdc\Servicios_SIG_Taller\data\shapefiles\Administrativo_P.zip`

**Opción 2: Desde terminal (Windows PowerShell)**

```powershell
# Navegar al directorio del proyecto
cd C:\ws\ujdc\Servicios_SIG_Taller\data\shapefiles

# Descargar con Invoke-WebRequest
Invoke-WebRequest -Uri "https://github.com/epiragauta/Servicios_SIG_Taller/raw/guia-estudiantes/data/shapefiles/Administrativo_P.zip" -OutFile "Administrativo_P.zip"
```

**Opción 3: Desde terminal (Linux/Mac)**

```bash
# Navegar al directorio del proyecto
cd /ruta/al/proyecto/Servicios_SIG_Taller/data/shapefiles

# Descargar con wget o curl
wget https://github.com/epiragauta/Servicios_SIG_Taller/raw/guia-estudiantes/data/shapefiles/Administrativo_P.zip

# O con curl
curl -L -o Administrativo_P.zip https://github.com/epiragauta/Servicios_SIG_Taller/raw/guia-estudiantes/data/shapefiles/Administrativo_P.zip
```

### Verificar descarga

```bash
# Windows
dir C:\ws\ujdc\Servicios_SIG_Taller\data\shapefiles\Administrativo_P.zip

# Linux/Mac
ls -lh data/shapefiles/Administrativo_P.zip
```

**Resultado esperado:**
```
Administrativo_P.zip    [tamaño del archivo]
```

---

## A2.3 Paso 2: Verificar Volumen en Docker Compose

Antes de continuar, verifica que el directorio `data/shapefiles` esté montado como volumen en el contenedor PostGIS.

### Abrir docker-compose.yml

```bash
# Desde el directorio raíz del proyecto
cat docker-compose.yml | grep -A 10 postgis
```

### Verificar volúmenes del servicio postgis

**Debe contener:**
```yaml
services:
  postgis:
    # ...
    volumes:
      - postgis-data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d
      - ./data/shapefiles:/data    # ← Esta línea debe existir
```

**Si NO existe la línea `- ./data/shapefiles:/data`:**

1. Editar `docker-compose.yml`
2. Agregar en la sección `volumes` del servicio `postgis`:
   ```yaml
   - ./data/shapefiles:/data
   ```
3. Guardar archivo
4. Reiniciar contenedor:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

**Explicación:**
- `./data/shapefiles`: Directorio en tu máquina local
- `/data`: Directorio dentro del contenedor postgis
- Los archivos en `data/shapefiles` estarán accesibles en `/data` dentro del contenedor

---

## A2.4 Paso 3: Verificar y Preparar Contenedor PostGIS

**IMPORTANTE:** Este anexo requiere herramientas específicas (`shp2pgsql`, `unzip`) que deben estar instaladas en el contenedor PostGIS.

### Verificar si el contenedor tiene las herramientas

```bash
# Verificar que postgis y unzip estén en el Dockerfile
cat Dockerfile.postgis | grep -E "postgis|unzip"
```

**Resultado esperado:**
```
        postgis \
        unzip && \
```

**Si NO aparecen estas líneas**, el `Dockerfile.postgis` debe actualizarse:

```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gdal-bin \
        python3-gdal \
        postgis \
        unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

**Si tuviste que editar el Dockerfile:**

```bash
# 1. Reconstruir imagen PostGIS
docker-compose build postgis

# 2. Recrear y levantar el contenedor
docker-compose up -d postgis

# 3. Esperar a que esté healthy (puede tardar 30-60 segundos)
docker-compose ps postgis
```

**Resultado esperado:**
```
NAME      STATUS        PORTS
postgis   Up (healthy)  0.0.0.0:5432->5432/tcp
```

### Acceder al contenedor

Una vez verificado que el contenedor tiene las herramientas:

```bash
docker exec -it -u root postgis bash
```

**Resultado esperado:**
```
root@[container-id]:/#
```

### Verificar que el archivo está accesible

```bash
ls -lh /data/
```

**Resultado esperado:**
```
total [tamaño]
-rw-r--r-- 1 root root [tamaño] [fecha] Administrativo_P.zip
...
```

Si ves `Administrativo_P.zip`, el volumen está correctamente montado. ✅

### Verificar herramientas instaladas

```bash
# Verificar unzip
which unzip

# Verificar shp2pgsql
which shp2pgsql

# Verificar ogr2ogr (alternativa)
which ogr2ogr
```

**Resultado esperado:**
```
/usr/bin/unzip
/usr/bin/shp2pgsql
/usr/bin/ogr2ogr
```

Si todas las herramientas están presentes, continúa al Paso 4. ✅

---

## A2.5 Paso 4: Descomprimir Shapefile

### Navegar al directorio de datos

```bash
cd /data
```

### Descomprimir archivo ZIP

```bash
unzip Administrativo_P.zip
```

**Resultado esperado:**
```
Archive:  Administrativo_P.zip
  inflating: Administrativo_P.shp
  inflating: Administrativo_P.shx
  inflating: Administrativo_P.dbf
  inflating: Administrativo_P.prj
  inflating: Administrativo_P.cpg
```

### Verificar archivos descomprimidos

```bash
ls -lh /data/Administrativo_P.*
```

**Resultado esperado:**
```
-rw-r--r-- 1 root root [tamaño] [fecha] Administrativo_P.cpg
-rw-r--r-- 1 root root [tamaño] [fecha] Administrativo_P.dbf
-rw-r--r-- 1 root root [tamaño] [fecha] Administrativo_P.prj
-rw-r--r-- 1 root root [tamaño] [fecha] Administrativo_P.shp
-rw-r--r-- 1 root root [tamaño] [fecha] Administrativo_P.shx
```

**Archivos del shapefile:**
- `.shp`: Geometrías
- `.shx`: Índice espacial
- `.dbf`: Atributos (tabla)
- `.prj`: Sistema de coordenadas
- `.cpg`: Codificación de caracteres

---

## A2.6 Paso 5: Verificar Sistema de Coordenadas

Antes de cargar, verifica el sistema de coordenadas del shapefile.

### Ver proyección del shapefile

```bash
cat /data/Administrativo_P.prj
```

**Resultado esperado (puede variar):**
```
GEOGCS["GCS_MAGNA",DATUM["D_MAGNA",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]
```

**Interpretación:**
- `GEOGCS`: Sistema geográfico (latitud/longitud)
- `MAGNA`: Sistema de referencia de Colombia
- `GRS_1980`: Elipsoide (similar a WGS84)

**NOTA:** MAGNA es compatible con EPSG:4326 (WGS84) para nuestros propósitos. Cargaremos como EPSG:4326.

---

## A2.7 Paso 6: Cargar Shapefile a PostGIS

Usaremos `shp2pgsql` para convertir el shapefile a SQL y cargarlo a la base de datos.

**NOTA:** `shp2pgsql` debería estar instalado si reconstruiste el contenedor en el Paso 3. Si no lo está, vuelve al Paso 3.

### Paso 6.1: Verificar que shp2pgsql está disponible

```bash
which shp2pgsql
```

**Resultado esperado:**
```
/usr/bin/shp2pgsql
```

Si no está disponible, la imagen Docker de PostGIS debería incluirlo por defecto.

### Paso 6.2: Generar SQL y cargar a la base de datos

```bash
# Comando completo en una sola línea
shp2pgsql -s 4326 -I -W UTF-8 /data/Administrativo_P.shp public.puntos_administrativos | psql -U postgres -d postgres
```

**Desglose del comando:**

**`shp2pgsql`**: Herramienta de conversión shapefile → SQL

**Opciones:**
- `-s 4326`: SRID (Spatial Reference ID) = EPSG:4326 (WGS84)
- `-I`: Crear índice espacial (GIST index) automáticamente
- `-W UTF-8`: Codificación de caracteres de entrada (UTF-8)

**Argumentos:**
- `/data/Administrativo_P.shp`: Ruta al shapefile
- `public.puntos_administrativos`: Esquema.tabla de destino

**Pipeline `|`**: Pasa el SQL generado directamente a psql

**`psql`**: Cliente de PostgreSQL
- `-U postgres`: Usuario de base de datos
- `-d postgres`: Nombre de la base de datos

**Resultado esperado:**
```
Shapefile type: Point
Postgis type: POINT[2]
...
BEGIN
CREATE TABLE
...
ALTER TABLE
...
                      addgeometrycolumn
--------------------------------------------------------------
 public.puntos_administrativos.geom SRID:4326 TYPE:POINT DIMS:2
(1 row)

INSERT 0 1
INSERT 0 1
...
INSERT 0 [total de puntos]
CREATE INDEX
COMMIT
```

**Si aparece error de contraseña:**
```bash
# El usuario postgres puede no tener contraseña en Docker
# Intenta sin -W (sin pedir contraseña)
shp2pgsql -s 4326 -I -W UTF-8 /data/Administrativo_P.shp public.puntos_administrativos | psql -U postgres -d postgres
```

### Paso 6.3: Verificar carga

```bash
psql -U postgres -d postgres -c "SELECT COUNT(*) FROM puntos_administrativos;"
```

**Resultado esperado:**
```
 count
-------
  [número de puntos]
(1 row)
```

**Ver algunos registros:**
```bash
psql -U postgres -d postgres -c "SELECT * FROM puntos_administrativos LIMIT 5;"
```

**Verificar columna de geometría:**
```bash
psql -U postgres -d postgres -c "SELECT gid, ST_AsText(geom) as geometria FROM puntos_administrativos LIMIT 3;"
```

**Resultado esperado:**
```
 gid |      geometria
-----+---------------------
   1 | POINT(-76.xxx 5.xxx)
   2 | POINT(-77.xxx 4.xxx)
   3 | POINT(-75.xxx 6.xxx)
(3 rows)
```

### Alternativa: Usar ogr2ogr (GDAL)

Si `shp2pgsql` no está disponible, puedes usar `ogr2ogr` (ya instalado con `gdal-bin`):

```bash
ogr2ogr -f "PostgreSQL" \
    PG:"host=localhost dbname=postgres user=postgres password=postgres" \
    -nln puntos_administrativos \
    -lco GEOMETRY_NAME=geom \
    -lco SPATIAL_INDEX=GIST \
    -a_srs EPSG:4326 \
    /data/Administrativo_P.shp
```

**Desglose del comando:**

**`-f "PostgreSQL"`**: Formato de salida (PostGIS/PostgreSQL)

**`PG:"..."`**: String de conexión a PostgreSQL
- `host=localhost`: Dentro del contenedor, PostgreSQL está en localhost
- `dbname=postgres`: Nombre de la base de datos
- `user=postgres`: Usuario
- `password=postgres`: Contraseña (si está configurada)

**`-nln puntos_administrativos`**: Nombre de la tabla de destino

**`-lco GEOMETRY_NAME=geom`**: Nombre de la columna de geometría

**`-lco SPATIAL_INDEX=GIST`**: Crear índice espacial GIST

**`-a_srs EPSG:4326`**: Sistema de coordenadas de destino

**Ventajas de ogr2ogr:**
- Más versátil (soporta múltiples formatos)
- Maneja reproyecciones automáticamente
- Puede sobrescribir tablas existentes con `-overwrite`

**Desventajas:**
- Sintaxis más compleja
- Nombres de columnas pueden ser diferentes (usa nombres del shapefile)

**Recomendación:** Usa `shp2pgsql` (más simple y directo). Usa `ogr2ogr` solo si `shp2pgsql` no está disponible.

---

## A2.6 Paso 5: Verificar Tabla de Límite Departamental

Antes de hacer la intersección, verifica que la tabla `dpto_choco` existe.

### Verificar tabla dpto_choco

```bash
psql -U postgres -d postgres -c "\dt public.dpto_choco"
```

**Resultado esperado:**
```
           List of relations
 Schema |    Name    | Type  |  Owner
--------+------------+-------+----------
 public | dpto_choco | table | postgres
(1 row)
```

**Si la tabla NO existe:**

**Opción A: Cargar desde choco.gpkg**

```bash
# Verificar que existe choco.gpkg
ls -lh /data/choco.gpkg

# Cargar capa de departamentos con ogr2ogr
ogr2ogr -f "PostgreSQL" PG:"dbname=postgres user=postgres" /data/choco.gpkg -nln dpto_choco -lco GEOMETRY_NAME=geom -a_srs EPSG:4326 dpto_choco
```

**Opción B: Si la tabla tiene otro nombre, buscarla:**

```bash
# Listar todas las tablas
psql -U postgres -d postgres -c "\dt"

# Buscar tablas con geometría
psql -U postgres -d postgres -c "SELECT f_table_name FROM geometry_columns;"
```

**NOTA:** Para este anexo, asumiremos que `dpto_choco` existe. Si usas otro nombre, ajusta los comandos SQL siguientes.

---

## A2.6 Paso 5: Crear Tabla de Puntos Intersectados con Chocó

Ahora crearemos una nueva tabla con solo los puntos que caen dentro del departamento de Chocó.

### Crear tabla puntos_admin_depto

```bash
psql -U postgres -d postgres << 'EOF'
CREATE TABLE puntos_admin_depto AS
SELECT p.gid, p.geom
FROM puntos_administrativos p, dpto_choco d
WHERE ST_Intersects(p.geom, d.geom);
EOF
```

**Explicación del SQL:**

**`CREATE TABLE ... AS SELECT ...`**
- Crea tabla y la llena con el resultado del SELECT

**`FROM puntos_administrativos p, dpto_choco d`**
- Une dos tablas (producto cartesiano filtrado por WHERE)
- Alias: `p` para puntos, `d` para departamento

**`WHERE ST_Intersects(p.geom, d.geom)`**
- Función espacial de PostGIS
- Retorna `true` si las geometrías se intersectan
- En este caso: si el punto está dentro del polígono del departamento

**Resultado esperado:**
```
SELECT [número de puntos en Chocó]
```

### Verificar tabla creada

```bash
psql -U postgres -d postgres -c "SELECT COUNT(*) FROM puntos_admin_depto;"
```

**Resultado esperado:**
```
 count
-------
  [número menor que la tabla completa]
(1 row)
```

### Agregar clave primaria e índice espacial

```bash
psql -U postgres -d postgres << 'EOF'
-- Agregar clave primaria
ALTER TABLE puntos_admin_depto ADD PRIMARY KEY (gid);

-- Crear índice espacial GIST
CREATE INDEX idx_puntos_admin_depto_geom ON puntos_admin_depto USING GIST(geom);

-- Registrar geometría en geometry_columns (si no está)
SELECT UpdateGeometrySRID('public', 'puntos_admin_depto', 'geom', 4326);
EOF
```

**Resultado esperado:**
```
ALTER TABLE
CREATE INDEX
 updategeometrysrid
--------------------
 public.puntos_admin_depto.geom SRID changed to 4326
(1 row)
```

---

## A2.6 Paso 5: Crear Vista con Buffer de 5000 Metros

Crearemos una vista que genera polígonos de buffer de 5000 metros alrededor de cada punto intersectado.

### Entender el problema de buffer en grados

**EPSG:4326 usa grados (lat/lon), NO metros.**

Para crear buffer de 5000 metros:
1. Reproyectar geometría a sistema métrico (EPSG:3857 - Web Mercator)
2. Hacer buffer de 5000 metros
3. Reproyectar resultado de vuelta a EPSG:4326

### Crear vista puntos_admin_buffer5000

```bash
psql -U postgres -d postgres << 'EOF'
CREATE OR REPLACE VIEW puntos_admin_buffer5000 AS
SELECT
    gid,
    ST_Transform(
        ST_Buffer(
            ST_Transform(geom, 3857),
            5000
        ),
        4326
    ) AS geom
FROM puntos_admin_depto;
EOF
```

**Explicación del SQL:**

**`CREATE OR REPLACE VIEW`**
- Crea una vista (tabla virtual que ejecuta query en tiempo real)
- `OR REPLACE`: Sobrescribe si ya existe

**`ST_Transform(geom, 3857)`** (interno)
- Reproyecta de EPSG:4326 (grados) a EPSG:3857 (metros)
- Web Mercator es proyección métrica

**`ST_Buffer(..., 5000)`**
- Crea buffer de 5000 unidades
- En EPSG:3857, las unidades son metros
- Resultado: polígono circular de 5000m de radio

**`ST_Transform(..., 4326)`** (externo)
- Reproyecta resultado de vuelta a EPSG:4326
- Para compatibilidad con GeoServer y Leaflet

**Resultado esperado:**
```
CREATE VIEW
```

### Verificar vista creada

```bash
psql -U postgres -d postgres -c "SELECT COUNT(*) FROM puntos_admin_buffer5000;"
```

**Ver geometría de un buffer:**
```bash
psql -U postgres -d postgres -c "SELECT gid, ST_GeometryType(geom), ST_NPoints(geom) FROM puntos_admin_buffer5000 LIMIT 3;"
```

**Resultado esperado:**
```
 gid | st_geometrytype | st_npoints
-----+-----------------+------------
   1 | ST_Polygon      |         33
   2 | ST_Polygon      |         33
   3 | ST_Polygon      |         33
(3 rows)
```

**Explicación:**
- `ST_Polygon`: Buffer genera polígonos
- `st_npoints`: ~32-33 puntos por buffer (aproximación circular)

### Registrar vista en geometry_columns (para GeoServer)

```bash
psql -U postgres -d postgres << 'EOF'
-- Insertar en geometry_columns manualmente
INSERT INTO geometry_columns
(f_table_catalog, f_table_schema, f_table_name, f_geometry_column, coord_dimension, srid, type)
VALUES
('', 'public', 'puntos_admin_buffer5000', 'geom', 2, 4326, 'POLYGON')
ON CONFLICT DO NOTHING;
EOF
```

**Resultado esperado:**
```
INSERT 0 1
```

O si ya existe:
```
INSERT 0 0
```

---

## A2.6 Paso 5: Salir del Contenedor PostGIS

```bash
exit
```

Ahora estás de vuelta en tu terminal local.

---

## A2.12 Paso 11: Publicar Capas en GeoServer

Ahora publicaremos las 3 capas en GeoServer usando la interfaz web.

### Paso 11.1: Acceder a GeoServer

1. Abrir navegador
2. Visitar: http://localhost:8080/geoserver/web/
3. Login:
   - **Usuario:** `admin`
   - **Contraseña:** `geoserver`

### Paso 11.2: Verificar Store de PostGIS

**Verificar que existe conexión a PostGIS:**

1. En menú lateral: **Stores** → Click en store existente (ej: `postgis_store`)
2. Verificar parámetros de conexión:
   - **host:** `postgis` (nombre del servicio Docker)
   - **port:** `5432`
   - **database:** `postgres`
   - **user:** `postgres`
   - **passwd:** [contraseña si existe]

**Si NO existe store de PostGIS:**

1. **Stores** → **Add new Store**
2. Seleccionar: **PostGIS - PostGIS Database**
3. Configurar:
   - **Workspace:** `ne`
   - **Data Source Name:** `postgis_store`
   - **host:** `postgis`
   - **port:** `5432`
   - **database:** `postgres`
   - **schema:** `public`
   - **user:** `postgres`
   - **passwd:** [vacío o contraseña]
4. Click **Save**

### Paso 11.3: Publicar Capa 1 - puntos_administrativos (WMS)

**1. Crear nueva capa:**
- **Layers** → **Add a new layer**
- Seleccionar store: `ne:postgis_store`
- Click **Configure new layer**

**2. Buscar tabla:**
- En lista, buscar: `puntos_administrativos`
- Click **Publish**

**3. Configurar capa:**

**Tab "Data":**
- **Name:** `puntos_administrativos`
- **Title:** `Puntos Administrativos (Completo)`
- **Abstract:** `Capa completa de puntos administrativos de Colombia`

**Native Bounding Box:**
- Click **Compute from data**
- Click **Compute from native bounds**

**Coordinate Reference Systems:**
- **Native SRS:** `EPSG:4326`
- **Declared SRS:** `EPSG:4326`
- **SRS handling:** `Force declared`

**Tab "Publishing":**
- **Default Style:** Seleccionar `point` o crear estilo personalizado

**4. Guardar:**
- Scroll abajo
- Click **Save**

**Resultado esperado:**
```
Layer 'ne:puntos_administrativos' saved successfully
```

### Paso 11.4: Publicar Capa 2 - puntos_admin_depto (WFS)

**Repetir pasos de 11.3 con estos datos:**

- **Name:** `puntos_admin_depto`
- **Title:** `Puntos Administrativos - Chocó`
- **Abstract:** `Puntos administrativos dentro del departamento de Chocó`
- **Native SRS:** `EPSG:4326`
- **Declared SRS:** `EPSG:4326`

**IMPORTANTE para WFS:**

**Tab "Publishing":**
- Scroll hasta **Service Metadata**
- Marcar checkbox: **WFS** (habilitar para WFS)

**Guardar:** Click **Save**

### Paso 11.5: Publicar Capa 3 - puntos_admin_buffer5000 (WFS)

**Repetir pasos de 11.3 con estos datos:**

- **Name:** `puntos_admin_buffer5000`
- **Title:** `Buffer 5000m - Puntos Administrativos Chocó`
- **Abstract:** `Buffer de 5000 metros alrededor de puntos administrativos en Chocó`
- **Native SRS:** `EPSG:4326`
- **Declared SRS:** `EPSG:4326`

**Tab "Publishing":**
- **Default Style:** `polygon` (es polígono, no punto)
- Marcar checkbox: **WFS**

**Guardar:** Click **Save**

---

## A2.6 Paso 5: Verificar Capas en GeoServer

### Verificar con Layer Preview

1. En menú lateral: **Layer Preview**
2. Buscar capas:
   - `ne:puntos_administrativos`
   - `ne:puntos_admin_depto`
   - `ne:puntos_admin_buffer5000`

3. Para cada capa, click en **OpenLayers**

**Resultado esperado:**
- Se abre mapa con la capa visible
- Puntos o polígonos renderizados correctamente

### Probar WFS GetCapabilities

```bash
# En terminal local
curl "http://localhost:8080/geoserver/ne/wfs?service=WFS&version=2.0.0&request=GetCapabilities" | grep -i "puntos_admin"
```

**Resultado esperado:**
```xml
<FeatureType>
  <Name>ne:puntos_administrativos</Name>
  ...
</FeatureType>
<FeatureType>
  <Name>ne:puntos_admin_depto</Name>
  ...
</FeatureType>
<FeatureType>
  <Name>ne:puntos_admin_buffer5000</Name>
  ...
</FeatureType>
```

### Probar WFS GetFeature

```bash
# Obtener 1 feature de puntos_admin_depto
curl "http://localhost:8080/geoserver/ne/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=ne:puntos_admin_depto&maxFeatures=1&outputFormat=application/json"
```

**Resultado esperado:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "puntos_admin_depto.1",
      "geometry": {
        "type": "Point",
        "coordinates": [-76.xxx, 5.xxx]
      },
      "properties": {
        "gid": 1
      }
    }
  ],
  ...
}
```

---

## A2.14 Paso 13: Integrar Capas al Visor Web

Ahora modificaremos `webapp/static/js/app.js` para agregar las 3 nuevas capas.

### Paso 13.1: Abrir app.js

```bash
# Abrir en tu editor de código
# Ubicación: webapp/static/js/app.js
```

### Paso 13.2: Agregar Capa WMS (puntos_administrativos)

**Buscar la sección de capas WMS** (después de `municipiosWMS`):

```javascript
// ============================================
// Capas WMS de GeoServer
// ============================================

const departamentosWMS = L.tileLayer.wms(GEOSERVER_URL, {
    layers: 'ne:dpto_choco',
    format: 'image/png',
    transparent: true,
    attribution: 'IGAC - Instituto Geográfico Agustín Codazzi',
    styles: ''
});

const municipiosWMS = L.tileLayer.wms(GEOSERVER_URL, {
    layers: 'ne:mpios_choco',
    format: 'image/png',
    transparent: true,
    attribution: 'IGAC',
    styles: ''
});

// AGREGAR AQUÍ ↓
const puntosAdministrativosWMS = L.tileLayer.wms(GEOSERVER_URL, {
    layers: 'ne:puntos_administrativos',
    format: 'image/png',
    transparent: true,
    attribution: 'IGAC',
    styles: ''
});
```

### Paso 13.3: Agregar al Control de Capas

**Buscar `overlayLayers`:**

```javascript
const overlayLayers = {
    'Departamentos (WMS)': departamentosWMS,
    'Municipios (WMS)': municipiosWMS,
    // AGREGAR AQUÍ ↓
    'Puntos Administrativos (WMS)': puntosAdministrativosWMS
};
```

### Paso 13.4: Agregar Funciones de Carga WFS

**Buscar la función `loadDepartamentosWFS()` y agregar después de ella:**

```javascript
// Función para cargar puntos administrativos Chocó desde WFS
function loadPuntosAdminDeptoWFS() {
    const wfsUrl = `/api/geoserver-proxy?service=WFS&version=2.0.0&request=GetFeature&typeName=ne:puntos_admin_depto&outputFormat=application/json`;

    fetch(wfsUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar puntos administrativos WFS');
            }
            return response.json();
        })
        .then(data => {
            const puntosAdminGeoJSON = L.geoJSON(data, {
                pointToLayer: function (feature, latlng) {
                    return L.circleMarker(latlng, {
                        radius: 6,
                        fillColor: "#ff7800",
                        color: "#000",
                        weight: 1,
                        opacity: 1,
                        fillOpacity: 0.8
                    });
                },
                onEachFeature: function (feature, layer) {
                    if (feature.properties) {
                        const popupContent = `
                            <div class="popup-title">Punto Administrativo</div>
                            <div class="popup-divider"></div>
                            <div class="popup-info"><strong>GID:</strong> ${feature.properties.gid || 'N/A'}</div>
                        `;
                        layer.bindPopup(popupContent);
                    }
                }
            }).addTo(map);

            layerControl.addOverlay(puntosAdminGeoJSON, 'Puntos Admin Chocó (WFS)');
            console.log('Puntos administrativos Chocó cargados:', data.features.length);
        })
        .catch(error => {
            console.error('Error cargando puntos admin WFS:', error);
        });
}

// Función para cargar buffer de puntos desde WFS
function loadBufferWFS() {
    const wfsUrl = `/api/geoserver-proxy?service=WFS&version=2.0.0&request=GetFeature&typeName=ne:puntos_admin_buffer5000&outputFormat=application/json`;

    fetch(wfsUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar buffer WFS');
            }
            return response.json();
        })
        .then(data => {
            const bufferGeoJSON = L.geoJSON(data, {
                style: function (feature) {
                    return {
                        fillColor: '#3388ff',
                        weight: 2,
                        opacity: 0.6,
                        color: '#0066cc',
                        fillOpacity: 0.3
                    };
                },
                onEachFeature: function (feature, layer) {
                    if (feature.properties) {
                        const popupContent = `
                            <div class="popup-title">Buffer 5000m</div>
                            <div class="popup-divider"></div>
                            <div class="popup-info"><strong>GID:</strong> ${feature.properties.gid || 'N/A'}</div>
                        `;
                        layer.bindPopup(popupContent);
                    }
                }
            }).addTo(map);

            layerControl.addOverlay(bufferGeoJSON, 'Buffer 5000m (WFS)');
            console.log('Buffer 5000m cargado:', data.features.length);
        })
        .catch(error => {
            console.error('Error cargando buffer WFS:', error);
        });
}
```

**Explicación:**

**`pointToLayer`:**
- Función para personalizar cómo se renderizan los puntos
- `L.circleMarker`: Crea círculos de tamaño fijo (no escalan con zoom)
- `radius: 6`: Tamaño del círculo
- `fillColor: "#ff7800"`: Color naranja

**`style` (para buffer):**
- Buffer son polígonos, usan `style` (no `pointToLayer`)
- Color azul semi-transparente

### Paso 13.5: Llamar Funciones en Inicialización

**Buscar la sección de inicialización:**

```javascript
// ============================================
// Inicialización
// ============================================

// Cargar datos WFS al cargar la página
window.addEventListener('load', function() {
    console.log('Iniciando aplicación...');
    loadDepartamentosWFS();
    // AGREGAR AQUÍ ↓
    loadPuntosAdminDeptoWFS();
    loadBufferWFS();
});
```

### Paso 13.6: Guardar y Reiniciar

```bash
# Guardar app.js

# Reiniciar contenedor webapp
docker-compose restart webapp

# Ver logs
docker-compose logs -f webapp
```

---

## A2.15 Checkpoint: Verificar Aplicación Completa

### Paso 1: Abrir navegador

Visitar: http://localhost:5000/map-dpto

### Paso 2: Verificar capas en control

**Control de capas (superior derecha) debe mostrar:**

**Base Layers (radio buttons):**
- ○ Mapa base (OSM)
- ○ Satélite (Esri)
- ○ Calles (CartoDB)

**Overlay Layers (checkboxes):**
- ☐ Departamentos (WMS)
- ☐ Municipios (WMS)
- ☐ Puntos Administrativos (WMS)
- ☑ Departamentos Interactivos (WFS)
- ☑ Puntos Admin Chocó (WFS)
- ☑ Buffer 5000m (WFS)

### Paso 3: Verificar carga automática

**Al cargar la página:**
- Polígonos de departamentos (amarillo)
- Puntos administrativos (naranja, solo Chocó)
- Buffers azules alrededor de puntos

### Paso 4: Verificar interactividad

**Capa WMS (Puntos Administrativos):**
- Activar checkbox "Puntos Administrativos (WMS)"
- Aparecen puntos de toda Colombia
- No interactivos (son imagen)

**Capa WFS (Puntos Admin Chocó):**
- Click en punto naranja
- Popup con información
- Círculo naranja fijo (no escala con zoom)

**Capa WFS (Buffer 5000m):**
- Click en buffer azul
- Popup con GID
- Polígono circular azul semi-transparente

### Paso 5: Verificar consola (F12)

**Mensajes esperados:**
```
Iniciando aplicación...
Departamentos cargados: 33
Puntos administrativos Chocó cargados: [número]
Buffer 5000m cargado: [número]
```

**Sin errores de:**
- CORS
- 404 (proxy funciona)
- JavaScript

---

## A2.16 Visualización de Capas Superpuestas

**Vista esperada del mapa:**

```
┌──────────────────────────────────────────┐
│                                          │
│    ╔════════════════════╗                │
│    ║   Departamento    ║  ← Polígono amarillo (WFS)
│    ║     Chocó         ║                 │
│    ║                   ║                 │
│    ║    ⚪ ← Punto     ║                 │
│    ║    🔵 ← Buffer    ║                 │
│    ║                   ║                 │
│    ╚════════════════════╝                │
│                                          │
└──────────────────────────────────────────┘

Leyenda:
⚪ Punto administrativo (naranja)
🔵 Buffer 5000m (azul, semi-transparente)
```

**Capas superpuestas:**
1. Capa base (OSM/Satélite/CartoDB)
2. Departamento Chocó (polígono amarillo)
3. Buffer 5000m (polígonos azules)
4. Puntos administrativos (círculos naranjas)

---

## A2.17 Resumen

Has aprendido:

**Descarga y preparación:**
- Descargar shapefile desde GitHub
- Montar volumen Docker para acceso a archivos

**Gestión de contenedor PostGIS:**
- Acceder al shell del contenedor
- Instalar herramientas (unzip)
- Navegar sistema de archivos del contenedor

**Carga de datos geográficos:**
- Descomprimir shapefiles
- Usar `shp2pgsql` para cargar shapefile a PostGIS
- Verificar carga con SQL

**Operaciones espaciales en PostGIS:**
- `ST_Intersects()`: Filtrar puntos dentro de polígono
- `ST_Transform()`: Reproyectar geometrías
- `ST_Buffer()`: Crear buffers métricos
- Crear tablas y vistas geográficas

**Publicación en GeoServer:**
- Publicar capas desde PostGIS
- Configurar capas para WMS y WFS
- Verificar servicios OGC

**Integración al visor web:**
- Agregar capas WMS a Leaflet
- Cargar capas WFS con fetch()
- Personalizar estilos de puntos (`pointToLayer`)
- Estilizar polígonos (buffers)
- Agregar popups informativos

### Archivos modificados

- `docker-compose.yml` (volumen agregado, si no existía)
- `webapp/static/js/app.js` (~100 líneas agregadas)

### Tablas/vistas creadas en PostGIS

- `puntos_administrativos` (tabla) - ~[total] puntos
- `puntos_admin_depto` (tabla) - ~[filtrado] puntos
- `puntos_admin_buffer5000` (vista) - ~[filtrado] buffers

### Capas publicadas en GeoServer

- `ne:puntos_administrativos` (WMS)
- `ne:puntos_admin_depto` (WFS)
- `ne:puntos_admin_buffer5000` (WFS)

### Conceptos clave de PostGIS

| Función | Descripción |
|---------|-------------|
| **ST_Intersects(geom1, geom2)** | Verifica si geometrías se intersectan |
| **ST_Transform(geom, srid)** | Reproyecta geometría a otro SRID |
| **ST_Buffer(geom, distance)** | Crea buffer de distancia especificada |
| **ST_AsText(geom)** | Convierte geometría a WKT (texto) |
| **ST_GeometryType(geom)** | Retorna tipo de geometría |
| **ST_NPoints(geom)** | Cuenta puntos en geometría |

### Comandos útiles aprendidos

```bash
# Docker
docker exec -it postgis bash          # Entrar a contenedor
docker-compose restart webapp          # Reiniciar servicio

# PostGIS
shp2pgsql -s 4326 -I file.shp table   # Convertir shapefile a SQL
psql -U postgres -d postgres -c "SQL" # Ejecutar SQL
\dt                                    # Listar tablas (dentro de psql)

# Sistema
unzip archivo.zip                      # Descomprimir
ls -lh /data/                         # Listar archivos con detalles
apt-get install -y unzip              # Instalar paquete
```

### Ejercicios adicionales (opcionales)

**1. Filtrar por atributo:**
- Crear tabla con puntos de un tipo específico
- Ejemplo: `WHERE tipo = 'Municipalidad'`

**2. Buffer variable:**
- Crear buffers de diferentes tamaños según atributo
- Ejemplo: 2000m para unos, 5000m para otros

**3. Unión espacial:**
- Agregar nombre del municipio a cada punto
- Usar `ST_Intersects` con capa de municipios

**4. Análisis de densidad:**
- Contar puntos por departamento
- Crear mapa coroplético con colores según cantidad

---

**[⬅️ Volver al Índice](README.md)** | **[Siguiente: Módulo 8 - Troubleshooting ➡️](08_TROUBLESHOOTING.md)**
