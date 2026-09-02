import time

import pytest

from ..timing import Time, parse_duration, timestamp_after


@pytest.mark.parametrize(
  "value, want",
  [
    ("1h 30m 20s", Time(1, 30, 20)),
    ("1h30m20s", Time(1, 30, 20)),
    ("1h20s", Time(1, 0, 20)),
    ("30m20s", Time(0, 30, 20)),
    ("1h", Time(1, 0, 0)),
    ("20s", Time(0, 0, 20)),
    ("30m", Time(0, 30, 0)),
  ],
)
def test_parse_duration(value: str, want: Time):
  got = parse_duration(value)

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
    _ = parse_duration(value)


@pytest.mark.parametrize(
  "value, want",
  [
    (Time(), 0),
    (Time(seconds=1), 1),
    (Time(seconds=30), 30),
    (Time(minutes=1), 60),
    (Time(minutes=30), 1800),
    (Time(hours=1), 3600),
    (Time(hours=2), 7200),
    (Time(hours=1, minutes=30), 5400),
    (Time(hours=1, minutes=30, seconds=20), 5420),
    (Time(hours=2, minutes=15, seconds=45), 8145),
  ],
)
def test_total_seconds(value: Time, want: int):
  got = value.total_seconds()
  assert got == want


def test_to_timestamp(monkeypatch: pytest.MonkeyPatch):
  monkeypatch.setattr(time, "time", lambda: 1_000_000)

  duration = Time(1, 30, 20)

  assert timestamp_after(duration) == 1_005_420
