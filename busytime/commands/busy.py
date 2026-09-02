import json
from dataclasses import asdict, dataclass

from ..arguments import BusyArgs
from ..format import Format
from ..timing import timestamp_after


@dataclass
class BusyData:
  finish: int

  def to_json(self) -> str:
    return json.dumps(asdict(self))


def build_busy_data(args: BusyArgs) -> BusyData:
  finish = timestamp_after(args.duration)

  return BusyData(finish=finish)


def format_output(data: BusyData) -> str:
  return f"""**Doing things** hasta <t:{data.finish}:t>
Si quieres unirte descarga busytime ―GH: heizeisaburou/busy-time― y ejecuta:
```sh
busytime join -j '{data.to_json()}'
```"""


def run(args: BusyArgs):
  data = build_busy_data(args)
  match args.format:
    case Format.DISCORD:
      print(format_output(data))
    case Format.JSON:
      print(data.to_json())
    case _:  # pyright: ignore[reportUnnecessaryComparison]
      raise ValueError(f"Formato de salida desconocido {args.format}")  # pyright: ignore[reportUnreachable]
