import json
import os

DATA_FILE = "results.json"


def calculate_bmi(weight: float, height_cm: float) -> float:
    bmi = weight / ((height_cm / 100) ** 2)
    return round(bmi, 2)


def classify_bmi(bmi: float) -> str:
    if bmi < 18.5:
        return "niedowaga"
    elif bmi < 25.0:
        return "waga prawidłowa"
    elif bmi < 30.0:
        return "nadwaga"
    else:
        return "otyłość"


def read_positive_float(prompt: str, min_value: float, max_value: float) -> float:
    while True:
        user_input = input(prompt).strip().replace(",", ".")
        if not user_input:
            print("Błąd: Pole nie może być puste.")
            continue
        try:
            value = float(user_input)
            if min_value <= value <= max_value:
                return value
            print(f"Błąd: Wartość musi być z zakresu {min_value}-{max_value}.")
        except ValueError:
            print("Błąd: Podaj poprawną liczbę.")


def read_non_empty_string(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Błąd: Pole nie może być puste.")


def add_person(results: list) -> None:
    name = read_non_empty_string("Podaj imię: ")
    height = read_positive_float("Podaj wzrost w cm (80-250): ", 80.0, 250.0)
    weight = read_positive_float("Podaj masę w kg (20-300): ", 20.0, 300.0)

    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)

    results.append({
        "name": name,
        "height": height,
        "weight": weight,
        "bmi": bmi,
        "category": category
    })
    print(f"BMI dla {name}: {bmi:.2f} ({category})")


def show_history(results: list) -> None:
    if not results:
        print("Historia wyników jest pusta.")
        return

    for idx, p in enumerate(results, start=1):
        print(f"{idx}. {p['name']} | Wzrost: {p['height']} cm | Masa: {p['weight']} kg | BMI: {p['bmi']:.2f} | {p['category']}")


def show_summary(results: list) -> None:
    if not results:
        print("Brak zapisanych wyników.")
        return

    bmis = [p["bmi"] for p in results]
    categories_count = {
        "niedowaga": 0,
        "waga prawidłowa": 0,
        "nadwaga": 0,
        "otyłość": 0
    }

    for p in results:
        if p["category"] in categories_count:
            categories_count[p["category"]] += 1

    print(f"Liczba osób: {len(results)}")
    print(f"Średnie BMI: {sum(bmis) / len(results):.2f}")
    print(f"Min: {min(bmis):.2f}")
    print(f"Max: {max(bmis):.2f}")
    for cat, count in categories_count.items():
        print(f"{cat}: {count}")


def delete_person(results: list) -> None:
    if not results:
        print("Historia jest pusta.")
        return

    show_history(results)
    try:
        idx = int(input("Podaj numer wyniku do usunięcia: ").strip())
        if 1 <= idx <= len(results):
            removed = results.pop(idx - 1)
            print(f"Usunięto: {removed['name']}")
        else:
            print("Błąd: Nieprawidłowy numer.")
    except ValueError:
        print("Błąd: Podaj liczbę całkowitą.")


def search_person(results: list) -> None:
    if not results:
        print("Historia jest pusta.")
        return

    query = read_non_empty_string("Podaj fragment imienia: ").lower()
    matches = [p for p in results if query in p["name"].lower()]

    if not matches:
        print("Brak pasujących rekordów.")
        return

    for idx, p in enumerate(matches, start=1):
        print(f"{idx}. {p['name']} | BMI: {p['bmi']:.2f} | {p['category']}")


def load_from_json(filename: str = DATA_FILE) -> list:
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_to_json(results: list, filename: str = DATA_FILE) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
    except OSError:
        print("Błąd zapisu pliku.")


def main() -> None:
    results = load_from_json()

    while True:
        print("\n1. Dodaj wynik")
        print("2. Wyświetl historię")
        print("3. Pokaż podsumowanie")
        print("4. Usuń wynik")
        print("5. Wyszukaj osobę")
        print("0. Zakończ")

        choice = input("Wybierz opcję: ").strip()

        if choice == "1":
            add_person(results)
        elif choice == "2":
            show_history(results)
        elif choice == "3":
            show_summary(results)
        elif choice == "4":
            delete_person(results)
        elif choice == "5":
            search_person(results)
        elif choice == "0":
            save_to_json(results)
            break
        else:
            print("Nieprawidłowa opcja.")


if __name__ == "__main__":
    main()