#!/usr/bin/env python3
#
# SETTINGS
#

MAX_STATE_SEATS: int = (
    100  # Choose this value, so CA doesn't run out of priority values.
)

NOMINAL_SEATS: int = 435  # The number of seats to apportion using the census data.
LIST_SEATS: int = 50  # The number of list seats, if fixed (Strategy 5).
TOTAL_SEATS: int = 600  # Total number of seats to apportion, if fixed (Strategy 6).

STATES: list[str] = [
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
]

EPSILON: float = 1 / (10**6)
