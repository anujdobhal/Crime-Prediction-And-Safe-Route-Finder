import sys
import csv
from datetime import datetime

if len(sys.argv) != 5:
    print("Error: Expected 4 arguments", file=sys.stderr)
    sys.exit(1)

latitude = sys.argv[1]
longitude = sys.argv[2]
crime_type = sys.argv[3]
crime_time = sys.argv[4]

try:
    with open(r'utility\dummy_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([latitude, longitude, crime_type, crime_time])
except Exception as e:
    print(f"File write error: {e}", file=sys.stderr)
    sys.exit(1)
