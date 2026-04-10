# Aplicación Web de Visualización Geoespacial - Amazonas Colombia

## Descripción

Aplicación web desarrollada con Flask y Folium para visualizar datos geoespaciales del departamento del Amazonas en Colombia. Los datos se obtienen desde una base de datos PostgreSQL/PostGIS y se visualizan en mapas interactivos.

## Características

### Funcionalidades Principales

- **Mapa Interactivo:** Visualización del departamento del Amazonas con Folium
- **Puntos Administrativos:** Marcadores con información detallada
- **Clustering:** Agrupación inteligente de marcadores para mejor rendimiento
- **Múltiples Capas:** OpenStreetMap, Terreno, Toner, CartoDB
- **Estadísticas en Tiempo Real:** Datos actualizados desde PostgreSQL
- **API RESTful:** Endpoints para consumo de datos

### Tecnologías Utilizadas

- **Backend:** Flask 3.0.0
- **Mapas:** Folium 0.15.0
- **Base de Datos:** PostgreSQL/PostGIS con psycopg2
- **Análisis Geoespacial:** GeoPandas, Shapely
- **Frontend:** Bootstrap 5.3.0, Font Awesome
- **Contenedorización:** Docker

## Estructura de Archivos

```
webapp/
├── app.py                  # Aplicación Flask principal
├── requirements.txt        # Dependencias de Python
├── templates/
│   └── index.html         # Plantilla HTML principal
├── static/
│   ├── css/
│   │   └── style.css      # Estilos personalizados
│   └── js/                # Scripts JavaScript (futuro)
└── README.md              # Este archivo
```

## Endpoints API

### GET /
- **Descripción:** Página principal con el visor de mapas
- **Respuesta:** HTML

### GET /mapa
- **Descripción:** Genera el mapa de Folium
- **Respuesta:** HTML embebido del mapa

### GET /api/estadisticas
- **Descripción:** Obtiene estadísticas generales
- **Respuesta JSON:**
```json
{
  "total_departamentos": 1,
  "total_puntos": 131,
  "total_proyectos": 5,
  "area_km2": 109665.45
}
```

### GET /api/departamento
- **Descripción:** Obtiene datos del departamento
- **Respuesta JSON:**
```json
{
  "codigo": "91",
  "nombre": "AMAZONAS",
  "geojson": {
    "type": "MultiPolygon",
    "coordinates": [...]
  }
}
```

### GET /api/puntos
- **Descripción:** Lista todos los puntos administrativos
- **Respuesta JSON:**
```json
[
  {
    "gid": 1,
    "nombre_geo": "Leticia",
    "codigo_nom": "91001",
    "symbol": "circle",
    "proyecto": "IGAC",
    "fecha": "2023-01-15",
    "escala": 25000,
    "geojson": {
      "type": "Point",
      "coordinates": [-69.9406, 4.2154, 96]
    }
  },
  ...
]
```

### GET /health
- **Descripción:** Health check de la aplicación
- **Respuesta JSON:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

## Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `DB_HOST` | Host de PostgreSQL | `postgis` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `DB_NAME` | Nombre de la base de datos | `geodatos` |
| `DB_USER` | Usuario de la base de datos | `postgres` |
| `DB_PASSWORD` | Contraseña de la base de datos | `postgres` |
| `FLASK_ENV` | Entorno de Flask | `development` |

## Instalación y Ejecución

### Con Docker (Recomendado)

```bash
# Construir la imagen
docker-compose build webapp

# Iniciar el servicio
docker-compose up -d webapp

# Ver logs
docker logs -f webapp
```

### Sin Docker (Desarrollo Local)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=geodatos
export DB_USER=postgres
export DB_PASSWORD=postgres

