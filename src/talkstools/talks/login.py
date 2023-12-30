from dataclasses import dataclass
from typing import Optional
import requests

from talkstools.auth import read_credentials

from talkstools.talks.url import get_talks_url

login_route = "login/other_users"
invalid_route = "login/not_raven_login"


@dataclass
class TalksCredentials:
    user: str
    password: str


def get_talks_credentials() -> TalksCredentials:
    credentials_dict = read_credentials()["talks"]
    credentials = TalksCredentials(
        credentials_dict["user"], credentials_dict["password"]
    )
    return credentials


login_route = "/login/not_raven_login"


def login(credentials: Optional[TalksCredentials] = None) -> str:
    if credentials is None:
        talks_credentials = get_talks_credentials()
    else:
        talks_credentials = credentials
    url = get_talks_url(login_route)
    data = {
        "email": talks_credentials.user,
        "password": talks_credentials.password,
        "commit": "Log+in",
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise SystemExit("Could not log in")
    cookies = response.cookies.get_dict()
    session_id = cookies.get("_session_id")
    if session_id is None:
        raise SystemExit("Could not get session id")
    return session_id


def get_talks_session_cookies(session_id: str) -> dict[str, str]:
    return {"_session_id": session_id}
