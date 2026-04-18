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

### 2.2.1 Verificar Docker y Docker Compose

**Este proyecto requiere Docker y Docker Compose instalados.**

Abre una terminal y ejecuta:

```bash
docker --version
```

**Salida esperada:**
```
Docker version 20.10.12, build e91ed57 (o superior)
```

**Verificar Docker Compose:**
```bash
docker-compose --version
```

**Salida esperada:**
```
docker-compose version 1.29.2, build 5becea4c (o superior)
```

### 2.2.2 Iniciar el proyecto con Docker Compose

**Navegar al directorio del proyecto (Directorio de trabajo en donde descargó e repositorio):**
```bash
cd C:\ws\ujdc\Servicios_SIG_Taller
NOTA: Este es un directorio de ejemplo
```

**Construir y levantar todos los servicios:**
```bash
docker-compose up -d
```

**Salida esperada:**
```
Creating network "servicios_sig_taller_default" with the default driver
Creating volume "servicios_sig_taller_postgres_data" with local driver
Creating volume "servicios_sig_taller_geoserver_data" with local driver
Creating postgis ... done
Creating geoserver ... done
Creating webapp ... done
```

**Verificar que los contenedores están ejecutándose:**
```bash
docker-compose ps
```

**Salida esperada:**
```
NAME         COMMAND                  SERVICE      STATUS       PORTS
geoserver    "/bin/sh /opt/startup…"  geoserver    Up           0.0.0.0:8080->8080/tcp
postgis      "docker-entrypoint.s…"   postgis      Up (healthy) 0.0.0.0:5432->5432/tcp
webapp       "python app.py"          webapp       Up (healthy) 0.0.0.0:5000->5000/tcp
```

> **IMPORTANTE:** Los tres servicios deben estar en estado "Up" o "Up (healthy)".

**Ver logs de un servicio específico:**
```bash
# Ver logs de webapp
docker-compose logs -f webapp

# Ver logs de geoserver
docker-compose logs -f geoserver

# Ver logs de todos los servicios
docker-compose logs -f
```

### 2.2.3 Verificar GeoServer (Contenedor)

**GeoServer se ejecuta en el contenedor `geoserver` y está accesible en el puerto 8080.**

#### Método 1: Navegador

Abre tu navegador y visita:
```
http://localhost:8080/geoserver/web/
```

**Resultado esperado:**
- Página de login de GeoServer
- Credenciales: `admin` / `geoserver`

#### Método 2: Línea de comandos

```bash
curl http://localhost:8080/geoserver/web/
```

**Resultado esperado:**
- HTML de la página de GeoServer (sin error 404 o connection refused)

#### Método 3: Verificar desde el contenedor

```bash
# Verificar estado del contenedor
docker-compose ps geoserver

# Ver logs del contenedor
docker-compose logs geoserver

# Ejecutar comando dentro del contenedor
docker exec geoserver curl -s http://localhost:8080/geoserver/web/ | grep -i "geoserver"
```

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

### 2.2.4 Verificar PostgreSQL/PostGIS (Contenedor)

**PostgreSQL/PostGIS se ejecuta en el contenedor `postgis`.**

**Verificar versión de PostgreSQL:**
```bash
docker exec postgis psql -U postgres -d geodatos -c "SELECT version();"
```

**Resultado esperado:**
```
PostgreSQL 14.x on ...
```

**Verificar extensión PostGIS:**
```bash
docker exec postgis psql -U postgres -d geodatos -c "SELECT PostGIS_Version();"
```

**Resultado esperado:**
```
3.1 USE_GEOS=1 USE_PROJ=1 ...
```

**Verificar tablas importadas:**
```bash
docker exec postgis psql -U postgres -d geodatos -c "\dt"
```

**Credenciales de la base de datos (definidas en docker-compose.yml):**
- **Host:** postgis (dentro de Docker) / localhost (desde host)
- **Puerto:** 5432
- **Base de datos:** geodatos
- **Usuario:** postgres
- **Contraseña:** postgres

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

## 2.3 Arquitectura Docker del Proyecto

Este proyecto está completamente **dockerizado** usando Docker Compose. Todos los servicios se ejecutan en contenedores.

### Servicios del proyecto

El archivo `docker-compose.yml` define 3 servicios:

| Servicio | Imagen/Dockerfile | Puerto | Propósito |
|----------|-------------------|--------|-----------|
| **postgis** | Dockerfile.postgis | 5432 | Base de datos PostgreSQL/PostGIS |
| **geoserver** | docker.osgeo.org/geoserver:2.24.0 | 8080 | Servidor de mapas OGC |
| **webapp** | Dockerfile.webapp | 5000 | Aplicación Flask (proxy) |