# Ejecutar la aplicación
python app.py
```

## Acceso

Una vez iniciada la aplicación:

- **Interfaz Web:** http://localhost:5000
- **API Estadísticas:** http://localhost:5000/api/estadisticas
- **API Departamento:** http://localhost:5000/api/departamento
- **API Puntos:** http://localhost:5000/api/puntos
- **Health Check:** http://localhost:5000/health

## Desarrollo

### Agregar Nuevas Rutas

```python
@app.route('/nueva-ruta')
def nueva_ruta():
    """Documentación de la ruta"""
    # Lógica aquí
    return render_template('template.html')
```

### Consultas a la Base de Datos

```python
def obtener_datos():
    conn = get_db_connection()
    try:
        query = "SELECT * FROM tabla WHERE condicion = %s"
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (parametro,))
            results = cursor.fetchall()
            return results
    finally:
        conn.close()
```

### Personalizar el Mapa

Editar la función `mapa()` en `app.py`:

```python
# Cambiar ubicación inicial
m = folium.Map(
    location=[nueva_lat, nueva_lon],
    zoom_start=nuevo_zoom
)

# Agregar nuevos tiles
folium.TileLayer('Stamen Watercolor', name='Acuarela').add_to(m)

# Agregar plugins
from folium.plugins import HeatMap, Draw
```

## Características del Mapa

### Capas Incluidas
- OpenStreetMap (por defecto)
- Stamen Terrain
- Stamen Toner
- CartoDB Positron

### Plugins Activos
- **MarkerCluster:** Agrupa marcadores cercanos
- **MeasureControl:** Herramienta de medición
- **MiniMap:** Mini mapa de navegación
- **LayerControl:** Control de capas

### Personalización de Marcadores

Los marcadores se colorean según el símbolo:
- `circle` → Azul
- `square` → Rojo
- `triangle` → Verde
- `star` → Naranja
- Otros → Gris

## Optimización

### Performance

1. **Clustering de Marcadores:** Reduce el número de marcadores visibles
2. **Lazy Loading:** El mapa se carga después del DOM
3. **Índices Geoespaciales:** La base de datos tiene índices GIST
4. **Caché de Tiles:** Los tiles del mapa se cachean en el navegador

### Escalabilidad

Para grandes volúmenes de datos:

```python
# Implementar paginación
@app.route('/api/puntos')
def api_puntos():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    # Consulta con LIMIT y OFFSET
    query = """
    SELECT * FROM puntos_administrativos
    ORDER BY nombre_geo
    LIMIT %s OFFSET %s;
    """
    # ...
```

## Troubleshooting

### La aplicación no se conecta a la base de datos

```bash
# Verificar que PostgreSQL está corriendo
docker ps | grep postgis

# Verificar conectividad
docker exec webapp ping -c 3 postgis

# Ver logs de la aplicación
docker logs webapp
```

### El mapa no se muestra

1. Verificar la consola del navegador (F12)
2. Verificar que `/mapa` retorna HTML
3. Verificar datos en la base de datos:
```bash
docker exec postgis psql -U postgres -d geodatos -c "SELECT COUNT(*) FROM dpto_amazonas;"
```

### Error de módulos Python

```bash
# Reconstruir la imagen
docker-compose build --no-cache webapp

# Verificar requirements.txt
docker exec webapp pip list
```

## Mejoras Futuras

- [ ] Autenticación de usuarios
- [ ] Panel de administración
- [ ] Exportación de datos (CSV, GeoJSON, KML)
- [ ] Análisis espacial en tiempo real
- [ ] Gráficas interactivas (Chart.js)
- [ ] WebSockets para actualizaciones en tiempo real
- [ ] Soporte multiidioma (i18n)
- [ ] Tema oscuro
- [ ] Reportes en PDF

## Contribuir

Para contribuir al proyecto:

1. Fork el repositorio
2. Crear una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Agrega nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## Licencia

Este proyecto es parte del curso de Servicios SIG - Universidad Juan de Castellanos.

## Contacto

Para preguntas o sugerencias sobre la aplicación web, por favor crear un issue en el repositorio.

---

**Última actualización:** 2025-11-07
**Versión:** 1.0.0
