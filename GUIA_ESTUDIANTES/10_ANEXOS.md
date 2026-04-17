# Módulo 10: Anexos - Recursos Adicionales

## 10.1 Glosario de Términos

### Términos Generales

**API (Application Programming Interface)**
- Interfaz para comunicación entre aplicaciones
- Ejemplo: Leaflet API, fetch API

**CORS (Cross-Origin Resource Sharing)**
- Política de seguridad de navegadores
- Bloquea peticiones entre orígenes diferentes
- Solución: Proxy servidor

**CDN (Content Delivery Network)**
- Red de servidores para distribuir contenido
- Usado para Leaflet CSS/JS
- Ejemplo: unpkg.com

**DOM (Document Object Model)**
- Representación del HTML como árbol de objetos
- JavaScript manipula el DOM

**GeoJSON**
- Formato JSON para datos geográficos
- Estándar abierto
- Usado por WFS

### Términos SIG

**Bounding Box (bbox)**
- Rectángulo que contiene geometrías
- Formato: minx,miny,maxx,maxy

**CRS/SRS (Coordinate Reference System / Spatial Reference System)**
- Sistema de coordenadas
- EPSG:4326 = WGS84 (lat/lon)
- EPSG:3857 = Web Mercator (metros)

**Feature**
- Objeto geográfico con geometría y atributos
- Ejemplo: Un departamento

**FeatureCollection**
- Colección de features en GeoJSON

**Layer (Capa)**
- Conjunto de datos geográficos
- Ejemplo: Capa de departamentos

**Tile**
- Cuadrado de 256x256 píxeles del mapa
- Mapas se dividen en tiles

**Workspace**
- Contenedor de capas en GeoServer
- Organiza proyectos

### Términos OGC

**GetCapabilities**
- Operación para obtener metadatos del servicio
- Disponible en WMS y WFS

**GetFeature**
- Operación WFS para obtener features

**GetMap**
- Operación WMS para obtener imagen del mapa

**OGC (Open Geospatial Consortium)**
- Organización de estándares geoespaciales

**WFS (Web Feature Service)**
- Estándar OGC para features vectoriales
- Retorna GeoJSON, GML, etc.

**WMS (Web Map Service)**
- Estándar OGC para mapas como imágenes
- Retorna PNG, JPEG, etc.

---

## 10.2 Referencias y Documentación

### Documentación Oficial

**Leaflet**
- Sitio oficial: https://leafletjs.com/
- Referencia API: https://leafletjs.com/reference.html
- Tutoriales: https://leafletjs.com/examples.html
- Plugins: https://leafletjs.com/plugins.html

**GeoServer**
- Sitio oficial: https://geoserver.org/
- Documentación: https://docs.geoserver.org/stable/en/user/
- WMS Reference: https://docs.geoserver.org/stable/en/user/services/wms/reference.html
- WFS Reference: https://docs.geoserver.org/stable/en/user/services/wfs/reference.html
- CQL Filter: https://docs.geoserver.org/stable/en/user/filter/ecql_reference.html

**OGC Standards**
- OGC.org: https://www.ogc.org/
- WMS Standard: https://www.ogc.org/standards/wms
- WFS Standard: https://www.ogc.org/standards/wfs
- GeoJSON: https://geojson.org/

**Flask**
- Sitio oficial: https://flask.palletsprojects.com/
- Quickstart: https://flask.palletsprojects.com/en/latest/quickstart/
- flask-cors: https://flask-cors.readthedocs.io/

**JavaScript/Web**
- MDN Web Docs: https://developer.mozilla.org/
- JavaScript.info: https://javascript.info/
- Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

---

## 10.3 Herramientas Recomendadas

### Editores de Código

**Visual Studio Code** (Recomendado)
- Sitio: https://code.visualstudio.com/
- Extensiones útiles:
  - Python (Microsoft)
  - Prettier
  - ESLint
  - Live Server
  - Thunder Client

**Otros editores:**
- Sublime Text
- Atom
- PyCharm
- WebStorm

### Herramientas SIG Desktop

**QGIS** (Recomendado)
- Sitio: https://qgis.org/
- Uso: Visualizar capas de GeoServer
- Conectar a WMS/WFS de GeoServer

**ArcGIS Pro**
- Alternativa comercial
- Soporta servicios OGC

### Clientes REST

**Thunder Client** (VS Code Extension)
- Integrado en VS Code
- Probar endpoints HTTP

**Postman**
- Sitio: https://www.postman.com/
- Probar APIs REST
- Guardar colecciones

**cURL**
- Línea de comandos
- Incluido en Linux/Mac
- Windows: incluido en Windows 10+

### Navegadores

**Chrome DevTools**
- Network tab para inspeccionar peticiones
- Console para debugging JavaScript
- Elements para inspeccionar DOM/CSS

**Firefox Developer Tools**
- Similar a Chrome
- Buen debugging de CSS Grid/Flexbox

---

## 10.4 Datasets y Fuentes de Datos

### Colombia

**IGAC (Instituto Geográfico Agustín Codazzi)**
- Sitio: https://www.igac.gov.co/
- Datos oficiales de Colombia
- Shapefiles, cartografía

**DANE (Departamento Administrativo Nacional de Estadística)**
- Sitio: https://www.dane.gov.co/
- Datos estadísticos y geográficos
- Censos, mapas

**IDECA (Infraestructura de Datos Espaciales de Bogotá)**
- Sitio: https://www.ideca.gov.co/
- Datos de Bogotá
- Servicios WMS/WFS

### Internacional

**Natural Earth**
- Sitio: https://www.naturalearthdata.com/
- Datos globales gratuitos
- Varios niveles de detalle

