import argparse
import sys
from dataclasses import dataclass
from typing import Literal, cast

from .format import Format
from .timing import Duration, parse_duration

Command = Literal["busy", "join"]
command_list: list[Command] = ["busy", "join"]


@dataclass
class BusyArgs:
  duration: Duration
  format: Format


# :TODO: Agregar un argumento para target time, es decir poder indicar la hora, minuto, segundo, etc.
# :TODO: Agregar un argumento para poder escoger la zona horaria


@dataclass
class JoinArgs:
  pass  # :TODO: pendiente


def parse() -> BusyArgs | JoinArgs:
  parser: argparse.ArgumentParser = argparse.ArgumentParser()

  subparsers = parser.add_subparsers(dest="command")

  parser.set_defaults(command="busy")

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

  argv = sys.argv[1:]

  if not argv or sys.argv[0] not in command_list:
    argv.insert(0, "busy")

  args = parser.parse_args(argv)

  command = cast(Command, args.command)
  match command:
    case "busy":
      duration = cast(Duration, args.duration)
      format = cast(Format, args.format)
      return BusyArgs(duration=duration, format=format)
    case "join":
      return JoinArgs()
    case _:  # pyright: ignore[reportUnnecessaryComparison]
      raise ValueError(f"Unexpected command {command!r}")  # pyright: ignore[reportUnreachable]
