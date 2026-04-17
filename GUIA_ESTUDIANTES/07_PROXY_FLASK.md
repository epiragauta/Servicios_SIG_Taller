# Módulo 7: Proxy Flask - Agregar Código a app.py

## Objetivos de Aprendizaje

Al completar este módulo, habrás:

- Agregado el endpoint `/map-dpto` a app.py
- Implementado la función proxy `geoserver_proxy()`
- Comprendido la comunicación entre contenedores Docker
- Resuelto el problema de CORS
- Verificado que la aplicación funciona completamente

---

## 7.1 Contexto

El archivo `webapp/app.py` **ya existe** con código base de Flask. En este módulo agregarás dos bloques de código:

1. **Endpoint `/map-dpto`**: Para servir la página principal
2. **Función `geoserver_proxy()`**: Para proxy de peticiones WFS/WMS

---

## 7.2 Preparación: Entender la Arquitectura Docker

**IMPORTANTE:** Este proyecto se ejecuta completamente en Docker usando Docker Compose.

### Servicios en docker-compose.yml

```yaml
services:
  postgis:      # Base de datos PostgreSQL/PostGIS (puerto 5432)
  geoserver:    # Servidor de mapas OGC (puerto 8080)
  webapp:       # Aplicación Flask (puerto 5000)
```

### Red Docker Interna

Docker crea automáticamente una red donde **los servicios se comunican entre sí usando sus nombres**:

```
┌─────────────────────────────────────────────────────────┐
│              RED DOCKER (servicios_sig_taller)          │
│                                                         │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐      │
│  │ webapp   │─────→│geoserver │      │ postgis  │      │
│  │ :5000    │      │ :8080    │←─────│ :5432    │      │
│  └──────────┘      └──────────┘      └──────────┘      │
│       ↑                                                 │
└───────┼─────────────────────────────────────────────────┘
        │
        │ Port mapping
        ↓
┌─────────────────────────┐
│   HOST (tu computadora) │
│   localhost:5000        │
│   localhost:8080        │
│   localhost:5432        │
└─────────────────────────┘
```

### Nombres de host según contexto

| Desde dónde | Para acceder a GeoServer | Para acceder a Flask |
|-------------|-------------------------|---------------------|
| **Código Python (webapp)** | `geoserver:8080` | - |
| **Navegador (tu computadora)** | `localhost:8080` | `localhost:5000` |
| **JavaScript (navegador)** | `localhost:8080` (con CORS!) | `localhost:5000` |

**Clave:** En el código Python del proxy, usamos `http://geoserver:8080` porque **ambos contenedores están en la misma red Docker**.

---

## 7.3 Paso 1: Localizar Dónde Agregar el Código

Abre el archivo `webapp/app.py` en tu editor.

Busca la sección de rutas (routes). Debería verse similar a:

```python
# Rutas existentes
@app.route('/')
def index():
    return render_template('index.html')

# ... posiblemente otras rutas ...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

Agregaremos el código **ANTES** de `if __name__ == '__main__':`.

---

## 7.4 Paso 2: Agregar Endpoint /map-dpto

Agrega este bloque de código antes de `if __name__ == '__main__':`:

```python
@app.route('/map-dpto')
def map_dpto():
    """Página principal del visor de departamentos"""
    return render_template('app/index.html')
```

**Explicación:**

**`@app.route('/map-dpto')`**
- Decorador que define la ruta URL
- La aplicación responderá en `http://localhost:5000/map-dpto`

**`def map_dpto():`**
- Función que se ejecuta cuando se visita la ruta
- Nombre de función: convención snake_case

**`return render_template('app/index.html')`**
- Renderiza la plantilla Jinja2 que creaste en Módulo 3
- Flask busca en directorio `webapp/templates/`
- Ruta completa: `webapp/templates/app/index.html`

**Resultado:**
- Visitar `http://localhost:5000/map-dpto` → Muestra tu aplicación de mapas

---

## 7.5 Paso 3: Importar Módulos Necesarios

Antes de agregar el proxy, verifica que app.py tenga estas importaciones al inicio del archivo:

```python
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS
import requests
```

**Si faltan:**

**`Response`:**
- Ya debería estar en `from flask import ...`
- Si no, agrégalo a la línea existente

