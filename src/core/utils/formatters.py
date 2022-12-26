""" (module) formatters
This module contains formatting functions
"""

from enum import Enum
from typing import Literal, Optional, Final

# Enum for amount of seconds per time period
class SecondIntervals(Enum):
    second = 1
    minute = 60
    hour = 3600
    day = 86400
    week = 604800
    month = 2627424
    year = 31536000
    century = 3153600000
    millennium = 31536000000


async def format_seconds(seconds: int, short: Optional[bool] = False) -> str:
    """
    Takes in seconds and formats it into a more human readable format

    Parameters:
        seconds (int): The time in seconds, this is the number that will be formated
        short (Optional[bool]): This decides if to format the text into a shorter form.
            Eg seconds -> sec, minutes -> min
            This is off by default and also it is only supported for ms, sec, min & hrs

    Returns:
        str: The formmated output
            if it fails to format is will return an empty string ("")
    """

    if not isinstance(seconds, int) or seconds == 0:
        return ""

    # milliseconds
    elif 0 < seconds < SecondIntervals.second.value:
        ms = int(round((seconds * 1000), 0))
        if short:
            return f"{ms} ms"
        return f"{ms} millisecond{'s' if ms != 1 else ''}"

    # convert to int (if not already) so we dont get shit like "7.0 minutes"
    seconds = int(seconds)

    # seconds
    if SecondIntervals.second.value <= seconds < SecondIntervals.minute.value:
        if short:
            return f"{seconds} sec"
        return f"{seconds} second{'s' if seconds != 1 else ''}"

    # minutes
    elif SecondIntervals.minute.value <= seconds < SecondIntervals.hour.value:
        minutes, seconds = divmod(seconds, SecondIntervals.minute.value)
        if short:
            seconds = f"{seconds} sec" if seconds != 0 else ""
            return f"{minutes} min {seconds}"

        seconds = (
            f"{seconds} second{'s' if seconds != 1 else ''}" if seconds != 0 else ""
        )
        return f"{minutes} minute{'s' if minutes != 1 else ''} {seconds}"

    # hours
    elif SecondIntervals.hour.value <= seconds < SecondIntervals.day.value:
        hours, minutes = divmod(seconds, SecondIntervals.hour.value)
        if short:
            return f"{hours} hrs " + await format_seconds(minutes, short)
        return f"{hours} hour{'s' if hours != 1 else ''} " + await format_seconds(
            minutes
        )

    # days
    elif SecondIntervals.day.value <= seconds < SecondIntervals.week.value:
        days, hours = divmod(seconds, SecondIntervals.day.value)
        return f"{days} day{'s' if days != 1 else ''} " + await format_seconds(hours)

    # weeks
    elif SecondIntervals.week.value <= seconds < SecondIntervals.month.value:
        weeks, days = divmod(seconds, SecondIntervals.week.value)
        return f"{weeks} week{'s' if weeks != 1 else ''} " + await format_seconds(days)

    # months
    elif SecondIntervals.month.value <= seconds < SecondIntervals.year.value:
        months, weeks = divmod(seconds, SecondIntervals.month.value)
        return f"{months} month{'s' if months != 1 else ''} " + await format_seconds(
            weeks
        )

    # years
    elif SecondIntervals.year.value <= seconds < SecondIntervals.century.value:
        years, months = divmod(seconds, SecondIntervals.year.value)
        return f"{years} year{'s' if years != 1 else ''} " + await format_seconds(
            months
        )

    # centuries
    elif SecondIntervals.century.value <= seconds < SecondIntervals.millennium.value:
        century, years = divmod(seconds, SecondIntervals.century.value)
        return (
            f"{century} {'centuries' if century != 1 else 'century'} "
            + await format_seconds(years)
        )

    # millennia
    elif SecondIntervals.millennium.value <= seconds:
        millennium, century = divmod(seconds, SecondIntervals.millennium.value)
        return (
            f"{millennium} {'millennia' if millennium != 1 else 'millennium'} "
            + await format_seconds(century)
        )

    # if none
    return ""


def number_suffix(number: int) -> str:
    """
    This function adds the suffix / ordinal after a number provided

    Parameters:
        number (int): The number that will be formatted

    Returns:
        str: The formatted result
    """
    SUFFIXES = {1: "st", 2: "nd", 3: "rd"}
    if 10 <= number % 100 < 20:
        suffix = "th"
    else:
        suffix = SUFFIXES.get(number % 10, "th")
    return str(number) + suffix


def discord_timestamp(
    time: int,
    format_type: Literal["mdy", "md_yt", "t", "md_y", "w_md_yt", "ts", "h_m_s"],
) -> Optional[str]:
    """
    This function takes in a timestamp and formats it into a discord timestamp
    Discord timestamps look something like this: <t:123456789:R>

    Parameters:
        time (int): The unix timestamp
        format_type: (Literal[str]): The type of timestamp you want
            mdy = Month/Day/Year
            md_yt = Month Day, Year Time
            t = Time
            md_y = Month Day, Year
            w_md_yt = Weekday, Month Day, Year Time
            ts = Time since
            h_m_s = Hour:Minute:Second

    Returns:
        Union[str, None]: str with the discord timestamp. If invalid code is provided it will return None
    """
    formated_times: Final = {
        "mdy": f"<t:{time}:d>",
        "md_yt": f"<t:{time}:f>",
        "t": f"<t:{time}:t>",
        "md_y": f"<t:{time}:D>",
        "w_md_yt": f"<t:{time}:F>",
        "ts": f"<t:{time}:R>",
        "h_m_s": f"<t:{time}:T>",
    }

    return formated_times.get(format_type)
