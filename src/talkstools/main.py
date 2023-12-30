from talkstools.talks.login import login_with_requests
from talkstools.talks.pull import get_talk
from talkstools.tasks.announce import print_email, write_announcement_email

if __name__ == "__main__":
    session_id = login_with_requests()
    talk = get_talk(5614, session_id)
    email = write_announcement_email("George", talk)
    print_email(email)
