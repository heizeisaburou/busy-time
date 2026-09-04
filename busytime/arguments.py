import argparse
from dataclasses import dataclass
from typing import Literal, cast

from pydantic import ValidationError

from .types.format import Format
from .types.interruptibility import Interruptibility
from .types.session import SessionData
from .types.timing.duration import Duration
from .types.timing.offset import Offset

Command = Literal["busy", "join"]
command_list: list[Command] = ["busy", "join"]


# :TODO: Agregar argumento de identidad, user_id.

# :TODO: Agregar un argumento para target time, es decir poder indicar la hora,
#  minuto, segundo, etc.

# :TODO: Agregar un argumento de mensaje personalizado

# :TODO: Agregar un argumento para poder escoger la zona horaria

# :TODO: Agregar un argumento para programar una hora concreta

# :TODO: Ver si podemos crear una lista de add_argument común para no duplicar
#  parámetros como -i

# :TODO: Hacer los tests de las funciones de parse_ de este archivo y de parse()
#  también.


def parse_interruptibility(value: str) -> Interruptibility:
  try:
    return Interruptibility(int(value))
  except ValueError as e:
    raise argparse.ArgumentTypeError(str(e)) from e


@dataclass
class BusyArgs:
  duration: Duration
  interruptibility: Interruptibility | None
  format: Format


def parse_duration(value: str) -> Duration:
  try:
    return Duration.from_string(value)
  except ValueError as e:
    raise argparse.ArgumentTypeError(str(e)) from e


@dataclass
class JoinArgs:
  session: SessionData
  offset: Offset
  interruptibility: Interruptibility | None


def parse_session_data(value: str) -> SessionData:
  try:
    return SessionData.from_json(value)
  except ValidationError as e:
    raise argparse.ArgumentTypeError(str(e)) from e


def parse_offset(value: str) -> Offset:
  try:
    return Offset.from_string(value)
  except ValueError as e:
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
    "-i",
    "--interruptibility",
    type=parse_interruptibility,
    choices=Interruptibility,
    default=None,
    help=(
      "A mayor nivel declaras que más importante debe ser el motivo por el cuál"
      "interrumpan tu sesión"
    ),
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
    "-s",
    "--session",
    type=parse_session_data,
    required=True,
    help="Sesión a la que quieres unirte",
  )

  _ = join_parser.add_argument(
    "-i",
    "--interruptibility",
    type=parse_interruptibility,
    choices=Interruptibility,
    default=None,
    help=(
      "A mayor nivel declaras que más importante debe ser el motivo por el cuál"
      "interrumpan tu sesión"
    ),
  )

  _ = join_parser.add_argument(
    "-o",
    "--offset",
    type=parse_offset,
    default=Offset(),
    help=(
      "Desplazamiento respecto al final de la sesión (para terminar antes o después)"
    ),
  )

  args = parser.parse_args()

  command = cast(Command, args.command)
  match command:
    case "busy":
      duration = cast(Duration, args.duration)
      format = cast(Format, args.format)
      interruptibility = cast(Interruptibility | None, args.interruptibility)

      return BusyArgs(
        duration=duration,
        interruptibility=interruptibility,
        format=format,
      )
    case "join":
      session = cast(SessionData, args.session)
      offset = cast(Offset, args.offset)
      interruptibility = cast(Interruptibility | None, args.interruptibility)

      return JoinArgs(
        session=session,
        offset=offset,
        interruptibility=interruptibility,
      )
    case _:  # pyright: ignore[reportUnnecessaryComparison]
      raise ValueError(f"Unexpected command {command!r}")  # pyright: ignore[reportUnreachable]
