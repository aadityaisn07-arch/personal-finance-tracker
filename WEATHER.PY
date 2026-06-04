# Weather Data Analyzer
# Analyzes weather patterns and provides climate insights
# Author: Your Name
# Built with Python 3

import json
import os
import statistics
from datetime import datetime

DATA_FILE = "weather_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"records": [], "city": ""}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_weather_condition(temp, humidity, wind_speed):
    if temp >= 35:
        condition = "🌞 Very Hot"
    elif temp >= 25:
        condition = "☀️  Warm"
    elif temp >= 15:
        condition = "⛅ Mild"
    elif temp >= 5:
        condition = "🌥️  Cool"
    else:
        condition = "❄️  Cold"

    if humidity >= 80:
        humidity_desc = "Very Humid"
    elif humidity >= 60:
        humidity_desc = "Humid"
    elif humidity >= 40:
        humidity_desc = "Comfortable"
    else:
        humidity_desc = "Dry"

    return condition, humidity_desc

def add_weather_record(data):
    print("\n--- ADD WEATHER RECORD ---")

    if not data["city"]:
        data["city"] = input("City Name: ").strip()

    date_input = input("Date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date_input:
        date_input = datetime.now().strftime("%Y-%m-%d")

    try:
        temp = float(input("Temperature (°C): "))
        humidity = float(input("Humidity (%): "))
        wind_speed = float(input("Wind Speed (km/h): "))
        rainfall = float(input("Rainfall (mm): "))
    except ValueError:
        print("Please enter valid numbers.")
        return

    condition, humidity_desc = get_weather_condition(temp, humidity, wind_speed)

    record = {
        "date": date_input,
        "temperature": temp,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "rainfall": rainfall,
        "condition": condition,
        "humidity_desc": humidity_desc,
        "recorded_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    data["records"].append(record)
    save_data(data)
    print(f"\n✓ Weather record for {date_input} added!")
    print(f"  Condition: {condition} | {humidity_desc}")

def view_all_records(data):
    if not data["records"]:
        print("\nNo weather records found.")
        return

    city = data.get("city", "Unknown City")
    sorted_records = sorted(data["records"], key=lambda x: x["date"], reverse=True)

    print(f"\n{'='*80}")
    print(f"  WEATHER RECORDS — {city.upper()}")
    print(f"{'='*80}")
    print(f"{'Date':<15} {'Temp°C':<10} {'Humidity':<12} {'Wind km/h':<12} {'Rain mm':<10} {'Condition'}")
    print("-"*80)

    for r in sorted_records:
        print(f"{r['date']:<15} {r['temperature']:<10.1f} {r['humidity']:<12.1f} {r['wind_speed']:<12.1f} {r['rainfall']:<10.1f} {r['condition']}")

    print("="*80)

def monthly_analysis(data):
    if not data["records"]:
        print("\nNo records found.")
        return

    monthly = {}
    for record in data["records"]:
        month = record["date"][:7]
        if month not in monthly:
            monthly[month] = {"temps": [], "humidity": [], "rainfall": [], "wind": []}
        monthly[month]["temps"].append(record["temperature"])
        monthly[month]["humidity"].append(record["humidity"])
        monthly[month]["rainfall"].append(record["rainfall"])
        monthly[month]["wind"].append(record["wind_speed"])

    print(f"\n{'='*75}")
    print(f"  MONTHLY WEATHER ANALYSIS")
    print(f"{'='*75}")
    print(f"{'Month':<12} {'Avg Temp':<12} {'Max Temp':<12} {'Min Temp':<12} {'Total Rain':<12} {'Avg Wind'}")
    print("-"*75)

    for month in sorted(monthly.keys()):
        m = monthly[month]
        print(f"{month:<12} {statistics.mean(m['temps']):<12.1f} {max(m['temps']):<12.1f} {min(m['temps']):<12.1f} {sum(m['rainfall']):<12.1f} {statistics.mean(m['wind']):.1f}")

    print("="*75)

def climate_summary(data):
    if not data["records"]:
        print("\nNo records found.")
        return

    temps = [r["temperature"] for r in data["records"]]
    humidity_list = [r["humidity"] for r in data["records"]]
    rainfall_list = [r["rainfall"] for r in data["records"]]
    wind_list = [r["wind_speed"] for r in data["records"]]

    hottest = max(data["records"], key=lambda x: x["temperature"])
    coldest = min(data["records"], key=lambda x: x["temperature"])
    rainiest = max(data["records"], key=lambda x: x["rainfall"])
    windiest = max(data["records"], key=lambda x: x["wind_speed"])

    print(f"\n{'='*55}")
    print(f"  CLIMATE SUMMARY — {data.get('city','').upper()}")
    print(f"{'='*55}")
    print(f"  Total Records:      {len(data['records'])}")
    print(f"\n  TEMPERATURE")
    print(f"    Average:          {statistics.mean(temps):.1f}°C")
    print(f"    Highest:          {max(temps):.1f}°C on {hottest['date']}")
    print(f"    Lowest:           {min(temps):.1f}°C on {coldest['date']}")

    print(f"\n  RAINFALL")
    print(f"    Total Rainfall:   {sum(rainfall_list):.1f} mm")
    print(f"    Highest Day:      {max(rainfall_list):.1f} mm on {rainiest['date']}")
    print(f"    Average Daily:    {statistics.mean(rainfall_list):.1f} mm")

    print(f"\n  WIND")
    print(f"    Average Speed:    {statistics.mean(wind_list):.1f} km/h")
    print(f"    Highest Speed:    {max(wind_list):.1f} km/h on {windiest['date']}")

    print(f"\n  HUMIDITY")
    print(f"    Average:          {statistics.mean(humidity_list):.1f}%")

    temp_ranges = {"Very Hot (35+)": 0, "Warm (25-34)": 0, "Mild (15-24)": 0, "Cool (5-14)": 0, "Cold (<5)": 0}
    for t in temps:
        if t >= 35: temp_ranges["Very Hot (35+)"] += 1
        elif t >= 25: temp_ranges["Warm (25-34)"] += 1
        elif t >= 15: temp_ranges["Mild (15-24)"] += 1
        elif t >= 5: temp_ranges["Cool (5-14)"] += 1
        else: temp_ranges["Cold (<5)"] += 1

    print(f"\n  TEMPERATURE DISTRIBUTION:")
    for range_name, count in temp_ranges.items():
        if count > 0:
            bar = "█" * count
            print(f"    {range_name:<20} {bar} ({count})")
    print("="*55)

def temperature_trend(data):
    if len(data["records"]) < 3:
        print("\nNeed at least 3 records for trend analysis.")
        return

    sorted_records = sorted(data["records"], key=lambda x: x["date"])
    temps = [r["temperature"] for r in sorted_records]
    dates = [r["date"] for r in sorted_records]

    print(f"\n{'='*60}")
    print(f"  TEMPERATURE TREND")
    print(f"{'='*60}")

    for i, (d, t) in enumerate(zip(dates, temps)):
        bar_length = int(t)
        bar = "█" * max(0, int(bar_length/2))
        trend = ""
        if i > 0:
            diff = t - temps[i-1]
            trend = f"  ↑ +{diff:.1f}" if diff > 0 else f"  ↓ {diff:.1f}" if diff < 0 else "  → same"
        print(f"  {d}  {t:>6.1f}°C  {bar}{trend}")

    if temps[-1] > temps[0]:
        print(f"\n  📈 Overall trend: WARMING (+{temps[-1]-temps[0]:.1f}°C over period)")
    elif temps[-1] < temps[0]:
        print(f"\n  📉 Overall trend: COOLING ({temps[-1]-temps[0]:.1f}°C over period)")
    else:
        print(f"\n  ➡️  Overall trend: STABLE")
    print("="*60)

def main():
    print("\n" + "="*55)
    print("    WEATHER DATA ANALYZER")
    print("    Climate Insights & Pattern Analysis")
    print("="*55)

    data = load_data()

    while True:
        print("\nMAIN MENU")
        print("-"*40)
        print("1. Add Weather Record")
        print("2. View All Records")
        print("3. Monthly Analysis")
        print("4. Climate Summary")
        print("5. Temperature Trend")
        print("6. Exit")
        print("-"*40)

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            add_weather_record(data)
            data = load_data()
        elif choice == "2":
            view_all_records(data)
        elif choice == "3":
            monthly_analysis(data)
        elif choice == "4":
            climate_summary(data)
        elif choice == "5":
            temperature_trend(data)
        elif choice == "6":
            print("\nGoodbye! Keep tracking the weather.")
            break
        else:
            print("\nInvalid choice. Please enter 1-6.")

if __name__ == "__main__":
    main()
