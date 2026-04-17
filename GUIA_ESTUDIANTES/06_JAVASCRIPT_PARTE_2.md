# Módulo 6: JavaScript Parte 2 - WFS e Interactividad

## Objetivos de Aprendizaje

Al completar este módulo, habrás:

- Implementado carga de datos WFS a través del proxy Flask
- Convertido GeoJSON a capas Leaflet interactivas
- Aplicado estilos dinámicos a features
- Agregado interactividad (hover, click, zoom)
- Creado control de información personalizado
- Implementado búsqueda de departamentos

---

## 6.1 Preparación

Continuaremos editando el archivo `webapp/static/js/app.js` que creamos en el Módulo 5.

En este módulo agregaremos aproximadamente **300 líneas** más de código.

---

## 6.2 Paso 1: Variables Globales para WFS

Después del control de escala (al final del código del Módulo 5), agrega estas variables globales:

```javascript
// ============================================
// Capa WFS (GeoJSON) para Interactividad
// ============================================

let departamentosGeoJSON = null;
let departamentosData = null;
```

**Explicación:**

**`let departamentosGeoJSON = null;`**
- Almacenará la capa Leaflet GeoJSON
- Se usa para: resetear estilos, iterar features, agregar/remover del mapa

**`let departamentosData = null;`**
- Almacenará los datos GeoJSON raw (objeto JavaScript)
- Se usa para: búsqueda sin nuevas peticiones al servidor

**¿Por qué `let` en lugar de `const`?**
```javascript
let departamentosGeoJSON = null;  // Inicialmente null
// ... más tarde:
departamentosGeoJSON = L.geoJSON(data);  // Se reasigna ✅
```

Con `const` obtendríamos error al intentar reasignar.

---

## 6.3 Paso 2: Función para Cargar Datos WFS

Agrega la función principal que carga datos WFS desde GeoServer:

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

**Explicación:**

**Paso 1: Construcción de la URL WFS**
```javascript
const wfsUrl = `/api/geoserver-proxy?service=WFS&version=2.0.0&request=GetFeature&typeName=ne:departamentos&outputFormat=application/json`;
```

**Desglose de parámetros:**
- `/api/geoserver-proxy`: Endpoint del proxy en Flask
- `service=WFS`: Tipo de servicio OGC
- `version=2.0.0`: Versión del protocolo WFS
- `request=GetFeature`: Operación solicitada
- `typeName=ne:departamentos`: Capa (workspace:layer)
- `outputFormat=application/json`: Formato de salida (GeoJSON)

**Paso 2: Petición HTTP con fetch()**
```javascript
fetch(wfsUrl)
```
- API moderna de JavaScript para peticiones HTTP
- Retorna una **Promesa**
- Reemplaza a `XMLHttpRequest` (antiguo)

**Paso 3: Verificar respuesta**
```javascript
.then(response => {
    if (!response.ok) {
        throw new Error('Error al cargar datos WFS');
    }
    return response.json();
})
```
- `response.ok`: `true` si status 200-299, `false` si error
- `response.json()`: Parsea el body como JSON (retorna otra promesa)

**¿Por qué verificar `ok`?**
- fetch() NO rechaza en errores HTTP 404, 500, etc.
- Solo rechaza en errores de red
- Debemos verificar manualmente

**Paso 4: Procesar datos GeoJSON**
```javascript
.then(data => {
    departamentosData = data;
    ...
})
```
- `data` es un objeto JavaScript (GeoJSON FeatureCollection)
- Lo guardamos en variable global para búsqueda posterior

**Paso 5: Crear capa GeoJSON de Leaflet**
```javascript
departamentosGeoJSON = L.geoJSON(data, {
    style: featureStyle,
    onEachFeature: onEachFeature
}).addTo(map);
```
- `L.geoJSON()`: Convierte objeto GeoJSON en capa de Leaflet
- `style`: Función que retorna objeto de estilo (crearemos en Paso 3)
- `onEachFeature`: Función para agregar interactividad (crearemos en Paso 5)

