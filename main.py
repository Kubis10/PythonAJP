import lab1_bmi
import lab2_temperatura


def main() -> None:
    while True:
        print("\n1. Laboratorium 1 - Kalkulator BMI")
        print("2. Laboratorium 2 - Dziennik temperatury")
        print("0. Wyjście")

        choice = input("Wybierz opcję: ").strip()

        if choice == "1":
            lab1_bmi.main()
        elif choice == "2":
            lab2_temperatura.main()
        elif choice == "0":
            break
        else:
            print("Niepoprawny wybór.")


if __name__ == "__main__":
    main()