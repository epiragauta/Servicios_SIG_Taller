# Módulo 3: Estructura HTML

## Objetivos de Aprendizaje

Al completar este módulo, comprenderás:

- 🎯 La estructura completa del archivo `index.html`
- 📖 El propósito de cada sección del documento
- 🔗 Cómo se enlazan las dependencias externas (Leaflet)
- 🎨 La integración con templates Jinja2 de Flask
- 🗺️ Dónde se renderiza el mapa y los controles

---

## 3.1 Visión General

El archivo `webapp/templates/app/index.html` contiene 82 líneas de HTML que definen:

1. **Metadatos** y configuración del documento
2. **Enlaces a CSS** (Leaflet y estilos personalizados)
3. **Estructura de la página** (header, sidebar, mapa, footer)
4. **Enlaces a JavaScript** (Leaflet y aplicación)

**Ubicación del archivo:**
```
webapp/templates/app/index.html
```

---

## 3.2 Análisis Línea por Línea

### Sección 1: DOCTYPE y HTML (Líneas 1-2)

```html
<!DOCTYPE html>
<html lang="es">
```

**Explicación:**

- **`<!DOCTYPE html>`**: Declaración HTML5
  - Indica al navegador que use el estándar HTML5
  - Debe ser siempre la primera línea del documento
  - No es case-sensitive pero por convención se escribe en mayúsculas

- **`<html lang="es">`**: Elemento raíz del documento
  - `lang="es"`: Define idioma español
  - **Beneficios:**
    - Mejora accesibilidad (lectores de pantalla)
    - Mejora SEO (motores de búsqueda)
    - Ayuda a navegadores con corrección ortográfica

---

### Sección 2: HEAD - Metadatos (Líneas 3-8)

```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Visualización interactiva de departamentos y municipios de Colombia usando servicios WMS y WFS de GeoServer">
    <meta name="author" content="Curso de Servicios Web Geográficos">
    <title>Colombia - Departamentos y Municipios | Servicios Web Geográficos</title>
```

**Análisis de cada meta tag:**

#### `<meta charset="UTF-8">`

**Propósito:** Define codificación de caracteres

**¿Por qué UTF-8?**
- Soporta todos los caracteres (español, símbolos, emojis)
- Estándar web universal
- Evita problemas con acentos y ñ

**Sin UTF-8:**
```
"División" → "DivisiÃ³n"  
```

**Con UTF-8:**
```
"División" → "División"  ✅
```

#### `<meta name="viewport" ...>`

**Propósito:** Controla visualización en dispositivos móviles

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**Parámetros:**
- `width=device-width`: Ancho = ancho del dispositivo
- `initial-scale=1.0`: Zoom inicial al 100%

**Importancia:**
- **Sin viewport:** El navegador móvil asume ancho de 980px y hace zoom out
- **Con viewport:** Se adapta al ancho real del dispositivo

**Ejemplo visual:**

```
Sin viewport (móvil):
┌────────────────────────────────┐
│  [Página muy pequeña]          │  ← Zoom out automático
│                                │
└────────────────────────────────┘

Con viewport (móvil):
┌────────────────┐
│  [Página       │
│   adaptada]    │  ← Tamaño legible
│                │
└────────────────┘
```

#### `<meta name="description" ...>`

**Propósito:** Descripción para motores de búsqueda

```html
<meta name="description" content="Visualización interactiva de departamentos y municipios de Colombia usando servicios WMS y WFS de GeoServer">
```

**Uso:**
- Aparece en resultados de búsqueda de Google
- Mejora SEO
- Longitud recomendada: 150-160 caracteres

#### `<meta name="author" ...>`

**Propósito:** Identificar autor del documento

```html
<meta name="author" content="Curso de Servicios Web Geográficos">
```

**Uso:**
- Documentación y atribución
- No afecta SEO directamente

#### `<title>`

**Propósito:** Título de la pestaña del navegador

