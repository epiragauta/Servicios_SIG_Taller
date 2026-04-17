# Módulo 5: JavaScript Parte 1 - Creación de app.js (WMS y Capas Base)

## Objetivos de Aprendizaje

Al completar este módulo, habrás:

- Creado el archivo `app.js` desde cero
- Inicializado un mapa de Leaflet
- Agregado capas base (OSM, Esri, CartoDB)
- Cargado servicios WMS desde GeoServer
- Implementado control de capas
- Agregado control de escala

---

## 5.1 Preparación

### Crear el archivo JavaScript

Crea el archivo en la ubicación correcta:

**Ubicación:** `webapp/static/js/app.js`

```bash
# Si no existe el directorio
mkdir -p webapp/static/js

# Crear archivo vacío (Linux/Mac)
touch webapp/static/js/app.js

# Windows PowerShell
New-Item -Path webapp/static/js/app.js -ItemType File
```

Abre `app.js` en tu editor de código.

---

## 5.2 Paso 1: Configuración Global

Comienza con los comentarios de cabecera y las constantes de configuración:

```javascript
/**
 * Aplicación de Visualización de Departamentos y Municipios de Colombia
 * Curso de Servicios Web Geográficos
 */

// ============================================
// Configuración Global
// ============================================

// URL de GeoServer (a través del proxy de Flask para evitar CORS)
const GEOSERVER_URL = 'http://localhost:8080/geoserver/ne/wms';
const WFS_URL = '/api/geoserver-proxy?service=wfs';

// Configuración del mapa
const MAP_CONFIG = {
    center: [4.5709, -74.2973], // Centro de Colombia
    zoom: 6,
    minZoom: 5,
    maxZoom: 18
};
```

**Explicación:**

**`const GEOSERVER_URL`**
- URL del servicio WMS de GeoServer
- Formato: `http://localhost:8080/geoserver/{workspace}/wms`
- `ne` es el workspace que contiene nuestras capas

**`const WFS_URL`**
- Endpoint del proxy en Flask
- Ruta relativa (mismo origen, evita CORS)
- Lo usaremos en Módulo 6 para cargar WFS

**`MAP_CONFIG`**
- `center`: Coordenadas iniciales `[latitud, longitud]`
- `[4.5709, -74.2973]` = Centro de Colombia (Bogotá)
- `zoom: 6`: Nivel de zoom inicial (vista de país)
- `minZoom` y `maxZoom`: Limitan el rango de zoom

**Convención de nombres:**
- `MAYÚSCULAS`: Constantes que no cambiarán
- `camelCase`: Variables y funciones

---

## 5.3 Paso 2: Inicialización del Mapa

Agrega el código para crear el mapa de Leaflet:

```javascript
// ============================================
// Inicialización del Mapa
// ============================================

// Crear el mapa
const map = L.map('map', {
    center: MAP_CONFIG.center,
    zoom: MAP_CONFIG.zoom,
    minZoom: MAP_CONFIG.minZoom,
    maxZoom: MAP_CONFIG.maxZoom,
    zoomControl: true
});
```

**Explicación:**

**`L.map('map', options)`**
- `L` es el objeto global de Leaflet
- `'map'`: ID del div HTML donde se renderizará (`<div id="map"></div>`)
- **IMPORTANTE:** El div debe existir en index.html

**Opciones:**
- `center`: Centro inicial del mapa
- `zoom`: Nivel de zoom inicial
- `minZoom` / `maxZoom`: Restricciones de zoom
- `zoomControl: true`: Mostrar botones +/- de zoom

**Variable `map`:**
- Se declara con `const` pero es global (fuera de funciones)
- Se usará en todo el código para interactuar con el mapa
- Permite: agregar capas, controlar vista, agregar controles

---

## 5.4 Paso 3: Capas Base (Tile Layers)

Agrega las capas base que el usuario podrá seleccionar:

```javascript
// ============================================
// Capas Base
// ============================================

const baseLayers = {
    'Mapa base (OSM)': L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }),

    'Satélite (Esri)': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri',
        maxZoom: 18
    }),

    'Calles (CartoDB)': L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19
    })
};

// Agregar capa base por defecto
baseLayers['Mapa base (OSM)'].addTo(map);
```

**Explicación:**

**`L.tileLayer(urlTemplate, options)`**
- Crea una capa de tiles (cuadrados de 256x256 px)
- Los tiles se cargan dinámicamente según el área visible

**URL Template:**
```javascript
'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
```
- `{s}`: Subdomain (a, b, c) - Balanceo de carga
- `{z}`: Zoom level
- `{x}`, `{y}`: Coordenadas del tile

