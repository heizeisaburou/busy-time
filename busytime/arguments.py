import argparse
from dataclasses import dataclass
from typing import Literal, cast

from pydantic import ValidationError

from .format import Format
from .models import BusyData
from .timing import Duration, Offset

Command = Literal["busy", "join"]
command_list: list[Command] = ["busy", "join"]


# :TODO: Agregar argumento de identidad, user_id.
# :TODO: Agregar un argumento para qué tan ocupado (0-5)
# :TODO: Agregar un argumento para target time, es decir poder indicar la hora, minuto, segundo, etc.
# :TODO: Agregar un argumento para poder escoger la zona horaria
# :TODO: Agregar un argumento para programar una hora concreta


@dataclass
class BusyArgs:
  duration: Duration
  format: Format


def parse_duration(value: str) -> Duration:
  try:
    return Duration.from_string(value)
  except ValueError as e:
    raise argparse.ArgumentTypeError(str(e)) from e


@dataclass
class JoinArgs:
  data: BusyData
  offset: Offset


def parse_busy_data(value: str) -> BusyData:
  try:
    return BusyData.from_json(value)
  except ValidationError as e:
    raise argparse.ArgumentTypeError(str(e)) from e


def parse_offset(value: str) -> Offset:
  try:
    return Offset.from_string(value)
  except ValidationError as e:
    raise argparse.ArgumentTypeError(str(e)) from e


def parse() -> BusyArgs | JoinArgs:
  parser: argparse.ArgumentParser = argparse.ArgumentParser()

  subparsers = parser.add_subparsers(dest="command", required=True)

  busy_parser: argparse.ArgumentParser = subparsers.add_parser("busy")

  _ = busy_parser.add_argument(
    "-d",
    "--duration",
    type=parse_duration,
    required=True,
    help="Tiempo que vas a estar ocupado",
  )

  _ = busy_parser.add_argument(
    "-f",
    "--format",
    type=Format,
    choices=Format,
    default=Format.DISCORD,
    help="Formato de salida",
  )

  join_parser: argparse.ArgumentParser = subparsers.add_parser("join")

  _ = join_parser.add_argument(
    "-j",
    "--json",
    type=parse_busy_data,
    required=True,
    help="JSON generado por el comando busy al que quieres unirte.",
  )

  _ = join_parser.add_argument(
    "-o",
    "--offset",
    type=parse_offset,
    default=Offset(),
    help="Desplazamiento respecto al final de la sesión (para terminar antes o después)",
  )

  args = parser.parse_args()

  command = cast(Command, args.command)
  match command:
    case "busy":
      duration = cast(Duration, args.duration)
      format = cast(Format, args.format)

      return BusyArgs(duration=duration, format=format)
    case "join":
      data = cast(BusyData, args.json)
      offset = cast(Offset, args.offset)

      return JoinArgs(data=data, offset=offset)
    case _:  # pyright: ignore[reportUnnecessaryComparison]
      raise ValueError(f"Unexpected command {command!r}")  # pyright: ignore[reportUnreachable]
