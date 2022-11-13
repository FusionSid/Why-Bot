from typing import Optional

import random
from dataclasses import dataclass


@dataclass
class LevelingDataGuild:
    """
    Dataclass to help with using the leveling data guild table
    """

    guild_id: int
    plugin_enabled: Optional[bool]

    # card customization
    text_font: Optional[str]
    text_color: Optional[str]
    background_image: Optional[str]
    background_color: Optional[str]
    progress_bar_color: Optional[str]

    # give xp execptions
    no_xp_roles: Optional[list]
    no_xp_channels: Optional[list]

    # level up announcment
    level_up_text: Optional[str]
    level_up_enabled: Optional[bool]
    per_minute: Optional[str]

    def get_per_minute_xp(self) -> int:
        if self.per_minute is None:
            return random.randrange(15, 30)

        if self.per_minute.isnumeric():
            return int(self.per_minute)

        try:
            left, right = self.per_minute.split("-")
            return random.randrange(int(left), int(right))
        except ValueError:
            return random.randrange(15, 30)


@dataclass
class LevelingDataMember:
    """Dataclass to help with the leveling data member table"""

    guild_id: int
    member_id: int
    member_name: str
    member_xp: int
    member_level: int
    member_total_xp: int
