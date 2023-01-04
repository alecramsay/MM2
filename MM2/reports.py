#!/usr/bin/env python3
#
# REPORTS
#

from .congress import *
from .readwrite import *
from .settings import *


def save_reps_by_state(
    byState: dict, rel_path: str, election_data: bool = True
) -> None:
    """Write reps_by_state CSV"""

    census_section: list[str] = ["n", "POWER", "n'", "POWER'"]
    election_section: list[str] = ["v/t", "s", "SKEW", "s'", "SKEW'"]
    headings: list[str] = (
        ["XX"] + census_section
        if not election_data
        else ["XX"] + census_section + election_section
    )
    rows: list[dict] = list()

    for k, v in byState.items():
        row: dict = dict()
        row["XX"] = k
        if not election_data:
            row["n"] = v["n"]
            row["POWER"] = v["POWER"]
            row["n'"] = v["n'"]
            row["POWER'"] = v["POWER'"]
        else:
            # Census section
            row["n"] = v["n"]
            row["POWER"] = v["POWER"]
            row["n'"] = v["n'"]
            row["POWER'"] = v["POWER'"]
            # Election section
            row["v/t"] = v["v/t"]
            row["s"] = v["s"]
            row["SKEW"] = v["SKEW"]
            row["s'"] = v["s'"]
            row["SKEW'"] = v["SKEW'"]
        rows.append(row)

    write_csv(rel_path, rows, headings)


def save_reps_by_priority(byPriority: list, rel_path: str) -> None:
    """Write reps_by_priority CSV"""
    write_csv(
        rel_path,
        byPriority,
        [
            "HOUSE SEAT",
            "PRIORITY VALUE",
            "STATE",
            "STATE SEAT",
        ],
    )


def save_reps_by_priority_SANDBOX(byPriority: list, rel_path: str) -> None:
    """Write reps_by_priority CSV -- for explorations in the sandbox"""
    write_csv(
        rel_path,
        byPriority,
        [
            "HOUSE SEAT",
            "PRIORITY VALUE",
            "STATE",
            "STATE SEAT",
            "Vf",
            "Sf",
            "SKEW|D",
            "SKEW|R",
            "THRESHOLD",
            "PARTY",
            "GAP",
            "SLACK",
        ],
    )


def save_report(app: MM2Apportioner, rel_path: str) -> None:
    """Write report.txt"""
    with open(rel_path, "w") as f:
        print("{}\n".format(app.baseline), file=f)

        print(
            "{} list seats ({} Democratic) were added for a total of {}.\n".format(
                app._total_seats - 435,
                # NOTE - This works for the sandbox class, but not the final class,
                # where N includes "other."
                # app.N - app.N0,
                app.S - app.S0,
                app._base_app.N,  # Reports the total seats, including "other."
            ),
            file=f,
        )

        if not app.queue_is_ok():
            print(
                "Warning: One or more states have no remaining priority values! Increase MAX_STATE_SEATS & re-run.\n",
                file=f,
            )
        else:
            print("All states have remaining priority values.\n", file=f)

        ones: list = app.one_rep_states()
        if len(ones) > 0:
            print(
                "Some states still have only one representative: {}\n".format(
                    ", ".join(ones)
                ),
                file=f,
            )
        else:
            print("All states have more than one representative.\n", file=f)

        unbalanced: list = app.unbalanced_states()
        if len(unbalanced) > 0:
            print(
                "Some states are still disproportional more than one seat: {}\n".format(
                    ", ".join(unbalanced)
                ),
                file=f,
            )
        else:
            print("All states are within one seat of proportional.\n", file=f)


### END ###
