import re
import time
from dataclasses import dataclass

TIME_REGEX = r"^(?:(\d+)\s*h)?\s*(?:(\d+)\s*m)?\s*(?:(\d+)\s*s)?$"
TIME_REGEX_CMP = re.compile(TIME_REGEX)


@dataclass
class Duration:
  hours: int = 0
  minutes: int = 0
  seconds: int = 0

  def total_seconds(self) -> int:
    return self.hours * 3600 + self.minutes * 60 + self.seconds


def timestamp_after(duration: Duration) -> int:
  return int(time.time()) + duration.total_seconds()


def parse_duration(value: str) -> Duration:
  """Convierte una duración en el formato 1h 2m 3s (todos opcionales pero requerido al menos uno) en un objeto Time"""

  match = TIME_REGEX_CMP.match(value)
  if not match or not any(match.groups()):
    raise ValueError(
      f"Formato de hora inválido: {value!r}. Formato válido de ejemplo 2h5m10s"
      + "(todos son opcionales, pero se requiere al menos uno)"
    )

  hours = int(match.group(1) or 0)
  minutes = int(match.group(2) or 0)
  seconds = int(match.group(3) or 0)

  return Duration(hours=hours, minutes=minutes, seconds=seconds)
