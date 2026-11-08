"""Compute the upright crew-only lateral moment from explicit positions."""

import argparse
import json


GRAVITY_M_S2 = 9.80665


def crew_moment_nm(crew):
    """Return g * sum(mass * transverse lever arm) in N m."""
    if not crew:
        raise ValueError("At least one crew member is required")
    total = 0.0
    for name, mass_kg, lever_m in crew:
        if not name.strip():
            raise ValueError("Crew member name cannot be empty")
        if mass_kg <= 0:
            raise ValueError("Crew mass must be positive")
        if lever_m < 0:
            raise ValueError("Transverse lever arm cannot be negative")
        total += mass_kg * lever_m
    return GRAVITY_M_S2 * total


def _parse_crew(value):
    try:
        name, mass, lever = value.split(":")
        return name, float(mass), float(lever)
    except (ValueError, TypeError) as error:
        raise argparse.ArgumentTypeError(
            "Expected NAME:MASS_KG:LEVER_M, e.g. crew:80:1.1"
        ) from error


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Calculate crew-only upright transverse moment; this is not total "
            "boat righting moment."
        )
    )
    parser.add_argument(
        "--crew",
        action="append",
        type=_parse_crew,
        required=True,
        metavar="NAME:MASS_KG:LEVER_M",
        help="Crew mass and measured transverse lever arm; repeat per person",
    )
    args = parser.parse_args()
    result = {
        "crew": [
            {"name": name, "mass_kg": mass, "transverse_lever_m": lever}
            for name, mass, lever in args.crew
        ],
        "crew_upright_moment_N_m": crew_moment_nm(args.crew),
        "scope": "Crew-only upright contribution; excludes hull hydrostatics and heel effects.",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
