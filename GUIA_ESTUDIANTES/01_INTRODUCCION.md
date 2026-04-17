# Módulo 1: Introducción

## Objetivos de Aprendizaje

Al completar este módulo, comprenderás:

- 🎯 Los objetivos generales del proyecto de visor web
- 📖 Los conceptos fundamentales de los estándares OGC (WMS y WFS)
- 🏗️ La arquitectura del sistema completo
- 🔄 El flujo de datos entre componentes
- 📊 Las diferencias entre WMS y WFS y cuándo usar cada uno

---

## 1.1 Descripción del Proyecto

### ¿Qué vamos a construir?

Desarrollaremos un **visor web interactivo** de datos geográficos de Colombia (departamentos y municipios) que:

- Muestra capas geográficas usando servicios WMS de GeoServer
- Permite interactividad (click, hover) usando servicios WFS
- Proporciona funcionalidad de búsqueda y filtrado
- Despliega información detallada de features
- Ofrece controles de capas y herramientas de navegación

### Características principales

| Característica | Tecnología | Propósito |
|----------------|------------|-----------|
| Mapa interactivo | Leaflet.js | Renderizado y navegación del mapa |
| Capas base | Tile layers (OSM, Esri) | Contexto geográfico |
| Departamentos (imagen) | WMS - GeoServer | Visualización rápida no interactiva |
| Municipios (imagen) | WMS - GeoServer | Capa base adicional |
| Departamentos (vectorial) | WFS - GeoServer | Interactividad y consultas |
| Backend/Proxy | Flask (Python) | Resolver CORS y servir la aplicación |
| Estilos | CSS3 + Flexbox | Diseño responsive |

---

## 1.2 Conceptos Fundamentales OGC

### ¿Qué es OGC?

**OGC (Open Geospatial Consortium)** es una organización internacional que desarrolla estándares abiertos para datos geoespaciales.

Los estándares OGC permiten que diferentes sistemas y aplicaciones compartan datos geográficos de manera interoperable.

### Estándares que usaremos

En este proyecto utilizamos dos estándares OGC:

1. **WMS** (Web Map Service)
2. **WFS** (Web Feature Service)

---

## 1.3 WMS (Web Map Service)

### Definición

WMS es un **estándar OGC** para servir mapas georeferenciados como **imágenes** (PNG, JPEG, etc.) a través de HTTP.

### ¿Cómo funciona?

```
Cliente (Navegador)                    Servidor (GeoServer)
       │                                        │
       │  Petición WMS GetMap                   │
       │  (layers, bbox, width, height, srs)    │
       ├───────────────────────────────────────>│
       │                                        │
       │                                   [Renderiza]
       │                                   [los datos]
       │                                   [como imagen]
       │                                        │
       │  Respuesta: imagen PNG/JPEG            │
       │<───────────────────────────────────────┤
       │                                        │
```

### Operaciones principales de WMS

#### 1. GetCapabilities
Obtiene información sobre las capas disponibles, sistemas de coordenadas soportados, formatos, etc.

```http
GET http://localhost:8080/geoserver/ne/wms?
    service=WMS&
    version=1.3.0&
    request=GetCapabilities
```

**Respuesta:** Documento XML con metadatos del servicio

#### 2. GetMap
Obtiene una imagen de una porción específica del mapa.

```http
GET http://localhost:8080/geoserver/ne/wms?
    service=WMS&
    version=1.3.0&
    request=GetMap&
    layers=ne:dpto_choco&
    bbox=-79.0,1.0,-74.0,6.0&
    width=800&
    height=600&
    srs=EPSG:4326&
    format=image/png&
    transparent=true
```

**Respuesta:** Imagen PNG

#### 3. GetFeatureInfo (Opcional)
Obtiene información de atributos de un punto específico del mapa.

### Parámetros principales de GetMap

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `service` | Tipo de servicio | `WMS` |
| `version` | Versión del protocolo | `1.3.0` o `1.1.1` |
| `request` | Operación solicitada | `GetMap` |
| `layers` | Capas a mostrar (workspace:layer) | `ne:dpto_choco` |
| `bbox` | Bounding box (minx,miny,maxx,maxy) | `-79,1,-74,6` |
| `width` | Ancho de imagen en píxeles | `800` |
| `height` | Alto de imagen en píxeles | `600` |
| `srs` o `crs` | Sistema de referencia espacial | `EPSG:4326` |
| `format` | Formato de imagen | `image/png` |
| `transparent` | Fondo transparente | `true` |
| `styles` | Estilo a aplicar | `polygon` o vacío |

### Ventajas de WMS

- **Rendimiento:** Rápido incluso con millones de features
- **Escalabilidad:** El servidor hace el trabajo pesado
- **Simplicidad:** Solo imágenes, fácil de implementar
- **Compatible:** Funciona en cualquier navegador