**Paso 6: Ajustar vista del mapa**
```javascript
map.fitBounds(departamentosGeoJSON.getBounds());
```
- `getBounds()`: Calcula bounding box de todas las geometrías
- `fitBounds()`: Ajusta zoom y centro para mostrar el área completa

**Paso 7: Agregar a control de capas**
```javascript
layerControl.addOverlay(departamentosGeoJSON, 'Departamentos Interactivos (WFS)');
```
- Agrega la capa al control de capas dinámicamente
- Usuario puede activar/desactivar

**Paso 8: Manejo de errores**
```javascript
.catch(error => {
    console.error('Error cargando WFS:', error);
    alert('No se pudieron cargar los datos...');
});
```
- Se ejecuta si hay error de red, proxy caído, o GeoServer no disponible

---

## 6.4 Flujo Completo de la Petición WFS

Este es el flujo que acabamos de implementar:

```
1. NAVEGADOR
   │ JavaScript ejecuta: loadDepartamentosWFS()
   │ fetch('/api/geoserver-proxy?service=WFS&...')
   ↓

2. PETICIÓN HTTP GET
   │ http://localhost:5000/api/geoserver-proxy?service=WFS&...
   ↓

3. CONTENEDOR WEBAPP (Flask - app.py)
   │ @app.route('/api/geoserver-proxy')
   │ def geoserver_proxy():
   │     service = request.args.get('service')  # 'WFS'
   │     url = 'http://geoserver:8080/geoserver/ne/wfs'
   │     response = requests.get(url, params=params)
   │     return Response(response.content)
   ↓

4. RED DOCKER INTERNA
   │ DNS resuelve 'geoserver' → IP del contenedor geoserver
   ↓

5. CONTENEDOR GEOSERVER
   │ Recibe petición WFS GetFeature
   │ Consulta datastore (PostGIS/Shapefile)
   │ Lee geometrías y atributos
   │ Reproyecta a EPSG:4326
   │ Serializa a GeoJSON
   │ Retorna JSON
   ↓

6. FLASK (proxy)
   │ Recibe GeoJSON de GeoServer
   │ Agrega headers CORS
   │ Retorna al navegador
   ↓

7. NAVEGADOR
   │ fetch() recibe respuesta
   │ .then(response => response.json())
   │ .then(data => {...})
   │     data = { type: "FeatureCollection", features: [...] }
   │ L.geoJSON(data).addTo(map)
   │ Mapa muestra polígonos interactivos ✅
```

**Diferencia clave con WMS:**
- WMS: Solo imágenes (no interactivo)
- WFS: Datos vectoriales (interactivo, con atributos)

---

## 6.5 Paso 3: Función de Estilo de Features

Agrega las funciones de estilo antes de `loadDepartamentosWFS()`:

```javascript
// ============================================
// Estilos de Features
// ============================================

// Estilo normal de las features
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

**Explicación:**

**`featureStyle(feature)`**
- Se llama automáticamente por Leaflet al crear cada feature
- Parámetro `feature`: Objeto GeoJSON de la feature actual
- Retorna objeto con propiedades de estilo

**Propiedades de estilo:**
- `fillColor`: Color de relleno (`'#e8f881'` = amarillo verdoso)
- `weight`: Grosor del borde en píxeles (2px)
- `opacity`: Opacidad del borde (0.8 = 80%)
- `color`: Color del borde (`'#232323'` = gris oscuro)
- `fillOpacity`: Opacidad del relleno (0.4 = 40% transparente)

**`highlightStyle()`**
- Se usa al pasar el mouse sobre una feature
- Borde más grueso (`weight: 4`)
- Color diferente (`#667eea` = violeta)
- Más opaco (`fillOpacity: 0.7`)

**Ejemplo de estilo dinámico (opcional):**
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

---

## 6.6 Paso 4: Manejadores de Eventos