**`requests`:**
- Agregar línea: `import requests`
- **IMPORTANTE:** Esta librería está en `requirements.txt`

**`flask_cors`:**
- Verifica que esté en `requirements.txt`: `flask-cors`
- Importación: `from flask_cors import CORS`

**Configuración de CORS (debe existir después de crear `app`):**
```python
app = Flask(__name__)
CORS(app)  # ← Debe estar presente
```

**¿Qué hace `CORS(app)`?**
- Agrega headers CORS a todas las respuestas de Flask
- Permite peticiones desde cualquier origen
- Header agregado: `Access-Control-Allow-Origin: *`

---

## 7.6 Paso 4: Agregar Función Proxy

Agrega este bloque de código antes de `if __name__ == '__main__':` (después del endpoint `/map-dpto`):

```python
@app.route('/api/geoserver-proxy')
def geoserver_proxy():
    """Proxy para peticiones a GeoServer (soluciona problema de CORS)"""
    try:
        # URL base de GeoServer
        # IMPORTANTE: Usa 'geoserver' (nombre del servicio Docker)
        # NO 'localhost', porque estamos dentro del contenedor webapp
        geoserver_base = 'http://geoserver:8080/geoserver'

        # Obtener el servicio y parámetros de la petición
        service = request.args.get('service', '')

        # Construir la URL completa a GeoServer
        if service.lower() == 'wfs':
            # Petición WFS
            url = f"{geoserver_base}/ne/wfs"
        elif service.lower() == 'wms':
            # Petición WMS
            url = f"{geoserver_base}/ne/wms"
        else:
            # Ruta genérica
            url = f"{geoserver_base}{request.path.replace('/api/geoserver-proxy', '')}"

        # Copiar todos los parámetros de query
        params = request.args.to_dict()

        # Hacer la petición a GeoServer
        response = requests.get(url, params=params, timeout=30)

        # Crear respuesta con los headers apropiados
        if response.headers.get('content-type'):
            return Response(
                response.content,
                status=response.status_code,
                content_type=response.headers.get('content-type')
            )
        return Response(response.content, status=response.status_code)

    except requests.exceptions.Timeout:
        return jsonify({'error': 'La petición a GeoServer tardó demasiado'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error conectando a GeoServer: {str(e)}'}), 502
    except Exception as e:
        print(f"Error en proxy de GeoServer: {e}")
        return jsonify({'error': str(e)}), 500
```

**Explicación detallada:**

### URL base de GeoServer

```python
geoserver_base = 'http://geoserver:8080/geoserver'
```

**MUY IMPORTANTE:**
- Usa `geoserver:8080`, NO `localhost:8080`
- `geoserver` es el nombre del servicio en docker-compose.yml
- Docker resuelve `geoserver` a la IP interna del contenedor

**¿Por qué NO localhost?**
```python
# INCORRECTO ❌
geoserver_base = 'http://localhost:8080/geoserver'
# localhost dentro del contenedor webapp apunta a SÍ MISMO, no a GeoServer

# CORRECTO ✅
geoserver_base = 'http://geoserver:8080/geoserver'
# Docker resuelve 'geoserver' al contenedor de GeoServer
```

### Obtener parámetros

```python
service = request.args.get('service', '')
```
- `request.args`: Parámetros de query string
- Ejemplo: `/api/geoserver-proxy?service=WFS&...` → `service = 'WFS'`

### Construir URL según servicio

```python
if service.lower() == 'wfs':
    url = f"{geoserver_base}/ne/wfs"
elif service.lower() == 'wms':
    url = f"{geoserver_base}/ne/wms"
else:
    url = f"{geoserver_base}{request.path.replace('/api/geoserver-proxy', '')}"
```

**Ejemplo de URLs generadas:**
- WFS: `http://geoserver:8080/geoserver/ne/wfs`
- WMS: `http://geoserver:8080/geoserver/ne/wms`

**f-strings:**
```python
f"{variable}"  # Interpola variable en string
```

### Copiar parámetros

```python
params = request.args.to_dict()
```
- Convierte parámetros de Flask a diccionario
- Ejemplo: `{'service': 'WFS', 'version': '2.0.0', ...}`

### Hacer petición a GeoServer

```python
response = requests.get(url, params=params, timeout=30)
```
- `requests.get()`: Petición HTTP GET
- `params`: Parámetros de query
- `timeout=30`: Espera máximo 30 segundos

