# Módulo 6: JavaScript Parte 2 - WFS e Interactividad

## Objetivos de Aprendizaje

Al completar este módulo, comprenderás:

- 📡 Cómo cargar datos WFS a través del proxy Flask
- 🔄 El flujo completo de peticiones WFS (cliente → proxy → GeoServer)
- 🗺️ Cómo convertir GeoJSON a capas Leaflet interactivas
- 🎨 Cómo aplicar estilos dinámicos a features
- 🖱️ Cómo implementar interactividad (click, hover, zoom)
- 🔍 Cómo implementar búsqueda en datos WFS
- 🎛️ Cómo crear controles personalizados de Leaflet

---

## 6.1 Visión General

En este módulo analizaremos las secciones más importantes de app.js:

1. **Carga de datos WFS** (líneas 84-120)
2. **Estilos de features** (líneas 122-140)
3. **Interactividad** (líneas 142-196)
4. **Control de capas** (líneas 199-211)
5. **Control personalizado** (líneas 213-249)
6. **Búsqueda** (líneas 252-337)
7. **Inicialización** (líneas 340-347)

---

## 6.2 Variables Globales para WFS (Líneas 84-88)

```javascript
// ============================================
// Capa WFS (GeoJSON) para Interactividad
// ============================================

let departamentosGeoJSON = null;
let departamentosData = null;
```

### ¿Por qué variables globales?

**`let departamentosGeoJSON`**
- Almacena la capa Leaflet GeoJSON
- Necesaria para:
  - Resetear estilos: `departamentosGeoJSON.resetStyle(layer)`
  - Iterar features: `departamentosGeoJSON.eachLayer(...)`
  - Agregar/remover del mapa

**`let departamentosData`**
- Almacena los datos GeoJSON raw (JavaScript object)
- Necesaria para:
  - Búsqueda sin hacer nuevas peticiones al servidor
  - Filtrado en el cliente
  - Análisis de atributos

**¿Por qué `let` y no `const`?**
```javascript
let departamentosGeoJSON = null;  // Inicialmente null
// ... más tarde:
departamentosGeoJSON = L.geoJSON(data);  // Se reasigna
```

---

## 6.3 Carga de Datos WFS (Líneas 90-120)

Esta es una de las funciones MÁS IMPORTANTES del archivo.

```javascript
// Función para cargar departamentos desde WFS
function loadDepartamentosWFS() {
    const wfsUrl = `/api/geoserver-proxy?service=WFS&version=2.0.0&request=GetFeature&typeName=ne:departamentos&outputFormat=application/json`;

    fetch(wfsUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al cargar datos WFS');
            }
            return response.json();
        })
        .then(data => {
            departamentosData = data;

            // Crear capa GeoJSON con estilo y eventos
            departamentosGeoJSON = L.geoJSON(data, {
                style: featureStyle,
                onEachFeature: onEachFeature
            }).addTo(map);

            // Ajustar vista al extent de los datos
            map.fitBounds(departamentosGeoJSON.getBounds());
            layerControl.addOverlay(departamentosGeoJSON, 'Departamentos Interactivos (WFS)');

            console.log('Departamentos cargados:', data.features.length);
        })
        .catch(error => {
            console.error('Error cargando WFS:', error);
            alert('No se pudieron cargar los datos de departamentos. Verifica que GeoServer esté ejecutándose en localhost:8080');
        });
}
```

### Paso 1: Construcción de la URL WFS

```javascript
const wfsUrl = `/api/geoserver-proxy?service=WFS&version=2.0.0&request=GetFeature&typeName=ne:departamentos&outputFormat=application/json`;
```

**Desglose de parámetros:**

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| **Base** | `/api/geoserver-proxy` | Endpoint del proxy en Flask |
| `service` | `WFS` | Tipo de servicio OGC |
| `version` | `2.0.0` | Versión del protocolo WFS |
| `request` | `GetFeature` | Operación solicitada |
| `typeName` | `ne:departamentos` | Capa (workspace:layer) |
| `outputFormat` | `application/json` | Formato de salida (GeoJSON) |

