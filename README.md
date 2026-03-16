# Prayer Time API

A lightweight REST API for calculating **Islamic prayer times** using astronomical calculations based on **PyEphem**.

This API calculates **Imsak, Fajr, Sunrise, Dhuhr, Asr, Maghrib, and Isha** using geographic coordinates (latitude, longitude, elevation).

The calculation follows an astronomical approach aligned with **Indonesian Ministry of Religious Affairs (Kemenag) standards with Ihtiyat adjustment**.

---

## Features

* Astronomical prayer time calculation
* Based on geographic coordinates
* JSON REST API
* Lightweight Flask server
* Default location included
* Suitable for web, bots, and IoT devices

---

## Technology Stack

* Python
* Flask
* PyEphem
* pytz

---

## Installation

Clone the repository:

```bash
git clone https://github.com/username/prayer-time-api.git
cd prayer-time-api
```

Install dependencies:

```bash
pip install flask ephem pytz
```

Run the server:

```bash
python app.py
```

The server will start at:

```
http://localhost:5000
```

---

## API Endpoint

### GET `/api/jadwal`

Returns prayer times based on geographic coordinates.

### Query Parameters

| Parameter | Description        | Default    |
| --------- | ------------------ | ---------- |
| lat       | Latitude           | -7.667808  |
| lon       | Longitude          | 109.656167 |
| elev      | Elevation (meters) | 20         |

### Example Request

```
http://localhost:5000/api/jadwal
```

or

```
http://localhost:5000/api/jadwal?lat=-7.667808&lon=109.656167&elev=20
```

---

## Example Response

```json
{
  "status": "sukses",
  "data": {
    "tanggal": "2026-03-16",
    "koordinat": {
      "latitude": -7.667808,
      "longitude": 109.656167,
      "elevation": 20
    },
    "standar": "Kemenag RI (+ Ihtiyat)",
    "jadwal": {
      "imsak": "04:21",
      "subuh": "04:31",
      "syuruq": "05:44",
      "dzuhur": "11:52",
      "ashar": "15:07",
      "maghrib": "17:56",
      "isya": "19:02"
    }
  }
}
```

---

## Error Response

```json
{
  "status": "error",
  "pesan": "Invalid coordinates or system error."
}
```

---

## Usage Example

### JavaScript

```javascript
fetch("http://localhost:5000/api/jadwal?lat=-7.667808&lon=109.656167")
  .then(response => response.json())
  .then(data => console.log(data));
```

### Python

```python
import requests

url = "http://localhost:5000/api/jadwal"
params = {
    "lat": -7.667808,
    "lon": 109.656167
}

response = requests.get(url, params=params)
print(response.json())
```

---

## Default Location

If no parameters are provided, the API uses the following location:

```
Kebumen, Central Java, Indonesia
Latitude: -7.667808
Longitude: 109.656167
Elevation: 20 meters
```

---

## License

MIT License
