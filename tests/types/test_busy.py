import json

import pytest

from busytime.types.busy import BusyData

from_json_samples = [
  ('{"finish":1788378120}', BusyData(finish=1788378120)),
]

to_json_samples = [(model, json) for json, model in from_json_samples]


@pytest.mark.parametrize(
  "value, want",
  from_json_samples,
)
def test_busy_data_from_json(value: str, want: BusyData):
  got = BusyData.from_json(value)

  assert got == want


@pytest.mark.parametrize(
  "data, want",
  to_json_samples,
)
def test_busy_data_to_json(data: BusyData, want: str):
  got = data.to_json()

  assert json.loads(got) == json.loads(want)
