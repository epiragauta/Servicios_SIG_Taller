# Módulo 4: Creación de Estilos CSS

## Objetivos de Aprendizaje

Al completar este módulo, habrás:

- Creado el archivo `app.css` completo desde cero
- Implementado un layout de dos columnas con Flexbox
- Agregado diseño responsive para móviles
- Personalizado los componentes de Leaflet
- Aplicado gradientes, animaciones y efectos visuales

---

## 4.1 Preparación

### Crear el archivo CSS

Crea el archivo en la ubicación correcta:

**Ubicación:** `webapp/static/css/app.css`

```bash
# Si no existe el directorio
mkdir -p webapp/static/css

# Crear archivo vacío (Linux/Mac)
touch webapp/static/css/app.css

# Windows PowerShell
New-Item -Path webapp/static/css/app.css -ItemType File
```

Abre `app.css` en tu editor de código.

---

## 4.2 Paso 1: Reset CSS y Estilos Base

Comienza con el reset CSS y estilos base del body:

```css
/* Reset y estilos base */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f5f5f5;
    color: #333;
    line-height: 1.6;
}
```

**Explicación:**
- `*`: Selector universal, aplica a todos los elementos
- `margin: 0; padding: 0;`: Elimina márgenes por defecto de navegadores
- `box-sizing: border-box;`: El ancho incluye padding y border
- `font-family`: Lista de fuentes en orden de preferencia
- `line-height: 1.6`: Mejor legibilidad (160% del tamaño de fuente)

---

## 4.3 Paso 2: Estilos del Header

Agrega los estilos del header con gradiente:

```css
/* Header */
.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem 2rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header-content h1 {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.header-content p {
    font-size: 0.95rem;
    opacity: 0.9;
}
```

**Explicación:**
- `linear-gradient(135deg, ...)`: Gradiente diagonal de violeta a púrpura
- `box-shadow`: Sombra sutil para profundidad visual
- `rem`: Unidades relativas al tamaño de fuente raíz (16px por defecto)
- `opacity: 0.9`: Texto ligeramente transparente

---

## 4.4 Paso 3: Layout Principal con Flexbox

Agrega el contenedor principal que usará Flexbox:

```css
/* Contenedor principal */
.main-container {
    display: flex;
    height: calc(100vh - 140px);
}
```

**Explicación:**
- `display: flex`: Activa Flexbox (los hijos se alinean horizontalmente)
- `calc(100vh - 140px)`: Altura dinámica
  - `100vh`: 100% de la altura del viewport (ventana)
  - `-140px`: Resta altura de header y footer
  - Resultado: El contenedor ocupa todo el espacio restante

---

## 4.5 Paso 4: Sidebar (Panel Lateral)

Agrega los estilos completos del sidebar:

```css
/* Sidebar */
.sidebar {
    width: 320px;
    background-color: white;
    padding: 1.5rem;
    overflow-y: auto;
    box-shadow: 2px 0 10px rgba(0,0,0,0.1);
}

.sidebar-section {
    margin-bottom: 2rem;
}

.sidebar-section h2 {
    font-size: 1.1rem;
    margin-bottom: 1rem;
    color: #667eea;
    border-bottom: 2px solid #667eea;
    padding-bottom: 0.5rem;
}

.sidebar-section p {
    margin-bottom: 0.75rem;
}

.sidebar-section ul {
    list-style-type: none;
    padding-left: 0;
}

.sidebar-section li {
    padding: 0.5rem 0;
    border-bottom: 1px solid #eee;
}

.info-text {
    color: #666;
    font-size: 0.9rem;
    font-style: italic;
}

.small-text {
    font-size: 0.85rem;
    line-height: 1.6;
}
```

**Explicación:**
- `width: 320px`: Ancho fijo del sidebar
- `overflow-y: auto`: Scrollbar vertical si el contenido es muy largo
- `box-shadow: 2px 0 ...`: Sombra a la derecha (efecto de separación)
- `border-bottom`: Línea decorativa bajo el título de cada sección

---

## 4.6 Paso 5: Estilos de Búsqueda

Agrega estilos para el input y botón de búsqueda:

