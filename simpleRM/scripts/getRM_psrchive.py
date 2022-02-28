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

from simpleRM import read_Timer
 
fmt = "{name}:{level} - <level>{message}</level>"
logger.remove()
logger.add(sys.stderr, level="WARNING", colorize=True, format=fmt)

from simpleRM import simpleRM


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("file", help="PSRCHIVE Timer file to process")
    parser.add_argument(
        "--interval", default=100, type=float, help="Computation interval [sec]"
    )
    parser.add_argument(
        "--start", default=False, action="store_true",help="Only return value for start time of file"
    )
    parser.add_argument(
        "--stop", default=False, action="store_true",help="Only return value for stop time of file"
    )
    parser.add_argument(
        "--mid", default=False, action="store_true",help="Only return value for midpoint time of file"
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

    times, RM, header = simpleRM.simpleRM_from_psrchive(
        args.file,
        timestep=args.interval * u.s,
        ionexPath=args.ionex,
    )
    if args.out is not None:
        fout = open(args.out, "w")
    else:
        fout = sys.stdout

    if args.start:
        logger.debug("Returning RM for start only")
        # just the single time
        RM_out = np.interp(header.mjd.mjd, times.mjd, RM.flatten())
        times = [header.mjd]
        RM = [[RM_out]]
    elif args.stop:
        logger.debug("Returning RM for stop only")
        stoptime = header.mjd+header.duration
        # just the single time
        RM_out = np.interp(stoptime.mjd, times.mjd, RM.flatten())
        times = [stoptime]
        RM = [[RM_out]]
    elif args.mid:
        logger.debug("Returning RM for midpoint only")
        midpoint = header.mjd+header.duration/2
        # just the single time
        RM_out = np.interp(midpoint.mjd, times.mjd, RM.flatten())
        times = [midpoint]
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
