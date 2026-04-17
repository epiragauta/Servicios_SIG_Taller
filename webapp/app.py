#!/usr/bin/env python3
"""
Aplicación Flask para visualizar datos geoespaciales del Amazonas
usando Folium y datos de PostgreSQL/PostGIS
"""

import os
from flask import Flask, render_template, jsonify, request, Response
import psycopg2
from psycopg2.extras import RealDictCursor
import folium
from folium.plugins import MarkerCluster
import json
import requests
from urllib.parse import urlencode
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'postgis'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'geodatos'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres')
}


def get_db_connection():
    """Crear conexión a la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None


def get_departamento_data():
    """Obtener datos del departamento del Amazonas"""
    conn = get_db_connection()
    if not conn:
        return None

    try:
        query = """
        SELECT
            dpto_ccdgo as codigo,
            dpto_cnmbr as nombre,
            ST_AsGeoJSON(ST_Transform(geom, 4326)) as geojson
        FROM dpto_amazonas;
        """

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                return {
                    'codigo': result['codigo'],
                    'nombre': result['nombre'],
                    'geojson': json.loads(result['geojson'])
                }
            return None
    except Exception as e:
        print(f"Error obteniendo datos del departamento: {e}")
        return None
    finally:
        conn.close()


def get_puntos_data():
    """Obtener datos de puntos administrativos"""
    conn = get_db_connection()
    if not conn:
        return []

    try:
        query = """
        SELECT
            gid,
            nombre_geo,
            codigo_nom,
            symbol,
            proyecto,
            fecha,
            escala,
            ST_AsGeoJSON(ST_Transform(geom, 4326)) as geojson
        FROM puntos_administrativos
        ORDER BY nombre_geo;
        """

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

            puntos = []
            for row in results:
                punto = dict(row)
                punto['geojson'] = json.loads(row['geojson'])
                puntos.append(punto)

            return puntos
    except Exception as e:
        print(f"Error obteniendo puntos administrativos: {e}")
        return []
    finally:
        conn.close()


def get_estadisticas():
    """Obtener estadísticas de la base de datos"""
    conn = get_db_connection()
    if not conn:
        return None

    try:
        query = """
        SELECT
            (SELECT COUNT(*) FROM dpto_amazonas) as total_departamentos,
            (SELECT COUNT(*) FROM puntos_administrativos) as total_puntos,
            (SELECT COUNT(DISTINCT proyecto) FROM puntos_administrativos) as total_proyectos,
            (SELECT ST_Area(ST_Transform(geom, 32618)) / 1000000
             FROM dpto_amazonas) as area_km2;
        """

        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return dict(result) if result else None
    except Exception as e:
        print(f"Error obteniendo estadísticas: {e}")
        return None
    finally:
        conn.close()


@app.route('/')
def index():
    """Página principal con el mapa"""
    return render_template('index.html')

@app.route('/visor')
def visor():
    """Página secundaria con el mapa"""
    return render_template('visor.html')

@app.route('/map-dpto')
def map_dpto():
    """Página secundaria con el mapa"""
    return render_template('app/index.html')

@app.route('/mapa')
def mapa():
    """Generar y retornar el mapa de Folium"""
    try:
        # Obtener datos
        departamento = get_departamento_data()
        puntos = get_puntos_data()

        # Crear mapa inicial
        m = folium.Map(
            tiles='OpenStreetMap',
            name='Mapa Base',
        )

        # Agregar capa del departamento y calcular bounds
        if departamento:
            geojson_layer = folium.GeoJson(
                departamento['geojson'],
                name=f'Departamento: {departamento["nombre"]}',
                style_function=lambda x: {
                    'fillColor': '#3388ff',
                    'color': '#003366',
                    'weight': 2,
                    'fillOpacity': 0.2
                },
                #tooltip=folium.Tooltip(f"<b>{departamento['nombre']}</b><br>Código: {departamento['codigo']}")
            ).add_to(m)

            # Calcular bounds del departamento
            def get_bounds(geometry):
                """Calcular bounds de una geometría GeoJSON"""
                coords = []

                def extract_coords(geom):
                    if geom['type'] == 'Polygon':
                        for ring in geom['coordinates']:
                            coords.extend([[lat, lon] for lon, lat in ring])
                    elif geom['type'] == 'MultiPolygon':
                        for polygon in geom['coordinates']:
                            for ring in polygon:
                                coords.extend([[lat, lon] for lon, lat in ring])

                extract_coords(geometry)

                if coords:
                    lats = [c[0] for c in coords]
                    lons = [c[1] for c in coords]
                    return [[min(lats), min(lons)], [max(lats), max(lons)]]
                return None

            bounds = get_bounds(departamento['geojson'])
            if bounds:
                m.fit_bounds(bounds)

        # Agregar puntos administrativos con clustering
        if puntos:
            marker_cluster = MarkerCluster(name='Puntos Administrativos').add_to(m)

            # Agrupar puntos por símbolo para diferentes colores
            symbol_colors = {
                'circle': 'blue',
                'square': 'red',
                'triangle': 'green',
                'star': 'orange'
            }

            for punto in puntos:
                if punto['geojson']['type'] == 'Point':
                    coords = punto['geojson']['coordinates']
                    # Las coordenadas vienen como [lon, lat, z], necesitamos [lat, lon]
                    lat, lon = coords[1], coords[0]

                    # Determinar color basado en símbolo
                    symbol = str(punto.get('symbol', '')).lower() if punto.get('symbol') else ''
                    color = symbol_colors.get(symbol, 'blue')

                    # Crear popup con información
                    popup_html = f"""
                    <div style="width: 200px;">
                        <h4>{punto['nombre_geo']}</h4>
                        <table style="width: 100%;">
                            <tr><td><b>Código:</b></td><td>{punto['codigo_nom'] or 'N/A'}</td></tr>
                            <tr><td><b>Proyecto:</b></td><td>{punto['proyecto'] or 'N/A'}</td></tr>
                            <tr><td><b>Fecha:</b></td><td>{punto['fecha'] or 'N/A'}</td></tr>
                            <tr><td><b>Escala:</b></td><td>{punto['escala'] or 'N/A'}</td></tr>
                        </table>
                    </div>
                    """

                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_html, max_width=250),
                        tooltip=punto['nombre_geo'],
                        icon=folium.Icon(color=color, icon='info-sign')
                    ).add_to(marker_cluster)

        # Agregar capas adicionales de tiles
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Satélite',
            overlay=False,
            control=True
        ).add_to(m)

        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Topográfico',
            overlay=False,
            control=True
        ).add_to(m)

        # Agregar control de capas
        folium.LayerControl().add_to(m)

        # Retornar el HTML del mapa
        return m._repr_html_()

    except Exception as e:
        print(f"Error generando mapa: {e}")
        return f"<h1>Error generando el mapa</h1><p>{str(e)}</p>"


@app.route('/api/estadisticas')
def api_estadisticas():
    """API endpoint para obtener estadísticas"""
    stats = get_estadisticas()
    if stats:
        return jsonify(stats)
    return jsonify({'error': 'No se pudieron obtener estadísticas'}), 500


@app.route('/api/departamento')
def api_departamento():
    """API endpoint para obtener datos del departamento"""
    data = get_departamento_data()
    if data:
        return jsonify(data)
    return jsonify({'error': 'No se pudieron obtener datos del departamento'}), 500


@app.route('/api/puntos')
def api_puntos():
    """API endpoint para obtener puntos administrativos"""
    data = get_puntos_data()
    return jsonify(data)


@app.route('/health')
def health():
    """Health check endpoint"""
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    return jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 503

@app.route('/api/mi-nuevo-endpoint')
def mi_nuevo_endpoint():
    """Nueva funcionalidad"""
    # Tu código aquí
    return jsonify({'mensaje': 'Hola Mundo'})


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


if __name__ == '__main__':
    print("=" * 50)
    print("Iniciando aplicación de visualización del Amazonas")
    print(f"Conectando a base de datos: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    print("=" * 50)

    app.run(host='0.0.0.0', port=5000, debug=True)
