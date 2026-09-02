import time

import pytest

from ..timing import Duration, Offset, timestamp_after, total_seconds


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


@pytest.mark.parametrize(
  "value, want",
  [
    ("1h 30m 20s", Duration(1, 30, 20)),
    ("1h30m20s", Duration(1, 30, 20)),
    ("1h20s", Duration(1, 0, 20)),
    ("30m20s", Duration(0, 30, 20)),
    ("1h", Duration(1, 0, 0)),
    ("20s", Duration(0, 0, 20)),
    ("30m", Duration(0, 30, 0)),
    ("0", Duration(0, 0, 0)),
  ],
)
def test_duration_from_string(value: str, want: Duration):
  got = Duration.from_string(value)

  assert got == want


@pytest.mark.parametrize(
  "value",
  ["patata", "1", "", "h", "h1"],
)
def test_duration_from_string_rejects_invalid_values(value: str):
  with pytest.raises(ValueError):
    _ = Duration.from_string(value)


def test_to_timestamp(monkeypatch: pytest.MonkeyPatch):
  monkeypatch.setattr(time, "time", lambda: 1_000_000)

  duration = Duration(1, 30, 20)

  assert timestamp_after(duration) == 1_005_420


@pytest.mark.parametrize(
  "value, want",
  [
    ("1h 30m 20s", Offset(1, 30, 20)),
    ("+1h 30m 20s", Offset(1, 30, 20)),
    ("-1h 30m 20s", Offset(-1, -30, -20)),
    ("0", Offset(0, 0, 0)),
  ],
)
def test_offset_from_string(value: str, want: Offset):
  got = Offset.from_string(value)

  assert got == want


@pytest.mark.parametrize(
  "value",
  ["patata", "1", "", "h", "h1"],
)
def test_offset_from_string_rejects_invalid_values(value: str):
  with pytest.raises(ValueError):
    _ = Offset.from_string(value)
