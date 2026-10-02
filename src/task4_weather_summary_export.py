import csv
from typing import Dict, List, Union, TextIO

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def summarize_weather_data(data: List[Dict[str, any]]) -> Dict[str, float]:
    """
    Summarize the weather data across all days.
    """

    if not data:
        return {
            "average_max_temp": 0,
            "average_min_temp": 0,
            "total_precipitation": 0,
            "average_wind_speed": 0,
            "average_humidity": 0,
            "hot_days": 0,
            "windy_days": 0,
            "rainy_days": 0
        }

    average_max_temp = sum(
        day["max_temperature"] for day in data
    ) / len(data)

    average_min_temp = sum(
        day["min_temperature"] for day in data
    ) / len(data)

    total_precipitation = sum(
        day["precipitation"] for day in data
    )

    average_wind_speed = sum(
        day["wind_speed"] for day in data
    ) / len(data)

    average_humidity = sum(
        day["humidity"] for day in data
    ) / len(data)

    # Same thresholds expected by the tests.
    hot_days = sum(
        1 for day in data
        if day["max_temperature"] > 30
    )

    windy_days = sum(
        1 for day in data
        if day["wind_speed"] >= 15
    )

    rainy_days = sum(
        1 for day in data
        if day["precipitation"] > 0
    )

    return {
        "average_max_temp": average_max_temp,
        "average_min_temp": average_min_temp,
        "total_precipitation": total_precipitation,
        "average_wind_speed": average_wind_speed,
        "average_humidity": average_humidity,
        "hot_days": hot_days,
        "windy_days": windy_days,
        "rainy_days": rainy_days
    }


def export_to_csv(
    data: List[Dict[str, any]],
    file: Union[str, TextIO]
) -> None:
    """
    Export weather data to a CSV file or file-like object.
    """

    headers = [
        "Date",
        "Max Temperature",
        "Min Temperature",
        "Precipitation",
        "Wind Speed",
        "Humidity",
        "Weather Description",
        "Is Hot Day",
        "Is Windy Day",
        "Is Rainy Day"
    ]

    def write_data(writer: csv.DictWriter) -> None:
        writer.writeheader()

        for day in data:
            writer.writerow({
                "Date": day["date"],
                "Max Temperature": day["max_temperature"],
                "Min Temperature": day["min_temperature"],
                "Precipitation": day["precipitation"],
                "Wind Speed": day["wind_speed"],
                "Humidity": day["humidity"],
                "Weather Description": day["weather_description"],
                "Is Hot Day": day["max_temperature"] >= 30,
                "Is Windy Day": day["wind_speed"] >= 15,
                "Is Rainy Day": day["precipitation"] > 0
            })

    if isinstance(file, str):
        with open(file, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=headers
            )
            write_data(writer)
    else:
        writer = csv.DictWriter(
            file,
            fieldnames=headers
        )
        write_data(writer)


if __name__ == "__main__":
    try:
        # Load the JSON data
        import os

        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        # Summarize the weather data
        summary = summarize_weather_data(weather_data['daily'])

        # Print the summary for verification
        print("Weather Data Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")

        # Export the summarized data to a CSV file
        export_to_csv(weather_data['daily'], "tokyo_weather_summary.csv")

        print("Data successfully exported to tokyo_weather_summary.csv")
    except Exception as e:
        print(f"An error occurred: {e}")