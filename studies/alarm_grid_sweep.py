#!/usr/bin/env python3
"""Sweep the stateless alarm grid for the two properties the design claims.

The proposed next-wake arithmetic (QUEUE.md, "Best of both worlds") computes the
alarm from the clock and snaps it to the schedule:

    next = ((secondsIntoDay / step) + 1) * step

The claim is that this is (1) always strictly in the future of the moment it was
computed, so it cannot deadlock, and (2) always a multiple of step past midnight,
so it cannot drift. Both are mechanical, though a sweep is what shows no step or
overrun falsifies them. Run it with no arguments; it prints the numbers quoted in
QUEUE.md.

Pass --falsify to run the same sweep against the two schemes the grid replaces,
which is what shows each check measures its own property: Bobby's `now + N` fails
the grid check alone, and ALog's `previous + N` fails the future check alone.

Usage: python3 studies/alarm_grid_sweep.py [--falsify]
"""
import random
import sys

DAY = 86400
GUARD = 2  # seconds of lead a wake needs, so the alarm is armed before it passes
STEPS = [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60, 120, 180, 240, 300, 360,
         600, 720, 900, 1200, 1800, 3600]

# The legible schedule: divisors of 60 applied to seconds, minutes dividing the
# hour, and hours dividing the day. The backup alarm is checked over all of them,
# including the long steps a log interval would not normally use.
LEGIBLE = sorted(set([s for s in range(1, 61) if 60 % s == 0]
                     + [60 * m for m in range(1, 61) if 3600 % (60 * m) == 0]
                     + [3600 * h for h in range(1, 25) if 24 % h == 0]))


