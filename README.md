# simpleRM

* Basic ionospheric RM calculations using [`RMextract`](https://github.com/lofar-astron/RMextract) for a single position and a range of times.  
* Position/time/observatory info can be given explicitly, or extracted from `PSRFITS` or `PSRCHIVE/Timer` files
* Requires `RMextract`, but best to install with `--no-deps` so it doesn't try to pull in `casacore`
* Other requirements: `astropy`, `numpy`, `scipy`, `loguru`, `pyephem`

## Core functionality
```python

times, RM = simpleRM.simpleRM(coord,
                              starttime,
                              stoptime,
                              site,
                              timestep=100*u.s,
                              ionexPath="./IONEXdata")
    """
    Compute RM for a single position/site and a range of times

    Parameters
    ----------
    pointing : `astropy.coordinates.SkyCoord`
    starttime : `astropy.time.Time`
    stopttime : `astropy.time.Time`
    site : `astropy.coordinates.EarthLocation`
    timestep : `astropy.units.Quantity`, optional
    ionexPath : str, optional

    Returns
    -------
    times : `astropy.time.Times`
    RM : `numpy.ndarray`
    """
```

## Provide info explicitly (uses `astropy` for site info)
```
(rm) kaplan@plock[~/pythonpackages/simpleRM] (main) % getRM --start 59001  --site GBT 01:23:45 +56:12:34           
RMextract.PosTools:WARNING - We will need PyEphem to perform calculations! the accuracy of results might decrease a bit
RMextract.getIONEX:WARNING - function readTEC obsolete, use read_tec instead
RMextract.getIONEX:WARNING - function readTEC obsolete, use read_tec instead
# TIME(mjd)		RM (rad/m^2)
59001.000		0.398
```

## PSRFITS
```
(rm) kaplan@plock[~/pythonpackages/simpleRM] (main) % getRM_psrfits ~/askap/lmc/uwl_220122_151118.calib.paz1.SF32b4
RMextract.PosTools:WARNING - We will need PyEphem to perform calculations! the accuracy of results might decrease a bit
Loading (header only): /Users/kaplan/askap/lmc/uwl_220122_151118.calib.paz1.SF32b4
Load time: 0.05 s
RMextract.getIONEX:WARNING - function readTEC obsolete, use read_tec instead
# TIME(mjd)		RM (rad/m^2)
59601.632		-0.617
59601.633		-0.613
59601.634		-0.609
59601.635		-0.605
59601.636		-0.601
59601.638		-0.597
...
```

## Timer
```
(rm) kaplan@plock[~/pythonpackages/simpleRM] (main) % getRM_psrchive -vv J2035+36_59216.ar
RMextract.PosTools:WARNING - We will need PyEphem to perform calculations! the accuracy of results might decrease a bit
simpleRM.simpleRM:DEBUG - Computing for:
simpleRM.simpleRM:DEBUG - site=(-2059166.31287071, -3621302.97192224, 4814304.11311302) m
simpleRM.simpleRM:DEBUG - position=<SkyCoord (ICRS): (ra, dec) in deg
    (308.89497757, 36.87900162)>
simpleRM.simpleRM:DEBUG - times=59216.89949564594 - 59216.90382452048
RMextract.getIONEX:INFO - Retrieving data for %d or %02d%03d
RMextract.getIONEX:INFO - Retrieving data from %s
RMextract.getIONEX:INFO - CODG0020.21I.Z
RMextract.getIONEX:WARNING - function readTEC obsolete, use read_tec instead
RMextract.getIONEX:DEBUG - timerange 24.000000 hours. step = 1.000000 
RMextract.getIONEX:INFO - reading data with shapes 25 x 71 x 73
RMextract.getIONEX:DEBUG - indices time 21 22 indices lat 15 16 indices                   lon 12 13 12 13
RMextract.getIONEX:DEBUG - weights time 0.560118 lat 0.596386 lon 0.116924 0.116924
RMextract.getIONEX:DEBUG - indices time 21 22 indices lat 15 16 indices                   lon 12 13 12 13
RMextract.getIONEX:DEBUG - weights time 0.587896 lat 0.596595 lon 0.110156 0.110156
RMextract.getIONEX:DEBUG - indices time 21 22 indices lat 15 16 indices                   lon 12 13 12 13
RMextract.getIONEX:DEBUG - weights time 0.615673 lat 0.596767 lon 0.103389 0.103389
RMextract.getIONEX:DEBUG - indices time 21 22 indices lat 15 16 indices                   lon 12 13 12 13
RMextract.getIONEX:DEBUG - weights time 0.643451 lat 0.596902 lon 0.096622 0.096622
RMextract.getIONEX:DEBUG - indices time 21 22 indices lat 15 16 indices                   lon 12 13 12 13
RMextract.getIONEX:DEBUG - weights time 0.671229 lat 0.597000 lon 0.089857 0.089857
RMextract.getIONEX:DEBUG - indices time 21 22 indices lat 15 16 indices                   lon 12 13 12 13
RMextract.getIONEX:DEBUG - weights time 0.699007 lat 0.597062 lon 0.083092 0.083092
RMextract.getIONEX:DEBUG - indices time 21 22 indices lat 15 16 indices                   lon 12 13 12 13
RMextract.getIONEX:DEBUG - weights time 0.726784 lat 0.597086 lon 0.076327 0.076327
RMextract.getRM:DEBUG - *********** finished ionosphere predictions ***************
# TIME(mjd)		RM (rad/m^2)
59216.898		1.064
59216.899		1.063
59216.901		1.062
59216.902		1.061
59216.903		1.060
59216.904		1.059
59216.905		1.058
```
