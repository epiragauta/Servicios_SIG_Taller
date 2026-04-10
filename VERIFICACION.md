# Guía de Verificación - PostgreSQL/PostGIS con GeoPackage

## Problema común: Scripts no se ejecutan

Los scripts en `init-scripts/` **solo se ejecutan la primera vez** que se inicializa la base de datos. Si el volumen de PostgreSQL ya existe, los scripts se omiten.

## Solución: Reiniciar desde cero

```bash
# 1. Detener y eliminar contenedores
docker-compose down

# 2. Eliminar el volumen de PostgreSQL (esto borra los datos)
docker volume rm servicios_sig_taller_postgres_data

# 3. Iniciar los servicios
docker-compose up -d

# 4. Ver los logs en tiempo real para verificar la ejecución
docker logs -f postgis
```

## Verificar que los scripts se ejecutaron correctamente

### 1. Ver los logs del contenedor postgis
```bash
docker logs postgis
```

**Buscar estos mensajes:**
- `Habilitando extensión PostGIS en la base de datos geodatos...`
- `PostGIS habilitado correctamente en la base de datos geodatos`
- `Instalando herramientas GDAL para importar GeoPackage...`
- `Importando capa: dpto_amazonas`
- `Importando capa: puntos_administrativos`
- `Todas las capas han sido importadas!`

**NO debe aparecer:**
- `PostgreSQL Database directory appears to contain a database; Skipping initialization`

### 2. Conectarse a la base de datos y verificar las tablas
```bash
docker exec -it postgis psql -U postgres -d geodatos
```

Una vez dentro de psql, ejecutar:
```sql
-- Listar todas las tablas
\dt

-- Ver las extensiones de PostGIS instaladas
\dx

-- Contar registros en cada tabla
SELECT 'dpto_amazonas' as tabla, COUNT(*) as registros FROM dpto_amazonas
UNION ALL
SELECT 'puntos_administrativos' as tabla, COUNT(*) as registros FROM puntos_administrativos;

-- Ver la estructura de las tablas
\d dpto_amazonas
\d puntos_administrativos

-- Verificar que las geometrías están correctamente configuradas
SELECT f_table_name, f_geometry_column, type, srid
FROM geometry_columns
WHERE f_table_name IN ('dpto_amazonas', 'puntos_administrativos');

-- Salir
\q
```

### 3. Verificar desde fuera del contenedor
```bash
# Listar las tablas
docker exec -it postgis psql -U postgres -d geodatos -c "\dt"

# Contar registros
docker exec -it postgis psql -U postgres -d geodatos -c "SELECT 'dpto_amazonas' as tabla, COUNT(*) as registros FROM dpto_amazonas UNION ALL SELECT 'puntos_administrativos' as tabla, COUNT(*) as registros FROM puntos_administrativos;"
```

## Información de conexión

- **Host:** localhost
- **Puerto:** 5432
- **Base de datos:** geodatos
- **Usuario:** postgres
- **Contraseña:** postgres

## Conexión desde herramientas externas

### QGIS
1. Agregar nueva conexión PostGIS
2. Usar los datos de conexión de arriba
3. Las capas `dpto_amazonas` y `puntos_administrativos` deberían aparecer

### pgAdmin
1. Crear nuevo servidor
2. Connection → Host: localhost, Port: 5432
3. Connection → Username: postgres, Password: postgres
4. Navegar a: Servers → [tu servidor] → Databases → geodatos → Schemas → public → Tables

### DBeaver / DataGrip
1. Nueva conexión PostgreSQL
2. Usar los datos de conexión de arriba
3. Explorar las tablas en el schema `public`

## Solución de problemas

### Los scripts fallan durante la ejecución
```bash
# Ver logs completos con errores
docker logs postgis 2>&1 | grep -i error

# Verificar que el archivo GeoPackage está montado correctamente
docker exec -it postgis ls -lh /geopackage/

# Debe mostrar: amazonas.gpkg
```

### Verificar permisos de los scripts
```bash
# Los scripts deben ser ejecutables
chmod +x init-scripts/*.sh
```

### Reiniciar solo el contenedor de PostGIS
```bash
docker-compose restart postgis
docker logs -f postgis
```

## Estructura de archivos

```
.
├── docker-compose.yml
├── init-scripts/
│   ├── 01-init-postgis.sh       # Habilita extensiones PostGIS
│   └── 02-import-geopackage.sh  # Importa las capas del GeoPackage
└── data/
    └── geopackage/
        └── amazonas.gpkg         # Contiene: dpto_amazonas, puntos_administrativos
```

## Tablas creadas

| Tabla | Geometría | SRID | Origen |
|-------|-----------|------|--------|
| `dpto_amazonas` | MULTIPOLYGON/POLYGON | Según GeoPackage | amazonas.gpkg |
| `puntos_administrativos` | POINT | Según GeoPackage | amazonas.gpkg |

Ambas tablas tienen:
- Columna de geometría: `geom`
- Clave primaria: `gid`
