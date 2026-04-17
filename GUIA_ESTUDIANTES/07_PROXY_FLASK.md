# Módulo 7: Proxy Flask

## Objetivos de Aprendizaje

Al completar este módulo, comprenderás:

- 🔄 La implementación completa del proxy en Flask
- 🛡️ Cómo se resuelve el problema de CORS
- 🔀 El enrutamiento de peticiones WMS y WFS
- ⚠️ El manejo de errores y timeouts
- 🔧 Configuración de flask-cors

---

## 7.1 Ubicación y Contexto

**Archivo:** `webapp/app.py`
**Función del proxy:** Líneas 320-363

El proxy es la pieza clave que permite que la aplicación web funcione sin problemas de CORS al consumir servicios WFS de GeoServer.

---

## 7.2 Código Completo del Proxy

```python
@app.route('/api/geoserver-proxy')
def geoserver_proxy():
    """Proxy para peticiones a GeoServer (soluciona problema de CORS)"""
    try:
        # URL base de GeoServer
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
        print("url:", url)
        print("params:", params)
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

---

## 7.3 Configuración de CORS

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
```

**¿Qué hace `CORS(app)`?**
- Agrega headers CORS a todas las respuestas
- Permite peticiones desde cualquier origen
- Headers agregados: `Access-Control-Allow-Origin: *`

---

## 7.4 Resumen

Has aprendido la implementación completa del proxy Flask que resuelve CORS y enruta peticiones a GeoServer.

---

**[⬅️ Módulo 6: JavaScript Parte 2](06_JAVASCRIPT_PARTE_2.md)** | **[Volver al Índice](README.md)** | **[Siguiente: Módulo 8 - Troubleshooting ➡️](08_TROUBLESHOOTING.md)**
