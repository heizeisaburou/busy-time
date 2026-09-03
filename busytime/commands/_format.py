from ..types.interruptibility import Interruptibility


# :TODO: Testear _format.interruptibility.
def interruptibility(interruptibility: Interruptibility) -> str:
  accessible = (
    "accessible"
    if interruptibility != Interruptibility.LEVEL_0
    else "**accessible**"
  )

  enfocado = (
    "enfocado" if interruptibility != Interruptibility.LEVEL_5 else "**enfocado**"
  )

  return f"- {accessible} ❮{interruptibility.as_bar()}❯ {enfocado}"
