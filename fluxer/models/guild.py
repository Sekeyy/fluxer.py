from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any

from ..utils import snowflake_to_datetime

if TYPE_CHECKING:
    from ..http import HTTPClient


@dataclass(slots=True)
class Guild:
    """Represents a Fluxer guild (server/community)."""

    id: str
    name: str | None = None
    icon: str | None = None
    owner_id: str | None = None
    member_count: int | None = None
    unavailable: bool = False

    _http: HTTPClient | None = field(default=None, repr=False)

    @classmethod
    def from_data(cls, data: dict[str, Any], http: HTTPClient | None = None) -> Guild:
        return cls(
            id=data["id"],
            name=data.get("name"),
            icon=data.get("icon"),
            owner_id=data.get("owner_id"),
            member_count=data.get("member_count"),
            unavailable=data.get("unavailable", False),
            _http=http,
        )

    @property
    def created_at(self) -> datetime:
        return snowflake_to_datetime(self.id)

    @property
    def icon_url(self) -> str | None:
        if self.icon:
            ext = "gif" if self.icon.startswith("a_") else "png"
            return f"https://fluxerusercontent.com/icons/{self.id}/{self.icon}.{ext}"
        return None

    def __str__(self) -> str:
        return self.name or f"Guild({self.id})"