**Ejemplo de URL generada:**
```
https://a.tile.openstreetmap.org/6/32/25.png
         │                         │ │  │
         └─ subdomain              │ │  └─ y
                                   │ └──── x
                                   └────── z
```

**`attribution`**
- Texto de créditos/copyright
- Aparece en esquina inferior derecha
- **Obligatorio** para la mayoría de proveedores

**Tres capas base:**
1. **OSM (OpenStreetMap):** Mapa de calles estilo clásico
2. **Esri:** Imágenes satelitales
3. **CartoDB:** Mapa de calles estilo minimalista

**Agregar capa por defecto:**
```javascript
baseLayers['Mapa base (OSM)'].addTo(map);
```
- Selecciona OSM como capa inicial
- Sin esto, el mapa estaría vacío al cargar

---

## 5.5 Paso 4: Primera Capa WMS (Departamentos)

Agrega la primera capa WMS de GeoServer:

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
```

**Explicación:**

**`L.tileLayer.wms(baseUrl, wmsOptions)`**
- Similar a `L.tileLayer()` pero para servicios WMS
- Genera peticiones WMS GetMap automáticamente

**Diferencias con tile layers normales:**

| `L.tileLayer()` | `L.tileLayer.wms()` |
|-----------------|---------------------|
| URL template fija | URL base + parámetros WMS |
| Tiles precalculados | Tiles generados dinámicamente |
| Ejemplo: OSM, Esri | Ejemplo: GeoServer, MapServer |

**Parámetros WMS:**

**`layers: 'ne:dpto_choco'`**
- Formato: `workspace:layer_name`
- `ne`: Workspace en GeoServer
- `dpto_choco`: Nombre de la capa

**`format: 'image/png'`**
- Formato de la imagen retornada
- PNG soporta transparencia (necesario para superponer capas)
- Alternativa: `'image/jpeg'` (más pequeño, sin transparencia)

**`transparent: true`**
- `true`: Fondo transparente (deja ver la capa base)
- `false`: Fondo opaco (típicamente blanco)

**`styles: ''`**
- `''` (vacío): Usa estilo por defecto de GeoServer
- Puedes especificar un estilo personalizado si existe en GeoServer

**URL generada internamente por Leaflet:**
```
http://localhost:8080/geoserver/ne/wms?
    service=WMS&
    version=1.1.1&
    request=GetMap&
    layers=ne:dpto_choco&
    styles=&
    format=image/png&
    transparent=true&
    width=256&
    height=256&
    srs=EPSG:3857&
    bbox=-8575595.864,556597.454,-8566051.864,566141.454
```

**NOTA:** Esta capa NO se agrega automáticamente al mapa. El usuario la activará desde el control de capas.

---

## 5.6 Paso 5: Segunda Capa WMS (Municipios)

Agrega la segunda capa WMS:

```javascript
const municipiosWMS = L.tileLayer.wms(GEOSERVER_URL, {
    layers: 'ne:mpios_choco',
    format: 'image/png',
    transparent: true,
    attribution: 'IGAC',
    styles: ''
});
```

**Explicación:**

**Diferencias con la capa de departamentos:**
- Capa: `mpios_choco` (municipios en lugar de departamentos)
- Attribution más corto: `'IGAC'`
- Todo lo demás es idéntico

**¿Por qué no agregarla al mapa?**
- Evitar sobrecarga visual (demasiadas capas al inicio)
- Usuario decide qué capas activar
- Se agregará a través del control de capas

---

## 5.7 Paso 6: Control de Capas

Agrega el control que permite al usuario seleccionar capas:

```javascript
// ============================================
// Control de Capas
// ============================================

const overlayLayers = {
    'Departamentos (WMS)': departamentosWMS,
    'Municipios (WMS)': municipiosWMS
};

const layerControl = L.control.layers(baseLayers, overlayLayers, {
    position: 'topright',
    collapsed: false
}).addTo(map);
```

**Explicación:**

**`overlayLayers`**
- Capas que se superponen sobre la capa base
- Varias pueden estar activas simultáneamente
- Se muestran como checkboxes en el control

**`L.control.layers(baseLayers, overlayLayers, options)`**
- Crea el control de capas
- `baseLayers`: Capas mutuamente excluyentes (radio buttons)
- `overlayLayers`: Capas que se pueden combinar (checkboxes)

**Opciones:**
- `position: 'topright'`: Esquina superior derecha
  - Otras opciones: `'topleft'`, `'bottomleft'`, `'bottomright'`
- `collapsed: false`: Mostrar expandido por defecto
  - `true`: Mostrar colapsado (solo icono)

**Resultado visual:**
```
┌──────────────────────────┐
│ ○ Mapa base (OSM)       │  ← Radio buttons (solo uno activo)
│ ○ Satélite (Esri)       │
│ ○ Calles (CartoDB)      │
├──────────────────────────┤
│ ☐ Departamentos (WMS)    │  ← Checkboxes (múltiples activos)
│ ☐ Municipios (WMS)       │
└──────────────────────────┘
```

**`.addTo(map)`**
- Agrega el control al mapa
- Variable `layerControl` guardada para uso posterior

---

## 5.8 Paso 7: Control de Escala

Finalmente, agrega un control de escala al mapa:

```javascript
// ============================================
// Control de Escala
// ============================================

