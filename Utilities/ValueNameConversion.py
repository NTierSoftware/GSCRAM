# ValueToName.py
#
# Alex Erf, airspace, alex.erf@airspace.co
# Created 8/20/2018


def valueToName(val: 'DataElement', enumGroup):
    try: val = enumGroup(val).name
    except Exception: val = val.data
    finally: return val

def objectToValue(o, t):
    return t[o].value if isinstance(o, str) else o
