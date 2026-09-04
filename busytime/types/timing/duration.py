import re
import time
from dataclasses import dataclass
from typing import Self

from . import _utils

DURATION_REGEX = r"^(?:0|(?:(\d+)\s*h)?\s*(?:(\d+)\s*m)?\s*(?:(\d+)\s*s)?)$"
DURATION_CMP = re.compile(DURATION_REGEX)


@dataclass
class Duration:
  hours: int = 0
  minutes: int = 0
  seconds: int = 0

  @classmethod
  def from_string(cls, value: str) -> Self:
    """Convierte una duración en el formato 1h 2m 3s (todos opcionales pero requerido al menos uno) en un objeto Duration"""

    if value.strip() == "0":
      return cls()

    match = DURATION_CMP.match(value)
    if not match or not any(match.groups()):
      raise ValueError(
        f"Formato de duración inválido: {value!r}. "
        "Ejemplo válido: '2h 5m 10s' (se requiere al menos una unidad)"
      )

    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)

    return cls(hours=hours, minutes=minutes, seconds=seconds)

  def total_seconds(self) -> int:
    return _utils.total_seconds(self.hours, self.minutes, self.seconds)


def timestamp_after(duration: Duration) -> int:
  return int(time.time()) + duration.total_seconds()
