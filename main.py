import argparse
import path_creator

def dodaj_argumenty(parser):
    parser.add_argument("--miesiące", required=True, nargs="+", type=str, help="lista miesięcy (słownie)")
    parser.add_argument("--dni_tygodnia", required=True, nargs="+", type=str, help="lista dni tygodnia (słownie); musi być ich dokładnie tyle co wymienionych miesięcy")
    parser.add_argument("--pora_dnia", default="rano", nargs="+", type=str, help="pora dnia (słownie); domyślnie rano")
    parser.add_argument("-t", "--twórz", action="store_true", dest="twórz", default=False, help="parametr na tworzenie (nadpisywanie) plików")
    parser.add_argument("-o", "--odczytaj", action="store_true", dest="odczytaj", default=False, help="parametr na odczytywanie plików")


def do_ziemi(l):
    l = list(map(lambda s: s.lower(), l))


def standaryzuj_argumenty(args):
    do_ziemi(args.miesiące)
    do_ziemi(args.dni_tygodnia)
    do_ziemi(args.pora_dnia)


def sparsuj_argumenty():
    parser = argparse.ArgumentParser(description="Zapisuj (nadpisuj) i odczytuj pliki z katalogów!")
    dodaj_argumenty(parser)
    args = parser.parse_args()
    standaryzuj_argumenty(args)
    return args


def czy_długości_ok(args):
    if len(args.miesiące) != len(args.dni_tygodnia):
        print("Miesięcy musi być wymienionych dokładnie tyle co dni tygodnia!")
        return False
    elif len(args.miesiące) < len(args.dni_tygodnia):
        print("Nie może być wymienionych dni tygodnia więcej niż poprzednich wartości!")
        return False
    else:
        return True


def czy_parametry_ok(args):
    if args.twórz and args.odczytaj:
        print("Albo tworzysz pliki, albo je odczytujesz!")
        return False
    elif not args.twórz and not args.odczytaj:
        print("Musisz albo tworzyć pliki, albo je odczytywać!")
        return False
    else:
        return True


def czy_zawartość_ok(args):
    miesiące = {"styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"}
    dni_tygodnia = {"poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"}
    pory_dnia = {"rano", "wieczór", "r", "w"}

    if not set(args.miesiące).issubset(miesiące):
        print("Zła nazwa miesiąca!")
        return False
    # To jest źle, bo mogą być przedziały, np. pn-wt i tutaj to byłby błąd:
    elif not set(args.dni_tygodnia).issubset(dni_tygodnia):
        print("Zła nazwa dnia tygodnia!")
        return False
    elif not set(args.pora_dnia).issubset(pory_dnia):
        print("Zła nazwa pory dnia!")
        return False
    else:
        return True


def czy_argumenty_są_poprawne(args):
    return czy_długości_ok(args) and czy_parametry_ok(args) and czy_zawartość_ok(args)


def main():
    args = sparsuj_argumenty()

    # Nie sprawdzasz poprawności argumentów, bo ja to robię lepiej
    # Sprawdzasz tylko, czy dobry tryb
    if czy_parametry_ok(args):
        if args.pora_dnia == 'rano':
            paths = path_creator.parse_paths(months = args.miesiące, days = args.dni_tygodnia)
        else:
            paths = path_creator.parse_paths(months = args.miesiące, days = args.dni_tygodnia, times = args.pora_dnia)

        for path in paths:
            path_exists = path_creator.create_or_check_path(path, args.odczytaj, args.twórz)
            if path_exists:
                print('Tralalala') # roboczo, bo się nie skompiluje
                # TODO
                # Tutaj trzeba stworzyć plik csv w ścieżce path, jeżeli nie istnieje (tryb zapisu)
                # Odczytać zawartość pliku i wypisać na standardowe wyjście (tryb odczytu)
                # Lub wygenerować zapis do pliku (tryb zapisu)
                # (osobny plik pythonowy, importujemy funkcję stamtąd)
            else:
                print('Próbowano odczytać nieistniejącą ścieżkę!')

        pass

main()