Agrega los manejadores de eventos del mouse:

```javascript
// ============================================
// Manejadores de Eventos
// ============================================

// Resaltar feature al pasar el mouse
function highlightFeature(e) {
    const layer = e.target;

    layer.setStyle(highlightStyle());
    layer.bringToFront();

    // Actualizar panel de información
    if (layer.feature.properties) {
        updateInfoControl(layer.feature.properties);
    }
}

// Resetear highlight al quitar el mouse
function resetHighlight(e) {
    const layer = e.target;

    if (departamentosGeoJSON) {
        departamentosGeoJSON.resetStyle(layer);
    }

    // Resetear panel de información
    updateInfoControl();
}

// Hacer zoom al hacer click
function clickFeature(e) {
    const layer = e.target;
    map.fitBounds(layer.getBounds());
    layer.openPopup();
}
```

**Explicación:**

**`highlightFeature(e)`**
- Se ejecuta cuando el mouse pasa sobre una feature
- Parámetro `e`: Objeto evento con propiedad `target` (la capa)

```javascript
layer.setStyle(highlightStyle());
```
- Cambia el estilo de la capa al estilo de highlight

```javascript
layer.bringToFront();
```
- Mueve la capa al frente (z-index)
- Evita que otras capas la tapen

```javascript
updateInfoControl(layer.feature.properties);
```
- Actualiza control de información con datos de la feature
- Crearemos `updateInfoControl()` en Paso 7

**`resetHighlight(e)`**
- Se ejecuta cuando el mouse sale de una feature

```javascript
departamentosGeoJSON.resetStyle(layer);
```
- Vuelve al estilo original definido en `featureStyle()`

**`clickFeature(e)`**
- Se ejecuta al hacer click en una feature

```javascript
map.fitBounds(layer.getBounds());
```
- Hace zoom a la feature clickeada

```javascript
layer.openPopup();
```
- Abre el popup asociado (lo crearemos en siguiente paso)

---

## 6.7 Paso 5: Función onEachFeature

Agrega la función que configura cada feature individual:

```javascript
// Configurar cada feature
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

**Explicación:**

**`onEachFeature(feature, layer)`**
- Se llama por cada feature al crear la capa GeoJSON
- `feature`: Datos GeoJSON de la feature
- `layer`: Capa Leaflet correspondiente

**Crear popup con template literal:**
```javascript
const popupContent = `
    <div class="popup-title">${props.dpto_cnmbr || 'Sin nombre'}</div>
    ...
`;
```
- `` `...` ``: Template literals (backticks) permiten multi-línea
- `${variable}`: Inserta valor de variable
- `props.dpto_cnmbr || 'Sin nombre'`: Valor por defecto si es null

**Clases CSS usadas:**
- `.popup-title`: Definida en app.css (Módulo 4)
- `.popup-divider`: Línea decorativa
- `.popup-info`: Texto de información

**Asociar popup a la capa:**
```javascript
layer.bindPopup(popupContent);
```
- El popup se muestra al hacer click en la feature

**Agregar eventos:**
```javascript
layer.on({
    mouseover: highlightFeature,
    mouseout: resetHighlight,
    click: clickFeature
});
```
- Asocia los manejadores de eventos creados en Paso 4

---

## 6.8 Paso 6: Control de Información Personalizado

Agrega el control de información que se actualiza al pasar el mouse:

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

**Explicación:**

**Crear control personalizado:**
```javascript
const infoControl = L.control({position: 'topleft'});
```
- `L.control()`: Crea control base
- `position: 'topleft'`: Esquina superior izquierda

**Método `onAdd()`:**
```javascript
infoControl.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info-control');
    this.update();
    return this._div;
};
```
- Se llama cuando el control se agrega al mapa
- `L.DomUtil.create('div', 'info-control')`: Crea `<div class="info-control"></div>`
- Debe retornar elemento DOM del control

**Método `update()`:**
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

**Si `props` existe (usuario pasa mouse sobre departamento):**
```html
<h4>Información del Departamento</h4>
<p class="highlight">Chocó</p>
<p><strong>Código:</strong> 27</p>
```

**Si `props` es null (sin hover):**
```html
<h4>Información del Departamento</h4>
<p>Pasa el cursor sobre un departamento</p>
```

**Función auxiliar:**
```javascript
function updateInfoControl(props) {
    infoControl.update(props);
}
```
- Permite llamar `updateInfoControl()` desde `highlightFeature()`

---

## 6.9 Paso 7: Implementar Búsqueda (Parte 1 - Event Listeners)

Agrega el código de búsqueda. Como es largo, lo dividiremos en dos partes:

```javascript
// ============================================
// Búsqueda de Departamentos
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('search-button');
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    if (searchButton && searchInput) {
        // Búsqueda al hacer clic en el botón
        searchButton.addEventListener('click', performSearch);

        // Búsqueda al presionar Enter
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }

    // Continúa en siguiente paso...
});
```

**Explicación:**

**`document.addEventListener('DOMContentLoaded', ...)`**
- Garantiza que el DOM esté completamente cargado
- Elementos HTML existen antes de intentar accederlos

**Capturar elementos del DOM:**
```javascript
const searchButton = document.getElementById('search-button');
const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
```
- Estos elementos están definidos en index.html (Módulo 3)

**Verificar que existen:**
```javascript
if (searchButton && searchInput) {
    ...
}
```
- Evita errores si los elementos no existen

**Eventos de búsqueda:**
```javascript
searchButton.addEventListener('click', performSearch);

searchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        performSearch();
    }
});
```
- Dos formas de activar búsqueda: click en botón o Enter en input

---

## 6.10 Paso 8: Implementar Búsqueda (Parte 2 - Funciones)

Dentro del mismo `DOMContentLoaded`, después del código anterior, agrega las funciones de búsqueda:

```javascript
    // Función de búsqueda
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

    // Función para hacer zoom a un departamento
    function zoomToDepartamento(codigo) {
        if (!departamentosGeoJSON) return;

        departamentosGeoJSON.eachLayer(function(layer) {
            if (layer.feature.properties.dpto_ccdgo === codigo) {
                map.fitBounds(layer.getBounds());
                layer.openPopup();

                // Highlight temporal (2 segundos)
                layer.setStyle(highlightStyle());
                setTimeout(() => {
                    departamentosGeoJSON.resetStyle(layer);
                }, 2000);
            }
        });
    }
```

**Explicación:**

**Función `performSearch()`:**

**1. Obtener término de búsqueda:**
```javascript
const searchTerm = searchInput.value.trim().toLowerCase();
```
- `.value`: Texto del input
- `.trim()`: Elimina espacios al inicio/final
- `.toLowerCase()`: Convierte a minúsculas (búsqueda insensible a mayúsculas)

**2. Validar entrada:**
```javascript
if (!searchTerm) {
    searchResults.innerHTML = '...';
    return;
}
```

**3. Verificar que datos estén cargados:**
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
- `Array.filter()`: Retorna nuevo array con elementos que cumplen condición
- `.includes(searchTerm)`: Búsqueda parcial (no requiere coincidencia exacta)

**Ejemplo:**
```javascript
searchTerm = "cho"
"Chocó".toLowerCase().includes("cho")  → true ✅
"Antioquia".toLowerCase().includes("cho")  → false ❌
```

**5. Construir HTML de resultados:**
```javascript
matches.forEach(feature => {
    html += `
        <div class="search-result-item" data-codigo="${codigo}">
            <strong>${nombre}</strong><br>
            <small>Código: ${codigo}</small>
        </div>
    `;
});
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
- Al hacer click en resultado, hace zoom al departamento

**Función `zoomToDepartamento(codigo)`:**

```javascript
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
```

**`.eachLayer(callback)`:**
- Itera sobre cada capa en el grupo
- Similar a `forEach` pero para capas Leaflet