### Dependencias Python en Docker

Las dependencias de Python están definidas en `webapp/requirements.txt`:

```
Flask==3.0.0
folium==0.15.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
Werkzeug==3.0.1
branca==0.7.0
flask-cors
requests>=2.28.0
```

**IMPORTANTE:** Las dependencias se instalan **automáticamente** al construir el contenedor Docker.

### Cómo actualizar dependencias

**Si necesitas agregar o actualizar dependencias:**

1. **Editar `webapp/requirements.txt`:**
```bash
# Ejemplo: Agregar nueva librería
echo "numpy==1.24.0" >> webapp/requirements.txt
```

2. **Reconstruir el contenedor webapp:**
```bash
docker-compose build webapp
```

3. **Reiniciar el servicio:**
```bash
docker-compose up -d webapp
```

**Verificar dependencias instaladas en el contenedor:**
```bash
docker exec webapp pip list
```

### Iniciar todos los servicios

```bash
# Construir y levantar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f webapp

# Detener servicios
docker-compose down
```

> **NOTA:** No es necesario instalar Python ni las dependencias localmente. Todo se ejecuta dentro de contenedores Docker.

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

## 2.6 Pruebas Iniciales con Docker

### Prueba 1: Verificar que la aplicación Flask está ejecutándose

**La aplicación Flask se ejecuta automáticamente en el contenedor `webapp`.**

**Ver logs de Flask:**
```bash
docker-compose logs webapp
```

**Salida esperada:**
```
webapp  | =================================================
webapp  | Iniciando aplicación de visualización del Amazonas
webapp  | Conectando a base de datos: postgis:5432/geodatos
webapp  | =================================================
webapp  |  * Serving Flask app 'app'
webapp  |  * Debug mode: on
webapp  |  * Running on http://0.0.0.0:5000
```

**Verificar en navegador:**
```
http://localhost:5000/
```

**Resultado esperado:**
- Página HTML cargada
- Sin errores en consola del navegador (F12)

**Si necesitas reiniciar el servicio webapp:**
```bash
docker-compose restart webapp
```

### Prueba 2: Verificar proxy

Con Flask ejecutándose, en otra terminal:

```bash
curl "http://localhost:5000/api/geoserver-proxy?service=WFS&version=2.0.0&request=GetFeature&typeName=ne:departamentos&maxFeatures=1&outputFormat=application/json"
```

**Resultado esperado:**
- GeoJSON válido

---

## 2.7 Resolución de Problemas en Verificación

### Problema: "docker: command not found"

**Causa:** Docker no está instalado o no está en el PATH

**Solución:**
- Verificar instalación de Docker Desktop
- Reiniciar terminal después de instalar
- En Windows: Asegurar que Docker Desktop está ejecutándose

### Problema: "dcker-compose: command not found"

**Causa:** Docker Compose no está instalado

**Solución:**
- Docker Desktop incluye Docker Compose
- En Linux: `sudo apt-get install docker-compose`
- Verificar versión: `docker-compose --version`

### Problema: Contenedor no inicia o se reinicia constantemente

**Causa:** Problemas con el build o configuración

**Solución:**
```bash
# Ver logs del contenedor problemático
docker-compose logs webapp

# Reconstruir el contenedor
docker-compose build webapp

# Reiniciar servicios
docker-compose down
docker-compose up -d
```

### Problema: Puerto ya está en uso (8080, 5000, 5432)

**Causa:** Otro servicio está usando el puerto

**Solución:**
```bash
# Verificar qué está usando el puerto (Windows)
netstat -ano | findstr :8080

# Verificar qué está usando el puerto (Linux/Mac)
lsof -i :8080

# Detener el servicio conflictivo o cambiar puerto en docker-compose.yml
```

### Problema: GeoServer no responde

**Causa:** Contenedor no está ejecutándose o aún está iniciando

**Solución:**
```bash
# Verificar estado del contenedor
docker-compose ps geoserver

# Ver logs
docker-compose logs -f geoserver

# Reiniciar el servicio
docker-compose restart geoserver
```

### Problema: "Connection refused" al conectar a GeoServer

**Causa:** GeoServer aún está iniciando (puede tardar 1-3 minutos)

**Solución:**
```bash
# Esperar y ver logs
docker-compose logs -f geoserver

# Buscar mensaje: "INFO: Started SelectChannelConnector@0.0.0.0:8080"
# Esto indica que GeoServer está listo
```

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

**Causa:** El contenedor no se construyó correctamente o requirements.txt tiene errores

**Solución:**
```bash
# Reconstruir el contenedor webapp
docker-compose build --no-cache webapp

# Reiniciar el servicio
docker-compose up -d webapp

# Verificar que las dependencias están instaladas
docker exec webapp pip list
```

