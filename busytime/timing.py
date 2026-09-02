import re
import time
from dataclasses import dataclass
from typing import Self

TIME_REGEX = r"^(?:(\d+)\s*h)?\s*(?:(\d+)\s*m)?\s*(?:(\d+)\s*s)?$"
TIME_REGEX_CMP = re.compile(TIME_REGEX)


@dataclass
class Duration:
  hours: int = 0
  minutes: int = 0
  seconds: int = 0

  @classmethod
  def from_string(cls, value: str) -> Self:
    """Convierte una duración en el formato 1h 2m 3s (todos opcionales pero requerido al menos uno) en un objeto Time"""

    match = TIME_REGEX_CMP.match(value)
    if not match or not any(match.groups()):
      raise ValueError(
        f"Formato de duración inválido: {value!r}. "
        "Ejemplo válido: 2h5m10s (se requiere al menos una unidad)"
      )

    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)

    return cls(hours=hours, minutes=minutes, seconds=seconds)

  def total_seconds(self) -> int:
    return self.hours * 3600 + self.minutes * 60 + self.seconds


def timestamp_after(duration: Duration) -> int:
  return int(time.time()) + duration.total_seconds()
