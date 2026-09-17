import psutil as ps


def current_user():
    try:
        user = ps.users()[0]
        return f"user: {user.name} | pid: {user.pid} | terminal: {user.terminal}"
    except IndexError:
        return "user: None | pid: None | terminal: None"


if __name__ == "__main__":
    print(current_user())