**Formatos de salida disponibles:**
- `application/json` ✅ (GeoJSON)
- `text/xml; subtype=gml/3.2.1` (GML)
- `csv` (CSV)
- `application/vnd.google-earth.kml+xml` (KML)

**URL completa generada:**
```
/api/geoserver-proxy?
    service=WFS&
    version=2.0.0&
    request=GetFeature&
    typeName=ne:departamentos&
    outputFormat=application/json
```

### Paso 2: Fetch API

```javascript
fetch(wfsUrl)
```

**¿Qué es fetch()?**
- API moderna de JavaScript para peticiones HTTP
- Retorna una **Promesa**
- Reemplaza a `XMLHttpRequest` (antiguo)

**Alternativas:**
```javascript
// Fetch (moderno) ✅
fetch(url).then(...)

// Async/await (más moderno aún) ✅
const response = await fetch(url);
const data = await response.json();

// XMLHttpRequest (antiguo) ❌
const xhr = new XMLHttpRequest();
xhr.open('GET', url);
...
```

### Paso 3: Procesar respuesta HTTP

```javascript
.then(response => {
    if (!response.ok) {
        throw new Error('Error al cargar datos WFS');
    }
    return response.json();
})
```

**Objeto `response`:**
```javascript
{
    ok: true/false,        // true si status 200-299
    status: 200,           // Código HTTP
    statusText: 'OK',
    headers: {...},
    body: ReadableStream   // Datos
}
```

**`response.ok`**
- `true`: Status 200-299 (éxito)
- `false`: Status 400+, 500+ (error)

**¿Por qué verificar `ok`?**
- fetch() NO rechaza en errores HTTP 404, 500, etc.
- Solo rechaza en errores de red (sin conexión, DNS fail, etc.)
- Debemos verificar manualmente

**`return response.json()`**
- Parsea el body como JSON
- Retorna **otra promesa**
- Resultado es un objeto JavaScript

### Paso 4: Procesar datos GeoJSON

```javascript
.then(data => {
    departamentosData = data;
    ...
})
```

**Estructura de `data` (GeoJSON FeatureCollection):**
```javascript
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "departamentos.1",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[lon, lat], [lon, lat], ...]]
            },
            "properties": {
                "dpto_ccdgo": "27",
                "dpto_cnmbr": "Chocó"
            }
        },
        // ... más features
    ],
    "totalFeatures": 33,
    "numberReturned": 33
}
```

**Guardar datos:**
```javascript
departamentosData = data;
```
- Variable global para búsqueda posterior
- No es necesario hacer nueva petición al buscar

### Paso 5: Crear capa GeoJSON de Leaflet

```javascript
departamentosGeoJSON = L.geoJSON(data, {
    style: featureStyle,
    onEachFeature: onEachFeature
}).addTo(map);
```

**`L.geoJSON()`**
- Convierte objeto GeoJSON en capa de Leaflet
- Crea automáticamente capas para cada feature

**Opciones:**

**`style: featureStyle`**
- Función que retorna objeto de estilo
- Se llama para cada feature
- Permite estilos dinámicos basados en atributos

**`onEachFeature: onEachFeature`**
- Función que se ejecuta para cada feature
- Agrega interactividad (popups, eventos)

### Paso 6: Ajustar vista del mapa

```javascript
map.fitBounds(departamentosGeoJSON.getBounds());
```

**`getBounds()`**
- Calcula bounding box de todas las geometrías
- Retorna objeto `LatLngBounds`

**`fitBounds(bounds)`**
- Ajusta zoom y centro para mostrar el área completa
- Garantiza que todos los departamentos sean visibles

**Ejemplo:**
```javascript
const bounds = departamentosGeoJSON.getBounds();
// bounds = LatLngBounds([[minLat, minLon], [maxLat, maxLon]])

map.fitBounds(bounds);
// Mapa se ajusta para mostrar todo
```

### Paso 7: Agregar a control de capas

```javascript
layerControl.addOverlay(departamentosGeoJSON, 'Departamentos Interactivos (WFS)');
```

- Agrega la capa al control de capas (veremos más adelante)
- Usuario puede activar/desactivar

### Paso 8: Manejo de errores