**Highlight temporal:**
- Aplica highlight con `setStyle(highlightStyle())`
- Después de 2 segundos (2000ms), quita highlight con `resetStyle()`

---

## 6.11 Paso 9: Inicialización

Al final del archivo, agrega el código de inicialización:

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

**Explicación:**

**`window.addEventListener('load', ...)`**
- Se ejecuta cuando TODO está cargado (HTML, CSS, imágenes, scripts)
- Alternativa: `DOMContentLoaded` (solo DOM, más rápido)

**Llamada a `loadDepartamentosWFS()`:**
- Inicia carga automática de datos WFS
- Todo el proceso del Paso 2 comienza aquí

---

## 6.12 Checkpoint: Probar la Aplicación Completa

### Paso 1: Guardar el archivo

Asegúrate de que `webapp/static/js/app.js` está guardado.

### Paso 2: Verificar que el proxy existe en app.py

Tu archivo `app.py` DEBE tener:
```python
@app.route('/api/geoserver-proxy')
def geoserver_proxy():
    ...
```

Si no existe, lo agregaremos en Módulo 7. Por ahora, puedes agregarlo temporalmente o continuar (tendrás error de red).

### Paso 3: Reiniciar el contenedor webapp

```bash
docker-compose restart webapp
```

### Paso 4: Verificar que GeoServer está ejecutándose

```bash
# Ver estado de contenedores
docker-compose ps

# GeoServer debe estar "Up (healthy)"
# Si no:
docker-compose up -d geoserver
```

### Paso 5: Abrir en navegador

Visita: http://localhost:5000/map-dpto

### Paso 6: Verificar resultado esperado

**Mapa base y WMS:**
- Mapa de OSM visible
- Control de capas funcional
- Puedes activar capas WMS (Departamentos, Municipios)

**Carga automática de WFS:**
- Al cargar la página, aparece capa "Departamentos Interactivos (WFS)" en control de capas
- Polígonos amarillos con bordes grises
- Vista ajustada automáticamente a Colombia

**Interactividad:**
- Al pasar mouse sobre departamento:
  - Se resalta (borde violeta más grueso)
  - Control de información (superior izquierda) muestra nombre y código
- Al salir el mouse:
  - Vuelve al estilo normal
  - Control de información muestra texto por defecto
- Al hacer click en departamento:
  - Zoom a ese departamento
  - Popup con nombre y código

**Búsqueda:**
- En sidebar, input de búsqueda funcional
- Buscar "Cho" → encuentra "Chocó"
- Click en resultado → zoom al departamento
- Highlight temporal de 2 segundos

**Consola (F12):**
- Mensaje: "Iniciando aplicación..."
- Mensaje: "Departamentos cargados: 33" (o el número de features)
- Sin errores de JavaScript

### Posibles errores:

**❌ Error: "No se pudieron cargar los datos de departamentos"**
- **Causa:** GeoServer no está ejecutándose o proxy no existe
- **Solución:**
  ```bash
  # Verificar GeoServer
  docker-compose ps geoserver

  # Ver logs
  docker-compose logs geoserver

  # Verificar proxy (Módulo 7)
  ```

**❌ Error: "L is not defined"**
- **Causa:** Leaflet.js no cargó
- **Solución:** Verificar que index.html carga Leaflet.js antes de app.js

**❌ Mapa no aparece (área gris):**
- **Causa:** CSS sin dimensiones
- **Solución:** Verificar app.css tiene `#map { width: 100%; height: 100%; }`

**❌ Click en resultado de búsqueda no hace nada:**
- **Causa:** Error en evento click
- **Solución:** Abrir consola (F12) y buscar errores

---

## 6.13 Verificación: Archivo Completo

Tu archivo `app.js` completo debe tener aproximadamente **370 líneas**.

