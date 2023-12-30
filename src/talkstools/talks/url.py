from typing import Sequence

talks_endpoint = "http://talks.bham.ac.uk"


def get_talks_url(route: str, options: Sequence[tuple[str, str]] = []) -> str:
    base_url = f"{talks_endpoint}/{route}"
    if len(options) != 0:
        options_string = "&".join(list(map(lambda x: f"{x[0]}={x[1]}", options)))
        final_url = f"{base_url}?{options_string}"
    else:
        final_url = base_url
    return final_url