```javascript
.catch(error => {
    console.error('Error cargando WFS:', error);
    alert('No se pudieron cargar los datos...');
});
```

**Cuándo se ejecuta `.catch()`:**
- Error de red (sin conexión)
- Error en proxy (Flask caído)
- Error en GeoServer (servicio no disponible)
- `throw new Error()` en `.then()`

---

## 6.4 Flujo Completo de la Petición WFS

```
╔════════════════════════════════════════════════════════════╗
║                  CLIENTE (Navegador)                       ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  1. JavaScript ejecuta:                                    ║
║     fetch('/api/geoserver-proxy?service=WFS&...')          ║
║                           │                                ║
║                           ↓                                ║
║  2. Navegador hace petición HTTP GET a:                    ║
║     http://localhost:5000/api/geoserver-proxy?service=...  ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
                            │
                            │ HTTP GET
                            ↓
╔════════════════════════════════════════════════════════════╗
║              PROXY (Flask - app.py)                        ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  3. Flask recibe petición en ruta:                         ║
║     @app.route('/api/geoserver-proxy')                     ║
║                           │                                ║
║                           ↓                                ║
║  4. Extrae parámetros:                                     ║
║     service = request.args.get('service')  # 'WFS'         ║
║     params = request.args.to_dict()                        ║
║                           │                                ║
║                           ↓                                ║
║  5. Construye URL a GeoServer:                             ║
║     url = 'http://geoserver:8080/geoserver/ne/wfs'         ║
║                           │                                ║
║                           ↓                                ║
║  6. Hace petición HTTP a GeoServer:                        ║
║     response = requests.get(url, params=params)            ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
                            │
                            │ HTTP GET
                            ↓
╔════════════════════════════════════════════════════════════╗
║            GEOSERVER (Servidor OGC)                        ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  7. GeoServer recibe petición WFS:                         ║
║     GET /geoserver/ne/wfs?                                 ║
║         service=WFS&                                       ║
║         request=GetFeature&                                ║
║         typeName=ne:departamentos&                         ║
║         outputFormat=application/json                      ║
║                           │                                ║
║                           ↓                                ║
║  8. GeoServer procesa:                                     ║
║     - Consulta datastore (PostGIS/Shapefile)               ║
║     - Lee geometrías y atributos                           ║
║     - Filtra por bbox (si se especificó)                   ║
║     - Reproyecta a EPSG:4326                               ║
║                           │                                ║
║                           ↓                                ║
║  9. Serializa a GeoJSON:                                   ║
║     {                                                      ║
║       "type": "FeatureCollection",                         ║
║       "features": [...]                                    ║
║     }                                                      ║
║                           │                                ║
║                           ↓                                ║
║  10. Retorna HTTP 200 + JSON                               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
                            │
                            │ HTTP Response (GeoJSON)
                            ↓
╔════════════════════════════════════════════════════════════╗
║              PROXY (Flask)                                 ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  11. Flask recibe respuesta de GeoServer                   ║
║                           │                                ║
║                           ↓                                ║
║  12. Retorna al navegador:                                 ║
║      return Response(                                      ║
║          response.content,                                 ║
║          content_type='application/json'                   ║
║      )                                                     ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
                            │
                            │ HTTP Response (GeoJSON)
                            ↓
╔════════════════════════════════════════════════════════════╗
║                  CLIENTE (Navegador)                       ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  13. fetch() recibe respuesta                              ║
║                           │                                ║
║                           ↓                                ║
║  14. .then(response => response.json())                    ║
║      Parsea JSON a objeto JavaScript                       ║
║                           │                                ║
║                           ↓                                ║
║  15. .then(data => {...})                                  ║
║      data = objeto GeoJSON con features                    ║
║                           │                                ║
║                           ↓                                ║
║  16. L.geoJSON(data).addTo(map)                            ║
║      Crea capas Leaflet y las agrega al mapa               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

---

## 6.5 Estilos de Features (Líneas 122-140)

```javascript
// Estilo de las features
function featureStyle(feature) {
    return {
        fillColor: '#e8f881',
        weight: 2,
        opacity: 0.8,
        color: '#232323',
        fillOpacity: 0.4
    };
}