```css
/* Búsqueda */
.search-input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.95rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.3s;
}

.search-input:focus {
    outline: none;
    border-color: #667eea;
}

.btn-primary {
    width: 100%;
    padding: 0.75rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:active {
    transform: translateY(0);
}

#search-results {
    margin-top: 1rem;
}

.search-result-item {
    padding: 0.75rem;
    margin-bottom: 0.5rem;
    background-color: #f9f9f9;
    border-left: 3px solid #667eea;
    cursor: pointer;
    transition: background-color 0.2s;
}

.search-result-item:hover {
    background-color: #e8f0fe;
}
```

**Explicación:**
- `transition`: Animación suave en cambios de propiedad
- `:focus`: Estilo cuando el input está seleccionado
- `:hover`: Estilo cuando el mouse pasa sobre el elemento
- `:active`: Estilo cuando se hace click
- `transform: translateY(-2px)`: Mueve 2px hacia arriba (efecto "levitar")
- `cursor: pointer`: Cambia cursor a manita

---

## 4.7 Paso 6: Contenedor del Mapa

Agrega los estilos del contenedor del mapa:

```css
/* Contenedor del mapa */
.map-container {
    flex: 1;
    position: relative;
}

#map {
    width: 100%;
    height: 100%;
}
```

**Explicación:**
- `flex: 1`: El mapa crece para llenar todo el espacio restante
  - Sidebar: 320px fijo
  - Mapa: Todo lo demás (gracias a `flex: 1`)
- `width: 100%; height: 100%;`: **CRÍTICO** para que Leaflet funcione
  - Sin dimensiones, el mapa será invisible (0px x 0px)

---

## 4.8 Paso 7: Footer

Agrega los estilos del footer:

```css
/* Footer */
.footer {
    background-color: #2c3e50;
    color: white;
    text-align: center;
    padding: 1rem;
    font-size: 0.9rem;
}
```

---

## 4.9 Paso 8: Personalización de Leaflet

Agrega estilos para personalizar los componentes de Leaflet:

```css
/* Estilos de Leaflet personalizados */
.leaflet-popup-content-wrapper {
    border-radius: 8px;
    box-shadow: 0 3px 14px rgba(0,0,0,0.4);
}

.leaflet-popup-content {
    margin: 1rem;
    font-size: 0.95rem;
}

.popup-title {
    font-size: 1.3rem;
    color: #667eea;
    margin-bottom: 0.75rem;
    font-weight: 600;
}

.popup-divider {
    height: 2px;
    background: linear-gradient(to right, #667eea, #764ba2);
    margin: 0.5rem 0;
}

.popup-info {
    color: #555;
    line-height: 1.6;
}

/* Control de información */
.info-control {
    padding: 10px 15px;
    font: 14px/16px Arial, sans-serif;
    background: white;
    background: rgba(255,255,255,0.95);
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    border-radius: 5px;
    min-width: 200px;
}

.info-control h4 {
    margin: 0 0 5px;
    color: #667eea;
}

.info-control p {
    margin: 5px 0;
}

.highlight {
    font-weight: bold;
    color: #764ba2;
    font-size: 1.1rem;
}

/* Control de capas */
.leaflet-control-layers {
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

/* Escala */
.leaflet-control-scale {
    background: rgba(255,255,255,0.8);
    border-radius: 4px;
}
```

**Explicación:**
- Leaflet genera automáticamente clases CSS (`.leaflet-popup-content-wrapper`, etc.)
- Nosotros las sobrescribimos para personalizar
- `.popup-title`, `.popup-divider`: Clases personalizadas que usaremos en JavaScript
- `rgba(255,255,255,0.95)`: Blanco con 95% opacidad (5% transparente)

---

## 4.10 Paso 9: Responsive Design

Agrega media query para dispositivos móviles:

```css
/* Responsive */
@media (max-width: 768px) {
    .main-container {
        flex-direction: column;
        height: auto;
    }

    .sidebar {
        width: 100%;
        max-height: 300px;
    }

    .map-container {
        height: 500px;
    }

    .header-content h1 {
        font-size: 1.4rem;
    }

    .header-content p {
        font-size: 0.85rem;
    }
}
```

**Explicación:**
- `@media (max-width: 768px)`: Se aplica en pantallas ≤768px (tablets/móviles)
- `flex-direction: column`: Cambia de horizontal a vertical
  - Desktop: Sidebar | Mapa (horizontal)
  - Móvil: Sidebar arriba, Mapa abajo (vertical)
