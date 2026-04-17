# Módulo 3: Creación del Archivo HTML

## Objetivos de Aprendizaje

Al completar este módulo, habrás:

- Creado el archivo `index.html` completo desde cero
- Aprendido la estructura de un documento HTML5
- Enlazado las dependencias externas (Leaflet CSS/JS)
- Integrado templates Jinja2 de Flask
- Preparado el contenedor para el mapa de Leaflet

---

## 3.1 Preparación

### Verificar estructura de directorios

Antes de comenzar, verifica que existe la estructura base:

```bash
webapp/
├── templates/
│   └── app/          # ← Aquí crearemos index.html
├── static/
│   ├── css/          # ← Aquí crearemos app.css (Módulo 4)
│   └── js/           # ← Aquí crearemos app.js (Módulos 5 y 6)
└── app.py            # ← Ya existe con código base
```

Si no existe la carpeta `templates/app/`, créala:

```bash
mkdir -p webapp/templates/app
```

---

## 3.2 Crear el Archivo index.html

Abre tu editor de código y crea el archivo:

**Ubicación:** `webapp/templates/app/index.html`

---

## 3.3 Paso 1: Estructura Básica HTML5

Comienza escribiendo la estructura básica de un documento HTML5:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Colombia - Departamentos y Municipios | Servicios Web Geográficos</title>
</head>
<body>

</body>
</html>
```

**Explicación:**
- `<!DOCTYPE html>`: Declaración HTML5 (siempre primera línea)
- `<html lang="es">`: Idioma español para accesibilidad y SEO
- `<meta charset="UTF-8">`: Codificación UTF-8 (soporta acentos y ñ)
- `<meta name="viewport" ...>`: Diseño responsive para móviles
- `<title>`: Título que aparece en la pestaña del navegador

---

## 3.4 Paso 2: Agregar Metadatos en el HEAD

Dentro de `<head>`, después de la línea del `<title>`, agrega los metadatos:

```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Visualización interactiva de departamentos y municipios de Colombia usando servicios WMS y WFS de GeoServer">
    <meta name="author" content="Curso de Servicios Web Geográficos">
    <title>Colombia - Departamentos y Municipios | Servicios Web Geográficos</title>
</head>
```

**Explicación:**
- `description`: Aparece en resultados de búsqueda de Google
- `author`: Identifica al autor del documento

---

## 3.5 Paso 3: Enlazar Leaflet CSS

Después del `<title>`, agrega los enlaces a hojas de estilo:

```html
    <title>Colombia - Departamentos y Municipios | Servicios Web Geográficos</title>

    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
        crossorigin=""/>

    <!-- Estilos personalizados -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/app.css') }}">
</head>
```

**Explicación:**
- **Leaflet CSS:** Desde CDN (unpkg.com) con hash SRI para seguridad
- **app.css:** Nuestros estilos personalizados usando Jinja2 `{{ url_for() }}`
- **Orden:** Primero Leaflet (base), luego nuestros estilos (pueden sobrescribir)

**NOTA:** `{{ url_for() }}` es sintaxis de Jinja2 que Flask procesa en el servidor.

---

## 3.6 Paso 4: Crear el Header

Ahora vamos al `<body>`. Agrega el header de la página:

```html
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-content">
            <h1>🗺️ Colombia - División Administrativa</h1>
            <p>Visualización de Departamentos y Municipios mediante Servicios Web Geográficos (WMS/WFS)</p>
        </div>
    </header>

</body>
```

**Explicación:**
- `<header>`: Elemento semántico HTML5 para encabezado
- `.header`: Clase CSS para estilos (lo crearemos en Módulo 4)
- Emoji 🗺️ funciona gracias a `charset="UTF-8"`

---

## 3.7 Paso 5: Crear el Contenedor Principal

Después del header, agrega el contenedor principal que tendrá sidebar y mapa:

```html
    </header>

    <!-- Contenedor principal -->
    <div class="main-container">

    </div>

</body>
```

Este contenedor usará Flexbox (CSS en Módulo 4) para crear un layout de dos columnas.

---

## 3.8 Paso 6: Crear el Sidebar (Panel Lateral)

Dentro del `.main-container`, agrega el sidebar completo:

```html
    <div class="main-container">
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

    </div>
```

**Explicación:**
- `<aside>`: Elemento semántico para contenido lateral
- `#search-input`, `#search-button`, `#search-results`: IDs que usará JavaScript
- `#info-panel`: Div para información dinámica
- Tres secciones: Información, Búsqueda, Acerca de

---

## 3.9 Paso 7: Crear el Contenedor del Mapa

Después del sidebar (dentro de `.main-container`), agrega el contenedor del mapa:

```html
        </aside>

        <!-- Mapa -->
        <main class="map-container">
            <div id="map"></div>
        </main>
    </div>
```

**IMPORTANTE:**
- `<div id="map"></div>` es donde Leaflet renderizará el mapa
- **DEBE** tener el atributo `id="map"` exactamente así
- Sin este div, el mapa no funcionará

---

## 3.10 Paso 8: Crear el Footer

