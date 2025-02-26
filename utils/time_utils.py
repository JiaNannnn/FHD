from datetime import datetime, timedelta
import time
def current_milli_time():
    return round(time.time() * 1000)

def round_to_nearest_interval(dt, interval):
    minutes = (dt.minute // interval) * interval
    if dt.minute % interval >= (interval / 2):
        minutes += interval
    dt = dt.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=minutes)
    if dt.minute >= 60:
        dt += timedelta(hours=1)
        dt = dt.replace(minute=0)
    return dt

def split_into_one_week_intervals(start_time_total, end_time_total):
    start_time = datetime.fromisoformat(start_time_total)
    end_time = datetime.fromisoformat(end_time_total)
    current_time = start_time
    while current_time < end_time:
        next_week = min(current_time + timedelta(weeks=1), end_time)
        yield current_time, next_week
        current_time = next_week 

def split_into_daily_intervals(start_time_str, end_time_str):
    """
    Split a time range into daily intervals
    
    Args:
        start_time_str (str): Start time in ISO format
        end_time_str (str): End time in ISO format
        
    Returns:
        list: List of tuples containing (start_time, end_time) for each day
    """
    start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
    end_time = datetime.fromisoformat(end_time_str.replace('Z', '+00:00'))
    
    intervals = []
    current_start = start_time
    
    while current_start < end_time:
        # Calculate the end of the current day
        current_end = current_start + timedelta(days=1)
        
        # If current_end would exceed the overall end_time, use end_time instead
        if current_end > end_time:
            current_end = end_time
            
        intervals.append((current_start, current_end))
        current_start = current_end
        
    return intervals 