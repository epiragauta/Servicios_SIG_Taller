# Módulo 9: Ejercicios Prácticos

## Objetivos

Este módulo contiene ejercicios graduales para reforzar los conceptos aprendidos.

---

## Ejercicio 1: Básico - Agregar nueva capa base

**Objetivo:** Comprender cómo agregar tile layers

**Nivel:** Principiante

**Tarea:**
Agregar una nueva capa base de OpenTopoMap

**Archivo a modificar:** `app.js`

**Solución:**
```javascript
// En la sección de capas base (después de línea 54):
const baseLayers = {
    'Mapa base (OSM)': L.tileLayer(...),
    'Satélite (Esri)': L.tileLayer(...),
    'Calles (CartoDB)': L.tileLayer(...),

    // AGREGAR ESTA NUEVA CAPA:
    'Topográfico (OpenTopo)': L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data: &copy; OpenTopoMap contributors',
        maxZoom: 17
    })
};
```

**Verificación:**
- Recargar página
- Abrir control de capas
- Debe aparecer opción "Topográfico (OpenTopo)"

---

## Ejercicio 2: Intermedio - Estilos condicionales

**Objetivo:** Aplicar estilos dinámicos basados en atributos

**Nivel:** Intermedio

**Tarea:**
Colorear departamentos según su código (pares vs impares)

**Archivo a modificar:** `app.js` (línea 122)

**Solución:**
```javascript
function featureStyle(feature) {
    // Obtener código del departamento
    const codigo = parseInt(feature.properties.dpto_ccdgo);

    // Color diferente para pares e impares
    const color = codigo % 2 === 0 ? '#3388ff' : '#ff6b6b';

    return {
        fillColor: color,
        weight: 2,
        opacity: 0.8,
        color: '#232323',
        fillOpacity: 0.5
    };
}
```

**Verificación:**
- Departamentos pares azules
- Departamentos impares rojos

---

## Ejercicio 3: Intermedio - Filtro WFS con CQL

**Objetivo:** Filtrar features en el servidor usando CQL

**Nivel:** Intermedio

**Tarea:**
Cargar solo departamentos cuyo código sea mayor a 50

**Archivo a modificar:** `app.js` (línea 92)

**Solución:**
```javascript
function loadDepartamentosWFS() {
    const cqlFilter = "dpto_ccdgo > '50'";
    const wfsUrl = `/api/geoserver-proxy?service=WFS&version=2.0.0&request=GetFeature&typeName=ne:departamentos&outputFormat=application/json&cql_filter=${encodeURIComponent(cqlFilter)}`;

    fetch(wfsUrl)
        .then(...)
        .catch(...);
}
```

**Puntos de aprendizaje:**
- Parámetro `cql_filter`
- Filtrado en servidor (más eficiente)
- `encodeURIComponent()` para URLs

---

## Ejercicio 4: Avanzado - Popup personalizado

**Objetivo:** Crear popup con más información y estilos

**Nivel:** Avanzado

**Tarea:**
Mejorar el popup con más detalles y mejor formato

**Archivo a modificar:** `app.js` (línea 150)

**Solución:**
```javascript
function onEachFeature(feature, layer) {
    if (feature.properties) {
        const props = feature.properties;

        const popupContent = `
            <div style="min-width: 200px; font-family: Arial;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white; padding: 10px; margin: -15px -15px 10px -15px;
                            border-radius: 5px 5px 0 0;">
                    <h3 style="margin: 0; font-size: 1.2rem;">${props.dpto_cnmbr || 'Sin nombre'}</h3>
                </div>
                <table style="width: 100%; font-size: 0.9rem;">
                    <tr>
                        <td style="padding: 5px;"><strong>Código:</strong></td>
                        <td style="padding: 5px;">${props.dpto_ccdgo || 'N/A'}</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px;"><strong>Tipo:</strong></td>
                        <td style="padding: 5px;">Departamento</td>
                    </tr>
                </table>
                <div style="margin-top: 10px; padding: 8px; background: #f0f0f0;
                            border-radius: 3px; font-size: 0.85rem;">
                    <strong>📌 Dato:</strong> Click para hacer zoom
                </div>
            </div>
        `;

        layer.bindPopup(popupContent, {
            maxWidth: 300,
            className: 'custom-popup'
        });
    }

    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: clickFeature
    });
}
```

---

