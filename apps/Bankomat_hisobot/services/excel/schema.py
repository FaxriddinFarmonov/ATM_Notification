from dataclasses import dataclass

from dataclasses import dataclass
from typing import Optional


from dataclasses import dataclass


@dataclass(slots=True)
class ColumnSchema:

    index: int

    header: str

    category: str

    field: str | None = None

    service: str | None = None

    year: int | None = None

    month: int | None = None