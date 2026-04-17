# Módulo 4: Estilos CSS

## Objetivos de Aprendizaje

Al completar este módulo, comprenderás:

- 🎯 La estructura completa del archivo `app.css`
- 🎨 Cómo se crea el layout de dos columnas con Flexbox
- 📱 Cómo funciona el diseño responsive
- ✨ La personalización de componentes de Leaflet
- 🔧 Técnicas modernas de CSS (gradientes, animaciones, scrollbar personalizado)

---

## 4.1 Visión General

El archivo `webapp/static/css/app.css` contiene **320 líneas** de CSS organizadas en secciones:

1. **Reset y estilos base** (líneas 1-13)
2. **Header** (líneas 15-32)
3. **Layout principal con Flexbox** (líneas 34-38)
4. **Sidebar** (líneas 40-89)
5. **Búsqueda y botones** (líneas 91-145)
6. **Mapa** (líneas 147-156)
7. **Footer** (líneas 158-165)
8. **Personalización de Leaflet** (líneas 167-256)
9. **Responsive design** (líneas 263-285)
10. **Animaciones** (líneas 287-301)
11. **Scrollbar personalizado** (líneas 303-320)

---

## 4.2 Reset y Estilos Base (Líneas 1-13)

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

### Selector universal (`*`)

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
```

**Propósito:** Reset CSS básico

**`margin: 0; padding: 0;`**
- Elimina márgenes y rellenos por defecto de todos los elementos
- Los navegadores tienen estilos predeterminados diferentes
- Esto garantiza consistencia

**`box-sizing: border-box;`**
- Cambia el modelo de caja CSS
- **Sin `border-box`:** `width` incluye solo el contenido
- **Con `border-box`:** `width` incluye contenido + padding + border

**Ejemplo:**

```css
/* Sin border-box */
.caja {
    width: 300px;
    padding: 20px;
    border: 5px solid black;
}
/* Ancho total: 300 + (20*2) + (5*2) = 350px */