### Desventajas de WMS

- **No interactivo:** No se puede hacer click en features
- **Sin atributos:** No se accede a propiedades de features
- **Solo visualización:** No editable
- **Dependiente de red:** Requiere peticiones constantes

### Cuándo usar WMS

- Capas con **muchas features** (>1000)
- Cuando solo se necesita **visualización**
- Capas base o de contexto
- Datos raster (imágenes satelitales, modelos de elevación)

---

## 1.4 WFS (Web Feature Service)

### Definición

WFS es un **estándar OGC** para servir **features vectoriales** (geometrías + atributos) en formatos como GeoJSON, GML, etc.

### ¿Cómo funciona?

```
Cliente (Navegador)                    Servidor (GeoServer)
       │                                        │
       │  Petición WFS GetFeature               │
       │  (typeName, outputFormat)              │
       ├───────────────────────────────────────>│
       │                                        │
       │                                   [Consulta]
       │                                   [base de datos]
       │                                   [serializa]
       │                                        │
       │  Respuesta: GeoJSON con geometrías     │
       │  y atributos completos                 │
       │<───────────────────────────────────────┤
       │                                        │
```

### Operaciones principales de WFS

#### 1. GetCapabilities
Obtiene información sobre las capas (feature types) disponibles.

```http
GET http://localhost:8080/geoserver/ne/wfs?
    service=WFS&
    version=2.0.0&
    request=GetCapabilities
```

#### 2. GetFeature
Obtiene features (geometrías + atributos).

```http
GET http://localhost:8080/geoserver/ne/wfs?
    service=WFS&
    version=2.0.0&
    request=GetFeature&
    typeName=ne:departamentos&
    outputFormat=application/json
```

**Respuesta:** GeoJSON

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "id": "departamentos.1",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[-77.5, 2.3], ...]]
      },
      "properties": {
        "dpto_ccdgo": "27",
        "dpto_cnmbr": "Chocó"
      }
    }
  ]
}
```

#### 3. DescribeFeatureType
Describe la estructura de atributos de una capa.

#### 4. Transaction (WFS-T)
Permite editar datos (Insert, Update, Delete).

### Parámetros principales de GetFeature

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `service` | Tipo de servicio | `WFS` |
| `version` | Versión del protocolo | `2.0.0` |
| `request` | Operación solicitada | `GetFeature` |
| `typeName` | Feature type (workspace:layer) | `ne:departamentos` |
| `outputFormat` | Formato de salida | `application/json` |
| `maxFeatures` o `count` | Límite de features | `100` |
| `srsName` | Sistema de coordenadas | `EPSG:4326` |
| `propertyName` | Atributos específicos a retornar | `dpto_cnmbr,dpto_ccdgo` |
| `bbox` | Filtro espacial por bounding box | `minx,miny,maxx,maxy` |
| `cql_filter` | Filtro por atributos (CQL) | `dpto_ccdgo='27'` |

### Ventajas de WFS

- **Interactivo:** Permite click, hover, selección
- **Acceso a atributos:** Toda la información disponible
- **Filtrado:** Consultas espaciales y por atributos
- **Análisis:** Procesamiento en el cliente
- **Edición:** Soporta WFS-T para editar datos

### Desventajas de WFS

- **Rendimiento:** Lento con muchas features
- **Transferencia de datos:** Mayor uso de ancho de banda
- **CORS:** Requiere configuración especial o proxy
- **Complejidad:** Más difícil de implementar

### Cuándo usar WFS

- Capas con **pocas features** (<1000)
- Cuando se necesita **interactividad**
- Acceso a **atributos** de features
- **Consultas y filtros** espaciales o por atributos
- **Edición** de datos (WFS-T)

---

## 1.5 WMS vs WFS: Comparación

| Aspecto | WMS | WFS |
|---------|-----|-----|
| **Tipo de datos** | Imágenes (raster) | Features vectoriales |
| **Formato** | PNG, JPEG | GeoJSON, GML, CSV |
| **Tamaño típico** | ~50-200 KB por tile | ~100 KB - 10 MB |
| **Interactividad** | - No |  Sí |
| **Atributos** | - No accesibles |  Totalmente accesibles |
| **Rendimiento** |  Rápido |  Depende de cantidad |
| **Escalabilidad** |  Excelente |  Limitada |
| **CORS** |  No es problema | - Requiere proxy |
| **Edición** | - No |  Con WFS-T |
| **Uso típico** | Capas base, contexto | Capas interactivas |

### Estrategia híbrida (recomendada)

En nuestro proyecto usamos **ambos estándares**:

```javascript
// WMS para visualización rápida (imagen)
const departamentosWMS = L.tileLayer.wms(url, {
    layers: 'ne:dpto_choco'
});

