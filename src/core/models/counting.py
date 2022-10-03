from dataclasses import dataclass


@dataclass
class CountingData:
    guild_id: int
    last_counter: int | None
    current_number: int | None
    counting_channel: int | None

    high_score: int | None
    plugin_enabled: bool | None
    auto_calculate: bool | None

    # will do later
    # banned_counters: list[int] = None

    @property
    def next_number(self):
        if self.current_number is None:
            return 1
        return self.current_number + 1