/* Con border-box */
.caja {
    box-sizing: border-box;
    width: 300px;
    padding: 20px;
    border: 5px solid black;
}
/* Ancho total: 300px (padding y border incluidos) */
```

### Estilos del body

```css
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f5f5f5;
    color: #333;
    line-height: 1.6;
}
```

**`font-family`**
- Lista de fuentes en orden de preferencia
- Si 'Segoe UI' no está disponible → Tahoma → Geneva → etc.
- `sans-serif` es la fuente genérica final

**`background-color: #f5f5f5`**
- Gris muy claro
- Mejor que blanco puro (#fff) para reducir fatiga visual

**`color: #333`**
- Gris oscuro para el texto
- Mejor contraste que negro puro (#000)

**`line-height: 1.6`**
- Espacio entre líneas = 160% del tamaño de fuente
- Mejora legibilidad

---

## 4.3 Header (Líneas 15-32)

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

### Gradiente lineal

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

**Sintaxis:**
```css
linear-gradient(ángulo, color1 posición%, color2 posición%);
```

**Parámetros:**
- `135deg`: Ángulo diagonal (de esquina superior izquierda a inferior derecha)
- `#667eea`: Color inicial (azul/violeta)
- `0%`: Comienza al 0% del gradiente
- `#764ba2`: Color final (púrpura)
- `100%`: Termina al 100%

**Visualización:**
```
Gradiente 135deg:
┌─────────────────┐
│#667eea         │
│    ↘          │
│        ↘      │
│            ↘  │
│         #764ba2│
└─────────────────┘
```

### Box-shadow

```css
box-shadow: 0 2px 10px rgba(0,0,0,0.1);
```

**Sintaxis:**
```css
box-shadow: offset-x offset-y blur-radius color;
```

**Parámetros:**
- `0`: Desplazamiento horizontal (0 = centrado)
- `2px`: Desplazamiento vertical (sombra hacia abajo)
- `10px`: Radio de difuminado (blur)
- `rgba(0,0,0,0.1)`: Negro con 10% de opacidad

**Efecto:**
- Sombra sutil debajo del header
- Crea sensación de profundidad

### Unidades rem

```css
padding: 1.5rem 2rem;
font-size: 1.8rem;
```

**¿Qué es `rem`?**
- **rem** = "root em"
- Relativo al tamaño de fuente del `<html>` (generalmente 16px)
- `1rem` = 16px
- `1.5rem` = 24px
- `2rem` = 32px

**Ventajas de rem:**
- ✅ Escalable (accesibilidad)
- ✅ Consistente en toda la aplicación
- ✅ Fácil de cambiar globalmente

**Ejemplo:**
```css
html {
    font-size: 18px; /* Cambiar tamaño base */
}
/* Ahora 1rem = 18px en todo el sitio */
```

---

## 4.4 Layout Principal con Flexbox (Líneas 34-38)

```css
/* Contenedor principal */
.main-container {
    display: flex;
    height: calc(100vh - 140px);
}
```

### Display flex

```css
display: flex;
```

**¿Qué hace `display: flex`?**
- Convierte el contenedor en un **contenedor flexbox**
- Los hijos directos se convierten en **flex items**
- Por defecto: se alinean horizontalmente

**Estructura HTML:**
```html
<div class="main-container">  ← Flex container
    <aside class="sidebar">...</aside>     ← Flex item 1
    <main class="map-container">...</main> ← Flex item 2
</div>
```

**Resultado visual:**
```
┌──────────┬──────────────────────────────┐
│ Sidebar  │     Map Container            │
│          │                              │
└──────────┴──────────────────────────────┘
```

### Función calc()

```css
height: calc(100vh - 140px);
```

**Sintaxis:**
```css
calc(expresión)
```

**En este caso:**
- `100vh`: 100% de la altura del viewport (ventana del navegador)
- `-`: Operador de resta
- `140px`: Altura del header + footer

**Ejemplo:**
```
Viewport height: 800px
Header: 80px
Footer: 60px
Total a restar: 140px

Altura de .main-container: 800px - 140px = 660px
```

**Ventaja:**
- Layout adaptable a cualquier tamaño de pantalla
- El mapa siempre ocupa el espacio disponible

---

## 4.5 Sidebar (Líneas 40-89)

```css
/* Sidebar */
.sidebar {
    width: 320px;
    background-color: white;
    padding: 1.5rem;
    overflow-y: auto;
    box-shadow: 2px 0 10px rgba(0,0,0,0.1);
}
```

### Ancho fijo

```css
width: 320px;
```

- Sidebar tiene ancho fijo de 320px
- El mapa ocupa el resto del espacio (gracias a `flex: 1`)

### Overflow-y

```css
overflow-y: auto;
```

**Opciones de overflow:**
- `visible`: Contenido desborda (predeterminado)
- `hidden`: Contenido oculto si desborda
- `scroll`: Siempre muestra scrollbar
- `auto`: Scrollbar solo si es necesario ✅

**En este caso:**
- Si el contenido del sidebar es más alto que el contenedor
- Aparece scrollbar vertical automáticamente

### Secciones del sidebar

```css
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
```

**`border-bottom`**
- Línea decorativa debajo del título
- Color coordina con el header

**Resultado visual:**
```
📊 Información
─────────────
Contenido...
```

---

## 4.6 Búsqueda y Botones (Líneas 91-145)

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
```

### Pseudo-clase :focus

```css
.search-input:focus {
    outline: none;
    border-color: #667eea;
}
```

**¿Cuándo se aplica `:focus`?**
- Cuando el usuario hace click en el input
- Cuando el input está seleccionado (con tab)

**`outline: none`**
- Elimina el outline predeterminado del navegador
- **IMPORTANTE:** Debe reemplazarse con otro indicador visual

**`border-color: #667eea`**
- Cambia el borde a color violeta cuando está activo
- Indica visualmente que el input está enfocado

### Transiciones

```css
transition: border-color 0.3s;
```

**Sintaxis:**
```css
transition: propiedad duración función-timing;
```

**Efecto:**
- Cuando `border-color` cambia (por `:focus`)
- El cambio ocurre gradualmente en 0.3 segundos
- Mejora UX (no es abrupto)

### Botón principal

```css
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
```

### Transform

```css
.btn-primary:hover {
    transform: translateY(-2px);
}
```

**`transform: translateY(-2px)`**
- Mueve el botón 2px hacia arriba
- Simula un "levantamiento" al pasar el mouse

**Pseudo-clases de interacción:**
- `:hover`: Cursor sobre el elemento
- `:active`: Elemento siendo clickeado

**Secuencia de interacción:**
```
Estado normal → Hover → Active
translateY(0)   -2px     0px
```

**Efecto visual:**
```
Normal:  [  Buscar  ]

Hover:   [  Buscar  ] ↑ (levanta)
         └─ sombra ─┘

Active:  [  Buscar  ] (vuelve)
```

---

## 4.7 Mapa (Líneas 147-156)

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

### Flex: 1

```css
.map-container {
    flex: 1;
}
```

**¿Qué significa `flex: 1`?**

Es shorthand para:
```css
flex-grow: 1;     /* Puede crecer */
flex-shrink: 1;   /* Puede encogerse */
flex-basis: 0%;   /* Base de tamaño */
```

**Efecto:**
- El contenedor del mapa **crece** para llenar todo el espacio disponible
- Sidebar (320px fijo) + Map container (resto del espacio)

**Ejemplo:**
```
Ancho total: 1200px
Sidebar: 320px
Map container: 1200px - 320px = 880px (gracias a flex: 1)
```

### Dimensiones del mapa

```css
#map {
    width: 100%;
    height: 100%;
}
```

**CRÍTICO para Leaflet:**
- Si no tiene dimensiones definidas, el mapa no se muestra
- `100%` significa: ocupa todo el contenedor padre (`.map-container`)

---

## 4.8 Footer (Líneas 158-165)

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

**Estilos simples:**
- Fondo oscuro
- Texto centrado
- Padding uniforme

---

## 4.9 Personalización de Leaflet (Líneas 167-256)

### Popups

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
```

**Clases de Leaflet:**
- `.leaflet-popup-content-wrapper`: Contenedor del popup
- `.leaflet-popup-content`: Contenido del popup

**Clases personalizadas:**
- `.popup-title`: Usada en JavaScript (app.js línea 151)

**Generación dinámica del popup (app.js):**
```javascript
const popupContent = `
    <div class="popup-title">${props.dpto_cnmbr}</div>
    <div class="popup-divider"></div>
    <div class="popup-info"><strong>Código:</strong> ${props.dpto_ccdgo}</div>
`;
```

### Control de información

```css
.info-control {
    padding: 10px 15px;
    font: 14px/16px Arial, sans-serif;
    background: white;
    background: rgba(255,255,255,0.95);
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    border-radius: 5px;
    min-width: 200px;
}
```

**`rgba(255,255,255,0.95)`**
- Blanco con 95% de opacidad (5% transparente)
- Permite ver ligeramente el mapa detrás

**Uso en JavaScript (app.js línea 217-233):**
```javascript
const infoControl = L.control({position: 'topleft'});

infoControl.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info-control');
    this.update();
    return this._div;
};
```

---

## 4.10 Responsive Design (Líneas 263-285)

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

### Media queries

```css
@media (max-width: 768px) {
    /* Estilos para pantallas ≤ 768px */
}
```

**Breakpoints comunes:**
- `480px`: Móviles pequeños
- `768px`: Tablets ✅ (usado aquí)
- `1024px`: Tablets grandes / laptops pequeñas
- `1200px`: Desktops

### Cambio de layout

```css
.main-container {
    flex-direction: column;
    height: auto;
}
```

**Desktop (>768px):**
```
┌──────────┬──────────────────────┐
│ Sidebar  │      Mapa            │
│          │                      │
└──────────┴──────────────────────┘
```

**Móvil (≤768px):**
```
┌────────────────────────────┐
│        Sidebar             │
├────────────────────────────┤
│                            │
│          Mapa              │
│                            │
└────────────────────────────┘
```

**`flex-direction: column`**
- Cambia orientación de horizontal a vertical
- Los elementos se apilan uno sobre otro

**`height: auto`**
- En móvil, la altura se adapta al contenido
- No usa `calc(100vh - 140px)`

### Ajustes de dimensiones

```css
.sidebar {
    width: 100%;
    max-height: 300px;
}

.map-container {
    height: 500px;
}
```

**Sidebar:**
- `width: 100%`: Ocupa todo el ancho
- `max-height: 300px`: Limitado a 300px (con scroll si es necesario)

**Map container:**
- `height: 500px`: Altura fija en móvil
- Antes era `100%` (relativo al padre)

---

## 4.11 Animaciones (Líneas 287-301)

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

### Keyframes

```css
@keyframes fadeIn {
    from { ... }
    to { ... }
}
```

**Definición de animación:**
- `from`: Estado inicial (0%)
- `to`: Estado final (100%)

**Efecto de fadeIn:**
```
Estado inicial:
- opacity: 0 (invisible)
- translateY(-10px) (10px arriba)

↓ Animación (0.5s)

Estado final:
- opacity: 1 (visible)
- translateY(0) (posición original)
```

### Aplicación de animación

```css
.sidebar-section {
    animation: fadeIn 0.5s ease-in-out;
}
```

**Sintaxis:**
```css
animation: nombre duración timing-function;
```

**Parámetros:**
- `fadeIn`: Nombre de la animación (definida en @keyframes)
- `0.5s`: Duración (medio segundo)
- `ease-in-out`: Aceleración suave al inicio y final

**Resultado:**
- Cada sección del sidebar aparece gradualmente
- Mejora UX (sensación de carga progresiva)

---

## 4.12 Scrollbar Personalizado (Líneas 303-320)

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

### Pseudo-elementos de scrollbar

**`::-webkit-scrollbar`**
- Funciona en Chrome, Edge, Safari
- No funciona en Firefox (usa `scrollbar-width` y `scrollbar-color`)

**Partes del scrollbar:**
```
┌─┐ ← ::-webkit-scrollbar (ancho total)
│▓│ ← ::-webkit-scrollbar-thumb (el "pulgar" arrastrable)
│ │ ← ::-webkit-scrollbar-track (el fondo)
│▓│
└─┘
```

**Personalización:**
- `width: 8px`: Scrollbar delgado
- Track (fondo): Gris claro
- Thumb (pulgar): Violeta (color del tema)
- Hover: Púrpura más oscuro

---

## 4.13 Técnicas CSS Destacadas

### 1. Variables CSS (Alternativa recomendada)

Aunque no se usan en este proyecto, una mejora sería:

```css
:root {
    --color-primary: #667eea;
    --color-secondary: #764ba2;
    --sidebar-width: 320px;
    --border-radius: 4px;
}

.btn-primary {
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
}
```

**Ventajas:**
- Centraliza valores
- Fácil de cambiar tema
- Mejor mantenibilidad

### 2. Modelo de espaciado consistente

En app.css se usa un sistema de espaciado basado en rem:

```css
0.5rem = 8px
0.75rem = 12px
1rem = 16px
1.5rem = 24px
2rem = 32px
```

**Beneficio:** Espaciado visual consistente

### 3. Box-shadow para profundidad

Se usa box-shadow para crear jerarquía visual:

```css
.header {
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);  /* Sombra sutil */
}

