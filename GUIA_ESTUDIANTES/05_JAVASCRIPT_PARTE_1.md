# Módulo 5: JavaScript Parte 1 - WMS y Capas Base

## Objetivos de Aprendizaje

Al completar este módulo, comprenderás:

- 🎯 La estructura y configuración global de app.js
- 🗺️ Cómo inicializar un mapa con Leaflet
- 🌍 Cómo agregar capas base (tile layers)
- 📡 Cómo cargar servicios WMS desde GeoServer
- 🎛️ Cómo implementar control de capas

---

## 5.1 Visión General del Archivo app.js

**Ubicación:** `webapp/static/js/app.js` (372 líneas)

### Estructura general:

```javascript
// 1. Configuración Global (líneas 1-20)
const GEOSERVER_URL = ...
const MAP_CONFIG = ...

// 2. Inicialización del Mapa (líneas 22-33)
const map = L.map('map', {...});

// 3. Capas Base (líneas 36-58)
const baseLayers = {...};

// 4. Capas WMS de GeoServer (líneas 60-81)
const departamentosWMS = ...
const municipiosWMS = ...

// 5. Capa WFS (líneas 84-120)
function loadDepartamentosWFS() {...}

// 6. Estilos e Interactividad (líneas 122-196)

// 7. Control de Capas (líneas 199-211)

// 8. Controles Personalizados (líneas 213-249)

// 9. Búsqueda (líneas 252-337)

// 10. Inicialización (líneas 340-372)
```

---

## 5.2 Configuración Global (Líneas 1-20)

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

### Constantes con `const`

```javascript
const GEOSERVER_URL = 'http://localhost:8080/geoserver/ne/wms';
```

**¿Por qué `const`?**
- No se puede reasignar
- Convención: NOMBRES_EN_MAYÚSCULAS para constantes globales
- Facilita identificar valores de configuración

**Convención vs let/var:**
```javascript
const API_URL = 'http://...';  ✅ Configuración
let contador = 0;              ✅ Variable que cambia
var antiguo = 1;               ❌ No usar var (ES5)
```

### URLs de servicios

```javascript
const GEOSERVER_URL = 'http://localhost:8080/geoserver/ne/wms';
const WFS_URL = '/api/geoserver-proxy?service=wfs';
```

**Diferencias clave:**

| Servicio | URL | ¿Usa proxy? | Razón |
|----------|-----|-------------|-------|
| WMS | `http://localhost:8080/geoserver/ne/wms` | ❌ No | Imágenes (sin CORS) |
| WFS | `/api/geoserver-proxy?service=wfs` | ✅ Sí | JSON (requiere CORS) |

**Desglose de GEOSERVER_URL:**
```
http://localhost:8080/geoserver/ne/wms
│      │         │    │         │  │
│      │         │    │         │  └─ Servicio (wms)
│      │         │    │         └──── Workspace (ne)
│      │         │    └────────────── Aplicación (geoserver)
│      │         └──────────────────── Puerto (8080)
│      └────────────────────────────── Host (localhost)
└───────────────────────────────────── Protocolo (http)
```

**Desglose de WFS_URL:**
```
/api/geoserver-proxy?service=wfs
│   │               │
│   │               └─ Parámetro que indica tipo de servicio
│   └───────────────── Endpoint del proxy en Flask
└────────────────────── Ruta relativa (mismo origen)
```

### Configuración del mapa

```javascript
const MAP_CONFIG = {
    center: [4.5709, -74.2973], // Centro de Colombia
    zoom: 6,
    minZoom: 5,
    maxZoom: 18
};
```

**Parámetros:**

**`center: [lat, lon]`**
- Coordenadas iniciales del mapa
- `[4.5709, -74.2973]` = Bogotá, Colombia
- Formato Leaflet: `[latitud, longitud]`
- ⚠️ **Cuidado:** GeoJSON usa `[longitud, latitud]` (orden invertido)

**`zoom: 6`**
- Nivel de zoom inicial
- Escala: 0 (mundo completo) a 18+ (calle)
- 6 = Vista de país completo

**`minZoom: 5` y `maxZoom: 18`**
- Limita rango de zoom
- Evita que usuario haga zoom out excesivo (minZoom)
- Evita zoom in excesivo si no hay datos de detalle (maxZoom)

