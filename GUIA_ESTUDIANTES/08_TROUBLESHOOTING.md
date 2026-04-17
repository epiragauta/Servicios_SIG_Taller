# Módulo 8: Troubleshooting - Solución de Problemas

## Objetivos

Al completar este módulo, serás capaz de:

- Diagnosticar problemas comunes
- Aplicar soluciones paso a paso
- Prevenir errores frecuentes
- Usar herramientas de debugging

---

## 8.1 Problemas de GeoServer

### Error: "No se pudieron cargar los datos de departamentos"

**Síntomas:**
- Alert en el navegador
- Error en consola: `Error cargando WFS`

**Causas posibles:**

1. **GeoServer no está ejecutándose**

**Diagnóstico:**
```bash
curl http://localhost:8080/geoserver/web/
```

**Solución:**
```bash
docker ps  # Verificar contenedor
docker-compose up -d geoserver  # Iniciar si no está
```

2. **Capa no existe o nombre incorrecto**

**Diagnóstico:**
- Ir a http://localhost:8080/geoserver/web/
- Login: admin/geoserver
- Layers → Buscar "departamentos"

**Solución:**
```javascript
// Verificar nombre de capa en app.js línea 92:
const wfsUrl = `/api/geoserver-proxy?...&typeName=ne:departamentos...`;
//                                                        ↑↑↑↑↑↑↑↑↑↑↑↑↑↑
// Debe coincidir con el nombre en GeoServer
```

3. **Workspace incorrecto**

**Solución:**
- Verificar que workspace `ne` existe en GeoServer
- Cambiar en código si es diferente

---

## 8.2 Problemas de CORS

### Error: "blocked by CORS policy"

**Síntoma en consola:**
```
Access to fetch at 'http://localhost:8080/geoserver/ne/wfs'
from origin 'http://localhost:5000' has been blocked by CORS policy
```

**Causa:**
- Petición directa a GeoServer desde JavaScript (sin proxy)

**Solución:**

 **Usar el proxy:**
```javascript
// INCORRECTO 
fetch('http://localhost:8080/geoserver/ne/wfs?...')

// CORRECTO 
fetch('/api/geoserver-proxy?service=WFS&...')
```

 **Verificar flask-cors:**
```bash
pip install flask-cors
```

```python
# En app.py verificar:
from flask_cors import CORS
CORS(app)  # ← Debe estar presente
```

---

## 8.3 Problemas del Mapa

### Error: "Map container not found"

**Síntoma:**
- Mapa no aparece
- Error en consola

**Causas:**

1. **Div #map no existe**

**Solución:**
```html
<!-- Verificar en index.html: -->
<div id="map"></div>
```

2. **Script se ejecuta antes del DOM**

**Solución:**
```javascript
// app.js línea 344:
window.addEventListener('load', function() {
    loadDepartamentosWFS();
});
```

### Mapa invisible (0px × 0px)

**Causa:**
- CSS sin dimensiones

**Solución:**
```css
/* app.css debe tener: */
#map {
    width: 100%;
    height: 100%;
}

.map-container {
    flex: 1;
}
```

### Capas WMS no se ven

**Diagnósticos:**

1. **Verificar orden de capas:**
```javascript
// Última capa agregada queda arriba
departamentosWMS.addTo(map);  // Abajo
municipiosWMS.addTo(map);     // Encima (puede tapar)
```

2. **Verificar transparencia:**
```javascript
L.tileLayer.wms(url, {
    transparent: true  // ← Debe ser true
});
```

3. **Verificar zoom level:**
- Algunas capas tienen restricciones de escala en GeoServer
- Hacer zoom in/out para verificar

---

## 8.4 Problemas de Conexión

### Error: "Connection refused to geoserver:8080"

**Causa:**
- Contenedores no están en la misma red Docker

**Solución:**
```bash
# Verificar redes
docker network ls

# Crear red compartida
docker network create sig-network

# Conectar contenedores
docker network connect sig-network flask-container
docker network connect sig-network geoserver
```

### Flask no puede conectar a GeoServer

**Diagnóstico:**
```bash
# Desde contenedor de Flask:
docker exec -it flask-container ping geoserver
```

**Solución:**
```python
# En app.py, verificar URL:
geoserver_base = 'http://geoserver:8080/geoserver'
#                         ↑↑↑↑↑↑↑↑
# Debe ser nombre del contenedor, no "localhost"
```

---

## 8.5 Problemas de Rendimiento

### Mapa lento con muchas features

**Causa:**
- Capa WFS con miles de features

**Soluciones:**

1. **Usar WMS en lugar de WFS:**
```javascript
// Para capas grandes (>1000 features), usar WMS
const municipiosWMS = L.tileLayer.wms(GEOSERVER_URL, {
    layers: 'ne:municipios'
});
```

2. **Limitar features en WFS:**
```javascript
const wfsUrl = `/api/geoserver-proxy?service=WFS&...&maxFeatures=100`;
```

3. **Usar filtros espaciales (bbox):**
```javascript
const bounds = map.getBounds();
const bbox = `${bounds.getWest()},${bounds.getSouth()},${bounds.getEast()},${bounds.getNorth()}`;
const wfsUrl = `/api/geoserver-proxy?service=WFS&...&bbox=${bbox}`;
```

---

## 8.6 Herramientas de Debugging

### Chrome DevTools

**Network Tab:**
```
1. Abrir DevTools (F12)
2. Tab "Network"
3. Filtrar por "XHR" o "Fetch"
4. Buscar peticiones a /api/geoserver-proxy
5. Verificar:
   - Status: 200 OK
   - Response: JSON válido
   - Headers: Content-Type correcto
```

**Console Tab:**
```
- Ver errores de JavaScript
- Ver console.log() de app.js
- Probar código en vivo:
  > map.getZoom()
  > departamentosData
```

### Pruebas de endpoints

**Probar WFS directamente:**
```bash
curl "http://localhost:8080/geoserver/ne/wfs?service=WFS&version=2.0.0&request=GetFeature&typeName=ne:departamentos&maxFeatures=1&outputFormat=application/json"
```

**Probar proxy:**
```bash
curl "http://localhost:5000/api/geoserver-proxy?service=WFS&version=2.0.0&request=GetFeature&typeName=ne:departamentos&maxFeatures=1&outputFormat=application/json"
```

---

## 8.7 Checklist de Verificación

Cuando algo no funciona, verificar en orden:

- [ ] ¿GeoServer está ejecutándose? (`docker ps`)
- [ ] ¿Flask está ejecutándose? (`python app.py`)
- [ ] ¿Capas existen en GeoServer?
- [ ] ¿Nombres de capas son correctos en el código?
- [ ] ¿Hay errores en consola del navegador?
- [ ] ¿Peticiones WFS usan el proxy?
- [ ] ¿flask-cors está instalado?
- [ ] ¿Div #map existe en HTML?
- [ ] ¿CSS define dimensiones del mapa?

---

## 8.8 Resumen

Has aprendido a diagnosticar y resolver los problemas más comunes en aplicaciones Leaflet + GeoServer.

---

**[⬅️ Módulo 7: Proxy Flask](07_PROXY_FLASK.md)** | **[Volver al Índice](README.md)** | **[Siguiente: Módulo 9 - Ejercicios ➡️](09_EJERCICIOS.md)**
