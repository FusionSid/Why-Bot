def loading_bar(length: int, index: int, title: str, end: str):
    """
    Makes a loading bar when starting up the bot

    Parameters
        :param: length (int): The length of the list
        :param: index (int): Index of the list
        :param: title (str): The title of the loading bar
        :param: end (str): The message to say once the bar is done
    """
    percent_done = (index + 1) / length * 100
    done = round(percent_done / (100 / 50))
    togo = 50 - done

    done_str = "█" * int(done)
    togo_str = "░" * int(togo)

    print(f"{title} {done_str}{togo_str} {int(percent_done)}% Done", end="\r")

    if round(percent_done) == 100:
        print(f"\n\n{end}\n")