**Visualización de niveles de zoom:**
```
0-2: Mundo completo
3-5: Continente
6-8: País        ← Zoom inicial (6)
9-11: Región
12-14: Ciudad
15-18: Calle
```

---

## 5.3 Inicialización del Mapa (Líneas 22-33)

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

### L.map()

```javascript
const map = L.map('map', options);
```

**Sintaxis:**
```javascript
L.map(id_o_elemento, opciones)
```

**Parámetros:**

**1. `'map'`** (string)
- ID del elemento HTML donde se renderizará
- Busca `<div id="map"></div>` en el DOM

**Alternativa con elemento:**
```javascript
const elemento = document.getElementById('map');
const map = L.map(elemento, {...});
```

**2. `options`** (objeto)
- Configuración del mapa

**Opciones comunes:**

| Opción | Valor | Descripción |
|--------|-------|-------------|
| `center` | `[lat, lon]` | Centro inicial |
| `zoom` | `number` | Zoom inicial |
| `minZoom` | `number` | Zoom mínimo permitido |
| `maxZoom` | `number` | Zoom máximo permitido |
| `zoomControl` | `boolean` | Mostrar controles +/- |
| `dragging` | `boolean` | Permitir arrastrar mapa |
| `scrollWheelZoom` | `boolean` | Zoom con rueda del mouse |

### Variable global `map`

```javascript
const map = L.map(...);
```

**¿Por qué es importante?**
- Se usa en todo el código para interactuar con el mapa
- Permite agregar capas: `map.addLayer()`
- Permite controlar vista: `map.setView()`, `map.fitBounds()`
- Permite agregar controles: `L.control().addTo(map)`

**Ámbito (scope):**
```javascript
const map = L.map('map', {...});  // Scope global (no está en función)

function agregarCapa() {
    // 'map' es accesible aquí
    L.tileLayer(...).addTo(map);
}
```

---

## 5.4 Capas Base (Líneas 36-58)

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

### L.tileLayer()

**¿Qué son los tile layers?**
- Mapas divididos en "tiles" (cuadrados de 256x256 px)
- Se cargan dinámicamente según la vista del usuario
- Rápido y eficiente

**Visualización:**
```
Mapa completo dividido en tiles:
┌────┬────┬────┬────┐
│ 1  │ 2  │ 3  │ 4  │  Zoom 6
├────┼────┼────┼────┤
│ 5  │ 6  │ 7  │ 8  │  256x256 px cada uno
└────┴────┴────┴────┘

Al hacer zoom in, cada tile se divide en 4:
┌──┬──┐
│1a│1b│  Zoom 7
├──┼──┤
│1c│1d│
└──┴──┘
```

### Sintaxis de L.tileLayer()

```javascript
L.tileLayer(urlTemplate, options)
```

**URL Template:**
```javascript
'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
```

**Placeholders:**
- `{s}`: Subdomain (a, b, c) - Balanceo de carga
- `{z}`: Zoom level
- `{x}`: Coordenada X del tile
- `{y}`: Coordenada Y del tile
- `{r}`: Retina (@2x para pantallas de alta resolución)

**Ejemplo de URL real generada:**
```
https://a.tile.openstreetmap.org/6/32/25.png
         │                         │ │  │
         └─ subdomain              │ │  └─ y
                                   │ └──── x
                                   └────── z (zoom)
```

### Opciones de tileLayer

```javascript
{
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19,
    subdomains: 'abcd'
}
```

**`attribution`**
- Texto legal/créditos
- Aparece en esquina inferior derecha del mapa
- **Obligatorio** para la mayoría de proveedores de tiles

**`maxZoom`**
- Zoom máximo disponible para esta capa
- Varía según el proveedor

**`subdomains`**
- Letras usadas en `{s}`
- `'abcd'` → a.basemaps, b.basemaps, c.basemaps, d.basemaps
- Distribuye carga entre servidores

### Objeto baseLayers

```javascript
const baseLayers = {
    'Mapa base (OSM)': L.tileLayer(...),
    'Satélite (Esri)': L.tileLayer(...),
    'Calles (CartoDB)': L.tileLayer(...)
};
```

**Estructura:**
```javascript
{
    'Nombre mostrado al usuario': capa_leaflet,
    'Otro nombre': otra_capa
}
```

