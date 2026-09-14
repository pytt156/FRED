import time

PRESENCE_TIMEOUT_SECONDS = 300

last_motion_at = None


def update_motion(motion: bool) -> None:
    global last_motion_at

    if motion:
        last_motion_at = time.time()


def is_presence_active() -> bool:
    if last_motion_at is None:
        return False

    return time.time() - last_motion_at < PRESENCE_TIMEOUT_SECONDS
