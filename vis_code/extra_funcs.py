import time

# 12 hour labels
def format_hour(h):
    if h == 0:
        return "12 AM"
    elif h < 12:
        return f"{h} AM"
    elif h == 12:
        return "12 PM"
    else:
        return f"{h - 12} PM"

def typewrite(text, delay=0.4, dots=3):
    """Prints text followed by animated dots."""
    print(text, end="")
    for _ in range(dots):
        time.sleep(delay)
        print(".", end="", flush=True)
    print()