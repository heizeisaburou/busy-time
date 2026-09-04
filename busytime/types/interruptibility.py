from enum import IntEnum


class Interruptibility(IntEnum):
  LEVEL_0 = 0
  LEVEL_1 = 1
  LEVEL_2 = 2
  LEVEL_3 = 3
  LEVEL_4 = 4
  LEVEL_5 = 5

  # :TODO: Testear Interruptibility.as_bar.
  def as_bar(self) -> str:
    return "▰" * self.value + "▱" * (5 - self.value)
