# Módulo 2: Prerequisitos

## Objetivos de Aprendizaje

Al completar este módulo, habrás:

- Verificado que todo el software necesario está instalado
- Comprobado que los servicios están funcionando correctamente
- Identificado los conocimientos previos necesarios
- Preparado tu entorno de desarrollo
- Realizado pruebas básicas de conectividad

---

## 2.1 Software Requerido (Asumido Instalado)

Este módulo asume que ya tienes instalado el siguiente software. Si no es así, consulta con tu instructor.

### Componentes principales

| Software | Versión mínima | Propósito | Puerto |
|----------|----------------|-----------|--------|
| **GeoServer** | 2.20+ | Servidor de mapas OGC | 8080 |
| **Python** | 3.8+ | Backend y proxy | - |
| **Docker** | 20.10+ | Contenedores | - |
| **Docker Compose** | 1.29+ | Orquestación | - |
| **PostgreSQL/PostGIS** | 12+/3.0+ | Base de datos espacial | 5432 |

### Herramientas de desarrollo

| Herramienta | Recomendación | Propósito |
|-------------|---------------|-----------|
| **Editor de código** | VS Code | Edición de código |
| **Navegador** | Chrome/Firefox | Desarrollo y debugging |
| **Cliente REST** | Thunder Client/Postman | Pruebas de API |
| **Git** | Cualquier versión | Control de versiones |

---

## 2.2 Verificación del Entorno

### 2.2.1 Verificar Python

Abre una terminal y ejecuta:

```bash
python --version
```

**Salida esperada:**
```
Python 3.8.10  (o superior)
```

**Verificar pip:**
```bash
pip --version
```

**Salida esperada:**
```
pip 21.0.1 from ... (python 3.8)
```

### 2.2.2 Verificar Docker

```bash
docker --version
```

**Salida esperada:**
```
Docker version 20.10.12, build e91ed57
```

**Verificar Docker Compose:**
```bash
docker-compose --version
```

**Salida esperada:**
```
docker-compose version 1.29.2, build 5becea4c
```

**Verificar contenedores en ejecución:**
```bash
docker ps
```

**Salida esperada (ejemplo):**
```
CONTAINER ID   IMAGE              STATUS        PORTS                    NAMES
abc123def456   geoserver:latest   Up 2 hours    0.0.0.0:8080->8080/tcp   geoserver
def456abc789   postgis/postgis    Up 2 hours    0.0.0.0:5432->5432/tcp   postgis
```

> **IMPORTANTE:** Debes ver al menos los contenedores de GeoServer y PostgreSQL/PostGIS ejecutándose.

### 2.2.3 Verificar GeoServer

#### Método 1: Navegador

Abre tu navegador y visita:
```
http://localhost:8080/geoserver/web/
```

**Resultado esperado:**
- Página de login de GeoServer
- Credenciales por defecto: `admin` / `geoserver`

#### Método 2: Línea de comandos

```bash
curl http://localhost:8080/geoserver/web/
```

**Resultado esperado:**
- HTML de la página de GeoServer (sin error 404 o connection refused)

#### Verificar workspace y capas

Una vez dentro de GeoServer (admin/geoserver):

1. **Ir a "Workspaces"**
   - Debe existir un workspace llamado `ne`

2. **Ir a "Layers"**
   - Buscar: `ne:dpto_choco`
   - Buscar: `ne:mpios_choco`
   - Buscar: `ne:departamentos`

> **NOTA:** Si estas capas no existen, debes importarlas desde los shapefiles o GeoPackage del proyecto.

#### Probar servicio WMS

```bash
curl "http://localhost:8080/geoserver/ne/wms?service=WMS&version=1.3.0&request=GetCapabilities"
```

**Resultado esperado:**
- XML con información del servicio (GetCapabilities document)

#### Probar servicio WFS

```bash
curl "http://localhost:8080/geoserver/ne/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=ne:departamentos&maxFeatures=1&outputFormat=application/json"
```