// WFS para interactividad (vectorial)
const departamentosWFS = L.geoJSON(geoJsonData, {
    onEachFeature: (feature, layer) => {
        layer.on('click', () => {
            alert(feature.properties.dpto_cnmbr);
        });
    }
});
```

**Beneficios:**
- WMS: Rápido, muestra todas las capas
- WFS: Interactividad solo donde se necesita
- Usuario puede activar/desactivar según necesidad

---

## 1.6 Arquitectura del Sistema

### Diagrama de componentes

```
┌─────────────────────────────────────────────────────┐
│              NAVEGADOR (Cliente)                    │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │          HTML (index.html)                  │   │
│  │  - Estructura de la página                  │   │
│  │  - Div contenedor del mapa                  │   │
│  │  - Panel lateral (sidebar)                  │   │
│  └─────────────────────────────────────────────┘   │
│                     │                               │
│  ┌─────────────────────────────────────────────┐   │
│  │          CSS (app.css)                      │   │
│  │  - Estilos y layout                         │   │
│  │  - Diseño responsive                        │   │
│  │  - Personalización de Leaflet               │   │
│  └─────────────────────────────────────────────┘   │
│                     │                               │
│  ┌─────────────────────────────────────────────┐   │
│  │     JavaScript (app.js + Leaflet.js)        │   │
│  │  - Inicialización del mapa                  │   │
│  │  - Carga de capas WMS/WFS                   │   │
│  │  - Interactividad (eventos)                 │   │
│  │  - Búsqueda y filtros                       │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└──────────────┬──────────────────────────────────────┘
               │ HTTP Requests
               │
               │ 1. Peticiones a Flask (mismo origen)
               │    - Archivos estáticos (HTML, CSS, JS)
               │    - Proxy WFS: /api/geoserver-proxy
               │
               ↓
┌─────────────────────────────────────────────────────┐
│         SERVIDOR FLASK (Backend/Proxy)              │
│                   localhost:5000                    │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │          app.py (Python)                    │   │
│  │                                             │   │
│  │  Rutas:                                     │   │
│  │  - /map-dpto → Sirve index.html            │   │
│  │  - /api/geoserver-proxy → Proxy CORS       │   │
│  │                                             │   │
│  │  Funcionalidad del proxy:                  │   │
│  │  1. Recibe petición del navegador          │   │
│  │  2. Detecta servicio (WFS/WMS)             │   │
│  │  3. Reenvía a GeoServer                    │   │
│  │  4. Retorna respuesta al navegador         │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└──────────────┬──────────────────────────────────────┘
               │ HTTP Requests
               │
               │ 2. Peticiones directas (WMS)
               │    - Imágenes de tiles
               │    - No hay problema de CORS
               │
               │ 3. Peticiones vía proxy (WFS)
               │    - Datos GeoJSON
               │    - Evita problema de CORS
               │
               ↓
┌─────────────────────────────────────────────────────┐
│           GEOSERVER (Servidor OGC)                  │
│                localhost:8080                       │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │       Servicios OGC                         │   │
│  │                                             │   │
│  │  WMS: /geoserver/ne/wms                     │   │
│  │  - ne:dpto_choco → Imágenes PNG             │   │
│  │  - ne:mpios_choco → Imágenes PNG            │   │
│  │                                             │   │
│  │  WFS: /geoserver/ne/wfs                     │   │
│  │  - ne:departamentos → GeoJSON               │   │
│  │                                             │   │
│  └─────────────────────────────────────────────┘   │
│                     │                               │
│  ┌─────────────────────────────────────────────┐   │
│  │       Almacenamiento de Datos               │   │
│  │  - Shapefiles                               │   │
│  │  - PostgreSQL/PostGIS                       │   │
│  │  - GeoPackage                               │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Flujo de datos: Carga WMS (Departamentos como imagen)

```
1. JavaScript ejecuta:
   const departamentosWMS = L.tileLayer.wms(
       'http://localhost:8080/geoserver/ne/wms',
       { layers: 'ne:dpto_choco' }
   );
   departamentosWMS.addTo(map);

2. Leaflet divide el mapa en tiles (256x256 px)

3. Para cada tile visible, Leaflet hace petición DIRECTA a GeoServer:
   GET http://localhost:8080/geoserver/ne/wms?
       service=WMS&
       request=GetMap&
       layers=ne:dpto_choco&
       bbox=-77.5,4.0,-76.5,5.0&
       width=256&
       height=256&
       srs=EPSG:3857&
       format=image/png&
       transparent=true

4. GeoServer:
   - Consulta los datos de la capa
   - Renderiza la porción solicitada
   - Retorna imagen PNG

5. Navegador recibe imágenes y Leaflet las ensambla en el mapa

NOTA: No hay problema de CORS porque son imágenes
```

