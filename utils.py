import fastf1
from functools import lru_cache

fastf1.Cache.enable_cache('f1_cache')

@lru_cache(maxsize=10)
def load_session(year, gp, session_type):
    session = fastf1.get_session(year, gp, session_type)
    session.load()
    return session

def get_driver_lap_telemetry(session, driver_code):
    lap = session.laps.pick_driver(driver_code).pick_fastest()
    return lap