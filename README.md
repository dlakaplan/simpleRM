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