**Flujo:**
1. JavaScript hace: `fetch('/api/geoserver-proxy?service=WFS&...')`
2. Flask recibe petición
3. Flask hace: `requests.get('http://geoserver:8080/geoserver/ne/wfs?service=WFS&...')`
4. GeoServer responde a Flask
5. Flask responde a JavaScript

### Retornar respuesta

```python
return Response(
    response.content,
    status=response.status_code,
    content_type=response.headers.get('content-type')
)
```
- `response.content`: Cuerpo de la respuesta (bytes)
- `status`: Código HTTP (200, 404, etc.)
- `content_type`: Tipo MIME (`application/json`, `image/png`, etc.)

### Manejo de errores

```python
except requests.exceptions.Timeout:
    return jsonify({'error': '...'}), 504
```
- `Timeout`: Petición tardó más de 30 segundos
- `RequestException`: Error de red, GeoServer caído
- `Exception`: Cualquier otro error

**Códigos HTTP de error:**
- `502 Bad Gateway`: Error conectando a GeoServer
- `504 Gateway Timeout`: Petición tardó demasiado
- `500 Internal Server Error`: Error inesperado

---

## 7.7 Paso 5: Verificar el Código Completo

Tu archivo `app.py` debería tener esta estructura:

```python
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# ... otras rutas existentes ...

@app.route('/map-dpto')
def map_dpto():
    """Página principal del visor de departamentos"""
    return render_template('app/index.html')

@app.route('/api/geoserver-proxy')
def geoserver_proxy():
    """Proxy para peticiones a GeoServer (soluciona problema de CORS)"""
    try:
        geoserver_base = 'http://geoserver:8080/geoserver'
        service = request.args.get('service', '')

        if service.lower() == 'wfs':
            url = f"{geoserver_base}/ne/wfs"
        elif service.lower() == 'wms':
            url = f"{geoserver_base}/ne/wms"
        else:
            url = f"{geoserver_base}{request.path.replace('/api/geoserver-proxy', '')}"

        params = request.args.to_dict()
        response = requests.get(url, params=params, timeout=30)

        if response.headers.get('content-type'):
            return Response(
                response.content,
                status=response.status_code,
                content_type=response.headers.get('content-type')
            )
        return Response(response.content, status=response.status_code)

    except requests.exceptions.Timeout:
        return jsonify({'error': 'La petición a GeoServer tardó demasiado'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error conectando a GeoServer: {str(e)}'}), 502
    except Exception as e:
        print(f"Error en proxy de GeoServer: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

---

## 7.8 Checkpoint: Probar la Aplicación Completa

### Paso 1: Guardar el archivo

Asegúrate de que `webapp/app.py` está guardado.

### Paso 2: Reiniciar el contenedor webapp

```bash
docker-compose restart webapp
```

**¿Por qué reiniciar?**
- Los cambios en código Python requieren reinicio
- Los volúmenes Docker montan el código, pero Flask necesita reiniciar

### Paso 3: Ver logs del contenedor

```bash
docker-compose logs -f webapp
```

**Logs esperados:**
```
webapp_1     |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
webapp_1     |  * Restarting with stat
webapp_1     |  * Debugger is active!
```

Si ves errores de importación:
```
ModuleNotFoundError: No module named 'requests'
```

**Solución:**
```bash
# Verificar requirements.txt tiene 'requests'
cat webapp/requirements.txt | grep requests

# Si falta, agregarlo
echo "requests>=2.28.0" >> webapp/requirements.txt

# Reconstruir contenedor
docker-compose build webapp
docker-compose up -d webapp
```

### Paso 4: Verificar que GeoServer está ejecutándose

```bash
docker-compose ps geoserver
```

**Resultado esperado:**
```
Name              State       Ports
geoserver   Up (healthy)   0.0.0.0:8080->8080/tcp
```

Si no está "healthy":
```bash
# Ver logs de GeoServer
docker-compose logs geoserver

