import json
import os
from datetime import datetime

# Wybrałem słownik (dict) dla pojedynczego pomiaru oraz listę (list) dla wszystkich pomiarów, ponieważ słownik zapewnia czytelny dostęp po kluczach i łatwy zapis do JSON, a lista zachowuje kolejność pomiarów potrzebną do analizy zmian i trendu.

DATA_FILE = "measurements.json"
DATE_FORMAT = "%Y-%m-%d %H:%M"


def read_datetime(prompt: str) -> str:
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Pole nie może być puste.")
            continue
        try:
            valid_dt = datetime.strptime(user_input, DATE_FORMAT)
            return valid_dt.strftime(DATE_FORMAT)
        except ValueError:
            print("Niepoprawny format daty i godziny.")


def read_temperature(prompt: str) -> float:
    while True:
        user_input = input(prompt).strip().replace(",", ".")
        if not user_input:
            print("Podaj liczbę.")
            continue
        try:
            temp = float(user_input)
            if -90.0 <= temp <= 60.0:
                return round(temp, 2)
            print("Temperatura poza zakresem (-90 do 60 °C).")
        except ValueError:
            print("Podaj liczbę.")


def read_measurement() -> dict:
    dt_str = read_datetime("Data i godzina (RRRR-MM-DD GG:MM): ")
    temp = read_temperature("Temperatura (°C): ")
    return {
        "datetime": dt_str,
        "temperature": temp
    }


def add_measurement(measurements: list) -> None:
    measurement = read_measurement()
    measurements.append(measurement)
    print(f"Dodano: {measurement['datetime']} -> {measurement['temperature']:.1f} °C")


def show_measurements(measurements: list) -> None:
    if not measurements:
        print("Historia pomiarów jest pusta.")
        return

    for idx, m in enumerate(measurements, start=1):
        print(f"{idx}. {m['datetime']} | {m['temperature']:.1f} °C")


def calculate_statistics(measurements: list) -> tuple | None:
    # Wybrałem krotkę (tuple), ponieważ zwracamy stały, niemutowalny zestaw obliczonych wartości statystycznych.
    if not measurements:
        return None

    temps = [m["temperature"] for m in measurements]
    count = len(temps)
    min_temp = min(temps)
    max_temp = max(temps)
    avg_temp = sum(temps) / count
    temp_range = max_temp - min_temp

    return (count, min_temp, max_temp, avg_temp, temp_range)


def show_summary(measurements: list) -> None:
    stats = calculate_statistics(measurements)
    if stats is None:
        print("Brak pomiarów.")
        return

    count, min_temp, max_temp, avg_temp, temp_range = stats
    print(f"Liczba pomiarów: {count}")
    print(f"Minimum: {min_temp:.1f} °C")
    print(f"Maksimum: {max_temp:.1f} °C")
    print(f"Średnia: {avg_temp:.2f} °C")
    print(f"Zakres: {temp_range:.1f} °C")


def calculate_changes(measurements: list) -> dict | None:
    if len(measurements) < 2:
        return None

    deltas = []
    increases = 0
    decreases = 0
    no_changes = 0

    for i in range(1, len(measurements)):
        diff = round(measurements[i]["temperature"] - measurements[i - 1]["temperature"], 2)
        deltas.append(diff)
        if diff > 0:
            increases += 1
        elif diff < 0:
            decreases += 1
        else:
            no_changes += 1

    pos = [d for d in deltas if d > 0]
    neg = [d for d in deltas if d < 0]

    max_inc = max(pos) if pos else 0.0
    max_dec = min(neg) if neg else 0.0

    if increases > 0 and decreases == 0:
        trend = "temperatura ogólnie rośnie"
    elif decreases > 0 and increases == 0:
        trend = "temperatura ogólnie spada"
    elif increases == 0 and decreases == 0:
        trend = "brak zmian"
    else:
        trend = "zmiany są mieszane"

    return {
        "deltas": deltas,
        "max_increase": max_inc,
        "max_decrease": max_dec,
        "increases": increases,
        "decreases": decreases,
        "no_changes": no_changes,
        "trend": trend
    }


def show_changes(measurements: list) -> None:
    analysis = calculate_changes(measurements)
    if analysis is None:
        print("Wymagane co najmniej 2 pomiary.")
        return

    print("Zmiany (ΔT):", ", ".join(f"{d:+.1f} °C" for d in analysis["deltas"]))
    print(f"Największy wzrost: +{analysis['max_increase']:.1f} °C")
    print(f"Największy spadek: {analysis['max_decrease']:.1f} °C")
    print(f"Liczba wzrostów: {analysis['increases']}")
    print(f"Liczba spadków: {analysis['decreases']}")
    print(f"Liczba przypadków bez zmiany: {analysis['no_changes']}")
    print(f"Trend: {analysis['trend']}")


def delete_measurement(measurements: list) -> None:
    if not measurements:
        print("Historia jest pusta.")
        return

    show_measurements(measurements)
    try:
        idx = int(input("Podaj numer pomiaru do usunięcia: ").strip())
        if 1 <= idx <= len(measurements):
            removed = measurements.pop(idx - 1)
            print(f"Usunięto: {removed['datetime']} ({removed['temperature']:.1f} °C)")
        else:
            print("Błąd: Nieprawidłowy numer.")
    except ValueError:
        print("Błąd: Podaj liczbę całkowitą.")


def filter_measurements(measurements: list) -> None:
    if not measurements:
        print("Historia jest pusta.")
        return

    t_min = read_temperature("Podaj T_min: ")
    t_max = read_temperature("Podaj T_max: ")

    if t_min > t_max:
        t_min, t_max = t_max, t_min

    filtered = [m for m in measurements if t_min <= m["temperature"] <= t_max]

    if not filtered:
        print("Brak pomiarów w podanym zakresie.")
        return

    for idx, m in enumerate(filtered, start=1):
        print(f"{idx}. {m['datetime']} | {m['temperature']:.1f} °C")


def load_from_json(filename: str = DATA_FILE) -> list:
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_to_json(measurements: list, filename: str = DATA_FILE) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(measurements, file, ensure_ascii=False, indent=4)
    except OSError:
        print("Błąd zapisu pliku.")


def main() -> None:
    measurements = load_from_json()

    while True:
        print("\n1. Dodaj pomiar")
        print("2. Wyświetl historię")
        print("3. Pokaż statystyki")
        print("4. Analiza zmian temperatury")
        print("5. Usuń pomiar")
        print("6. Filtruj pomiary")
        print("0. Zakończ")

        choice = input("Wybierz opcję: ").strip()

        if choice == "1":
            add_measurement(measurements)
        elif choice == "2":
            show_measurements(measurements)
        elif choice == "3":
            show_summary(measurements)
        elif choice == "4":
            show_changes(measurements)
        elif choice == "5":
            delete_measurement(measurements)
        elif choice == "6":
            filter_measurements(measurements)
        elif choice == "0":
            save_to_json(measurements)
            break
        else:
            print("Nieprawidłowa opcja.")


if __name__ == "__main__":
    main()