**Resultado esperado:**
- JSON con un GeoJSON feature

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {...},
      "properties": {...}
    }
  ]
}
```

### 2.2.4 Verificar PostgreSQL/PostGIS

```bash
docker exec -it postgis psql -U postgres -d geodatos -c "SELECT version();"
```

**Resultado esperado:**
```
PostgreSQL 14.x on ...
```

**Verificar extensión PostGIS:**
```bash
docker exec -it postgis psql -U postgres -d geodatos -c "SELECT PostGIS_Version();"
```

**Resultado esperado:**
```
3.1 USE_GEOS=1 USE_PROJ=1 ...
```

> **NOTA:** El nombre del contenedor puede variar. Usa `docker ps` para verificar el nombre correcto.

### 2.2.5 Verificar estructura del proyecto

Navega al directorio del proyecto y verifica la estructura:

```bash
cd C:\ws\ujdc\Servicios_SIG_Taller
ls -la
```

**Estructura esperada:**
```
Servicios_SIG_Taller/
├── data/
│   └── shapefiles/
│       └── choco.gpkg
├── init-scripts/
│   ├── 01-init-postgis.sh
│   └── 02-import-geopackage.sh
├── webapp/
│   ├── app.py
│   ├── static/
│   │   ├── css/
│   │   │   └── app.css
│   │   └── js/
│   │       └── app.js
│   └── templates/
│       └── app/
│           └── index.html
├── docker-compose.yml
└── README.md
```

---

## 2.3 Instalación de Dependencias Python

Si aún no has instalado las dependencias de Python, ejecuta:

```bash
cd webapp
pip install Flask psycopg2-binary requests flask-cors
```

**Paquetes instalados:**

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| `Flask` | 2.0+ | Framework web |
| `psycopg2-binary` | 2.9+ | Conector PostgreSQL |
| `requests` | 2.27+ | Cliente HTTP para proxy |
| `flask-cors` | 3.0+ | Manejo de CORS |

**Verificar instalación:**
```bash
pip list | grep -E "Flask|psycopg2|requests|flask-cors"
```

**Alternativa: requirements.txt**

Crear archivo `webapp/requirements.txt`:
```
Flask==2.3.0
psycopg2-binary==2.9.6
requests==2.28.2
flask-cors==3.0.10
```

Instalar:
```bash
pip install -r requirements.txt
```

---

## 2.4 Conocimientos Previos Necesarios

### 2.4.1 HTML5 - Nivel Básico

**Debes conocer:**

Estructura básica de documento HTML
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Título</title>
</head>
<body>
    <!-- Contenido -->
</body>
</html>
```

Elementos semánticos: `<header>`, `<main>`, `<aside>`, `<footer>`

Enlaces a recursos externos:
```html
<link rel="stylesheet" href="styles.css">
<script src="script.js"></script>
```

Atributos `id` y `class`:
```html
<div id="map" class="container"></div>
```

**Recursos de repaso:**
- MDN HTML Basics: https://developer.mozilla.org/es/docs/Learn/HTML

### 2.4.2 CSS3 - Nivel Básico

**Debes conocer:**

Selectores básicos:
```css
/* Por elemento */
body { }

/* Por clase */
.container { }

/* Por ID */
#map { }
```

Modelo de caja (box model):
```css
.box {
    width: 300px;
    height: 200px;
    padding: 10px;
    margin: 20px;
    border: 1px solid #ccc;
}
```

Flexbox (nivel básico):
```css
.container {
    display: flex;
    flex-direction: row;
}

.item {
    flex: 1;
}
```

Unidades: `px`, `%`, `rem`, `vh`, `vw`

**Recursos de repaso:**
- MDN CSS Basics: https://developer.mozilla.org/es/docs/Learn/CSS
- Flexbox Froggy (juego): https://flexboxfroggy.com/

### 2.4.3 JavaScript ES6 - Nivel Intermedio

**Debes conocer:**

Variables con `let` y `const`:
```javascript
const API_URL = 'http://localhost:8080';
let contador = 0;
```

Funciones arrow:
```javascript
const suma = (a, b) => a + b;
```

