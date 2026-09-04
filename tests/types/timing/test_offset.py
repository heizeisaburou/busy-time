import pytest

from busytime.types.timing.offset import Offset, timestamp_with_offset


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


@pytest.mark.parametrize(
  "offset, want",
  [
    (Offset(1, 0, 0), 3600),
    (Offset(0, 30, 0), 1800),
    (Offset(0, 0, 45), 45),
    (Offset(1, 30, 45), 5445),
    (Offset(-1, 0, 0), -3600),
    (Offset(0, -30, 0), -1800),
    (Offset(-1, -30, -20), -5420),
    (Offset(), 0),
  ],
)
def test_offset_total_seconds(offset: Offset, want: int):
  assert offset.total_seconds() == want


@pytest.mark.parametrize(
  "offset, want",
  [
    (Offset(0, -30, 0), 1_788_376_320),
    (Offset(1, 0, 0), 1_788_381_720),
    (Offset(), 1_788_378_120),
  ],
)
def test_timestamp_with_offset(offset: Offset, want: int):
  assert timestamp_with_offset(1_788_378_120, offset) == want
