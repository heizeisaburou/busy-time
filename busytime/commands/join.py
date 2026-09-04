from ..arguments import JoinArgs
from ..types.timing.offset import timestamp_with_offset
from . import _format


# :TODO: Testear format_output.
def format_output(args: JoinArgs):
  lines: list[str] = []

  total_seconds = args.offset.total_seconds()
  if total_seconds == 0:
    lines.append("Me uno a la sesión.")
  else:
    until = timestamp_with_offset(args.session.finish, args.offset)
    adverbio = "más tarde" if total_seconds > 0 else "antes"
    lines.append(f"Me uno a la sesión pero termino {adverbio}, a las <t:{until}:t>.")

  if args.interruptibility is not None:
    lines.append(_format.interruptibility(args.interruptibility))

  return "\n".join(lines)


def run(args: JoinArgs):
  print(format_output(args))
