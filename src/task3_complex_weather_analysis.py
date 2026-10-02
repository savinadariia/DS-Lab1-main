from typing import Dict, List, Any

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def analyze_daily_weather(
    day: Dict[str, Any],
    temp_threshold: float = 30,
    wind_threshold: float = 15,
    humidity_threshold: float = 70
) -> Dict[str, Any]:
    """
    Analyze weather data for a single day.

    Args:
        day (dict): The weather data for the day.
        temp_threshold (float): The temperature threshold to determine a hot day.
        wind_threshold (float): The wind speed threshold to determine a windy day.
        humidity_threshold (float): The humidity threshold to determine uncomfortable weather.

    Returns:
        dict: A dictionary with analysis results for the day.
    """

    max_temperature = day["max_temperature"]
    min_temperature = day["min_temperature"]
    wind_speed = day["wind_speed"]
    humidity = day["humidity"]
    precipitation = day["precipitation"]

    return {
        "date": day["date"],
        "is_hot_day": max_temperature > temp_threshold,
        "max_temperature": max_temperature,
        "min_temperature": min_temperature,
        "temperature_swing": max_temperature - min_temperature,
        "is_windy_day": wind_speed >= wind_threshold,
        "wind_speed": wind_speed,
        "is_uncomfortable_day": humidity >= humidity_threshold,
        "humidity": humidity,
        "is_rainy_day": precipitation > 0,
        "precipitation": precipitation,
        "weather_description": day["weather_description"]
    }


def generate_daily_report(analysis: Dict[str, Any]) -> str:
    """
    Generate a detailed report based on the analysis results for a single day.

    Args:
        analysis (dict): The analysis results for the day.

    Returns:
        str: A detailed report as a string.
    """

    report = (
        f"Weather report for {analysis['date']}: "
        f"{analysis['weather_description']}. "
    )

    if analysis["is_hot_day"]:
        report += "It was a hot day. "

    if analysis["is_windy_day"]:
        report += "It was a windy day. "

    if analysis["is_uncomfortable_day"]:
        report += "The weather was uncomfortable. "

    report += (
        f"Max {analysis['max_temperature']}°C, "
        f"Min {analysis['min_temperature']}°C. "
    )

    if analysis["is_rainy_day"]:
        report += (
            f"Precipitation: "
            f"{analysis['precipitation']} mm."
        )
    else:
        report += "There was no precipitation."

    return report


def summarize_weather_analysis(
    analyses: List[Dict[str, Any]]
) -> str:
    """
    Summarize the weather analysis over multiple days.

    Args:
        analyses (list of dict): A list of daily analysis results.

    Returns:
        str: A summary report as a string.
    """

    if not analyses:
        return ""

    hottest_day = max(
        analyses,
        key=lambda day: day["max_temperature"]
    )

    windiest_day = max(
        analyses,
        key=lambda day: day["wind_speed"]
    )

    most_humid_day = max(
        analyses,
        key=lambda day: day["humidity"]
    )

    rainiest_day = max(
        analyses,
        key=lambda day: day["precipitation"]
    )

    return (
        f"Hottest day: {hottest_day['date']} "
        f"with {hottest_day['max_temperature']}°C\n"
        f"Windiest day: {windiest_day['date']} "
        f"with {windiest_day['wind_speed']} km/h\n"
        f"Most humid day: {most_humid_day['date']} "
        f"with {most_humid_day['humidity']}%\n"
        f"Rainiest day: {rainiest_day['date']} "
        f"with {rainiest_day['precipitation']} mm"
    )


if __name__ == "__main__":
    try:
        # Load the JSON data
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        # Analyze the weather data for each day
        analyses = [analyze_daily_weather(day) for day in weather_data['daily']]

        # Generate and print daily reports
        for analysis in analyses:
            report = generate_daily_report(analysis)
            print(report)

        # Generate and print a summary report
        summary_report = summarize_weather_analysis(analyses)
        print(summary_report)
    except Exception as e:
        print(f"An error occurred: {e}")
