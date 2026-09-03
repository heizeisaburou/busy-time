from ..arguments import JoinArgs
from ..types.timing.offset import timestamp_with_offset

# :TODO: Si alguien termina al mismo tiempo tiempo entonces no mostrar el finish, no es necesario.
#  Pero si termina antes o después, o descansa mas tiempo agregar pero, y .. etc


def format_output(args: JoinArgs):
  if args.offset.total_seconds() == 0:
    return "Me uno a la sesión."

  until = timestamp_with_offset(args.data.finish, args.offset)

  return f"Me uno a la sesión hasta las <t:{until}:t>."


def run(args: JoinArgs):
  print(format_output(args))
