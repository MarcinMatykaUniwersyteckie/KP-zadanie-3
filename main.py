import argparse
#import nie_mój_plik

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
    if czy_argumenty_są_poprawne(args):
        #nie_moja_funkcja(agrs);
        pass






