import pytest

from busytime.types.timing._utils import total_seconds


@pytest.mark.parametrize(
  "hours, minutes, seconds, want",
  [
    (1, 0, 0, 3600),
    (0, 30, 0, 1800),
    (0, 0, 45, 45),
    (1, 30, 45, 5445),
    (-1, 0, 0, -3600),
    (0, -30, 0, -1800),
  ],
)
def test_total_seconds(hours: int, minutes: int, seconds: int, want: int):
  assert total_seconds(hours, minutes, seconds) == want