Template literals:
```javascript
const nombre = "Juan";
const mensaje = `Hola ${nombre}`;
```

Promesas y `then/catch`:
```javascript
fetch(url)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
```

Async/await (opcional pero útil):
```javascript
async function cargarDatos() {
    try {
        const response = await fetch(url);
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error(error);
    }
}
```

Manipulación del DOM:
```javascript
document.getElementById('boton').addEventListener('click', () => {
    console.log('Click!');
});
```

Objetos y destructuring:
```javascript
const config = {
    zoom: 6,
    center: [4.5, -74.2]
};

const { zoom, center } = config;
```

**Recursos de repaso:**
- MDN JavaScript: https://developer.mozilla.org/es/docs/Web/JavaScript
- JavaScript.info: https://javascript.info/

### 2.4.4 Conceptos SIG - Nivel Básico

**Debes conocer:**

**Coordenadas geográficas:**
- Latitud: -90° a +90° (Sur a Norte)
- Longitud: -180° a +180° (Oeste a Este)
- Ejemplo: Bogotá = [4.5709, -74.2973]

**Sistemas de referencia (CRS/SRS):**
- EPSG:4326 = WGS84 (latitud/longitud)
- EPSG:3857 = Web Mercator (metros, usado por Google Maps, OSM)

**Tipos de geometrías:**
- Point: Un punto
- LineString: Una línea
- Polygon: Un polígono
- MultiPolygon: Varios polígonos

**GeoJSON (formato):**
```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [-74.2973, 4.5709]
  },
  "properties": {
    "nombre": "Bogotá"
  }
}
```

**Conceptos básicos:**
- Bounding Box (bbox): Rectángulo que contiene geometrías
- Zoom level: Nivel de detalle (mayor número = más detalle)
- Tiles: División del mapa en cuadrados de 256x256 px

**Recursos de repaso:**
- GeoJSON spec: https://geojson.org/
- Leaflet documentation: https://leafletjs.com/

---

## 2.5 Configuración del Editor (VS Code)

### Extensiones recomendadas

Si usas Visual Studio Code, instala:

| Extensión | Propósito |
|-----------|-----------|
| **Python** (Microsoft) | Soporte para Python |
| **Live Server** | Servidor local para HTML |
| **ESLint** | Linting para JavaScript |
| **Prettier** | Formateo de código |
| **Thunder Client** | Cliente REST integrado |

### Configuración recomendada

Crear archivo `.vscode/settings.json` en el proyecto:

```json
{
  "editor.formatOnSave": true,
  "editor.tabSize": 4,
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "[javascript]": {
    "editor.tabSize": 4
  },
  "[html]": {
    "editor.tabSize": 4
  }
}
```

---

## 2.6 Pruebas Iniciales

### Prueba 1: Iniciar Flask

```bash
cd webapp
python app.py
```

