import re
from dataclasses import dataclass
from typing import Self

from . import _utils

OFFSET_REGEX = r"^([+-])?(?:(\d+)\s*h)?\s*(?:(\d+)\s*m)?\s*(?:(\d+)\s*s)?$"
OFFSET_CMP = re.compile(OFFSET_REGEX)


@dataclass
class Offset:
  hours: int = 0
  minutes: int = 0
  seconds: int = 0

  @classmethod
  def from_string(cls, value: str) -> Self:
    """Convierte una duración en el formato 1h 2m 3s (todos opcionales pero requerido al menos uno) en un objeto Offset"""

    if value.strip() == "0":
      return cls()

    match = OFFSET_CMP.match(value)
    if not match or not any(match.groups()):
      raise ValueError(
        f"Formato de offset de tiempo inválido: {value!r}. "
        "Ejemplo válido: '-2h 5m 10s' (se requiere al menos una unidad)"
      )

    sign = -1 if match.group(1) == "-" else 1

    hours = int(match.group(2) or 0) * sign
    minutes = int(match.group(3) or 0) * sign
    seconds = int(match.group(4) or 0) * sign

    return cls(hours=hours, minutes=minutes, seconds=seconds)

  def total_seconds(self) -> int:
    return _utils.total_seconds(self.hours, self.minutes, self.seconds)


def timestamp_with_offset(timestamp: int, offset: Offset):
  return timestamp + offset.total_seconds()