Después del `.main-container`, agrega el footer:

```html
    </div>

    <!-- Footer -->
    <footer class="footer">
        <p>&copy; 2024 Curso de Servicios Web Geográficos | Desarrollado con Leaflet.js y GeoServer</p>
    </footer>

</body>
```

**Explicación:**
- `<footer>`: Elemento semántico para pie de página
- `&copy;`: Entidad HTML para el símbolo © (copyright)

---

## 3.11 Paso 9: Enlazar JavaScript

Al final del `<body>`, **justo antes de `</body>`**, agrega los scripts de JavaScript:

```html
    </footer>

    <!-- Leaflet JavaScript -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
        crossorigin=""></script>

    <!-- Aplicación -->
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
```

**IMPORTANTE:**
- **Scripts al final del body:** Para que el DOM esté completamente cargado antes de ejecutar JavaScript
- **Orden:** Primero Leaflet.js (librería), luego app.js (nuestra aplicación que usa Leaflet)
- Si inviertes el orden, obtendrás error: "L is not defined"

---

## 3.12 Verificación: Archivo HTML Completo

Tu archivo `index.html` completo debe verse así:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Visualización interactiva de departamentos y municipios de Colombia usando servicios WMS y WFS de GeoServer">
    <meta name="author" content="Curso de Servicios Web Geográficos">
    <title>Colombia - Departamentos y Municipios | Servicios Web Geográficos</title>

    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
        crossorigin=""/>

    <!-- Estilos personalizados -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/app.css') }}">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-content">
            <h1>🗺️ Colombia - División Administrativa</h1>
            <p>Visualización de Departamentos y Municipios mediante Servicios Web Geográficos (WMS/WFS)</p>
        </div>
    </header>

    <!-- Contenedor principal -->
    <div class="main-container">
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

        <!-- Mapa -->
        <main class="map-container">
            <div id="map"></div>
        </main>
    </div>

    <!-- Footer -->
    <footer class="footer">
        <p>&copy; 2024 Curso de Servicios Web Geográficos | Desarrollado con Leaflet.js y GeoServer</p>
    </footer>

    <!-- Leaflet JavaScript -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
        crossorigin=""></script>

    <!-- Aplicación -->
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>
</body>
</html>
```

---

## 3.13 Checkpoint: Probar el HTML

Aunque aún no tenemos CSS ni JavaScript, podemos probar que el HTML se sirve correctamente.

### Paso 1: Guardar el archivo

Asegúrate de que `webapp/templates/app/index.html` está guardado.

### Paso 2: Verificar que el endpoint existe en app.py

Tu archivo `app.py` debe tener (lo agregarás en detalle en el Módulo 7):

```python
@app.route('/map-dpto')
def map_dpto():
    return render_template('app/index.html')
```

Si no existe, agrégalo temporalmente al final de `app.py` (antes de `if __name__ == '__main__':`).

### Paso 3: Reiniciar el contenedor webapp

```bash
docker-compose restart webapp
```

### Paso 4: Abrir en navegador

Visita: http://localhost:5000/map-dpto

**Resultado esperado:**
- Página sin estilos (sin CSS todavía)
- Texto del header visible
- Sidebar con las 3 secciones visibles
- Área vacía donde irá el mapa
- Footer al final
- **SIN errores en consola** (F12 → Console)

**Si ves errores de app.css o app.js no encontrados:** Es normal, los crearemos en los siguientes módulos.

---

## 3.14 Elementos Importantes para JavaScript

Estos elementos tienen `id` que JavaScript usará más adelante:

| Selector | Elemento | Uso futuro (Módulos 5-6) |
|----------|----------|---------------------------|
| `#map` | Div del mapa | Leaflet renderizará aquí el mapa |
| `#search-input` | Input de búsqueda | Capturar texto de búsqueda |
| `#search-button` | Botón de búsqueda | Evento click para buscar |
| `#search-results` | Div de resultados | Mostrar resultados de búsqueda |
| `#info-panel` | Div de información | Actualizar con datos de features |

**NO los cambies o el JavaScript no funcionará.**

---

## 3.15 Resumen

Has aprendido:

- Crear un documento HTML5 completo desde cero
- Usar elementos semánticos (`<header>`, `<main>`, `<aside>`, `<footer>`)
- Enlazar CSS y JavaScript (CDN y archivos locales)
- Integrar templates Jinja2 con `{{ url_for() }}`
- Preparar el contenedor `<div id="map">` para Leaflet
- Estructurar una página web para un visor geográfico

### Archivos creados

- `webapp/templates/app/index.html` (82 líneas)

### Próximo módulo

En el **Módulo 4 (Estilos CSS)**, crearás el archivo `app.css` para dar estilo a esta página:
- Layout de dos columnas con Flexbox
- Diseño responsive
- Estilos del header, sidebar y mapa
- Personalización de Leaflet

---

**[⬅️ Módulo 2: Prerequisitos](02_PREREQUISITOS.md)** | **[Volver al Índice](README.md)** | **[Siguiente: Módulo 4 - Estilos CSS ➡️](04_ESTILOS_CSS.md)**
