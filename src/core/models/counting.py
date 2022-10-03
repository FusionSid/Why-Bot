from dataclasses import dataclass


@dataclass
class CountingData:
    guild_id: int
    last_counter: int
    current_number: int
    counting_channel: int

    # will do later
    high_score: int = 0
    plugin_enabled: bool = True
    auto_calculate: bool = False
    banned_counters: list[int] = None

    @property
    def next_number(self):
        return self.counting_channel + 1
