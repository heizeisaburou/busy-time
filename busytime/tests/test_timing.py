import time

import pytest

from ..timing import Duration, timestamp_after


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
  ],
)
def test_parse_duration(value: str, want: Duration):
  got = Duration.from_string(value)

  assert got == want


@pytest.mark.parametrize(
  "value",
  [
    "patata",
    "1",
    "",
    "h",
    "h1",
  ],
)
def test_parse_duration_invalid_values(value: str):
  with pytest.raises(ValueError):
    _ = Duration.from_string(value)


@pytest.mark.parametrize(
  "value, want",
  [
    (Duration(), 0),
    (Duration(seconds=1), 1),
    (Duration(seconds=30), 30),
    (Duration(minutes=1), 60),
    (Duration(minutes=30), 1800),
    (Duration(hours=1), 3600),
    (Duration(hours=2), 7200),
    (Duration(hours=1, minutes=30), 5400),
    (Duration(hours=1, minutes=30, seconds=20), 5420),
    (Duration(hours=2, minutes=15, seconds=45), 8145),
  ],
)
def test_total_seconds(value: Duration, want: int):
  got = value.total_seconds()
  assert got == want


def test_to_timestamp(monkeypatch: pytest.MonkeyPatch):
  monkeypatch.setattr(time, "time", lambda: 1_000_000)

  duration = Duration(1, 30, 20)

  assert timestamp_after(duration) == 1_005_420
