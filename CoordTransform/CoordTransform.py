import math

a = 6378245.0
ee = 0.00669342162296594323

def transform(lng, lat):
    """
    """
    dLat = transformLat(lng - 105.0, lat - 35.0)
    dLng = transformLon(lng - 105.0, lat - 35.0)
    radLat = lat / 180.0 * math.pi
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic

    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * math.pi)
    dLng = (dLng * 180.0) / (a / sqrtMagic * math.cos(radLat) * math.pi)

    mgLat = lat + dLat
    mgLng = lng + dLng
    return mgLng, mgLat


def transformLat(x, y):
    """
    """
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
    return ret

def transformLon(x, y):
    """
    """
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
    return ret

def outOfChina(lng, lat):
    """
    """
    if lng < 72.004 or lng > 137.8347:
        return True
    
    if lat < 0.8293 or lat > 55.8271:
        return True
    
    return False


def WGSToGC02(lng, lat):
    """
    lng:
    lat:
    """
    if outOfChina(lng, lat):
        return lng, lat

    dLat = transformLat(lng - 105.0, lat - 35.0)
    dLng = transformLon(lng - 105.0, lat - 35.0)

    radLat = lat / 180.0 * math.pi
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)

    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * math.pi)
    dLng = (dLng * 180.0) / (a / sqrtMagic * math.cos(radLat) * math.pi)

    mgLat = lat + dLat
    mgLng = lng + dLng
    return mgLng, mgLat

def GC02ToWGS(lng, lat):
    """
    GCJ02 to GPS1984
    lng: GCJ02 lontitude
    lat: GCJ02 latitude
    """
    if outOfChina(lng, lat):
        return lng, lat
    
    dlat = transformLat(lng - 105.0, lat - 35.0)
    dlng = transformLon(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * math.pi)
    dlng = (dlng * 180.0) / (a / sqrtMagic * math.cos(radlat) * math.pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return lng * 2 - mglng, lat * 2 - mglat

def main():
    gclng, gclat = GC02ToWGS(121.503309,31.243886)
    print(gclng, gclat)

if __name__ == '__main__':
    main()