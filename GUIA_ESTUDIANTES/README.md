# Guía Completa: Desarrollo de Visor Web Geográfico con Servicios OGC WMS/WFS

## Implementación con Leaflet.js, Flask y GeoServer

### Maestría en Sistemas de Información Geográfica

---

## Descripción

Esta guía proporciona un tutorial completo paso a paso para que estudiantes de maestría en SIG desarrollen un visor web interactivo de datos geográficos utilizando estándares OGC (WMS y WFS).

## Estructura de la Guía

La guía está organizada en 10 módulos progresivos:

1. **[Introducción](01_INTRODUCCION.md)** - Objetivos, conceptos OGC y arquitectura del sistema
2. **[Prerequisitos](02_PREREQUISITOS.md)** - Software, conocimientos y verificación del entorno
3. **[Estructura HTML](03_ESTRUCTURA_HTML.md)** - Análisis detallado del archivo index.html
4. **[Estilos CSS](04_ESTILOS_CSS.md)** - Diseño, layout y personalización de Leaflet
5. **[JavaScript Parte 1](05_JAVASCRIPT_PARTE_1.md)** - Configuración, mapa base y servicios WMS
6. **[JavaScript Parte 2](06_JAVASCRIPT_PARTE_2.md)** - Servicios WFS, proxy y interactividad
7. **[Proxy Flask](07_PROXY_FLASK.md)** - Implementación del proxy y manejo de CORS
8. **[Troubleshooting](08_TROUBLESHOOTING.md)** - Solución de problemas comunes
9. **[Ejercicios Prácticos](09_EJERCICIOS.md)** - Ejercicios graduales de práctica
10. **[Anexos](10_ANEXOS.md)** - Glosario, referencias y recursos adicionales

## Objetivos de Aprendizaje

Al completar esta guía, los estudiantes serán capaces de:

- Comprender los estándares OGC WMS y WFS
- Implementar un visor web con Leaflet.js
- Consumir servicios WMS para visualización de capas base
- Consumir servicios WFS para capas interactivas
- Configurar un proxy Flask para resolver CORS
- Desarrollar interfaces interactivas con eventos del mouse
- Aplicar estilos dinámicos basados en atributos
- Implementar búsquedas y filtros espaciales
- Diagnosticar y resolver problemas comunes

## Duración Estimada

- **Lectura y comprensión:** 2-3 horas
- **Implementación práctica:** 3-4 horas
- **Ejercicios adicionales:** 2-3 horas
- **Total:** 7-10 horas

## Formato Pedagógico

Esta guía utiliza un enfoque **teórico-práctico** que combina:

- 📖 Explicaciones conceptuales de los estándares y tecnologías
- 💻 Código comentado línea por línea
- 🎯 Ejemplos prácticos y casos de uso
- ⚠️ Advertencias sobre errores comunes
- 💡 Tips y mejores prácticas
- 🔧 Ejercicios graduales para reforzar conceptos

## Requisitos Previos

Antes de comenzar, asegúrese de tener:

### Software Instalado
- GeoServer (v2.20+) ejecutándose en `localhost:8080`
- Python (v3.8+) con pip
- Docker y Docker Compose
- Editor de código (VS Code recomendado)
- Navegador moderno (Chrome/Firefox/Edge)

### Conocimientos Básicos
- HTML5 y CSS3
- JavaScript ES6 (variables, funciones, promesas)
- Conceptos básicos de SIG (coordenadas, proyecciones)
- Uso básico de línea de comandos

## Cómo Usar Esta Guía

### Modo Tutorial (Recomendado para principiantes)
Siga los módulos en orden secuencial (01 → 10):

```
01_INTRODUCCION.md
    ↓
02_PREREQUISITOS.md
    ↓
03_ESTRUCTURA_HTML.md
    ↓
... (continuar en orden)
```

### Modo Referencia (Para usuarios con experiencia)
Use el índice para ir directamente a los temas de interés:
- ¿Problemas con CORS? → Módulo 7 (Proxy Flask)
- ¿Cómo cargar WFS? → Módulo 6, Sección 6.6
- ¿Errores de visualización? → Módulo 8 (Troubleshooting)

### Modo Práctico
1. Lea los módulos 1-2 para contexto
2. Clone el código del proyecto
3. Siga los módulos 3-7 mientras examina el código
4. Complete los ejercicios del módulo 9

## Archivos de Referencia

Los siguientes archivos del proyecto son analizados en detalle:

```
webapp/
├── templates/
│   └── app/
│       └── index.html ← Módulo 3
├── static/
│   ├── css/
│   │   └── app.css ← Módulo 4
│   └── js/
│       └── app.js ← Módulos 5 y 6
└── app.py ← Módulo 7
```

## Cronograma Sugerido (4 Semanas)

### Semana 1: Fundamentos
- **Sesión 1 (2h):** Módulos 1-2 (Introducción y prerequisitos)
- **Sesión 2 (2h):** Módulo 3 (Estructura HTML)
- **Tarea:** Crear estructura HTML básica

### Semana 2: Estilos y WMS
- **Sesión 3 (2h):** Módulo 4 (CSS)
- **Sesión 4 (2h):** Módulo 5 (JavaScript - WMS)
- **Tarea:** Ejercicios 1-2

### Semana 3: WFS y Proxy
- **Sesión 5 (2h):** Módulo 6 (JavaScript - WFS)
- **Sesión 6 (2h):** Módulo 7 (Proxy Flask)
- **Tarea:** Ejercicios 3-4

### Semana 4: Debugging y Proyecto
- **Sesión 7 (2h):** Módulo 8 (Troubleshooting)
- **Sesión 8 (2h):** Proyecto final (Módulo 9)
- **Entrega:** Dashboard completo funcional

## Recursos de Apoyo

- **Documentación oficial:** Consulte el Módulo 10 (Anexos)
- **Código completo:** Disponible en `webapp/`
- **Troubleshooting:** Módulo 8 con soluciones paso a paso
- **Comunidad:** Enlaces a foros y recursos en Módulo 10

## Convenciones Usadas en Esta Guía

### Bloques de Código

```javascript
// Código de ejemplo con comentarios explicativos
const ejemplo = "valor";
```

```bash
# Comandos de terminal
comando --parametro
```

```python
# Código Python
def funcion():
    pass
```

### Notas Especiales

> **IMPORTANTE:** Información crítica que no debe omitirse

> **NOTA:** Información adicional útil

> **TIP:** Sugerencias y mejores prácticas

## Soporte y Feedback

Si encuentra errores o tiene sugerencias para mejorar esta guía:

1. Revise primero el Módulo 8 (Troubleshooting)
2. Consulte el Módulo 10 (Anexos) para recursos adicionales
3. Contacte al instructor del curso

## Licencia y Uso

Esta guía es material educativo desarrollado para el curso de Servicios Web Geográficos de la Maestría en SIG.

**Fuente de datos:** Instituto Geográfico Agustín Codazzi (IGAC)

---

## Inicio Rápido

¿Listo para comenzar?

**[➡️ Ir al Módulo 1: Introducción](01_INTRODUCCION.md)**

---

*Última actualización: Abril 2026*