## Ejercicio 5: Avanzado - Estadísticas dinámicas

**Objetivo:** Mostrar estadísticas de los datos cargados

**Nivel:** Avanzado

**Tarea:**
Agregar sección en sidebar que muestre estadísticas de departamentos

**Archivos a modificar:**
- `index.html`
- `app.js`

**Solución:**

**1. HTML (agregar en sidebar):**
```html
<div class="sidebar-section">
    <h2>📈 Estadísticas</h2>
    <div id="stats-panel">
        <p>Cargando...</p>
    </div>
</div>
```

**2. JavaScript (en app.js, función loadDepartamentosWFS):**
```javascript
.then(data => {
    departamentosData = data;

    // ... código existente ...

    // AGREGAR: Calcular y mostrar estadísticas
    const statsPanel = document.getElementById('stats-panel');
    if (statsPanel) {
        const totalFeatures = data.features.length;
        const codigos = data.features.map(f => parseInt(f.properties.dpto_ccdgo));
        const minCodigo = Math.min(...codigos);
        const maxCodigo = Math.max(...codigos);

        statsPanel.innerHTML = `
            <ul style="list-style: none; padding: 0;">
                <li><strong>Total:</strong> ${totalFeatures}</li>
                <li><strong>Código min:</strong> ${minCodigo}</li>
                <li><strong>Código max:</strong> ${maxCodigo}</li>
            </ul>
        `;
    }
})
```

---

## Ejercicio 6: Muy Avanzado - Exportar a GeoJSON

**Objetivo:** Permitir descargar features seleccionadas

**Nivel:** Muy avanzado

**Tarea:**
Agregar botón para exportar departamentos filtrados a archivo GeoJSON

**Solución:**

**1. HTML (en sidebar):**
```html
<div class="sidebar-section">
    <h2>💾 Exportar</h2>
    <button id="export-button" class="btn-primary">Descargar GeoJSON</button>
</div>
```

**2. JavaScript:**
```javascript
document.addEventListener('DOMContentLoaded', function() {
    const exportButton = document.getElementById('export-button');

    if (exportButton) {
        exportButton.addEventListener('click', function() {
            if (!departamentosData) {
                alert('No hay datos para exportar');
                return;
            }

            // Convertir a string JSON
            const json = JSON.stringify(departamentosData, null, 2);

            // Crear blob
            const blob = new Blob([json], { type: 'application/json' });

            // Crear enlace de descarga
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'departamentos.geojson';
            a.click();

            // Limpiar
            URL.revokeObjectURL(url);
        });
    }
});
```

---

## Proyecto Final: Dashboard Completo

**Objetivo:** Integrar múltiples funcionalidades en una aplicación completa

**Nivel:** Experto

**Requisitos:**

1. **Múltiples capas WFS:**
   - Departamentos
   - Municipios
   - Ríos (si está disponible)

2. **Filtros avanzados:**
   - Por nombre (búsqueda)
   - Por código (rango)
   - Por área (si está disponible)

3. **Estadísticas:**
   - Total de features
   - Feature seleccionada
   - Área total (si está disponible)

4. **Gráficos:**
   - Usar Chart.js para mostrar distribución de datos

5. **Exportación:**
   - Descargar features filtradas
   - Formato GeoJSON y CSV

**Estructura sugerida:**

```
webapp/static/js/
├── app.js (principal)
├── layers.js (gestión de capas)
├── filters.js (filtros)
├── stats.js (estadísticas)
└── export.js (exportación)
```

---

## Recursos para Ejercicios

### Documentación

- **Leaflet:** https://leafletjs.com/reference.html
- **GeoServer CQL:** https://docs.geoserver.org/stable/en/user/filter/ecql_reference.html
- **Chart.js:** https://www.chartjs.org/docs/latest/

### Datos de prueba

Puedes crear capas adicionales en GeoServer usando:
- Shapefiles del IGAC
- Datos de OpenStreetMap
- GeoPackage personalizados

---

## Resumen

Has practicado:

- Agregar capas base
- Estilos dinámicos basados en atributos
- Filtros CQL en servidor
- Popups personalizados
- Estadísticas dinámicas
- Exportación de datos

---

**[⬅️ Módulo 8: Troubleshooting](08_TROUBLESHOOTING.md)** | **[Volver al Índice](README.md)** | **[Siguiente: Módulo 10 - Anexos ➡️](10_ANEXOS.md)**
