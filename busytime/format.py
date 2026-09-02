from enum import Enum
from typing import override


class Format(Enum):
  DISCORD = "discord"
  JSON = "json"

  @override
  def __str__(self) -> str:
    return self.value