// Estilo al pasar el mouse (highlight)
function highlightStyle() {
    return {
        weight: 4,
        color: '#667eea',
        fillOpacity: 0.7
    };
}
```

### featureStyle()

**Cuándo se llama:**
- Automáticamente por Leaflet al crear cada feature
- Para cada polígono en el GeoJSON

**Parámetro `feature`:**
```javascript
{
    type: "Feature",
    geometry: {...},
    properties: {
        dpto_ccdgo: "27",
        dpto_cnmbr: "Chocó"
    }
}
```

**Objeto de estilo retornado:**

| Propiedad | Valor | Descripción |
|-----------|-------|-------------|
| `fillColor` | `'#e8f881'` | Color de relleno (amarillo verdoso) |
| `weight` | `2` | Grosor del borde en píxeles |
| `opacity` | `0.8` | Opacidad del borde (80%) |
| `color` | `'#232323'` | Color del borde (gris oscuro) |
| `fillOpacity` | `0.4` | Opacidad del relleno (40%) |

**Ejemplo de estilo dinámico:**
```javascript
function featureStyle(feature) {
    // Color diferente según código del departamento
    const codigo = parseInt(feature.properties.dpto_ccdgo);
    const color = codigo > 50 ? '#ff6b6b' : '#3388ff';

    return {
        fillColor: color,
        weight: 2,
        opacity: 0.8,
        color: '#232323',
        fillOpacity: 0.5
    };
}
```

### highlightStyle()

**Cuándo se usa:**
- Al pasar el mouse sobre una feature (evento `mouseover`)
- Se aplica manualmente con `layer.setStyle(highlightStyle())`

**Diferencias con featureStyle:**
- Borde más grueso (`weight: 4`)
- Color diferente (`#667eea` - violeta)
- Más opaco (`fillOpacity: 0.7`)

**Resultado visual:**
```
Estado normal:
┌──────────────┐
│ Departamento │  Borde delgado, color amarillo
└──────────────┘

Hover:
╔══════════════╗
║ Departamento ║  Borde grueso, color violeta
╚══════════════╝
```

---

## 6.6 Interactividad (Líneas 146-196)

### onEachFeature()

```javascript
function onEachFeature(feature, layer) {
    // Crear popup con información
    if (feature.properties) {
        const props = feature.properties;
        const popupContent = `
            <div class="popup-title">${props.dpto_cnmbr || 'Sin nombre'}</div>
            <div class="popup-divider"></div>
            <div class="popup-info"><strong>Código:</strong> ${props.dpto_ccdgo || 'N/A'}</div>
        `;
        layer.bindPopup(popupContent);
    }

    // Eventos del mouse
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: clickFeature
    });
}
```

**Cuándo se llama:**
- Por cada feature al crear la capa GeoJSON
- Parámetros: `feature` (datos) y `layer` (capa Leaflet)

### Crear popup

```javascript
const popupContent = `
    <div class="popup-title">${props.dpto_cnmbr || 'Sin nombre'}</div>
    <div class="popup-divider"></div>
    <div class="popup-info"><strong>Código:</strong> ${props.dpto_ccdgo || 'N/A'}</div>
`;
layer.bindPopup(popupContent);
```

**Template literals:**
- `` `...` `` (backticks) permiten multi-línea
- `${variable}` inserta valor de variable

**`props.dpto_cnmbr || 'Sin nombre'`**
- Si `dpto_cnmbr` existe → usar su valor
- Si es `null`/`undefined` → usar 'Sin nombre'

**`layer.bindPopup(html)`**
- Asocia popup a la capa
- Se muestra al hacer click

### Agregar eventos

```javascript
layer.on({
    mouseover: highlightFeature,
    mouseout: resetHighlight,
    click: clickFeature
});
```

**Sintaxis alternativa:**
```javascript
// Opción 1 (usado aquí):
layer.on({
    mouseover: handler1,
    mouseout: handler2
});

// Opción 2 (individual):
layer.on('mouseover', handler1);
layer.on('mouseout', handler2);
```

### Manejador highlightFeature

