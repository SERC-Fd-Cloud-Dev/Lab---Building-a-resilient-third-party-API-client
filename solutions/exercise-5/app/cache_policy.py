FRESH_SECONDS = 10
RETAIN_SECONDS = 60

def may_fallback(entry, now, error):
    return bool(entry is not None and error.fallback
                and 0 <= now - entry.saved_at < RETAIN_SECONDS)