**Salida esperada:**
```
=================================================
Iniciando aplicación de visualización del Amazonas
Conectando a base de datos: postgis:5432/geodatos
=================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

**Verificar en navegador:**
```
http://localhost:5000/map-dpto
```

**Resultado esperado:**
- Página HTML cargada
- Sin errores en consola del navegador (F12)

### Prueba 2: Verificar proxy

Con Flask ejecutándose, en otra terminal:

```bash
curl "http://localhost:5000/api/geoserver-proxy?service=WFS&version=2.0.0&request=GetFeature&typeName=ne:departamentos&maxFeatures=1&outputFormat=application/json"
```

**Resultado esperado:**
- GeoJSON válido

### Prueba 3: Verificar carga de recursos estáticos

En el navegador, abre:
```
http://localhost:5000/map-dpto
```

**Abrir DevTools (F12) → Network:**
- Verificar que se cargan:
  - `app.css` (200 OK)
  - `app.js` (200 OK)
  - Leaflet CSS y JS desde CDN (200 OK)

**Abrir DevTools (F12) → Console:**
- No debe haber errores de JavaScript
- Deben aparecer mensajes de log de app.js:
  ```
  🗺️ Aplicación de Servicios Web Geográficos
  Configuración:
  - GeoServer WMS: http://localhost:8080/geoserver/ne/wms
  ...
  ```

---

## 2.7 Resolución de Problemas en Verificación

### Problema: "python: command not found"

**Causa:** Python no está en el PATH

**Solución:**
- Windows: Reinstalar Python marcando "Add to PATH"
- Linux/Mac: Usar `python3` en lugar de `python`

### Problema: "docker: command not found"

**Causa:** Docker no está instalado o no está en el PATH

**Solución:**
- Verificar instalación de Docker Desktop
- Reiniciar terminal después de instalar

### Problema: GeoServer no responde

**Causa:** Contenedor no está ejecutándose

**Solución:**
```bash
docker-compose up -d geoserver
```

### Problema: "Connection refused" al conectar a GeoServer

**Causa:** GeoServer aún está iniciando

**Solución:**
- Esperar 1-2 minutos
- Verificar logs: `docker logs geoserver`

### Problema: Capas no aparecen en GeoServer

**Causa:** Datos no importados

**Solución:**
- Verificar que exista `data/shapefiles/choco.gpkg`
- Ejecutar scripts de importación:
  ```bash
  docker exec -it postgis bash /docker-entrypoint-initdb.d/02-import-geopackage.sh
  ```
- Configurar capas manualmente en GeoServer web interface

### Problema: "ModuleNotFoundError: No module named 'flask'"

**Causa:** Dependencias no instaladas

**Solución:**
```bash
pip install Flask psycopg2-binary requests flask-cors
```

### Problema: Errores CORS en navegador

**Causa:** Flask no tiene flask-cors instalado

**Solución:**
```bash
pip install flask-cors
```

Verificar en `app.py`:
```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # ← Debe estar presente
```

---

## 2.8 Checklist de Verificación

Antes de continuar al Módulo 3, verifica que cumples con:

### Software y servicios

- [ ] Python 3.8+ instalado y funcionando
- [ ] Docker y Docker Compose instalados
- [ ] Contenedores de GeoServer y PostGIS ejecutándose
- [ ] GeoServer accesible en http://localhost:8080/geoserver/web/
- [ ] Workspace `ne` existe en GeoServer
- [ ] Capas `ne:dpto_choco`, `ne:mpios_choco`, `ne:departamentos` existen

### Dependencias Python

- [ ] Flask instalado
- [ ] psycopg2-binary instalado
- [ ] requests instalado
- [ ] flask-cors instalado

### Verificaciones funcionales

- [ ] Flask inicia sin errores: `python app.py`
- [ ] Página principal carga: http://localhost:5000/map-dpto
- [ ] Proxy funciona: http://localhost:5000/api/geoserver-proxy?service=WFS&...
- [ ] No hay errores en consola del navegador
- [ ] DevTools → Network muestra recursos cargados correctamente

### Conocimientos

- [ ] Comprendo HTML básico
- [ ] Comprendo CSS y Flexbox básico
- [ ] Comprendo JavaScript ES6 (promesas, fetch, arrow functions)
- [ ] Comprendo conceptos SIG básicos (coordenadas, CRS, GeoJSON)

---

## 2.9 Resumen

En este módulo has verificado que:

- Todo el software necesario está instalado y funcionando
- Los servicios (GeoServer, PostgreSQL) están accesibles
- Las dependencias Python están instaladas
- El entorno de desarrollo está configurado
- Tienes los conocimientos previos necesarios
- Las pruebas básicas de conectividad funcionan

### Próximo módulo

Ahora estás listo para comenzar el análisis detallado del código.

En el **Módulo 3 (Estructura HTML)**, examinaremos línea por línea el archivo `index.html` y comprenderemos la estructura de la aplicación web.

---

**[⬅️ Módulo 1: Introducción](01_INTRODUCCION.md)** | **[Volver al Índice](README.md)** | **[Siguiente: Módulo 3 - Estructura HTML ➡️](03_ESTRUCTURA_HTML.md)**
