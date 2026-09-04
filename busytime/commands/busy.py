from ..arguments import BusyArgs
from ..types.busy import BusyData
from ..types.format import Format
from ..types.session import SessionData
from ..types.timing.duration import timestamp_after
from . import _format


# :TODO: Testear build_busy_data.
def build_busy_data(args: BusyArgs) -> BusyData:
  return BusyData(
    finish=timestamp_after(args.duration), interruptibility=args.interruptibility
  )


# :TODO: Testear session_from_busy_data.
def session_from_busy_data(data: BusyData) -> SessionData:
  return SessionData(
    finish=data.finish,
  )


# :TODO: Testear format_output.
def format_output(data: BusyData) -> str:
  lines = [f"**Doing things** hasta <t:{data.finish}:t>"]

  if data.interruptibility is not None:
    lines.append(_format.interruptibility(data.interruptibility))

  session_data = session_from_busy_data(data)
  lines.extend(
    [
      "",
      "Si quieres unirte descarga busytime ―GH: heizeisaburou/busy-time― y ejecuta:",
      "```sh",
      f"busytime join -s '{session_data.to_json()}'",
      "```",
    ],
  )

  return "\n".join(lines)


def run(args: BusyArgs):
  data = build_busy_data(args)

  match args.format:
    case Format.DISCORD:
      print(format_output(data))
    case Format.JSON:
      print(data.to_json())
    case _:  # pyright: ignore[reportUnnecessaryComparison]
      raise ValueError(f"Formato de salida desconocido {args.format}")  # pyright: ignore[reportUnreachable]
