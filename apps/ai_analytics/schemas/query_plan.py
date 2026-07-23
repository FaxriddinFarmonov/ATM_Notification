from dataclasses import dataclass, field
from typing import Optional


@dataclass
class QueryEntities:

    region: Optional[str] = None
    model: Optional[str] = None
    status: Optional[str] = None
    card_type: Optional[str] = None

    serial_number: Optional[str] = None
    terminal_id: Optional[str] = None
    merchant_id: Optional[str] = None

    atm_id: Optional[int] = None
    name: Optional[str] = None


@dataclass
class QueryPeriod:

    type: Optional[str] = None
    value: Optional[int] = None

    year: Optional[int] = None
    month: Optional[int] = None


@dataclass
class AnalyticsQueryPlan:

    entities: QueryEntities = field(
        default_factory=QueryEntities
    )

    period: QueryPeriod = field(
        default_factory=QueryPeriod
    )

    metrics: list[str] = field(
        default_factory=list
    )

    group_by: Optional[str] = None

    sort_by: Optional[str] = None

    sort_order: Optional[str] = None

    limit: Optional[int] = None