# Esperar 1-2 minutos (GeoServer tarda en iniciar)
```

### Paso 5: Abrir en navegador

Visita: http://localhost:5000/map-dpto

### Paso 6: Verificar resultado completo

**Página carga correctamente:**
- HTML, CSS, JavaScript cargados
- Mapa visible con controles

**Capas WMS funcionan:**
- Activar checkbox "Departamentos (WMS)" → Aparecen departamentos
- Activar checkbox "Municipios (WMS)" → Aparecen municipios

**Capa WFS carga automáticamente:**
- Al cargar página, se agrega "Departamentos Interactivos (WFS)" al control
- Polígonos amarillos visibles
- Vista ajustada a Colombia

**Interactividad funciona:**
- Hover sobre departamento → Resalta (violeta)
- Control de información actualiza (superior izquierda)
- Click en departamento → Zoom + popup
- Búsqueda funciona → Click en resultado hace zoom

**Consola sin errores (F12):**
- "Iniciando aplicación..."
- "Departamentos cargados: 33"
- Sin errores 404, 500, o CORS

### Paso 7: Verificar peticiones en DevTools

**Network Tab (F12):**

1. Buscar petición a `/api/geoserver-proxy`
2. Verificar:
   - **Status:** 200 OK
   - **Response:** JSON con GeoJSON FeatureCollection
   - **Headers → Response Headers:**
     - `Access-Control-Allow-Origin: *` (CORS configurado)
     - `Content-Type: application/json`

**Si Status es 502:**
- GeoServer no está ejecutándose o no es accesible desde webapp

**Si Status es 504:**
- Petición tardó más de 30 segundos (timeout)

**Si Status es 500:**
- Error en código Python (ver logs de webapp)

---

## 7.9 Debugging de Problemas Comunes

### Problema: Error 502 "Error conectando a GeoServer"

**Diagnóstico:**
```bash
# Verificar conectividad desde webapp a geoserver
docker exec webapp ping -c 3 geoserver

# Si falla "ping: unknown host geoserver"
# Los contenedores no están en la misma red
```

**Solución:**
```bash
# Recrear servicios (Docker recrea la red)
docker-compose down
docker-compose up -d

# Verificar red
docker network ls
docker network inspect servicios_sig_taller_default
```

### Problema: ModuleNotFoundError

**Diagnóstico:**
```bash
# Verificar dependencias instaladas
docker exec webapp pip list
```

**Solución:**
```bash
# Verificar requirements.txt
cat webapp/requirements.txt

# Debe tener:
# flask-cors
# requests>=2.28.0

# Reconstruir sin caché
docker-compose build --no-cache webapp
docker-compose up -d webapp
```

### Problema: Cambios en código no se reflejan

**Causa:**
- Volumen no montado correctamente o Flask no detecta cambios

**Solución:**
```bash
# Detener y levantar de nuevo
docker-compose down
docker-compose up -d

# Ver logs
docker-compose logs -f webapp
```

### Problema: GeoServer tarda mucho en responder

**Causa:**
- GeoServer procesando petición pesada

**Solución:**
- Esperar (GeoServer puede tardar 5-10 segundos la primera vez)
- Aumentar timeout en proxy:
  ```python
  response = requests.get(url, params=params, timeout=60)  # 60 segundos
  ```

---

## 7.10 Flujo Completo en Entorno Docker

Ahora que todo está funcionando, entiende el flujo completo:

```
1. NAVEGADOR (localhost:5000/map-dpto)
   │ Usuario visita la página
   │ GET http://localhost:5000/map-dpto
   ↓

2. CONTENEDOR WEBAPP (Flask)
   │ @app.route('/map-dpto')
   │ return render_template('app/index.html')
   │ Renderiza HTML con Jinja2
   ↓

3. NAVEGADOR
   │ Recibe HTML, carga CSS y JavaScript
   │ app.js ejecuta: loadDepartamentosWFS()
   │ fetch('/api/geoserver-proxy?service=WFS&...')
   ↓

4. CONTENEDOR WEBAPP (Flask)
   │ @app.route('/api/geoserver-proxy')
   │ geoserver_base = 'http://geoserver:8080/geoserver'
   │ url = 'http://geoserver:8080/geoserver/ne/wfs'
   │ requests.get(url, params=params)
   ↓

5. RED DOCKER INTERNA
   │ Docker resuelve 'geoserver' → IP del contenedor geoserver
   ↓

6. CONTENEDOR GEOSERVER
   │ Recibe petición WFS GetFeature
   │ Consulta datastore (PostGIS/Shapefile)
   │ Serializa a GeoJSON
   │ Retorna JSON
   ↓

