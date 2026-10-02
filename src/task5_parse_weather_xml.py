import xml.etree.ElementTree as ET
import csv
from typing import List, Dict


def parse_weather_xml(xml_file: str) -> List[Dict[str, any]]:
    """
    Parse weather data from an XML file.
    """

    tree = ET.parse(xml_file)
    root = tree.getroot()

    weather_data = []

    for day in root.findall("day"):
        weather_data.append({
            "date": day.findtext("date"),
            "temperature": float(day.findtext("temperature")),
            "humidity": float(day.findtext("humidity")),
            "precipitation": float(day.findtext("precipitation"))
        })

    return weather_data


def save_to_csv(
    data: List[Dict[str, any]],
    filename: str = "parsed_weather_data.csv"
) -> None:
    """
    Save parsed weather data to a CSV file.
    """

    headers = [
        "Date",
        "Temperature",
        "Humidity",
        "Precipitation"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=headers
        )

        writer.writeheader()

        for day in data:
            writer.writerow({
                "Date": day["date"],
                "Temperature": day["temperature"],
                "Humidity": day["humidity"],
                "Precipitation": day["precipitation"]
            })


if __name__ == "__main__":
    try:
        # Parse the XML file
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        xml_path = os.path.join(script_dir, "weather_data.xml")
        weather_data = parse_weather_xml(xml_path)

        # Save the parsed data to a CSV file
        save_to_csv(weather_data)
        print("Data has been successfully parsed and saved to parsed_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")