**Propósito:**
- Organizar capas base
- Pasar al control de capas (veremos más adelante)
- Usuario puede cambiar entre capas base

### Agregar capa por defecto

```javascript
baseLayers['Mapa base (OSM)'].addTo(map);
```

**Equivalente a:**
```javascript
const osmLayer = L.tileLayer(...);
osmLayer.addTo(map);
```

**`.addTo(map)`**
- Método de todos los layers de Leaflet
- Agrega la capa al mapa
- Si no se llama, la capa existe pero no se muestra

---

## 5.5 Capas WMS de GeoServer (Líneas 60-81)

### WMS - Departamentos

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

### L.tileLayer.wms()

**Diferencia con L.tileLayer():**

| `L.tileLayer()` | `L.tileLayer.wms()` |
|-----------------|---------------------|
| URL template fija | URL base + parámetros WMS |
| Tiles precalculados | Tiles generados dinámicamente |
| Ejemplo: OSM, Esri | Ejemplo: GeoServer, MapServer |

**Sintaxis:**
```javascript
L.tileLayer.wms(baseUrl, wmsOptions)
```

**baseUrl:**
```javascript
'http://localhost:8080/geoserver/ne/wms'
```
- URL base del servicio WMS
- Sin parámetros de query

**wmsOptions:**

### Parámetro `layers`

```javascript
layers: 'ne:dpto_choco'
```

**Formato:** `workspace:layer_name`

- `ne`: Workspace en GeoServer
- `dpto_choco`: Nombre de la capa

**Múltiples capas:**
```javascript
layers: 'ne:dpto_choco,ne:mpios_choco'  // Separadas por coma
```

### Parámetro `format`

```javascript
format: 'image/png'
```

**Opciones comunes:**
- `image/png`: PNG (soporta transparencia) ✅
- `image/jpeg`: JPEG (más pequeño, sin transparencia)
- `image/gif`: GIF (raramente usado)

**¿Por qué PNG?**
- Soporta transparencia (fondo transparente)
- Calidad sin pérdida
- Permite superponer capas

### Parámetro `transparent`

```javascript
transparent: true
```

**Efecto:**
- `true`: Fondo del mapa transparente
- `false`: Fondo opaco (típicamente blanco)

**Visualización:**
```
transparent: true
┌──────────────┐
│  [Capa base] │
│  ┌────────┐  │  ← Departamento con fondo transparente
│  │ Depto  │  │
│  └────────┘  │
└──────────────┘

transparent: false
┌──────────────┐
│ ░░░░░░░░░░░ │  ← Fondo blanco tapa capa base
│ ░┌────────┐░ │
│ ░│ Depto  │░ │
│ ░└────────┘░ │
└──────────────┘
```

### Parámetro `styles`

```javascript
styles: ''
```

**Opciones:**
- `''` (vacío): Usa estilo por defecto de GeoServer
- `'nombre_estilo'`: Usa estilo personalizado

**Ejemplo con estilo personalizado:**
```javascript
styles: 'polygon_blue'  // Estilo definido en GeoServer
```

### URL generada internamente

Leaflet genera URLs como esta:

```
http://localhost:8080/geoserver/ne/wms?
    service=WMS&
    version=1.1.1&
    request=GetMap&
    layers=ne:dpto_choco&
    styles=&
    format=image%2Fpng&
    transparent=true&
    width=256&
    height=256&
    srs=EPSG%3A3857&
    bbox=-8575595.864,556597.454,-8566051.864,566141.454
```

**Parámetros agregados automáticamente:**
- `service=WMS`
- `version=1.1.1` (o 1.3.0)
- `request=GetMap`
- `width=256`, `height=256` (tamaño del tile)
- `srs=EPSG:3857` (Web Mercator, usado por Leaflet)
- `bbox=...` (bounding box del tile específico)

### WMS - Municipios

```javascript
const municipiosWMS = L.tileLayer.wms(GEOSERVER_URL, {
    layers: 'ne:mpios_choco',
    format: 'image/png',
    transparent: true,
    attribution: 'IGAC',
    styles: ''
});
```

**Diferencias con departamentos:**
- Capa: `mpios_choco` (municipios)
- **No se agrega por defecto** (no hay `.addTo(map)`)
- Usuario puede activarla desde control de capas