```html
<title>Colombia - Departamentos y Municipios | Servicios Web Geográficos</title>
```

**Importancia:**
- Aparece en pestaña del navegador
- En favoritos/bookmarks
- En resultados de búsqueda (SEO)
- Longitud recomendada: 50-60 caracteres

**Buenas prácticas:**
```
"Colombia - Departamentos | Servicios Web"
 "Página 1"  (muy genérico)
 "Visualización interactiva avanzada de datos geoespaciales..." (muy largo)
```

---

### Sección 3: HEAD - Enlaces CSS (Líneas 10-16)

```html
    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
        crossorigin=""/>

    <!-- Estilos personalizados -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/app.css') }}">
</head>
```

#### Leaflet CSS desde CDN

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
    crossorigin=""/>
```

**Desglose:**

**1. `rel="stylesheet"`**
- Indica que es una hoja de estilos CSS

**2. `href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"`**
- URL del CDN (Content Delivery Network)
- `unpkg.com`: CDN popular para paquetes npm
- `@1.9.4`: Versión específica (importante para estabilidad)
- `dist/leaflet.css`: Archivo de distribución (minificado)

**3. `integrity="sha256-..."`**
- **SRI (Subresource Integrity)**: Hash criptográfico del archivo
- **Propósito:** Seguridad
- Verifica que el archivo no ha sido modificado/comprometido
- Si el hash no coincide, el navegador NO carga el archivo

**¿Cómo funciona SRI?**
```
Navegador descarga archivo → Calcula hash → Compara con integrity
                                                 │
                                          ┌──────┴──────┐
                                          │             │
                                        Coincide     No coincide
                                          │             │
                                       Carga       Bloquea 
```

**4. `crossorigin=""`**
- Habilita CORS para el recurso
- Necesario cuando se usa `integrity`
- Valor vacío equivale a `anonymous` (sin credenciales)

**Beneficios del CDN:**
- **Velocidad:** Servidores globales cercanos al usuario
- **Caché:** Probablemente ya está en caché del navegador
- **Mantenimiento:** No hay que hospedar el archivo

**Desventajas del CDN:**
-  **Dependencia externa:** Requiere conexión a internet
-  **Disponibilidad:** Si el CDN cae, la app no funciona completamente

**Alternativa local:**
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/leaflet.css') }}">
```

#### Estilos personalizados con Jinja2

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/app.css') }}">
```

**Explicación:**

**1. Templates Jinja2**
- Flask usa Jinja2 para templates dinámicos
- `{{ ... }}`: Expresión que se evalúa en el servidor

**2. `url_for('static', filename='css/app.css')`**
- Función de Flask para generar URLs
- `'static'`: Endpoint del directorio static de Flask
- `filename='css/app.css'`: Ruta relativa dentro de static/

**Renderizado en el servidor:**

Template (lo que escribimos):
```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/app.css') }}">
```

HTML enviado al navegador:
```html
<link rel="stylesheet" href="/static/css/app.css">
```

**Ventajas de `url_for()`:**
- **Mantenibilidad:** Si cambias la estructura de URLs, no hay que modificar templates
- **Portabilidad:** Funciona en cualquier ruta de despliegue
- **Claridad:** Código más legible

**Orden de carga de CSS:**
```
1. Leaflet CSS (base de Leaflet)
2. app.css (nuestros estilos personalizados)
```

> **IMPORTANTE:** Los estilos se aplican en orden. `app.css` puede sobrescribir estilos de Leaflet si es necesario.

---

### Sección 4: BODY - Header (Líneas 18-25)

```html
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-content">
            <h1>🗺️ Colombia - División Administrativa</h1>
            <p>Visualización de Departamentos y Municipios mediante Servicios Web Geográficos (WMS/WFS)</p>
        </div>
    </header>
```

**Análisis:**

#### Elemento semántico `<header>`

```html
<header class="header">
```

