from loguru import logger

import RMextract.getRM as gt
from astropy import units as u, constants as c
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, errors


def simpleRM(
    pointing, starttime, stoptime, site, timestep=100 * u.s, ionexPath="./IONEXdata/"
):
    """Compute RM for a single position/site and a range of times

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

    logger.debug(f"Computing for:")
    logger.debug(f"site={site}")
    logger.debug(f"position={pointing}")
    logger.debug(f"times={starttime} - {stoptime}")

    RMdict = gt.getRM(
        ionexPath=ionexPath,
        radec=[pointing.ra.rad, pointing.dec.rad],
        timestep=timestep.to_value(u.s),
        timerange=[
            (starttime.mjd * u.d).to_value(u.s),
            (stoptime.mjd * u.d).to_value(u.s),
        ],
        stat_positions=[[x.value for x in site.to_geocentric()],],
    )
    if RMdict is None:
        logger.error("No RM results returned")
        return None, None
    RM = RMdict["RM"]["st1"]
    times = Time(RMdict["times"] / 3600 / 24, format="mjd")
    return times, RM


def simpleRM_from_psrfits(filename, timestep=100 * u.s, ionexPath="./IONEXdata/"):
    """Compute RM for a single position/site and a range of times based on a PSRFITS file

    Parameters
    ----------
    filename : str
        PSRFITS file to read
    timestep : `astropy.units.Quantity`, optional
    ionexPath : str, optional

    Returns
    -------
    times : `astropy.time.Times`
    RM : `numpy.ndarray`
    ar : `pypulse` archive
    """
    import pypulse

    logger.debug(f"Reading PSRFITS file {filename}")
    ar = pypulse.Archive(filename, onlyheader=True)
    pointing = ar.getPulsarCoords()
    telescope = ar.getTelescope()
    try:
        site = EarthLocation.of_site(telescope)
    except errors.UnknownSiteException:
        xyz = ar.getTelescopeCoords()
        site = EarthLocation.from_geocentric(*xyz, unit=u.m)

    starttime = Time(ar.getMJD(full=True), format="mjd")
    stoptime = starttime + ar.getDuration() * u.s
    return (*simpleRM(
        pointing, starttime, stoptime, site, timestep=timestep, ionexPath=ionexPath
    ),ar)


def simpleRM_from_psrchive(filename, timestep=100 * u.s, ionexPath="./IONEXdata/"):
    """Compute RM for a single position/site and a range of times based on a PSRCHIVE file

    Parameters
    ----------
    filename : str
        PSRCHIVE Timer file to read
    timestep : `astropy.units.Quantity`, optional
    ionexPath : str, optional

    Returns
    -------
    times : `astropy.time.Times`
    RM : `numpy.ndarray`
    header : `read_Timer.TimerHeader`
    """
    from . import read_Timer

    logger.debug(f"Reading Timer file {filename}")
    t = read_Timer.TimerHeader(filename)
    pointing = t.position
    telescope = t.telescope
    try:
        site = EarthLocation.of_site(telescope)
    except errors.UnknownSiteException:
        logger.error(f"Unknown site '{telescope}'")
        return None

    starttime = t.mjd
    stoptime = starttime + t.duration
    return (
        *simpleRM(
            pointing, starttime, stoptime, site, timestep=timestep, ionexPath=ionexPath
        ),
        t,
    )