.sidebar {
    box-shadow: 2px 0 10px rgba(0,0,0,0.1);  /* Sombra lateral */
}

.leaflet-popup-content-wrapper {
    box-shadow: 0 3px 14px rgba(0,0,0,0.4);  /* Sombra prominente */
}
```

---

## 4.14 Ejercicio Práctico

**Tarea:** Cambia el tema de colores de la aplicación.

**Pasos:**

1. **Cambiar gradiente del header:**
```css
.header {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}
```

2. **Cambiar color de acento:**
```css
.sidebar-section h2 {
    color: #11998e;
    border-bottom: 2px solid #11998e;
}

.search-input:focus {
    border-color: #11998e;
}

.btn-primary {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}
```

3. **Verificar resultado:**
   - Recargar página
   - Tema verde en lugar de violeta

---

## 4.15 Resumen

Has aprendido:

✅ Reset CSS y modelo de caja con `box-sizing`
✅ Layout de dos columnas con Flexbox
✅ Gradientes lineales y sombras
✅ Unidades relativas (`rem`, `%`, `vh`)
✅ Pseudo-clases (`:hover`, `:focus`, `:active`)
✅ Responsive design con media queries
✅ Animaciones con `@keyframes`
✅ Personalización de scrollbars
✅ Integración con Leaflet

### Próximo módulo

En el **Módulo 5 (JavaScript Parte 1)**, comenzaremos el análisis del archivo `app.js`, cubriendo:
- Configuración global
- Inicialización del mapa
- Capas base (tile layers)
- Carga de servicios WMS

---

**[⬅️ Módulo 3: Estructura HTML](03_ESTRUCTURA_HTML.md)** | **[Volver al Índice](README.md)** | **[Siguiente: Módulo 5 - JavaScript Parte 1 ➡️](05_JAVASCRIPT_PARTE_1.md)**
