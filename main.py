import json
import os

DATA_FILE = "results.json"


def calculate_bmi(weight: float, height_cm: float) -> float:
    """Oblicza wskaźnik BMI i zaokrągla go do 2 miejsc po przecinku."""
    bmi = weight / ((height_cm / 100) ** 2)
    return round(bmi, 2)


def classify_bmi(bmi: float) -> str:
    """Zwraca interpretację wyniku BMI."""
    if bmi < 18.5:
        return "niedowaga"
    elif bmi < 25.0:
        return "waga prawidłowa"
    elif bmi < 30.0:
        return "nadwaga"
    else:
        return "otyłość"


def read_positive_float(prompt: str, min_value: float, max_value: float) -> float:
    """Pobiera i waliduje liczbę zmiennoprzecinkową z określonego przedziału."""
    while True:
        user_input = input(prompt).strip().replace(",", ".")
        if not user_input:
            print("Błąd: Pole nie może być puste. Spróbuj ponownie.")
            continue
        try:
            value = float(user_input)
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Błąd: Wartość musi mieścić się w zakresie od {min_value} do {max_value}.")
        except ValueError:
            print("Błąd: Wprowadzono niepoprawną wartość liczbową. Spróbuj ponownie.")


def read_non_empty_string(prompt: str) -> str:
    """Pobiera niepusty ciąg znaków (np. imię)."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Błąd: Imię nie może być puste. Spróbuj ponownie.")


def add_person(results: list) -> None:
    """Pobiera dane osoby, oblicza BMI i dodaje rekord do listy."""
    print("\n--- Dodawanie nowej osoby ---")
    name = read_non_empty_string("Podaj imię osoby: ")
    height = read_positive_float("Podaj wzrost w cm (80-250): ", 80.0, 250.0)
    weight = read_positive_float("Podaj masę ciała w kg (20-300): ", 20.0, 300.0)

    bmi = calculate_bmi(weight, height)
    category = classify_bmi(bmi)

    person_data = {
        "name": name,
        "height": height,
        "weight": weight,
        "bmi": bmi,
        "category": category
    }
    results.append(person_data)
    print(f"\nWynik dla {name}: BMI = {bmi:.2f} ({category})")


def show_history(results: list) -> None:
    """Wyświetla historię wszystkich zapisanych wyników."""
    print("\n--- Historia wyników ---")
    if not results:
        print("Historia wyników jest pusta.")
        return

    for idx, person in enumerate(results, start=1):
        print(
            f"{idx}. {person['name']} | "
            f"Wzrost: {person['height']} cm | "
            f"Masa: {person['weight']} kg | "
            f"BMI: {person['bmi']:.2f} | "
            f"{person['category']}"
        )


def show_summary(results: list) -> None:
    """Wyświetla podsumowanie statystyczne zapisanych wyników."""
    print("\n--- Podsumowanie wyników ---")
    if not results:
        print("Brak zapisanych wyników. Dodaj co najmniej jedną osobę, aby zobaczyć podsumowanie.")
        return

    count = len(results)
    bmis = [p["bmi"] for p in results]
    avg_bmi = sum(bmis) / count
    min_bmi = min(bmis)
    max_bmi = max(bmis)

    categories_count = {
        "niedowaga": 0,
        "waga prawidłowa": 0,
        "nadwaga": 0,
        "otyłość": 0
    }

    for p in results:
        cat = p["category"]
        if cat in categories_count:
            categories_count[cat] += 1

    print(f"Liczba osób: {count}")
    print(f"Średnie BMI: {avg_bmi:.2f}")
    print(f"Min: {min_bmi:.2f}")
    print(f"Max: {max_bmi:.2f}")
    print("\nPodział na kategorie:")
    for cat, cat_count in categories_count.items():
        print(f"  {cat}: {cat_count}")


# --- Zadanie dodatkowe: Poziom + ---
def delete_person(results: list) -> None:
    """Usuwa wybrany rekord z historii na podstawie numeru porządkowego."""
    if not results:
        print("\nHistoria jest pusta – brak wyników do usunięcia.")
        return

    show_history(results)
    user_input = input("\nPodaj numer wyniku do usunięcia: ").strip()
    try:
        idx = int(user_input)
        if 1 <= idx <= len(results):
            removed = results.pop(idx - 1)
            print(f"Usunięto wynik osoby: {removed['name']} (BMI: {removed['bmi']:.2f}).")
        else:
            print(f"Błąd: Nie istnieje wynik o numerze {idx}.")
    except ValueError:
        print("Błąd: Podano niepoprawny numer.")


# --- Zadanie dodatkowe: Poziom ++ ---
def search_person(results: list) -> None:
    """Wyszukuje osoby po fragmencie imienia (bez rozróżniania wielkości liter)."""
    if not results:
        print("\nHistoria jest pusta – brak wyników do przeszukania.")
        return

    query = read_non_empty_string("\nPodaj imię lub jego fragment do wyszukania: ").lower()
    matches = [p for p in results if query in p["name"].lower()]

    if not matches:
        print(f"Nie znaleziono osób pasujących do frazy '{query}'.")
        return

    print(f"\nZnaleziono {len(matches)} pasujących rekordów:")
    for idx, person in enumerate(matches, start=1):
        print(f"{idx}. {person['name']} | BMI: {person['bmi']:.2f} | {person['category']}")


# --- Zadanie dodatkowe: Poziom +++ ---
def load_from_json(filename: str = DATA_FILE) -> list:
    """Wczytuje historię wyników z pliku JSON przy starcie programu."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Uwaga: Nie udało się odczytać pliku historii. Inicjalizacja pustej listy.")
        return []


def save_to_json(results: list, filename: str = DATA_FILE) -> None:
    """Zapisuje historię wyników do pliku JSON przy zakończeniu programu."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
        print(f"Zapisano historię ({len(results)} rekordów) do pliku {filename}.")
    except OSError as e:
        print(f"Błąd podczas zapisu do pliku: {e}")


def main() -> None:
    """Główna pętla programu z menu tekstowym."""
    results = load_from_json()

    while True:
        print("\n=== KALKULATOR BMI ===")
        print("1. Dodaj wynik")
        print("2. Wyświetl historię")
        print("3. Pokaż podsumowanie")
        print("4. Usuń wynik (Poziom +)")
        print("5. Wyszukaj osobę (Poziom ++)")
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
            print("Koniec działania programu.")
            break
        else:
            print("Błąd: Nieznana opcja menu. Wybierz numer od 0 do 5.")


if __name__ == "__main__":
    main()