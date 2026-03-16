from flask import Flask, request, jsonify
import ephem
import math
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

def hitung_sholat(lat, lon, elevation=20):
    obs = ephem.Observer()
    obs.lat = str(lat)
    obs.lon = str(lon)
    obs.elevation = float(elevation)
    
    wib = pytz.timezone('Asia/Jakarta')
    sekarang_wib = datetime.now(wib)
    awal_hari_wib = wib.localize(datetime(sekarang_wib.year, sekarang_wib.month, sekarang_wib.day))
    awal_hari_utc = awal_hari_wib.astimezone(pytz.utc)
    
    obs.date = awal_hari_utc
    sun = ephem.Sun()
    
    # Perhitungan Astronomis
    dzuhur_utc = obs.next_transit(sun).datetime()
    
    obs.date = dzuhur_utc
    obs.horizon = '-20'
    subuh_utc = obs.previous_rising(sun, use_center=True).datetime()
    
    imsak_utc = subuh_utc - timedelta(minutes=10)
    
    obs.horizon = '-0:34'
    syuruq_utc = obs.previous_rising(sun, use_center=False).datetime()
    
    obs.horizon = '-0:34'
    obs.date = dzuhur_utc
    maghrib_utc = obs.next_setting(sun, use_center=False).datetime()
    
    obs.horizon = '-18'
    isya_utc = obs.next_setting(sun, use_center=True).datetime()
    
    obs.date = dzuhur_utc
    sun.compute(obs) 
    alt_dzuhur = float(sun.alt)
    
    alt_asr = math.atan(1.0 / (1.0 + 1.0 / math.tan(alt_dzuhur)))
    
    cek_waktu = dzuhur_utc
    ashar_utc = None
    while cek_waktu < maghrib_utc:
        obs.date = cek_waktu
        sun.compute(obs)
        if float(sun.alt) <= alt_asr:
            ashar_utc = cek_waktu
            break
        cek_waktu += timedelta(minutes=1)

    # Format Kemenag + Ihtiyat
    def format_kemenag(waktu_utc, is_waktu_sholat=True):
        waktu_utc_aware = waktu_utc.replace(tzinfo=pytz.utc)
        waktu_wib = waktu_utc_aware.astimezone(wib)
        
        if is_waktu_sholat:
            waktu_wib += timedelta(minutes=2)
            
        if waktu_wib.second > 0:
            waktu_wib += timedelta(minutes=1)
            
        return waktu_wib.strftime('%H:%M')

    # Return Data sebagai Dictionary (akan jadi JSON)
    return {
        "tanggal": sekarang_wib.strftime('%Y-%m-%d'),
        "koordinat": {"latitude": lat, "longitude": lon, "elevation": elevation},
        "standar": "Kemenag RI (+ Ihtiyat)",
        "jadwal": {
            "imsak": format_kemenag(imsak_utc),
            "subuh": format_kemenag(subuh_utc),
            "syuruq": format_kemenag(syuruq_utc, is_waktu_sholat=False),
            "dzuhur": format_kemenag(dzuhur_utc),
            "ashar": format_kemenag(ashar_utc) if ashar_utc else None,
            "maghrib": format_kemenag(maghrib_utc),
            "isya": format_kemenag(isya_utc)
        }
    }

# Endpoint API
@app.route('/api/jadwal', methods=['GET'])
def get_jadwal():
    lat = request.args.get('lat', '-7.670829')
    lon = request.args.get('lon', '109.660677')
    elev = request.args.get('elev', 20)
    
    try:
        data_sholat = hitung_sholat(lat, lon, elev)
        return jsonify({
            "status": "sukses",
            "data": data_sholat
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "pesan": "Koordinat tidak valid atau error sistem.",
            "detail": str(e)
        }), 400
