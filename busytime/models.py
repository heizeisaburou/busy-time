from typing import Self

from pydantic import BaseModel, ConfigDict


class BusyData(BaseModel):
  finish: int

  model_config = ConfigDict(extra="forbid")

  @classmethod
  def from_json(cls, data: str) -> Self:
    return cls.model_validate_json(data)

  def to_json(self) -> str:
    return self.model_dump_json()
