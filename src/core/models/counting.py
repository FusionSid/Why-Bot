""" (module) counting
Model for making counting management easier
"""

from dataclasses import dataclass


@dataclass
class CountingData:
    """
    dataclass to help with counting data information from the coutning table
    """

    guild_id: int
    last_counter: int | None
    current_number: int | None
    counting_channel: int | None

    high_score: int | None
    plugin_enabled: bool | None
    auto_calculate: bool | None

    # TODO later:
    # banned_counters: list[int] = None

    @property
    def next_number(self) -> int:
        """
        This property returns the next number which is just one
            more then the previous number (self.current_number + 1)

        Returns:
            int: the next number
        """
        if self.current_number is None:
            return 1
        return self.current_number + 1