L.control.scale({
    position: 'bottomleft',
    imperial: false,
    metric: true
}).addTo(map);
```

**Explicación:**

**`L.control.scale(options)`**
- Muestra escala gráfica del mapa
- Actualiza automáticamente al hacer zoom

**Opciones:**
- `position: 'bottomleft'`: Esquina inferior izquierda
- `imperial: false`: No mostrar escala en millas
- `metric: true`: Mostrar escala en metros/kilómetros

**Resultado visual:**
```
┌─────────────┐
│ 0  50  100km│  ← Escala gráfica
└─────────────┘
```

La escala se ajusta automáticamente:
- Zoom 6: "0 --- 50 --- 100 km"
- Zoom 10: "0 --- 5 --- 10 km"
- Zoom 14: "0 --- 500 --- 1000 m"

---

## 5.9 Checkpoint: Probar el Mapa

### Paso 1: Guardar el archivo

Asegúrate de que `webapp/static/js/app.js` está guardado.

### Paso 2: Reiniciar el contenedor webapp

```bash
docker-compose restart webapp
```

### Paso 3: Abrir en navegador

Visita: http://localhost:5000/map-dpto

### Paso 4: Verificar en navegador

**Resultado esperado:**

**Mapa visible:**
- Mapa de OpenStreetMap centrado en Colombia
- Controles de zoom (+/-) en esquina superior izquierda
- Escala en esquina inferior izquierda

**Control de capas (superior derecha):**
- 3 capas base (OSM seleccionado por defecto)
- 2 capas overlay (Departamentos y Municipios sin activar)

**Interactividad básica:**
- Puedes hacer zoom in/out
- Puedes arrastrar el mapa
- Puedes cambiar capa base (OSM, Satélite, CartoDB)

**Activar capas WMS:**
- Marca checkbox "Departamentos (WMS)"
  - **Si GeoServer está corriendo:** Aparecen polígonos de departamentos
  - **Si GeoServer NO está corriendo:** No aparece nada (esto es normal)
- Marca checkbox "Municipios (WMS)"
  - Similar a departamentos

### Paso 5: Abrir consola del navegador (F12)

**Errores esperados:**
- ❌ Error 404 para fetch WFS: **Normal**, aún no hemos implementado `loadDepartamentosWFS()` (Módulo 6)

**NO debe haber:**
- ❌ "L is not defined" → Leaflet no cargó
- ❌ "Map container not found" → Div #map no existe en HTML

**Si algo falla:**
- Verificar que index.html tiene `<div id="map"></div>`
- Verificar que index.html carga Leaflet.js antes de app.js
- Verificar que app.css define dimensiones del mapa (width: 100%, height: 100%)

---

## 5.10 Verificación: Archivo Completo hasta Ahora

Tu archivo `app.js` debe verse así (aproximadamente 70 líneas):

```javascript
/**
 * Aplicación de Visualización de Departamentos y Municipios de Colombia
 * Curso de Servicios Web Geográficos
 */

// ============================================
// Configuración Global
// ============================================

// URL de GeoServer (a través del proxy de Flask para evitar CORS)
const GEOSERVER_URL = 'http://localhost:8080/geoserver/ne/wms';
const WFS_URL = '/api/geoserver-proxy?service=wfs';

// Configuración del mapa
const MAP_CONFIG = {
    center: [4.5709, -74.2973], // Centro de Colombia
    zoom: 6,
    minZoom: 5,
    maxZoom: 18
};

// ============================================
// Inicialización del Mapa
// ============================================

// Crear el mapa
const map = L.map('map', {
    center: MAP_CONFIG.center,
    zoom: MAP_CONFIG.zoom,
    minZoom: MAP_CONFIG.minZoom,
    maxZoom: MAP_CONFIG.maxZoom,
    zoomControl: true
});

// ============================================
// Capas Base
// ============================================