```javascript
function highlightFeature(e) {
    const layer = e.target;

    layer.setStyle(highlightStyle());
    layer.bringToFront();

    // Actualizar panel de información
    if (layer.feature.properties) {
        updateInfoControl(layer.feature.properties);
    }
}
```

**Parámetro `e` (evento):**
```javascript
{
    type: 'mouseover',
    target: layer,  // La capa que disparó el evento
    latlng: LatLng,
    ...
}
```

**`layer.setStyle(newStyle)`**
- Cambia el estilo de la capa
- Aplica `highlightStyle()`

**`layer.bringToFront()`**
- Mueve la capa al frente (z-index)
- Evita que otras capas la tapen

**`updateInfoControl(props)`**
- Función personalizada (línea 236)
- Actualiza control de información en el mapa

### Manejador resetHighlight

```javascript
function resetHighlight(e) {
    const layer = e.target;

    if (departamentosGeoJSON) {
        departamentosGeoJSON.resetStyle(layer);
    }

    // Resetear panel de información
    updateInfoControl();
}
```

**`departamentosGeoJSON.resetStyle(layer)`**
- Vuelve al estilo original definido en `featureStyle()`
- Remueve el highlight

**`updateInfoControl()`** (sin argumentos)
- Resetea el control de información
- Muestra texto por defecto

### Manejador clickFeature

```javascript
function clickFeature(e) {
    const layer = e.target;
    map.fitBounds(layer.getBounds());
    layer.openPopup();
}
```

**`map.fitBounds(layer.getBounds())`**
- Hace zoom a la feature clickeada
- Centra la vista en ella

**`layer.openPopup()`**
- Abre el popup asociado (bindPopup)

---

## 6.7 Control de Capas (Líneas 199-211)

```javascript
// ============================================
// Control de Capas
// ============================================

const overlayLayers = {
    'Departamentos (WMS)': departamentosWMS,
    'Municipios (WMS)': municipiosWMS,
    //'Departamentos Interactivos (WFS)': departamentosGeoJSON
};

const layerControl = L.control.layers(baseLayers, overlayLayers, {
    position: 'topright',
    collapsed: false
}).addTo(map);
```

### L.control.layers()

**Sintaxis:**
```javascript
L.control.layers(baseLayers, overlayLayers, options)
```

**`baseLayers`** (objeto):
- Capas base mutuamente excluyentes
- Solo una puede estar activa a la vez
- Radio buttons en el control

**`overlayLayers`** (objeto):
- Capas que se superponen
- Varias pueden estar activas simultáneamente
- Checkboxes en el control

**Opciones:**
- `position: 'topright'`: Posición del control
- `collapsed: false`: Mostrar expandido por defecto

**Resultado visual:**
```
┌──────────────────────────┐
│ ○ Mapa base (OSM)       │  ← Radio buttons (baseLayers)
│ ○ Satélite (Esri)       │
│ ○ Calles (CartoDB)      │
├──────────────────────────┤
│ ☑ Departamentos (WMS)    │  ← Checkboxes (overlayLayers)
│ ☐ Municipios (WMS)       │
└──────────────────────────┘
```

### Agregar capa después

```javascript
layerControl.addOverlay(departamentosGeoJSON, 'Departamentos Interactivos (WFS)');
```

- Agrega capa al control después de la creación
- Necesario porque `departamentosGeoJSON` se crea asíncronamente

---

## 6.8 Control de Información (Líneas 213-238)

```javascript
// ============================================
// Control de Información
// ============================================

const infoControl = L.control({position: 'topleft'});

infoControl.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info-control');
    this.update();
    return this._div;
};

infoControl.update = function (props) {
    this._div.innerHTML = '<h4>Información del Departamento</h4>' +
        (props ?
            '<p class="highlight">' + props.dpto_cnmbr + '</p>' +
            '<p><strong>Código:</strong> ' + props.dpto_ccdgo + '</p>'
            : '<p>Pasa el cursor sobre un departamento</p>');
};

infoControl.addTo(map);

// Función auxiliar para actualizar el control
function updateInfoControl(props) {
    infoControl.update(props);
}
```

### Crear control personalizado

**`L.control(options)`**
- Crea control base
- Requiere definir método `onAdd()`

