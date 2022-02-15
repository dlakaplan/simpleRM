import logging

log = logging.getLogger(__name__)
import RMextract.getRM as gt
from astropy import units as u, constants as c
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation

def simpleRM(pointing,
             starttime,
             stoptime,
             site,
             timestep=100*u.s,
             ionexPath='./IONEXdata/'):
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

    RMdict = gt.getRM(ionexPath=ionexPath,
                      radec=[pointing.ra.rad,pointing.dec.rad],
                      timestep=timestep.to_value(u.s),
                      timerange = [(starttime.mjd*u.d).to_value(u.s), (stoptime.mjd*u.d).to_value(u.s)],
                      stat_positions=[[x.value for x in site.to_geocentric()],])
    if RMdict is None:
        log.error("No RM results returned")
        return None,None
    RM = RMdict['RM']['st1']
    times = Time(RMdict['times']/3600/24, format='mjd')
    return times, RM

  