**Razón:**
- Evitar sobrecarga visual
- Usuario decide qué capas activar

---

## 5.6 Flujo Completo de Carga WMS

### Paso a paso

**1. JavaScript crea capa WMS:**
```javascript
const departamentosWMS = L.tileLayer.wms(
    'http://localhost:8080/geoserver/ne/wms',
    { layers: 'ne:dpto_choco', ... }
);
```

**2. Se agrega al mapa:**
```javascript
departamentosWMS.addTo(map);
```

**3. Leaflet detecta viewport visible:**
```javascript
// Leaflet calcula qué tiles necesita
// Ejemplo: Tiles (z=6, x=32-35, y=24-27)
```

**4. Para cada tile, Leaflet hace petición HTTP GET:**
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

**5. GeoServer procesa petición:**
```
- Consulta datos de la capa 'ne:dpto_choco'
- Filtra features dentro del bbox
- Reproyecta a EPSG:3857
- Renderiza a imagen PNG 256x256
- Aplica estilo
- Retorna imagen
```

**6. Navegador recibe imagen PNG:**
```
Content-Type: image/png
[datos binarios de la imagen]
```

**7. Leaflet posiciona imagen en el mapa:**
```javascript
<img src="data:image/png;base64,..."
     style="position: absolute; left: 512px; top: 256px;">
```

**8. Usuario mueve/hace zoom:**
```
→ Leaflet calcula nuevos tiles necesarios
→ Repite proceso (pasos 4-7)
```

---

## 5.7 Ventajas de WMS para este Caso

### ¿Por qué usar WMS para departamentos?

✅ **Rendimiento:**
- Solo transfiere imágenes (~10-50 KB por tile)
- No importa cuántos polígonos tenga la capa

✅ **Escalabilidad:**
- Funciona igual con 10 features o 10,000

✅ **Sin CORS:**
- Imágenes no tienen restricciones de origen
- Petición directa a GeoServer

✅ **Caché:**
- GeoServer puede cachear tiles
- Mejora rendimiento en peticiones repetidas

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
- No se puede modificar geometrías

**Solución:** Usar WFS (veremos en Módulo 6)

---

## 5.8 Ejercicio Práctico 1

**Tarea:** Agregar una nueva capa WMS de topografía.

**Pasos:**

```javascript
// 1. Crear nueva capa (agregar después de municipiosWMS)
const topoWMS = L.tileLayer.wms(GEOSERVER_URL, {
    layers: 'ne:topografia',  // Capa debe existir en GeoServer
    format: 'image/png',
    transparent: true,
    attribution: 'IGAC'
});

// 2. Agregarla al objeto baseLayers u overlayLayers
// (veremos overlayLayers en siguiente sección)
```

---

## 5.9 Resumen

Has aprendido:

✅ Configuración global con constantes
✅ Inicializar mapa con `L.map()`
✅ Agregar capas base con `L.tileLayer()`
✅ Cargar capas WMS con `L.tileLayer.wms()`
✅ Diferencias entre tile layers normales y WMS
✅ Parámetros del protocolo WMS
✅ Flujo completo de petición WMS

### Conceptos clave

| Concepto | Descripción |
|----------|-------------|
| **Tile Layer** | Mapa dividido en cuadrados de 256x256px |
| **WMS** | Estándar para servir mapas como imágenes |
| **GEOSERVER_URL** | URL base del servicio WMS |
| **layers** | Parámetro WMS que especifica qué capa mostrar |
| **transparent** | Parámetro WMS para fondo transparente |
| **bbox** | Bounding box de la porción del mapa solicitada |

### Próximo módulo

En el **Módulo 6 (JavaScript Parte 2)**, cubriremos:
- Carga de datos WFS a través del proxy Flask
- Conversión de GeoJSON a capas Leaflet
- Interactividad (click, hover)
- Estilos dinámicos
- Búsqueda y filtrado

---

**[⬅️ Módulo 4: Estilos CSS](04_ESTILOS_CSS.md)** | **[Volver al Índice](README.md)** | **[Siguiente: Módulo 6 - JavaScript Parte 2 ➡️](06_JAVASCRIPT_PARTE_2.md)**
