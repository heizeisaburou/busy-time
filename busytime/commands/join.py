from ..arguments import JoinArgs
from ..types.timing.offset import timestamp_with_offset
from . import _format


# :TODO: Testear format_output.
def format_output(args: JoinArgs):
  lines: list[str] = []

  if args.offset.total_seconds() == 0:
    return "Me uno a la sesión."
  else:
    until = timestamp_with_offset(args.session.finish, args.offset)
    lines.append(f"Me uno a la sesión hasta las <t:{until}:t>.")

  if args.interruptibility is not None:
    lines.append(_format.interruptibility(args.interruptibility))

  return "\n".join(lines)


def run(args: JoinArgs):
  print(format_output(args))
