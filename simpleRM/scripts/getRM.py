#!/usr/bin/env python
import sys
import os
import argparse
import logging
import re
import numpy as np
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation
import astropy.coordinates

from loguru import logger

fmt = "{name}:{level} - {message}"
logger.remove()
logger.add(sys.stderr, level="WARNING", colorize=True, format=fmt)

import simpleRM


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("coord", nargs="+", help="Coordinates to search")
    parser.add_argument(
        "--start", type=str, required=True, help="Start time (MJD or parsable)"
    )
    parser.add_argument(
        "--stop",
        type=str,
        default=None,
        required=False,
        help="Stop time (MJD or parsable) [default=only at start time]",
    )
    parser.add_argument(
        "--interval", default=100, type=float, help="Computation interval [sec]"
    )
    parser.add_argument(
        "--site",
        default=None,
        required=True,
        type=str,
        help="Site (see EarthLocation.get_site_names())",
    )
    parser.add_argument(
        "--outfmt", default="mjd", choices=["mjd", "iso"], help="Output time format"
    )
    parser.add_argument("--out", default=None, type=str, help="Output file")
    parser.add_argument(
        "--ionex",
        default="./IONEXdata",
        type=str,
        help="IONEX data destination directory",
    )

    parser.add_argument(
        "-v", "--verbosity", default=0, action="count", help="Increase output verbosity"
    )
    args = parser.parse_args()
    if args.verbosity == 1:
        logger.remove()
        logger.add(sys.stderr, level="INFO", colorize=True, format=fmt)
    elif args.verbosity >= 2:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG", colorize=True, format=fmt)

    if len(args.coord) == 2:
        ra, dec = args.coord
    elif len(args.coord) == 1:
        c = args.coord[0].split()
        l = len(c)
        ra = " ".join(c[: (l // 2)])
        dec = " ".join(c[(l // 2) :])
    try:
        if (re.search(r"[^\d.+\-]", ra) is None) and (
            re.search(r"[^\d.+\-]", dec) is None
        ):
            coord = SkyCoord(ra, dec, unit="deg")
        else:
            try:
                coord = SkyCoord(ra, dec)
            except u.core.UnitsError:
                coord = SkyCoord(ra, dec, unit=("hour", "deg"))
    except ValueError:
        try:
            coord = SkyCoord(ra, dec, unit=("hour", "deg"))
        except ValueError:
            logger.error("Unable to parse input coordinates '{},{}'".format(ra, dec))
            sys.exit(1)

    try:
        site = EarthLocation.of_site(args.site)
    except astropy.coordinates.errors.UnknownSiteException as e:
        logger.error(e)
        sys.exit(1)

    starttime = None
    stoptime = None
    try:
        starttime = Time(float(args.start), format="mjd")
    except ValueError:
        starttime = Time(args.start)
    if args.stop is None:
        stoptime = starttime + args.interval * u.s
    else:
        try:
            stoptime = Time(float(args.stop), format="mjd")
        except ValueError:
            stoptime = Time(args.stop)

    if starttime is None:
        logger.error(f"Unable to parse start time '{args.start}'")
        sys.exit(1)
    if stoptime is None:
        logger.error(f"Unable to parse stop time '{args.stop}'")
        sys.exit(1)

    times, RM = simpleRM.simpleRM(
        coord,
        starttime,
        stoptime,
        site,
        timestep=args.interval * u.s,
        ionexPath=args.ionex,
    )
    if args.out is not None:
        fout = open(args.out, "w")
    else:
        fout = sys.stdout

    if args.stop is None:
        # just the single time
        RM_out = np.interp(starttime.mjd, times.mjd, RM.flatten())
        times = [starttime]
        RM = [[RM_out]]
        
    if args.outfmt == "mjd":
        print("# TIME(mjd)\t\tRM (rad/m^2)", file=fout)
    else:
        print("# TIME\t\tRM (rad/m^2)", file=fout)
    for tm, rm in zip(times, RM):
        if args.outfmt == "mjd":
            print(f"{tm.mjd:.3f}\t\t{rm[0]:.3f}", file=fout)
        else:
            print(f"{tm.iso}\t\t{rm[0]:.3f}", file=fout)


if __name__ == "__main__":
    main()