**¿Qué es un elemento semántico?**
- Elementos HTML5 que describen su contenido/propósito
- Mejoran accesibilidad y SEO
- Alternativos a `<div>` genéricos

**Elementos semánticos comunes:**
```html
<header>   → Encabezado de página o sección
<nav>      → Navegación
<main>     → Contenido principal
<aside>    → Contenido lateral
<footer>   → Pie de página
<article>  → Artículo independiente
<section>  → Sección temática
```

**Ventajas de usar `<header>` en lugar de `<div class="header">`:**
- Lectores de pantalla lo identifican como encabezado
- Buscadores entienden la estructura del documento
- Código más legible para desarrolladores

#### Emoji en el título

```html
<h1>🗺️ Colombia - División Administrativa</h1>
```

**Nota sobre emojis:**
- Funcionan gracias a `charset="UTF-8"`
- Mejoran UX (interfaz más amigable)
- **Precaución:** No abusar, pueden afectar accesibilidad
- Alternativa con accesibilidad:
  ```html
  <h1>
      <span role="img" aria-label="Mapa">🗺️</span>
      Colombia - División Administrativa
  </h1>
  ```

---

### Sección 5: BODY - Contenedor Principal (Líneas 27-28)

```html
    <!-- Contenedor principal -->
    <div class="main-container">
```

**Propósito:**
- Contenedor para el layout de dos columnas
- En CSS (app.css) se define como `display: flex`

**Estructura del layout:**
```
┌─────────────────────────────────────────┐
│           HEADER                        │
├──────────┬──────────────────────────────┤
│ SIDEBAR  │                              │
│          │       MAP CONTAINER          │
│ (320px)  │         (flex: 1)            │
│          │                              │
├──────────┴──────────────────────────────┤
│           FOOTER                        │
└─────────────────────────────────────────┘
```

**En CSS:**
```css
.main-container {
    display: flex;           /* Layout horizontal */
    height: calc(100vh - 140px);  /* Altura dinámica */
}
```

---

### Sección 6: BODY - Sidebar (Líneas 29-61)

```html
        <!-- Panel lateral -->
        <aside class="sidebar">
            <div class="sidebar-section">
                <h2>📊 Información</h2>
                <div id="info-panel">
                    <p><strong>Capas disponibles:</strong></p>
                    <ul>
                        <li>Departamentos (33)</li>
                        <li>Municipios (~1100)</li>
                    </ul>
                    <p class="info-text">
                        Haz clic en el mapa para ver información detallada de cada departamento.
                    </p>
                </div>
            </div>

            <div class="sidebar-section">
                <h2>🔍 Búsqueda</h2>
                <input type="text" id="search-input" placeholder="Buscar departamento..." class="search-input">
                <button id="search-button" class="btn-primary">Buscar</button>
                <div id="search-results"></div>
            </div>

            <div class="sidebar-section">
                <h2>ℹ️ Acerca de</h2>
                <p class="small-text">
                    <strong>Fuente de datos:</strong> Instituto Geográfico Agustín Codazzi (IGAC)<br>
                    <strong>Servidor:</strong> GeoServer<br>
                    <strong>Estándares:</strong> OGC WMS, WFS<br>
                    <strong>Biblioteca:</strong> Leaflet.js
                </p>
            </div>
        </aside>
```

#### Elemento `<aside>`

```html
<aside class="sidebar">
```

**Propósito semántico:**
- Contenido tangencialmente relacionado con el contenido principal
- Ideal para sidebars, widgets, información adicional

#### Sección de Información

```html
<div class="sidebar-section">
    <h2>📊 Información</h2>
    <div id="info-panel">
        ...
    </div>
</div>
```

**Elementos clave:**

**1. `id="info-panel"`**
- Identificador único
- JavaScript puede actualizar dinámicamente este div
- En app.js (línea 237):
  ```javascript
  function updateInfoControl(props) {
      infoControl.update(props);
  }
  ```