**`onAdd(map)`**
- Se llama cuando el control se agrega al mapa
- Debe retornar elemento DOM del control

**`L.DomUtil.create('div', 'info-control')`**
- Crea elemento DOM: `<div class="info-control"></div>`
- Equivalente a: `document.createElement('div')`

### Método update()

```javascript
infoControl.update = function (props) {
    this._div.innerHTML = '<h4>...</h4>' + ...;
};
```

**Operador ternario:**
```javascript
props ?
    'HTML con props' :
    'HTML sin props'
```

**Si props existe:**
```html
<h4>Información del Departamento</h4>
<p class="highlight">Chocó</p>
<p><strong>Código:</strong> 27</p>
```

**Si props es null:**
```html
<h4>Información del Departamento</h4>
<p>Pasa el cursor sobre un departamento</p>
```

---

## 6.9 Búsqueda (Líneas 252-337)

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('search-button');
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    if (searchButton && searchInput) {
        // Búsqueda al hacer clic
        searchButton.addEventListener('click', performSearch);

        // Búsqueda al presionar Enter
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }

    function performSearch() {
        const searchTerm = searchInput.value.trim().toLowerCase();

        if (!searchTerm) {
            searchResults.innerHTML = '<p class="info-text">Por favor ingresa un nombre de departamento</p>';
            return;
        }

        if (!departamentosData || !departamentosData.features) {
            searchResults.innerHTML = '<p class="info-text">Los datos aún no se han cargado. Espera un momento.</p>';
            return;
        }

        // Buscar departamentos que coincidan
        const matches = departamentosData.features.filter(feature => {
            const nombre = feature.properties.dpto_cnmbr || '';
            return nombre.toLowerCase().includes(searchTerm);
        });

        // Mostrar resultados
        if (matches.length === 0) {
            searchResults.innerHTML = '<p class="info-text">No se encontraron resultados</p>';
        } else {
            let html = '<h3 style="font-size: 0.9rem; margin-bottom: 0.5rem;">Resultados (' + matches.length + '):</h3>';

            matches.forEach(feature => {
                const nombre = feature.properties.dpto_cnmbr;
                const codigo = feature.properties.dpto_ccdgo;

                html += `
                    <div class="search-result-item" data-codigo="${codigo}">
                        <strong>${nombre}</strong><br>
                        <small>Código: ${codigo}</small>
                    </div>
                `;
            });

            searchResults.innerHTML = html;

            // Agregar evento click a los resultados
            document.querySelectorAll('.search-result-item').forEach(item => {
                item.addEventListener('click', function() {
                    const codigo = this.getAttribute('data-codigo');
                    zoomToDepartamento(codigo);
                });
            });
        }
    }

    function zoomToDepartamento(codigo) {
        if (!departamentosGeoJSON) return;

        departamentosGeoJSON.eachLayer(function(layer) {
            if (layer.feature.properties.dpto_ccdgo === codigo) {
                map.fitBounds(layer.getBounds());
                layer.openPopup();

                // Highlight temporal
                layer.setStyle(highlightStyle());
                setTimeout(() => {
                    departamentosGeoJSON.resetStyle(layer);
                }, 2000);
            }
        });
    }
});
```

### DOMContentLoaded

```javascript
document.addEventListener('DOMContentLoaded', function() {...});
```

**¿Por qué necesario?**
- Garantiza que el DOM esté completamente cargado
- Elementos HTML existen antes de intentar accederlos

### Capturar elementos del DOM

```javascript
const searchButton = document.getElementById('search-button');
const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
```

### Eventos de búsqueda

```javascript
searchButton.addEventListener('click', performSearch);

searchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        performSearch();
    }
});
```

**Dos formas de activar búsqueda:**
1. Click en botón
2. Presionar Enter en el input

### Función performSearch()

**1. Obtener término de búsqueda:**
```javascript
const searchTerm = searchInput.value.trim().toLowerCase();
```
- `.value`: Texto del input
- `.trim()`: Elimina espacios al inicio/final
- `.toLowerCase()`: Convierte a minúsculas

**2. Validar entrada:**
```javascript
if (!searchTerm) {
    searchResults.innerHTML = '...';
    return;
}
```

**3. Verificar datos cargados:**
```javascript
if (!departamentosData || !departamentosData.features) {
    searchResults.innerHTML = '...';
    return;
}
```

**4. Filtrar features:**
```javascript
const matches = departamentosData.features.filter(feature => {
    const nombre = feature.properties.dpto_cnmbr || '';
    return nombre.toLowerCase().includes(searchTerm);
});
```

**Array.filter():**
- Itera sobre features
- Retorna nuevo array con elementos que cumplen condición
- `.includes(searchTerm)`: Búsqueda parcial

**Ejemplo:**
```javascript
searchTerm = "cho"
"Chocó".toLowerCase().includes("cho")  → true ✅
"Antioquia".toLowerCase().includes("cho")  → false ❌
```

**5. Mostrar resultados:**
```javascript
matches.forEach(feature => {
    html += `
        <div class="search-result-item" data-codigo="${codigo}">
            <strong>${nombre}</strong><br>
            <small>Código: ${codigo}</small>
        </div>
    `;
});

searchResults.innerHTML = html;
```

**Atributo `data-*`:**
```html
<div data-codigo="27">
```
- Almacena datos personalizados en HTML
- Accesible con `getAttribute('data-codigo')`

**6. Agregar eventos a resultados:**
```javascript
document.querySelectorAll('.search-result-item').forEach(item => {
    item.addEventListener('click', function() {
        const codigo = this.getAttribute('data-codigo');
        zoomToDepartamento(codigo);
    });
});
```

### Función zoomToDepartamento()

```javascript
function zoomToDepartamento(codigo) {
    departamentosGeoJSON.eachLayer(function(layer) {
        if (layer.feature.properties.dpto_ccdgo === codigo) {
            map.fitBounds(layer.getBounds());
            layer.openPopup();

            // Highlight temporal
            layer.setStyle(highlightStyle());
            setTimeout(() => {
                departamentosGeoJSON.resetStyle(layer);
            }, 2000);
        }
    });
}
```

**`.eachLayer(callback)`**
- Itera sobre cada capa en el grupo
- Similar a `forEach` pero para capas Leaflet

**Highlight temporal:**
```javascript
layer.setStyle(highlightStyle());  // Aplicar highlight
setTimeout(() => {
    departamentosGeoJSON.resetStyle(layer);  // Quitar después de 2s
}, 2000);
```

---

## 6.10 Inicialización (Líneas 340-347)

```javascript
// ============================================
// Inicialización
// ============================================

// Cargar datos WFS al cargar la página
window.addEventListener('load', function() {
    console.log('Iniciando aplicación...');
    loadDepartamentosWFS();
});
```

**`window.addEventListener('load', ...)`**
- Se ejecuta cuando TODO está cargado (HTML, CSS, imágenes, scripts)
- Alternativa: `DOMContentLoaded` (solo DOM, más rápido)

**Llamada a `loadDepartamentosWFS()`**
- Inicia carga automática de datos WFS
- Todo el proceso explicado en sección 6.3 comienza aquí

---

## 6.11 Resumen

Has aprendido:

✅ Cómo cargar datos WFS a través del proxy con fetch()
✅ El flujo completo cliente → proxy → GeoServer
✅ Cómo convertir GeoJSON a capas Leaflet con L.geoJSON()
✅ Cómo aplicar estilos estáticos y dinámicos
✅ Cómo agregar interactividad (hover, click)
✅ Cómo crear controles personalizados de Leaflet
✅ Cómo implementar búsqueda en datos vectoriales
✅ Promesas y manejo de asincronía

### Próximo módulo

En el **Módulo 7 (Proxy Flask)**, analizaremos en detalle el archivo `app.py`:
- Implementación completa del proxy
- Manejo de CORS con flask-cors
- Enrutamiento de peticiones WMS/WFS
- Manejo de errores y timeouts

---

**[⬅️ Módulo 5: JavaScript Parte 1](05_JAVASCRIPT_PARTE_1.md)** | **[Volver al Índice](README.md)** | **[Siguiente: Módulo 7 - Proxy Flask ➡️](07_PROXY_FLASK.md)**