const baseLayers = {
    'Mapa base (OSM)': L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }),

    'Satélite (Esri)': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri',
        maxZoom: 18
    }),

    'Calles (CartoDB)': L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19
    })
};

// Agregar capa base por defecto
baseLayers['Mapa base (OSM)'].addTo(map);

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

// ============================================
// Control de Capas
// ============================================

const overlayLayers = {
    'Departamentos (WMS)': departamentosWMS,
    'Municipios (WMS)': municipiosWMS
};

const layerControl = L.control.layers(baseLayers, overlayLayers, {
    position: 'topright',
    collapsed: false
}).addTo(map);

// ============================================
// Control de Escala
// ============================================

L.control.scale({
    position: 'bottomleft',
    imperial: false,
    metric: true
}).addTo(map);
```

---

## 5.11 Flujo de Carga de una Capa WMS

Entender cómo funciona internamente:

**1. Usuario activa checkbox "Departamentos (WMS)"**

**2. Leaflet agrega la capa al mapa:**
```javascript
departamentosWMS.addTo(map);
```

**3. Leaflet detecta qué tiles son visibles:**
- Calcula qué porción del mundo está en viewport
- Divide en tiles de 256x256px

**4. Para cada tile, Leaflet hace petición HTTP GET a GeoServer:**
```
GET http://localhost:8080/geoserver/ne/wms?
    service=WMS&
    request=GetMap&
    layers=ne:dpto_choco&
    bbox=-8575595.864,556597.454,-8566051.864,566141.454&
    width=256&
    height=256&
    srs=EPSG:3857&
    format=image/png&
    transparent=true
```

**5. GeoServer procesa:**
- Consulta la capa `ne:dpto_choco` en su datastore
- Filtra features dentro del bbox
- Reproyecta a EPSG:3857 (Web Mercator)
- Renderiza a imagen PNG 256x256
- Retorna imagen

**6. Navegador recibe PNG y lo posiciona en el mapa**

**7. Usuario hace zoom o mueve mapa:**
- Leaflet calcula nuevos tiles necesarios
- Repite proceso (pasos 4-6)

---

## 5.12 Ventajas de WMS vs WFS

### ¿Por qué usar WMS para estas capas?

**Rendimiento:**
- Solo transfiere imágenes (~10-50 KB por tile)
- No importa si la capa tiene 10 polígonos o 10,000

**Sin CORS:**
- Imágenes no tienen restricciones de origen
- Petición directa a GeoServer (sin proxy)

**Escalabilidad:**
- Funciona igual con datasets grandes

**Caché:**
- GeoServer puede cachear tiles generados

### Limitaciones de WMS

❌ **No interactivo:**
```javascript
// Esto NO funciona con WMS:
departamentosWMS.on('click', function() {
    alert('Click!');  // No se ejecutará
});
```

❌ **Sin atributos:**
- No acceso a propiedades de features
- Solo visualización

❌ **No editable:**
- Read-only

**Solución:** Usar WFS (veremos en Módulo 6)

---

## 5.13 Resumen

Has aprendido:

- Crear archivo JavaScript desde cero
- Configurar constantes globales
- Inicializar mapa de Leaflet con `L.map()`
- Agregar capas base con `L.tileLayer()`
- Cargar capas WMS con `L.tileLayer.wms()`
- Implementar control de capas con `L.control.layers()`
- Agregar control de escala
- Diferencias entre WMS y tile layers normales

### Archivos creados

- `webapp/static/js/app.js` (~100 líneas)

### Conceptos clave

| Concepto | Descripción |
|----------|-------------|
| **Tile Layer** | Mapa dividido en cuadrados de 256x256px |
| **WMS** | Estándar OGC para servir mapas como imágenes |
| **L.map()** | Constructor de mapas de Leaflet |
| **L.tileLayer.wms()** | Capa WMS de Leaflet |
| **Control de capas** | Permite al usuario activar/desactivar capas |
| **Base layers** | Capas mutuamente excluyentes (radio buttons) |
| **Overlay layers** | Capas que se pueden combinar (checkboxes) |

### Próximo módulo

En el **Módulo 6 (JavaScript Parte 2)**, continuarás creando app.js agregando:
- Carga de datos WFS a través del proxy
- Conversión de GeoJSON a capas Leaflet interactivas
- Interactividad (click, hover, zoom a features)
- Estilos dinámicos
- Control de información personalizado
- Búsqueda de departamentos

---

**[⬅️ Módulo 4: Estilos CSS](04_ESTILOS_CSS.md)** | **[Volver al Índice](README.md)** | **[Siguiente: Módulo 6 - JavaScript Parte 2 ➡️](06_JAVASCRIPT_PARTE_2.md)**