**2. Lista de capas**
```html
<ul>
    <li>Departamentos (33)</li>
    <li>Municipios (~1100)</li>
</ul>
```
- Información estática
- Podría hacerse dinámica consultando GeoServer GetCapabilities

#### Sección de Búsqueda

```html
<div class="sidebar-section">
    <h2>🔍 Búsqueda</h2>
    <input type="text" id="search-input" placeholder="Buscar departamento..." class="search-input">
    <button id="search-button" class="btn-primary">Buscar</button>
    <div id="search-results"></div>
</div>
```

**Elementos clave:**

**1. Input de búsqueda**
```html
<input type="text" id="search-input" placeholder="Buscar departamento..." class="search-input">
```

- `type="text"`: Campo de texto simple
- `id="search-input"`: JavaScript lo captura (app.js línea 257)
- `placeholder`: Texto de ayuda que desaparece al escribir
- `class="search-input"`: Estilos CSS aplicados

**2. Botón de búsqueda**
```html
<button id="search-button" class="btn-primary">Buscar</button>
```

- `id="search-button"`: JavaScript detecta clicks (app.js línea 262)
- `class="btn-primary"`: Estilos del botón (gradiente, hover)

**3. Contenedor de resultados**
```html
<div id="search-results"></div>
```

- **Inicialmente vacío**
- JavaScript inserta resultados dinámicamente (app.js línea 309)
- Ejemplo de contenido generado:
  ```html
  <div class="search-result-item" data-codigo="27">
      <strong>Chocó</strong><br>
      <small>Código: 27</small>
  </div>
  ```

**Flujo de búsqueda:**
```
Usuario escribe "Chocó" y hace click en "Buscar"
    ↓
JavaScript captura el evento (app.js)
    ↓
Filtra departamentosData en el cliente
    ↓
Genera HTML con resultados
    ↓
Inserta HTML en #search-results
    ↓
Usuario hace click en resultado
    ↓
Zoom a ese departamento
```

#### Sección "Acerca de"

```html
<div class="sidebar-section">
    <h2>ℹ️ Acerca de</h2>
    <p class="small-text">
        <strong>Fuente de datos:</strong> Instituto Geográfico Agustín Codazzi (IGAC)<br>
        <strong>Servidor:</strong> GeoServer<br>
        <strong>Estándares:</strong> OGC WMS, WFS<br>
        <strong>Biblioteca:</strong> Leaflet.js
    </p>
</div>
```

**Propósito:**
- Documentar tecnologías usadas
- Atribución de datos (importante legal y éticamente)
- Información educativa para usuarios

---

### Sección 7: BODY - Contenedor del Mapa (Líneas 63-66)

```html
        <!-- Mapa -->
        <main class="map-container">
            <div id="map"></div>
        </main>
    </div>
```

**Análisis:**

#### Elemento `<main>`

```html
<main class="map-container">
```

**Propósito semántico:**
- Contenido principal de la página
- Debe ser único en el documento
- Mejora accesibilidad (lectores de pantalla saltan directamente aquí)

#### El div del mapa

```html
<div id="map"></div>
```

**Este es el elemento MÁS IMPORTANTE para Leaflet:**

**¿Qué pasa con este div?**

1. **En HTML:** Es un div vacío
2. **En CSS (app.css línea 153-156):**
   ```css
   #map {
       width: 100%;
       height: 100%;
   }
   ```
   - Ocupa todo el espacio del contenedor padre

3. **En JavaScript (app.js línea 27):**
   ```javascript
   const map = L.map('map', {
       center: [4.5709, -74.2973],
       zoom: 6
   });
   ```
   - Leaflet **busca** el elemento con `id="map"`
   - **Transforma** el div en un mapa interactivo
   - Inserta tiles, controles, capas, etc.

**Resultado final en el DOM (después de Leaflet):**
```html
<div id="map" class="leaflet-container">
    <div class="leaflet-pane leaflet-map-pane">
        <div class="leaflet-pane leaflet-tile-pane">
            <!-- Tiles del mapa -->
        </div>
        <div class="leaflet-pane leaflet-overlay-pane">
            <!-- Capas vectoriales -->
        </div>
        <!-- ... más elementos generados por Leaflet -->
    </div>
</div>
```

