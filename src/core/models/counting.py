""" (module) counting
Model for making counting management easier
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class CountingData:
    """dataclass to help with counting data information from the counting table"""

    guild_id: int
    last_counter: Optional[int]
    current_number: Optional[int]
    counting_channel: Optional[int]

    high_score: Optional[int]
    plugin_enabled: Optional[bool]
    auto_calculate: Optional[bool]

    # TODO later:
    # banned_counters: Optional[list[int]] = None

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