### Flujo de datos: Carga WFS (Departamentos interactivos)

```
1. JavaScript ejecuta:
   const wfsUrl = '/api/geoserver-proxy?service=WFS&...';
   fetch(wfsUrl)
       .then(response => response.json())
       .then(data => {
           L.geoJSON(data).addTo(map);
       });

2. Navegador hace petición a Flask (mismo origen, no CORS):
   GET http://localhost:5000/api/geoserver-proxy?
       service=WFS&
       version=2.0.0&
       request=GetFeature&
       typeName=ne:departamentos&
       outputFormat=application/json

3. Flask (app.py, función geoserver_proxy):
   - Recibe la petición
   - Extrae parámetros
   - Construye URL a GeoServer:
     http://geoserver:8080/geoserver/ne/wfs?service=WFS&...
   - Hace petición con requests.get()

4. GeoServer:
   - Consulta base de datos o shapefiles
   - Serializa a GeoJSON
   - Retorna JSON

5. Flask:
   - Recibe respuesta de GeoServer
   - Retorna al navegador sin modificar

6. JavaScript:
   - Recibe GeoJSON
   - Crea capa Leaflet con L.geoJSON()
   - Agrega interactividad (click, hover)
   - Agrega al mapa

NOTA: El proxy resuelve CORS porque Flask y GeoServer
      se comunican servidor-a-servidor
```

---

## 1.7 Problema de CORS y su Solución

### ¿Qué es CORS?

**CORS (Cross-Origin Resource Sharing)** es una política de seguridad de los navegadores que bloquea peticiones JavaScript a orígenes diferentes.

### Orígenes

Un **origen** se define por:
- Protocolo (http/https)
- Dominio (localhost, example.com)
- Puerto (5000, 8080)

**Ejemplos:**

| URL | Origen |
|-----|--------|
| `http://localhost:5000` | `http://localhost:5000` |
| `http://localhost:8080` | `http://localhost:8080` |
| `http://localhost:5000/api/datos` | `http://localhost:5000` |

### El problema en nuestro proyecto

```
Aplicación Flask:  http://localhost:5000  (Origen A)
GeoServer:         http://localhost:8080  (Origen B)

Si JavaScript desde Origen A intenta fetch() a Origen B
→ ¡BLOQUEADO POR CORS! -
```

**Error típico en consola:**
```
Access to fetch at 'http://localhost:8080/geoserver/ne/wfs'
from origin 'http://localhost:5000' has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present.
```

### ¿Por qué WMS no tiene este problema?

Las imágenes (`<img>`, tiles de mapas) están **exentas de CORS**.

```javascript
// Esto funciona sin problema:
L.tileLayer.wms('http://localhost:8080/geoserver/ne/wms', ...)
```

Internamente, Leaflet crea elementos `<img>` con `src=` apuntando a GeoServer.

### ¿Por qué WFS sí tiene problema de CORS?

Peticiones `fetch()` para JSON están sujetas a CORS.

```javascript
// Esto SÍ genera error CORS:
fetch('http://localhost:8080/geoserver/ne/wfs?service=WFS&...')
```

### Solución: Proxy en Flask

En lugar de petición directa:

```
Navegador → GeoServer  - (CORS)
```

Usamos proxy:

```
Navegador → Flask → GeoServer   (Sin CORS)
```

**Petición desde JavaScript:**
```javascript
// Petición al MISMO origen (Flask)
fetch('/api/geoserver-proxy?service=WFS&...')
```

**Proxy en Flask (app.py):**
```python
@app.route('/api/geoserver-proxy')
def geoserver_proxy():
    # Reenviar petición a GeoServer
    response = requests.get('http://geoserver:8080/geoserver/ne/wfs', ...)
    return Response(response.content)
```

Servidor-a-servidor **no tiene restricciones CORS**.

---

## 1.8 Resumen

### Conceptos clave aprendidos

- **WMS:** Servicio de mapas como imágenes
- **WFS:** Servicio de features vectoriales
- **Diferencias:** WMS es rápido pero no interactivo; WFS es interactivo pero más lento
- **Estrategia híbrida:** Usar ambos según necesidad
- **Arquitectura:** Cliente (Leaflet) → Flask (Proxy) → GeoServer → Datos
- **CORS:** Problema de seguridad resuelto con proxy Flask

### Preparación para próximo módulo

En el **Módulo 2 (Prerequisitos)**, verificaremos que tienes todo el software instalado y los conocimientos necesarios para comenzar la implementación.

---

**[⬅️ Volver al Índice](README.md)** | **[Siguiente: Módulo 2 - Prerequisitos ➡️](02_PREREQUISITOS.md)**
