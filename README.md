# simpleRM

Requires `RMextract`, but best to install with `--no-deps` so it doesn't try to pull in `casacore`

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

```
(rm) kaplan@plock[~/pythonpackages/simpleRM] (main) % getRM --start 59001  --site GBT 01:23:45 +56:12:34           
RMextract.PosTools:WARNING - We will need PyEphem to perform calculations! the accuracy of results might decrease a bit
RMextract.getIONEX:WARNING - function readTEC obsolete, use read_tec instead
RMextract.getIONEX:WARNING - function readTEC obsolete, use read_tec instead
# TIME(mjd)		RM (rad/m^2)
59001.000		0.398
```

```
(rm) kaplan@plock[~/pythonpackages/simpleRM] (main) % getRM --start 59001  --site GBT 01:23:45 +56:12:34           
RMextract.PosTools:WARNING - We will need PyEphem to perform calculations! the accuracy of results might decrease a bit
RMextract.getIONEX:WARNING - function readTEC obsolete, use read_tec instead
RMextract.getIONEX:WARNING - function readTEC obsolete, use read_tec instead
# TIME(mjd)		RM (rad/m^2)
59001.000		0.398
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