def next_wake(secondsIntoDay, step, guard=GUARD, phase=0):
    """The next scheduled wake, or None when step cannot divide the day."""
    if step == 0 or step > DAY or DAY % step:
        return None
    t = (secondsIntoDay + DAY - phase) % DAY
    nxt = ((t // step) + 1) * step  # strictly > t: integer division floors
    if nxt - t < guard:
        nxt += step                 # too close to arm safely: take the next one
    return (nxt + phase) % DAY


def hms(s):
    return "%02d:%02d:%02d" % (s // 3600, s // 60 % 60, s % 60)


def sweep(seed=7, per_step=4000):
    """Walk the schedule with injected awake times, including overruns."""
    random.seed(seed)
    not_future = off_grid = total = 0
    for step in STEPS:
        s = random.randrange(DAY)
        awakes = [0, 0, 0, 1, 2, 3, 7, step // 2 if step > 2 else 1, step * 2 + 5]
        for _ in range(per_step):
            armed = (s + random.choice(awakes)) % DAY  # the clock when we arm it
            nxt = next_wake(armed, step)
            total += 1
            if not 0 < (nxt - armed) % DAY <= 3 * step:
                not_future += 1
            if nxt % step != 0:
                off_grid += 1
            s = nxt
    return total, not_future, off_grid


def backup_wake(next_, step):
    """A2 = the first grid point on a whole minute strictly after A1.

    Alarm 2 carries hours and minutes only and matches at seconds = 00, so it can
    be placed on a whole minute and nowhere else. For every legible step a whole
    minute is itself a grid point, which is what lets the backup land on the grid.

    Returns None at a step of a whole day or more, where the backup is not
    expressible: alarm 2 carries no date, so one cycle later is the same time of
    day and the backup collapses onto the primary. The watchdog ceiling
    (step < NW_WDT_SECONDS / 2) already excludes those steps for a logger.
    """
    if step >= DAY:
        return None
    a2 = next_ + step                      # one cycle after the primary
    if a2 % 60:
        a2 = ((a2 // 60) + 1) * 60         # a sub-minute step: the next whole minute
    return a2 % DAY                        # a time of day: the alarm carries no date


def backup_check():
    """The three properties the backup plan claims, over every legible step."""
    off_grid = not_after = beyond_step = 0
    minute_off_grid = [s for s in LEGIBLE if 60 % s and s % 60]
    no_backup = [s for s in LEGIBLE if backup_wake(0, s) is None]
    for step in LEGIBLE:
        if step in no_backup:
            continue
        for k in range(0, DAY, max(step, 60)):
            a1 = k - (k % step)
            a2 = backup_wake(a1, step)
            if a2 % step:
                off_grid += 1
            ahead = (a2 - a1) % DAY        # modular: the backup may cross midnight
            if ahead == 0:
                not_after += 1
            if ahead > max(step, 60):
                beyond_step += 1
    return minute_off_grid, no_backup, off_grid, not_after, beyond_step


def relative(secondsIntoDay, step, guard=GUARD, phase=0):
    """Bobby's scheme: always ahead of now, never on the grid."""
    return (secondsIntoDay + step) % DAY


_previous = {}


def accumulator(secondsIntoDay, step, guard=GUARD, phase=0):
    """ALog's scheme: always on the grid, able to land in the past."""
    p = _previous.get(step)
    nxt = (step if p is None else p + step) % DAY
    _previous[step] = nxt
    return nxt


def falsify():
    """Run the sweep against each scheme, so each check is seen to measure its own property."""
    global next_wake
    grid = next_wake
    for name, fn in (("grid (proposed)", grid), ("now + N", relative), ("previous + N", accumulator)):
        _previous.clear()
        next_wake = fn
        total, not_future, off_grid = sweep()
        print("  %-16s not in the future %6d   off the grid %6d" % (name, not_future, off_grid))
    next_wake = grid


if __name__ == "__main__":
    if "--backup" in sys.argv:
        minute_off_grid, no_backup, off_grid, not_after, beyond = backup_check()
        print("the backup alarm, over all %d legible steps:" % len(LEGIBLE))
        print("  steps where a whole minute is not a grid point: %s"
              % (minute_off_grid if minute_off_grid else "none"))
        print("  steps with no expressible backup (a day or more):  %s"
              % (no_backup if no_backup else "none"))
        print("  backups off the grid:                %d" % off_grid)
        print("  backups not strictly after A1:       %d" % not_after)
        print("  backups further out than one cycle:  %d" % beyond)
        print()
        print("  ALog's fixed +2 min, for comparison, at a 900 s step:")
        a1 = 15 * 3600
        print("    A1 %s  A2 %s  on grid %s"
              % (hms(a1), hms(a1 + 120), "yes" if (a1 + 120) % 900 == 0 else "no"))
        print("  A2 = A1 + one cycle, same step:")
        print("    A1 %s  A2 %s  on grid %s"
              % (hms(a1), hms(backup_wake(a1, 900)), "yes" if backup_wake(a1, 900) % 900 == 0 else "no"))
        raise SystemExit(1 if (minute_off_grid or off_grid or not_after or beyond) else 0)
    if "--falsify" in sys.argv:
        print("the same sweep, against the two schemes the grid replaces:")
        falsify()
        raise SystemExit(0)
    total, not_future, off_grid = sweep()
    print("%d wakes over %d valid steps, awake times from 0 s to over an interval"
          % (total, len(STEPS)))
    print("  not strictly in the future: %d" % not_future)
    print("  not on the grid:            %d" % off_grid)
    print()
    print("a 900 s step whose cycle overruns, armed at 14:45:00:")
    for late in (3, 950):
        print("  %4d s late -> %s" % (late, hms(next_wake((14 * 3600 + 45 * 60 + late) % DAY, 900))))
    print()
    print("the guard, at 14:59:59 with a 900 s step:")
    for guard in (0, GUARD):
        print("  guard %d s -> %s" % (guard, hms(next_wake(14 * 3600 + 59 * 60 + 59, 900, guard=guard))))
    print()
    print("two loggers staggered off one window, phase 0 and phase 450:")
    for phase in (0, 450):
        print("  phase %3d -> %s" % (phase, " ".join(hms(next_wake(x, 900, phase=phase)) for x in (0, 900, 1800))))
    raise SystemExit(1 if (not_future or off_grid) else 0)
