from django import template
register = template . Library ()

@register.filter()
def smooth_timedelta(timedeltaobj):
    """Convert a datetime.timedelta object into Days, Hours, Minutes, Seconds."""
    secs = timedeltaobj.total_seconds()
    timetot = ""
    if secs > 86400:
        secs = secs - days*86400
    hrs = secs // 3600
    if int(hrs) < 10:
        timetot = "0"
    timetot += "{}:00".format(int(hrs))
    return timetot

@register.filter()
def smooth_timedelta2(timedeltaobj):
    """Convert a datetime.timedelta object into Days, Hours, Minutes, Seconds."""
    secs = timedeltaobj.total_seconds()
    timetot = ""
    if secs > 86400:
        secs = secs - days*86400
    hrs = secs // 3600
    if int(hrs) < 10:
        timetot = "0"
    timetot += "{}".format(int(hrs))
    return timetot

@register.filter()
def horas_emmilisegundos(timedeltaobj):
    return (timedeltaobj * 3600000)
