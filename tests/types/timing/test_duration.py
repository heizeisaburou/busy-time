import time

import pytest

from busytime.types.timing.duration import Duration, timestamp_after


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


@pytest.mark.parametrize(
  "duration, want",
  [
    (Duration(1, 0, 0), 3600),
    (Duration(0, 30, 0), 1800),
    (Duration(0, 0, 45), 45),
    (Duration(1, 30, 45), 5445),
    (Duration(), 0),
  ],
)
def test_duration_total_seconds(duration: Duration, want: int):
  assert duration.total_seconds() == want


def test_timestamp_after(monkeypatch: pytest.MonkeyPatch):
  monkeypatch.setattr(time, "time", lambda: 1_000_000)

  duration = Duration(1, 30, 20)

  assert timestamp_after(duration) == 1_005_420
