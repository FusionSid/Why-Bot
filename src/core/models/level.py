import random
from dataclasses import dataclass


@dataclass
class LevelingDataGuild:
    """
    Dataclass to help with using the leveling data guild table
    """

    guild_id: int
    plugin_enabled: bool | None

    # card customization
    text_font: str | None
    text_color: str | None
    background_image: str | None
    background_color: str | None
    progress_bar_color: str | None

    # give xp execptions
    no_xp_roles: list | None
    no_xp_channels: list | None

    # level up announcment
    level_up_text: str | None
    level_up_enabled: bool | None
    per_minute: str | None

    def get_per_minute_xp(self) -> int:
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
