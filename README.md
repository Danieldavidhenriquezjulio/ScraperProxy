
# Scraper Python (proxy / Tor)

Pequeño scraper de ejemplo que muestra la IP pública, el país y extrae el título de una página usando `bs4`.

<img width="867" height="484" alt="image" src="https://github.com/user-attachments/assets/9132c94b-6c1b-49dc-9ae2-7289ce9f47c2" />


## Instalación

```bash
python -m pip install -r requirements.txt
```

## Uso rápido

```bash
# Petición directa
python scraper.py 

# Usar proxy (HTTP o SOCKS):
python scraper.py --mode proxy --proxy "http://user:pass@proxy-host:port"

# Usar Tor (requiere Tor corriendo localmente en 127.0.0.1:9050 o 127.0.0.1:9150)
python scraper.py --mode tor
```
## Definiciones

- **Proxy**: servidor intermedio que recibe solicitudes en tu nombre y reenvía las respuestas. Hay varios tipos:
  - **HTTP proxy**: diseñado para tráfico HTTP/HTTPS; reescribe encabezados y puede cachear respuestas.
  - **SOCKS proxy**: proxy de bajo nivel que transmite cualquier tipo de tráfico TCP/UDP (útil para Tor con `socks5h://`).

- **VPN (Virtual Private Network)**: crea un túnel cifrado entre tu equipo y un servidor remoto; todo el tráfico sale por esa IP remota. Proporciona privacidad a nivel de sistema, no por petición.

- **Tor (The Onion Router)**: red de voluntarios que enruta tu tráfico a través de varios relays para anonimizar la IP de origen. Normalmente se usa vía un proxy SOCKS local (p.ej. `127.0.0.1:9050`).

- **Proxy residencial**: IPs asignadas a usuarios domésticos reales; menos detectables por sitios anti-bot, recomendadas para scraping serio (servicio de pago).

- **Proxy datacenter**: IPs alojadas en centros de datos; económicas y rápidas, pero más propensas a ser bloqueadas por detección anti-bot.

- **ControlPort / Stem**: `ControlPort` es un puerto que expone Tor para control (renovar circuito, pedir nueva identidad). `Stem` es una librería Python que facilita controlar Tor vía `ControlPort`.

## Tabla comparativa (visual)

| Solución | Ventajas | Inconvenientes | Cuándo usar | Coste | Detección / Bloqueo | Velocidad |
|---|---|---|---|---:|---|---:|
| Proxy (HTTP / SOCKS) | Fácil integración en código; permite rotación por petición | Calidad depende del proveedor; puede requerir autenticación | Scraping con rotación de IPs y requests por sesión | Bajo–Medio | Moderado | Alta |
| VPN | Cifra todo el tráfico; cambia la IP del sistema entero | No se rota por petición; menos práctico para múltiples IPs | Privacidad general del equipo o acceso regional desde una sola IP | Bajo–Medio | Bajo–Moderado | Media |
| Tor | Gratuito; anonimiza origen de la IP | Lento; muchas salidas bloqueadas; no ideal a escala | Pruebas puntuales o anonimato ocasional | Gratuito | Alto (bloqueos frecuentes) | Baja |
| Proxy residencial | Alto éxito: parece tráfico de usuarios reales; difícil de bloquear | Coste elevado; requiere proveedor confiable | Scraping serio a escala donde evitar bloqueos es crítico | Alto | Bajo | Media–Alta |
| Proxy datacenter | Barato y rápido | Fácilmente detectado como bot; más bloqueos | Tareas rápidas o sitios con baja protección | Bajo | Alto | Alta |


## Comparativa: Proxy vs VPN vs Tor y otras alternativas

- **Proxy (HTTP / SOCKS)**:
	- Ventajas: permite rotación por petición, fácil integración en el código (requests), soporta SOCKS para Tor.
	- Inconvenientes: la calidad depende del proveedor; proxies datacenter son baratos pero detectables; proxies residenciales son más fiables pero caros.
	- Cuándo usar: scraping a escala con rotación de IPs; pruebas con proxies puntuales.

- **VPN**:
	- Ventajas: cambia la IP del sistema completa y cifra todo el tráfico del equipo.
	- Inconvenientes: difícil rotar desde código, no práctico para múltiples IPs simultáneas; impacto en latencia; posible bloqueo si se detecta tráfico masivo.
	- Cuándo usar: cuando necesites privacidad general en tu máquina o acceder a recursos restringidos por región desde una sola IP.

- **Tor**:
	- Ventajas: gratuito, enruta tráfico por una red de relays y oculta tu IP real.
	- Inconvenientes: lento, muchos sitios bloquean salidas Tor, no apropiado para scraping intensivo. Recomendado sólo para pruebas o anonimato ocasional.
	- Cuándo usar: pruebas puntuales, verificación de acceso desde distintos países (con limitaciones).

- **Proxies residenciales (servicios de pago)**:
	- Ventajas: alta tasa de éxito, parecen conexiones de usuarios reales; buen choice para scraping serio.
	- Inconvenientes: coste elevado y necesidad de integración con API del proveedor.
	- Cuándo usar: scraping a gran escala donde la estabilidad y eludir bloqueos importan.

- **Proxies datacenter**:
	- Ventajas: baratos y rápidos.
	- Inconvenientes: altos índices de bloqueo en sitios anti-bot.
	- Cuándo usar: tareas internas o scraping de sitios con poca protección.



## Recomendaciones prácticas

- Para un proyecto de scraping real: usa proxies residenciales rotativos (servicio de pago) + rotación de `User-Agent` + backoff y delays aleatorios.
- Para pruebas rápidas y desarrollo: Tor es una opción gratuita, pero espera latencias y bloqueos; usa `--mode tor` con Tor corriendo.
- Evita pasar credenciales sensibles en la línea de comandos en entornos compartidos; usa variables de entorno o ficheros de configuración.

## Seguridad y cumplimiento

- Respeta los términos de uso y el archivo `robots.txt` de los sitios que raspas.
- No automatices acciones que violen políticas o leyes locales.

## Recursos y servicios útiles

- Servicios geo-IP: `ipwhois.app`, `api.ipify.org`, `ipapi.co`, `ip-api.com`.
- Control de Tor: `Stem` (Python) permite renovar circuitos y controlar Tor por `ControlPort`.
- Herramientas de desarrollo: `mitmproxy`, `curl`, `Fiddler` para inspeccionar tráfico.

---

Este README resume ventajas y cuándo elegir cada solución. Si quieres, puedo añadir ejemplos concretos de configuración para proveedores de proxies o un snippet mostrando cómo rotar `User-Agent` y aplicar backoff.