7. CONTENEDOR WEBAPP (Flask)
   │ Recibe GeoJSON de GeoServer
   │ return Response(response.content, ...)
   │ CORS headers agregados por CORS(app)
   ↓

8. NAVEGADOR
   │ fetch() recibe GeoJSON
   │ .then(data => L.geoJSON(data).addTo(map))
   │ Mapa muestra polígonos interactivos ✅
```

**¿Por qué funciona sin CORS?**
- **Entre navegador y Flask:** Mismo origen o CORS habilitado
- **Entre Flask y GeoServer:** Comunicación servidor-a-servidor (sin CORS)

---

## 7.11 Modificar el Proxy (Edición en Vivo)

Si necesitas modificar el código del proxy:

**1. Editar archivo** `webapp/app.py`

**2. El contenedor webapp monta el código como volumen:**
```yaml
# En docker-compose.yml
volumes:
  - ./webapp:/app
```

**3. Los cambios se detectan automáticamente** (modo desarrollo con `debug=True`)

**4. Si no se actualizan, reiniciar:**
```bash
docker-compose restart webapp
```

**5. Ver logs para confirmar:**
```bash
docker-compose logs -f webapp
```

---

## 7.12 Resumen

Has aprendido:

- Agregar endpoint `/map-dpto` a app.py existente
- Implementar función proxy completa
- Usar nombres de servicio Docker (`geoserver:8080`)
- Manejar peticiones WFS y WMS en el proxy
- Configurar CORS con flask-cors
- Manejar errores (timeout, conexión, excepciones)
- Debugging con logs de Docker
- Verificar conectividad entre contenedores

### Código agregado a app.py

- Endpoint `/map-dpto` (~3 líneas)
- Función `geoserver_proxy()` (~40 líneas)
- Total agregado: ~43 líneas

### Conceptos clave de Docker

| Concepto | Descripción |
|----------|-------------|
| **Nombre de servicio** | `geoserver`, `postgis`, `webapp` (en docker-compose.yml) |
| **Red Docker** | Red interna donde los servicios se comunican |
| **Port mapping** | `5000:5000`, `8080:8080` (host:contenedor) |
| **Volumen** | `./webapp:/app` (código local montado en contenedor) |
| **CORS** | Resuelto con flask-cors y comunicación servidor-a-servidor |

### Comandos Docker útiles

```bash
# Gestión de servicios
docker-compose ps                    # Ver estado de servicios
docker-compose logs -f webapp        # Ver logs en tiempo real
docker-compose restart webapp        # Reiniciar un servicio
docker-compose down                  # Detener todos los servicios
docker-compose up -d                 # Levantar todos los servicios

# Reconstrucción
docker-compose build webapp          # Reconstruir con caché
docker-compose build --no-cache webapp  # Reconstruir sin caché

# Debugging
docker exec webapp pip list          # Ver dependencias instaladas
docker exec webapp curl http://geoserver:8080/geoserver/web/
docker exec webapp ping geoserver    # Verificar conectividad
docker exec -it webapp bash          # Acceder al shell del contenedor

# Verificación de red
docker network ls                    # Listar redes Docker
docker network inspect servicios_sig_taller_default
```

### Aplicación completa funcionando

Has completado la implementación completa:
- HTML (Módulo 3)
- CSS (Módulo 4)
- JavaScript Parte 1 - WMS (Módulo 5)
- JavaScript Parte 2 - WFS (Módulo 6)
- Proxy Flask (Módulo 7)

**Tu aplicación ahora:**
- Muestra mapa interactivo de Colombia
- Carga capas WMS de GeoServer
- Carga datos WFS a través de proxy
- Permite interactividad (hover, click, zoom)
- Implementa búsqueda de departamentos
- Todo funcionando en entorno Docker

### Próximo módulo

En el **Módulo 8 (Troubleshooting)**, aprenderás a:
- Diagnosticar problemas comunes
- Usar herramientas de debugging
- Resolver errores de Docker, GeoServer, CORS
- Optimizar rendimiento

---

**[⬅️ Módulo 6: JavaScript Parte 2](06_JAVASCRIPT_PARTE_2.md)** | **[Volver al Índice](README.md)** | **[Siguiente: Módulo 8 - Troubleshooting ➡️](08_TROUBLESHOOTING.md)**