### Problema: Cambios en código Python no se reflejan

**Causa:** El código está montado como volumen, pero el contenedor no se recarga automáticamente

**Solución:**
```bash
# Opción 1: Reiniciar el contenedor
docker-compose restart webapp

# Opción 2: Ver logs en tiempo real (auto-reload en modo desarrollo)
docker-compose logs -f webapp
```

### Problema: Necesitas agregar nueva dependencia Python

**Solución:**
1. Editar `webapp/requirements.txt`:
```bash
echo "nueva-libreria==1.0.0" >> webapp/requirements.txt
```

2. Reconstruir el contenedor:
```bash
docker-compose build webapp
docker-compose up -d webapp
```

---

## 2.8 Checklist de Verificación

Antes de continuar al Módulo 3, verifica que cumples con:

### Docker y servicios

- [ ] Docker Desktop instalado y ejecutándose
- [ ] Docker Compose instalado (v1.29+)
- [ ] Proyecto clonado en directorio local
- [ ] Comando `docker-compose up -d` ejecutado sin errores
- [ ] Los 3 contenedores están "Up": postgis, geoserver, webapp

### Servicios accesibles

- [ ] GeoServer accesible en http://localhost:8080/geoserver/web/
- [ ] Credenciales de GeoServer funcionan: admin/geoserver
- [ ] Workspace `ne` existe en GeoServer
- [ ] Capas `ne:dpto_choco`, `ne:mpios_choco`, `ne:departamentos` existen
- [ ] PostgreSQL/PostGIS responde: `docker exec postgis psql -U postgres -d geodatos -c "SELECT 1;"`

### Aplicación Flask (webapp)

- [ ] Contenedor webapp en estado "Up (healthy)"
- [ ] Logs de webapp sin errores: `docker-compose logs webapp`
- [ ] Página principal carga: http://localhost:5000
- [ ] Proxy funciona: http://localhost:5000/api/geoserver-proxy?service=WFS&version=2.0.0&request=GetCapabilities
- [ ] No hay errores en consola del navegador (F12)
- [ ] DevTools → Network muestra recursos cargados correctamente

### Verificaciones de red Docker

- [ ] Contenedores pueden comunicarse entre sí
- [ ] webapp puede acceder a postgis (puerto 5432)
- [ ] webapp puede acceder a geoserver (puerto 8080)

**Comando útil para verificar todo:**
```bash
# Ver estado de todos los servicios
docker-compose ps

# Ver logs de todos los servicios
docker-compose logs --tail=50

# Verificar conectividad entre contenedores
docker exec webapp curl -s http://geoserver:8080/geoserver/web/ | grep -i "geoserver"
```

### Conocimientos

- [ ] Comprendo HTML básico
- [ ] Comprendo CSS y Flexbox básico
- [ ] Comprendo JavaScript ES6 (promesas, fetch, arrow functions)
- [ ] Comprendo conceptos SIG básicos (coordenadas, CRS, GeoJSON)

---

## 2.9 Resumen

En este módulo has aprendido que:

### Arquitectura Docker
- El proyecto está **completamente dockerizado** con Docker Compose
- **3 servicios:** postgis (base de datos), geoserver (servidor OGC), webapp (Flask)
- Las dependencias se gestionan a través de `requirements.txt` y Dockerfile
- Para actualizar dependencias: editar `requirements.txt` y reconstruir con `docker-compose build webapp`

### Verificaciones completadas
- Docker y Docker Compose instalados y funcionando
- Todos los servicios levantados con `docker-compose up -d`
- GeoServer accesible en puerto 8080
- PostgreSQL/PostGIS accesible en puerto 5432
- Aplicación Flask accesible en puerto 5000
- Los contenedores pueden comunicarse entre sí

### Comandos clave aprendidos
```bash
docker-compose up -d              # Levantar servicios
docker-compose ps                 # Ver estado
docker-compose logs -f webapp     # Ver logs
docker-compose build webapp       # Reconstruir contenedor
docker-compose restart webapp     # Reiniciar servicio
docker-compose down               # Detener todo
docker exec webapp pip list       # Ver dependencias instaladas
```

### Próximo módulo

Ahora estás listo para comenzar el análisis detallado del código.

En el **Módulo 3 (Estructura HTML)**, examinaremos línea por línea el archivo `index.html` y comprenderemos la estructura de la aplicación web.

---

**[⬅️ Módulo 1: Introducción](01_INTRODUCCION.md)** | **[Volver al Índice](README.md)** | **[Siguiente: Módulo 3 - Estructura HTML ➡️](03_ESTRUCTURA_HTML.md)**
