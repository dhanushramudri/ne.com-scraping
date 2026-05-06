import argparse
import calendar
import datetime as dt
import random
import subprocess
import time
from pathlib import Path

def month_starts(start: dt.date, end: dt.date):
    """Yield first day of each month between start and end (inclusive)."""
    y, m = start.year, start.month
    while True:
        first = dt.date(y, m, 1)
        if first > end:
            break
        yield first
        # increment month
        if m == 12:
            y, m = y + 1, 1
        else:
            m += 1

def month_range_bounds(first_of_month: dt.date) -> (dt.date, dt.date):
    """Return (first_day, last_day) for the month containing first_of_month."""
    y, m = first_of_month.year, first_of_month.month
    last_day = calendar.monthrange(y, m)[1]
    return dt.date(y, m, 1), dt.date(y, m, last_day)

def clip_range(a_start: dt.date, a_end: dt.date, clip_start: dt.date, clip_end: dt.date):
    """Clip [a_start, a_end] to [clip_start, clip_end]."""
    start = max(a_start, clip_start)
    end = min(a_end, clip_end)
    return start, end

def run_month(start_str: str, end_str: str, retries: int) -> bool:
    """Run scrapy for a month; retry on nonzero exit."""
    cmd = [
        "scrapy", "crawl", "xe.com",
        "-s", "LOG_LEVEL=INFO",
        "-a", f"start={start_str}",
        "-a", f"end={end_str}",
    ]
    attempt = 0
    while True:
        attempt += 1
        print(f"\n==> Running {start_str} .. {end_str} (attempt {attempt})")
        result = subprocess.run(cmd, shell=False)
        if result.returncode == 0:
            print(f"✅ Done {start_str} .. {end_str}")
            return True
        if attempt > (retries + 1):
            print(f"❌ Failed {start_str} .. {end_str} after {attempt-1} attempt(s)")
            return False
        # brief backoff before retrying
        sleep_sec = min(60, 5 * attempt + random.uniform(0, 5))
        print(f"Retrying after {sleep_sec:.1f}s ...")
        time.sleep(sleep_sec)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2013-04-01")
    ap.add_argument("--end",   default="2025-08-31")
    ap.add_argument("--sleep-min", type=int, default=10, help="min seconds between months")
    ap.add_argument("--sleep-max", type=int, default=25, help="max seconds between months")
    ap.add_argument("--retries", type=int, default=1, help="retries per month if scrapy exits nonzero")
    ap.add_argument("--resume-file", default="months_done.txt", help="file to track completed months")
    args = ap.parse_args()

    start_y, start_m, start_d = map(int, args.start.split("-"))
    end_y, end_m, end_d = map(int, args.end.split("-"))
    window_start = dt.date(start_y, start_m, start_d)
    window_end   = dt.date(end_y, end_m, end_d)
    if window_end < window_start:
        raise SystemExit("End date is before start date")

    # load resume file
    done_path = Path(args.resume_file)
    done = set()
    if done_path.exists():
        done = set(x.strip() for x in done_path.read_text(encoding="utf-8").splitlines() if x.strip())

    # iterate month by month
    for first in month_starts(window_start, window_end):
        m_start, m_end = month_range_bounds(first)
        # clip to global window
        m_start, m_end = clip_range(m_start, m_end, window_start, window_end)
        key = f"{m_start.strftime('%Y-%m')}"
        if key in done:
            print(f"↪ Skipping {key} (already done)")
            continue

        ok = run_month(m_start.isoformat(), m_end.isoformat(), retries=args.retries)
        if ok:
            # mark done
            with done_path.open("a", encoding="utf-8") as f:
                f.write(key + "\n")
            # polite sleep between months
            wait = random.uniform(args.sleep_min, args.sleep_max)
            print(f"Sleeping {wait:.1f}s before next month ...")
            time.sleep(wait)
        else:
            print("Stopping because a month failed (kept resume file).")
            break

    print("\nAll done (or stopped on failure).")

if __name__ == "__main__":
    main()