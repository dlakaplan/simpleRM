#!/usr/bin/env python
import sys
import os
import argparse
import logging
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation

logging.basicConfig()
log = logging.getLogger()

import simpleRM

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("coord", nargs="+", help="Coordinates to search")
    parser.add_argument("--start", type=str,help="Start time (MJD or parsable)")
    parser.add_argument("--stop", type=str,help="Stop time (MJD or parsable)")                        
    parser.add_argument("--interval",default=100,type=float, help="Computation interval [sec]")
    parser.add_argument("--site",default=None,type=str,help="Site (see EarthLocation.get_site_names())")

    parser.add_argument(
        "-v", "--verbosity", default=0, action="count", help="Increase output verbosity"
    )
    args = parser.parse_args()
    if args.verbosity == 1:
        pulsarsurveyscraper.log.setLevel("INFO")
    elif args.verbosity >= 2:
        pulsarsurveyscraper.log.setLevel("DEBUG")

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
            coord = SkyCoord(ra, dec)
    except ValueError:
        try:
            coord = SkyCoord(ra, dec, unit=("hour", "deg"))
        except ValueError:
            log.error("Unable to parse input coordinates '{},{}'".format(ra, dec))
            sys.exit(1)

    site = EarthLocation.of_site(args.site)

    try:
        starttime = Time(float(args.start), format='mjd')
    except ValueError:
        starttime = Time(args.start)
    try:
        stoptime = Time(float(args.stop), format='mjd')
    except ValueError:
        stoptime = Time(args.stop)
    
    times, RM = simpleRM.simpleRM(coord,
                                  starttime,
                                  stoptime,
                                  site,
                                  timestep=args.interval*u.s,
                                  ionexPath='./IONEXdata/'):   

    print ("TIME(mjd)     RM (rad/m^2)")
    for tm,rm in zip(times,RM):
        print ("%s        %1.3f"%(tm.iso,rm))

if __name__ == "__main__":
    main()
