from dataclasses import dataclass


@dataclass
class Tag:
    guild_id: int
    tag_name: str
    tag_value: str
    tag_author: str
    time_created: str