Estructura completa:
1. Configuración global (~20 líneas)
2. Inicialización del mapa (~15 líneas)
3. Capas base (~30 líneas)
4. Capas WMS (~20 líneas)
5. Control de capas (~15 líneas)
6. Control de escala (~8 líneas)
7. Variables WFS (~5 líneas)
8. Función loadDepartamentosWFS (~30 líneas)
9. Estilos de features (~20 líneas)
10. Manejadores de eventos (~40 líneas)
11. Función onEachFeature (~20 líneas)
12. Control de información (~30 líneas)
13. Búsqueda (~100 líneas)
14. Inicialización (~8 líneas)

---

## 6.14 Comparación WMS vs WFS

Ahora que has implementado ambos, entiende las diferencias:

| Aspecto | WMS | WFS |
|---------|-----|-----|
| **Tipo de dato** | Imágenes (PNG/JPEG) | Datos vectoriales (GeoJSON) |
| **Tamaño** | ~10-50 KB por tile | Variable (depende de features) |
| **Interactividad** | No (solo visualización) | Sí (click, hover, eventos) |
| **Atributos** | No accesibles | Sí accesibles |
| **Edición** | No | Sí (con WFS-T) |
| **Rendimiento** | Muy rápido | Más lento con muchas features |
| **CORS** | No requiere proxy | Requiere proxy |
| **Caché** | Sí | No (datos dinámicos) |
| **Uso ideal** | Capas base, muchas features | Capas interactivas, pocas features |

**En nuestra aplicación:**
- **Departamentos (WFS):** ~33 features → Perfecto para interactividad
- **Municipios (WMS):** ~1100 features → WMS para rendimiento
- Si municipios fueran WFS, la carga sería muy lenta

---

## 6.15 Resumen

Has aprendido:

- Cargar datos WFS a través del proxy con fetch()
- Entender el flujo completo: Cliente → Proxy → GeoServer
- Convertir GeoJSON a capas Leaflet con L.geoJSON()
- Aplicar estilos estáticos y dinámicos
- Agregar interactividad (hover, click, zoom)
- Crear controles personalizados de Leaflet
- Implementar búsqueda en datos vectoriales
- Trabajar con Promesas y asincronía
- Manipular el DOM con JavaScript

### Archivos creados

- `webapp/static/js/app.js` (~370 líneas completas)

### Conceptos clave

| Concepto | Descripción |
|----------|-------------|
| **fetch()** | API moderna para peticiones HTTP |
| **Promesas** | `.then()`, `.catch()` para código asíncrono |
| **L.geoJSON()** | Convierte GeoJSON a capas Leaflet |
| **onEachFeature** | Función para configurar cada feature |
| **Event listeners** | `mouseover`, `mouseout`, `click` |
| **L.control()** | Crear controles personalizados |
| **Template literals** | `` `...${variable}...` `` |
| **Array.filter()** | Filtrar arrays con condición |

### Técnicas JavaScript aprendidas

- **Promesas encadenadas:** `fetch().then().then().catch()`
- **Template literals:** `` `<div>${variable}</div>` ``
- **Operador ternario:** `condicion ? valor1 : valor2`
- **Arrow functions:** `(param) => { ... }`
- **Desestructuración:** No usada (opcional para futuro)
- **Array methods:** `.filter()`, `.forEach()`
- **DOM manipulation:** `innerHTML`, `addEventListener()`
- **Data attributes:** `data-codigo="${codigo}"`
- **setTimeout:** Para efectos temporales

### Próximo módulo

En el **Módulo 7 (Proxy Flask)**, agregarás el código del proxy a `app.py`:
- Endpoint `/api/geoserver-proxy`
- Función `geoserver_proxy()`
- Endpoint `/map-dpto`
- Todo en el entorno dockerizado

---

**[⬅️ Módulo 5: JavaScript Parte 1](05_JAVASCRIPT_PARTE_1.md)** | **[Volver al Índice](README.md)** | **[Siguiente: Módulo 7 - Proxy Flask ➡️](07_PROXY_FLASK.md)**
