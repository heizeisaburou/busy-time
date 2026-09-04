# busy-time

CLI sencilla para avisar de que estás ocupado, generar timestamps de Discord y compartir la sesión con otras personas para que se unan.

## Instalación

Clona el repositorio e instálalo con `pip`:

### Linux

```bash
git clone https://github.com/heizeisaburou/busy-time.git
cd busy-time

python -m venv .venv
source .venv/bin/activate
pip install .
```

### Windows

```powershell
git clone https://github.com/heizeisaburou/busy-time.git
Set-Location .\busy-time

python -m venv .venv
.venv\Scripts\activate
pip install .
```

## Uso

`busytime` se organiza en subcomandos:

```bash
busytime busy -d <duración> [-f <formato>]
busytime join -s <json de la sesión> [-o <offset>]
```

### `busy` — abrir una sesión

Marca que vas a estar ocupado durante un tiempo determinado:

```bash
busytime busy -d 1h
```

La duración se indica con horas, minutos y segundos. Todas las unidades son opcionales, pero hace falta al menos una (o el literal `0`). Se admiten espacios entre unidades:

```bash
busytime busy -d 1h30m
busytime busy -d "1h 30m 20s"
busytime busy -d 45m
busytime busy -d 30s
```

Por defecto la salida es un mensaje listo para pegar en Discord, con la hora de final como timestamp (`<t:...:t>`) y las instrucciones para que otros se unan:

````
**Doing things** hasta <t:1788398961:t>
Si quieres unirte descarga busytime ―GH: heizeisaburou/busy-time― y ejecuta:
```sh
busytime join -s '{"finish":1788398961}'
```
````

Con `-f json` obtienes en crudo lo que estableciste (incluye `interruptibility` si la indicaste con `-i`):

```bash
busytime busy -d 1h -f json
```

```json
{ "finish": 1788397161 }
```

Formatos disponibles (`-f`, `--format`):

- `discord` — mensaje listo para compartir en Discord (por defecto)
- `json` — lo que estableciste, en crudo

### `join` — unirse a una sesión

Toma el JSON de la sesión generado por `busy` y genera el mensaje de respuesta:

```bash
busytime join -s '{"finish":1788378120}'
```

```
Me uno a la sesión.
```

Con `-o` / `--offset` indicas si terminas antes o después que la sesión original. Acepta el mismo formato que `-d`, precedido opcionalmente de `+` o `-`, y el timestamp que se imprime es el final de la sesión ya desplazado:

```bash
busytime join -s '{"finish":1788378120}' -o -30m
```

```
Me uno a la sesión hasta las <t:1788376320:t>.
```

```bash
busytime join -s '{"finish":1788378120}' -o +1h
```

```
Me uno a la sesión hasta las <t:1788381720:t>.
```

`-o` es opcional. Si lo omites —o pasas `-o 0`— el mensaje no incluye hora, porque terminas a la vez que el resto.

## Formato de duraciones y offsets

| Entrada      | Significado                           |
| ------------ | ------------------------------------- |
| `1h`         | 1 hora                                |
| `30m`        | 30 minutos                            |
| `20s`        | 20 segundos                           |
| `1h30m20s`   | 1 hora, 30 minutos y 20 segundos      |
| `1h 30m 20s` | igual, con espacios                   |
| `0`          | sin duración / sin desplazamiento     |
| `-30m`       | 30 minutos antes (solo en `--offset`) |
| `+1h`        | 1 hora después (solo en `--offset`)   |

Valores como `1`, `h`, `h1` o texto libre se rechazan con un error.

## Desarrollo

Para trabajar sobre el proyecto, instálalo en **modo editable** en lugar de con `pip install .`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

La diferencia importa. `pip install .` copia el paquete dentro de `site-packages`, y a partir de ahí el comando `busytime` ejecuta esa copia, no tus fuentes: editas el código y no ves ningún cambio hasta que reinstalas. Con `-e`, pip deja en `site-packages` un puntero a este directorio, así que el siguiente `busytime ...` ya usa lo que acabas de escribir.

Ojo con este síntoma, porque despista: `python -m busytime.main ...` lanzado desde la raíz del repositorio siempre carga las fuentes (Python añade el directorio actual a `sys.path`), mientras que `busytime` a secas va a `site-packages`. Si los dos te dan resultados distintos, es que tienes una copia antigua instalada.

### Cuándo hay que reinstalar

Con el modo editable **no** hace falta reinstalar al cambiar código, ni al añadir módulos o subpaquetes nuevos dentro de `busytime/`. Sí hay que repetir `pip install -e .` cuando cambias metadata en `pyproject.toml`:

- añadir o cambiar dependencias (`dependencies`)
- cambiar el nombre o el destino del comando (`[project.scripts]`)
- cambiar `version` o `requires-python`

### Tests

Los tests usan `pytest`, que todavía no está declarado en `pyproject.toml`; hay que instalarlo aparte:

```bash
pip install pytest
pytest
```

## Requisitos

- Python 3.14+
