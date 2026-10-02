import csv
import re
from typing import List, Dict


def clean_text(line: str) -> str:
    """
    Clean the text line by removing non-ASCII characters and fixing known issues.

    Args:
        line (str): The line of text to clean.

    Returns:
        str: The cleaned line of text.
    """
    # Replace non-breaking spaces and other non-ASCII characters
    line = line.replace("\u00a0", " ")

    # Replace common special characters
    line = line.replace("–", "-")
    line = line.replace("—", "-")
    line = line.replace("°", "")

    # Remove all remaining non-ASCII characters
    line = line.encode("ascii", errors="ignore").decode("ascii")

    # Remove extra spaces
    line = re.sub(r"\s+", " ", line)

    return line.strip()


def extract_weather_data(text_file: str) -> List[Dict[str, any]]:
    """
    Extract weather data from a text file using regular expressions.
    """

    weather_data = []

    with open(text_file, "r", encoding="utf-8") as file:
        text = file.read()

    # Clean the entire text first
    text = clean_text(text)

    # Find individual weather records.
    # A record starts with a date and continues until the next date
    # or the end of the text.
    records = re.split(
        r"(?=Date\s*:\s*\d{4}-\d{2}-\d{2})",
        text,
        flags=re.IGNORECASE
    )

    for record in records:
        if not record.strip():
            continue

        date_match = re.search(
            r"Date\s*:\s*(\d{4}-\d{2}-\d{2})",
            record,
            re.IGNORECASE
        )

        max_temp_match = re.search(
            r"(?:Max(?:imum)?\s*(?:Temperature|Temp)|Maximum)\s*:\s*"
            r"(-?\d+(?:\.\d+)?)",
            record,
            re.IGNORECASE
        )

        min_temp_match = re.search(
            r"(?:Min(?:imum)?\s*(?:Temperature|Temp)|Minimum)\s*:\s*"
            r"(-?\d+(?:\.\d+)?)",
            record,
            re.IGNORECASE
        )

        humidity_match = re.search(
            r"Humidity\s*:\s*(\d+(?:\.\d+)?)",
            record,
            re.IGNORECASE
        )

        precipitation_match = re.search(
            r"Precipitation\s*:\s*(\d+(?:\.\d+)?)",
            record,
            re.IGNORECASE
        )

        if (
            date_match
            and max_temp_match
            and min_temp_match
            and humidity_match
            and precipitation_match
        ):
            weather_data.append({
                "date": date_match.group(1),
                "max_temperature": float(max_temp_match.group(1)),
                "min_temperature": float(min_temp_match.group(1)),
                "humidity": float(humidity_match.group(1)),
                "precipitation": float(
                    precipitation_match.group(1)
                )
            })

    return weather_data


def save_to_csv(
    data: List[Dict[str, any]],
    filename: str = "extracted_weather_data.csv"
) -> None:
    """
    Save extracted weather data to a CSV file.

    Args:
        data (list of dict): Extracted weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    headers = [
        "Date",
        "Max Temperature",
        "Min Temperature",
        "Humidity",
        "Precipitation"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=headers
        )

        writer.writeheader()

        for item in data:
            writer.writerow({
                "Date": item["date"],
                "Max Temperature": item["max_temperature"],
                "Min Temperature": item["min_temperature"],
                "Humidity": item["humidity"],
                "Precipitation": item["precipitation"]
            })


if __name__ == "__main__":
    try:
        # Extract data from the text file
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        txt_path = os.path.join(script_dir, "weather_report.txt")
        weather_data = extract_weather_data(txt_path)

        # Save the extracted data to a CSV file
        save_to_csv(weather_data)
        print("Data has been successfully extracted and saved to extracted_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")