- `max-height: 300px` en sidebar: Limita altura con scroll

---

## 4.11 Paso 10: Animaciones

Agrega animación fadeIn para el sidebar:

```css
/* Animaciones */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.sidebar-section {
    animation: fadeIn 0.5s ease-in-out;
}
```

**Explicación:**
- `@keyframes fadeIn`: Define la animación
  - `from`: Invisible y 10px arriba
  - `to`: Visible y en posición normal
- `.sidebar-section`: Aplica la animación (0.5 segundos)
- Resultado: Las secciones aparecen gradualmente al cargar

---

## 4.12 Paso 11: Scrollbar Personalizado

Finalmente, agrega estilos para personalizar el scrollbar del sidebar:

```css
/* Scrollbar personalizado para sidebar */
.sidebar::-webkit-scrollbar {
    width: 8px;
}

.sidebar::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.sidebar::-webkit-scrollbar-thumb {
    background: #667eea;
    border-radius: 4px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
    background: #764ba2;
}
```

**Explicación:**
- `::-webkit-scrollbar`: Pseudo-elementos para Chrome/Edge/Safari
- `width: 8px`: Scrollbar delgado
- `-track`: El fondo del scrollbar
- `-thumb`: La parte arrastrable del scrollbar
- **NOTA:** No funciona en Firefox (usa propiedades estándar)

---

## 4.13 Checkpoint: Probar los Estilos

### Paso 1: Guardar el archivo

Asegúrate de que `webapp/static/css/app.css` está guardado.

### Paso 2: Reiniciar el contenedor webapp

```bash
docker-compose restart webapp
```

### Paso 3: Abrir en navegador

Visita: http://localhost:5000/map-dpto

**Resultado esperado:**

**Header:**
- Fondo con gradiente violeta-púrpura
- Texto blanco centrado
- Emoji visible

**Layout:**
- Sidebar a la izquierda (320px, fondo blanco)
- Área del mapa a la derecha (ocupa resto del espacio)

**Sidebar:**
- 3 secciones con títulos violetas
- Línea decorativa bajo cada título
- Input de búsqueda con bordes grises
- Botón con gradiente

**Mapa:**
- Área gris vacía (aún no hay mapa, solo el contenedor)
- Ocupa todo el espacio a la derecha

**Footer:**
- Fondo gris oscuro, texto blanco

**Responsive:**
- Reducir ventana a <768px
- Sidebar cambia a la parte superior
- Mapa abajo

**Errores en consola (F12):**
- Error 404 para `app.js`: **Normal**, lo crearemos en Módulo 5
- El mapa no aparece: **Normal**, lo crearemos en Módulos 5-6

---

## 4.14 Resumen

Has aprendido:

- Crear un archivo CSS completo desde cero (~320 líneas)
- Implementar layout de dos columnas con Flexbox
- Usar `calc()` para dimensiones dinámicas
- Crear gradientes lineales con `linear-gradient()`
- Agregar transiciones y animaciones
- Personalizar scrollbars con pseudo-elementos
- Implementar diseño responsive con `@media queries`
- Personalizar componentes de Leaflet

### Archivos creados

- `webapp/static/css/app.css` (320 líneas)

### Técnicas CSS aprendidas

- **Flexbox:** `display: flex`, `flex: 1`, `flex-direction`
- **Gradientes:** `linear-gradient()`
- **Sombras:** `box-shadow`
- **Transiciones:** `transition`
- **Transformaciones:** `transform: translateY()`
- **Pseudo-clases:** `:hover`, `:focus`, `:active`
- **Pseudo-elementos:** `::-webkit-scrollbar`
- **Animaciones:** `@keyframes`, `animation`
- **Media queries:** `@media (max-width: 768px)`

### Próximo módulo

En el **Módulo 5 (JavaScript Parte 1)**, crearás el archivo `app.js` y aprenderás a:
- Inicializar el mapa de Leaflet
- Agregar capas base (OSM, Satélite, CartoDB)
- **Cargar servicios WMS** (departamentos y municipios)
- Crear control de capas

---

**[⬅️ Módulo 3: Estructura HTML](03_ESTRUCTURA_HTML.md)** | **[Volver al Índice](README.md)** | **[Siguiente: Módulo 5 - JavaScript Parte 1 ➡️](05_JAVASCRIPT_PARTE_1.md)**
