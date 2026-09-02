from .arguments import BusyArgs, JoinArgs
from .arguments import parse as parse_arguments
from .commands.busy import run as run_busy
from .commands.join import run as run_join


def main():
  args = parse_arguments()

  if isinstance(args, BusyArgs):
    run_busy(args)
  elif isinstance(args, JoinArgs):  # pyright: ignore[reportUnnecessaryIsInstance]
    run_join(args)
  else:
    raise TypeError(
      f"arguments.parse() ha devuelvo un tipo desconocido: {type(args)!r}"
    )


if __name__ == "__main__":
  main()