**OpenStreetMap**
- Sitio: https://www.openstreetmap.org/
- Mapas colaborativos
- Exportar datos o usar APIs

**GADM (Database of Global Administrative Areas)**
- Sitio: https://gadm.org/
- Divisiones administrativas mundiales
- Formato Shapefile, GeoPackage

---

## 10.5 Librerías y Plugins Adicionales

### Leaflet Plugins

**Leaflet.draw**
- GitHub: https://github.com/Leaflet/Leaflet.draw
- Dibujar y editar features
- Uso: Edición de geometrías

**Leaflet.markercluster**
- GitHub: https://github.com/Leaflet/Leaflet.markercluster
- Agrupar markers cercanos
- Uso: Muchos puntos

**Leaflet.heat**
- GitHub: https://github.com/Leaflet/Leaflet.heat
- Mapas de calor
- Uso: Densidad de puntos

**Leaflet.TimeDimension**
- GitHub: https://github.com/socib/Leaflet.TimeDimension
- Datos temporales animados
- Uso: Series de tiempo

**Leaflet.Geocoder**
- Varios plugins disponibles
- Búsqueda de direcciones
- Uso: Geocodificación

### JavaScript Libraries

**Chart.js**
- Sitio: https://www.chartjs.org/
- Gráficos interactivos
- Uso: Visualizar estadísticas

**Turf.js**
- Sitio: https://turfjs.org/
- Análisis espacial en JavaScript
- Uso: Buffer, intersección, etc.

**Proj4js**
- GitHub: https://github.com/proj4js/proj4js
- Reproyección de coordenadas
- Uso: Transformar CRS

---

## 10.6 Tutoriales y Cursos

### Leaflet

**Leaflet Quick Start Guide**
- https://leafletjs.com/examples/quick-start/

**Leaflet on Mobile**
- https://leafletjs.com/examples/mobile/

**Using GeoJSON with Leaflet**
- https://leafletjs.com/examples/geojson/

### GeoServer

**GeoServer Quickstart**
- https://docs.geoserver.org/stable/en/user/gettingstarted/

**Publishing a Shapefile**
- https://docs.geoserver.org/stable/en/user/gettingstarted/shapefile-quickstart/

**Styling (SLD)**
- https://docs.geoserver.org/stable/en/user/styling/

### Flask

**Flask Mega-Tutorial**
- https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

**Flask RESTful**
- https://flask-restful.readthedocs.io/

---

## 10.7 Comunidades y Foros

### Stack Overflow

**Tags relevantes:**
- `[leaflet]`: https://stackoverflow.com/questions/tagged/leaflet
- `[geoserver]`: https://stackoverflow.com/questions/tagged/geoserver
- `[wfs]`: https://stackoverflow.com/questions/tagged/wfs
- `[flask]`: https://stackoverflow.com/questions/tagged/flask

### GIS Stack Exchange

- Sitio: https://gis.stackexchange.com/
- Comunidad especializada en SIG
- Preguntas sobre OGC, proyecciones, etc.

### GitHub

- Leaflet Issues: https://github.com/Leaflet/Leaflet/issues
- GeoServer: https://github.com/geoserver/geoserver

---

## 10.8 Próximos Pasos

### Mejorar esta aplicación

1. **Agregar más capas:**
   - Ríos, carreteras, ciudades
   - Capas temáticas (población, clima)

2. **Análisis espacial:**
   - Buffer de features
   - Intersección de capas
   - Medición de distancias

3. **Interactividad avanzada:**
   - Edición de features (WFS-T)
   - Dibujo de nuevas geometrías
   - Guardar cambios en GeoServer

4. **Visualización:**
   - Gráficos con Chart.js
   - Dashboards con estadísticas
   - Exportar mapas a PDF

### Aprender más

1. **PostGIS:**
   - Consultas espaciales SQL
   - Análisis avanzado en base de datos

2. **Styling (SLD/CSS):**
   - Estilos avanzados en GeoServer
   - Tematización de datos

3. **Optimización:**
   - Caché de tiles en GeoServer
   - Indexación espacial
   - Clustering de datos

4. **Despliegue:**
   - Docker Compose producción
   - NGINX como reverse proxy
   - HTTPS con Let's Encrypt

---

## 10.9 Licencias y Atribuciones

### Software utilizado

- **Leaflet:** BSD 2-Clause License
- **GeoServer:** GPL License
- **Flask:** BSD License
- **OpenStreetMap:** ODbL License

### Datos

- **IGAC:** Verificar términos de uso
- **Natural Earth:** Public Domain

### Esta guía

- Material educativo para curso de SIG
- Uso libre para estudiantes del curso

---

## 10.10 Contacto y Soporte

### Para este curso

- Consultar con instructor
- Revisar documentación oficial
- Participar en foros de la maestría

### Reportar errores

Si encuentras errores en esta guía:
1. Documentar el error
2. Incluir capturas de pantalla
3. Reportar al instructor

---

## Conclusión

¡Felicitaciones por completar la guía!

Has aprendido:
- ✅ Estándares OGC (WMS/WFS)
- ✅ Desarrollo web con HTML/CSS/JavaScript
- ✅ Mapas interactivos con Leaflet
- ✅ Servicios geoespaciales con GeoServer
- ✅ Backend con Flask y Python

**Continúa aprendiendo y experimentando con datos geoespaciales.**

---

**[⬅️ Módulo 9: Ejercicios](09_EJERCICIOS.md)** | **[Volver al Índice](README.md)**

---

*Última actualización: Abril 2026*
*Curso de Servicios Web Geográficos - Maestría en SIG*