**Errores comunes:**

 **Olvidar el `id`:**
```html
<div class="map"></div>  
```
```javascript
L.map('map')  // ← No encuentra el elemento: Error!
```

 **Dimensiones no definidas:**
```html
<div id="map"></div>  <!-- Sin CSS de dimensiones -->
```
Resultado: Mapa de 0px x 0px (invisible)

**Correcto:**
```html
<div id="map"></div>
```
```css
#map { width: 100%; height: 100%; }
```

---

### Sección 8: BODY - Footer (Líneas 69-72)

```html
    <!-- Footer -->
    <footer class="footer">
        <p>&copy; 2024 Curso de Servicios Web Geográficos | Desarrollado con Leaflet.js y GeoServer</p>
    </footer>
```

**Análisis:**

#### Elemento `<footer>`

```html
<footer class="footer">
```

- Elemento semántico para pie de página
- Típicamente contiene: copyright, enlaces, información de contacto

#### Símbolo de copyright

```html
&copy;
```

- **Entidad HTML** para el símbolo ©
- Alternativas:
  - `©` (requiere UTF-8)
  - `&#169;` (código numérico)
  - `&copy;` (nombre de entidad, más legible) ✅

---

### Sección 9: BODY - Scripts JavaScript (Líneas 74-81)

```html
    <!-- Leaflet JavaScript -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
        crossorigin=""></script>

    <!-- Aplicación -->
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
```

**Análisis:**

#### Ubicación de los scripts

**¿Por qué los scripts van al FINAL del `<body>`?**

 **Scripts en `<head>`:**
```html
<head>
    <script src="app.js"></script>  
</head>
<body>
    <div id="map"></div>
</body>
```

**Problema:**
1. Navegador encuentra `<script>`, lo descarga y ejecuta
2. app.js intenta acceder a `<div id="map">`
3. **Error:** El div aún no existe en el DOM

**Scripts al final de `<body>`:**
```html
<body>
    <div id="map"></div>
    <script src="app.js"></script>  ✅
</body>
```

**Ventajas:**
1. Todo el HTML ya está parseado
2. Elementos del DOM están disponibles
3. Página se renderiza más rápido (mejor UX)

**Alternativa moderna (si scripts estuvieran en `<head>`):**
```html
<script defer src="app.js"></script>
```
- `defer`: Descarga en paralelo, ejecuta después del DOM

#### Orden de los scripts

```
1. Leaflet.js  (librería)
2. app.js      (nuestra aplicación)
```

**¿Por qué este orden?**

app.js usa Leaflet:
```javascript
const map = L.map('map');  // L viene de Leaflet.js
```

Si se invierten:
```
1. app.js ejecuta
   → const map = L.map('map');
   → Error: "L is not defined" 
2. Leaflet.js carga (demasiado tarde)
```

#### Leaflet.js desde CDN

```html
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
    crossorigin=""></script>
```

- Mismos atributos que Leaflet CSS (`integrity`, `crossorigin`)
- **Importante:** La versión debe coincidir (CSS y JS ambos 1.9.4)

#### app.js con Jinja2

```html
<script src="{{ url_for('static', filename='js/app.js') }}"></script>
```

Renderizado:
```html
<script src="/static/js/app.js"></script>
```

---

## 3.3 Resumen de la Estructura

### Mapa mental del documento

```
index.html
│
├── <head>
│   ├── Metadatos (charset, viewport, description, author)
│   ├── <title>
│   ├── Leaflet CSS (CDN)
│   └── app.css (local)
│
└── <body>
    ├── <header>
    │   └── Título y descripción
    │
    ├── <div class="main-container">
    │   ├── <aside class="sidebar">
    │   │   ├── Sección Información
    │   │   ├── Sección Búsqueda
    │   │   └── Sección Acerca de
    │   │
    │   └── <main class="map-container">
    │       └── <div id="map"></div>  ← ¡EL MAPA!
    │
    ├── <footer>
    │   └── Copyright
    │
    └── Scripts
        ├── Leaflet.js (CDN)
        └── app.js (local)
```

### Flujo de renderizado

```
1. Navegador solicita http://localhost:5000/map-dpto
2. Flask procesa la ruta (app.py línea 150-153):
   @app.route('/map-dpto')
   def map_dpto():
       return render_template('app/index.html')
3. Flask/Jinja2 procesa el template:
   {{ url_for('static', filename='css/app.css') }}
   → /static/css/app.css
4. Navegador recibe HTML completo
5. Navegador descarga recursos:
   - Leaflet CSS (unpkg.com)
   - app.css (localhost:5000)
   - Leaflet JS (unpkg.com)
   - app.js (localhost:5000)
6. Navegador renderiza HTML + CSS
7. Navegador ejecuta JavaScript:
   - Leaflet.js se carga
   - app.js ejecuta:
     - Inicializa mapa en #map
     - Carga capas WMS/WFS
     - Agrega interactividad
```

---

## 3.4 Elementos Importantes para JavaScript

Estos elementos tienen `id` o `class` que JavaScript usa:

| Selector | Elemento | Uso en app.js |
|----------|----------|---------------|
| `#map` | Div del mapa | Línea 27: `L.map('map')` |
| `#search-input` | Input de búsqueda | Línea 257: `document.getElementById('search-input')` |
| `#search-button` | Botón de búsqueda | Línea 256: `document.getElementById('search-button')` |
| `#search-results` | Div de resultados | Línea 258: `document.getElementById('search-results')` |

---

## 3.5 Modificaciones Comunes

### Cambiar título de la página

```html
<title>Mi Visor Geográfico</title>
```

### Agregar favicon

```html
<head>
    ...
    <link rel="icon" type="image/png" href="{{ url_for('static', filename='favicon.png') }}">
</head>
```

### Agregar más secciones al sidebar

```html
<aside class="sidebar">
    ...
    <div class="sidebar-section">
        <h2>📈 Estadísticas</h2>
        <div id="stats-panel">
            <!-- Contenido dinámico -->
        </div>
    </div>
</aside>
```

### Cambiar descripción

```html
<meta name="description" content="Tu nueva descripción aquí">
```

---

## 3.6 Ejercicio Práctico

**Tarea:** Agrega una nueva sección al sidebar con un botón que muestre una alerta.

**Pasos:**

1. **Agregar HTML:**
```html
<div class="sidebar-section">
    <h2>🧪 Prueba</h2>
    <button id="test-button" class="btn-primary">Hacer Click</button>
</div>
```

2. **Agregar JavaScript en app.js:**
```javascript
document.getElementById('test-button').addEventListener('click', function() {
    alert('¡Botón funcionando!');
});
```

3. **Verificar:**
   - Recargar página
   - Click en el botón
   - Debe aparecer alerta

---

## 3.7 Resumen

Has aprendido:

- La estructura completa de un documento HTML5
- Elementos semánticos (`<header>`, `<main>`, `<aside>`, `<footer>`)
- Cómo enlazar CSS y JavaScript
- El uso de templates Jinja2 con Flask
- La importancia del `<div id="map">` para Leaflet
- Buenas prácticas (SRI, viewport, orden de scripts)

### Próximo módulo

En el **Módulo 4 (Estilos CSS)**, analizaremos el archivo `app.css` y comprenderemos cómo se logra el diseño de dos columnas, el responsive design y la personalización de Leaflet.

---

**[⬅️ Módulo 2: Prerequisitos](02_PREREQUISITOS.md)** | **[Volver al Índice](README.md)** | **[Siguiente: Módulo 4 - Estilos CSS ➡️](04_ESTILOS_CSS.md)**
