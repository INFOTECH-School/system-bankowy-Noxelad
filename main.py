import datetime

class NiewystarczajaceSrodki(Exception):
    pass

class NieprawidlowyNumerKonta(Exception):
    pass

class Konto:
    def __init__(self, numer_konta, wlasciciel, saldo=0):
        self.numer_konta = numer_konta
        self.wlasciciel = wlasciciel
        self.saldo = saldo

    def wplata(self, kwota):
        if kwota > 0:
            self.saldo += kwota
        else:
            raise ValueError("Kwota musi być większa niż 0.")

    def wyplata(self, kwota):
        if kwota > self.saldo:
            raise NiewystarczajaceSrodki("Brak wystarczających środków na koncie.")
        self.saldo -= kwota

    def sprawdz_saldo(self):
        return self.saldo

class KontoOszczednosciowe(Konto):
    def __init__(self, numer_konta, wlasciciel, saldo=0, oprocentowanie=0.02):
        super().__init__(numer_konta, wlasciciel, saldo)
        self.oprocentowanie = oprocentowanie

    def nalicz_odsetki(self):
        odsetki = self.saldo * self.oprocentowanie
        self.saldo += odsetki
        return odsetki

class Klient:
    def __init__(self, imie, nazwisko, pesel):
        self.imie = imie
        self.nazwisko = nazwisko
        self.pesel = pesel
        self.konta = []

    def dodaj_konto(self, konto):
        self.konta.append(konto)

    def usun_konto(self, numer_konta):
        self.konta = [k for k in self.konta if k.numer_konta != numer_konta]

    def wyswietl_konta(self):
        return [k.numer_konta for k in self.konta]

class Transakcja:
    def __init__(self, data, kwota, typ_transakcji, konto_zrodlowe, konto_docelowe=None):
        self.data = data
        self.kwota = kwota
        self.typ_transakcji = typ_transakcji
        self.konto_zrodlowe = konto_zrodlowe
        self.konto_docelowe = konto_docelowe

class Bank:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.klienci = []
        self.konta = []
        self.transakcje = []

    def dodaj_klienta(self, klient):
        self.klienci.append(klient)

    def usun_klienta(self, pesel):
        self.klienci = [k for k in self.klienci if k.pesel != pesel]

    def znajdz_konto(self, numer_konta):
        for konto in self.konta:
            if konto.numer_konta == numer_konta:
                return konto
        raise NieprawidlowyNumerKonta("Nie znaleziono konta o podanym numerze.")

    def wykonaj_przelew(self, od_kogo, do_kogo, kwota):
        konto_od = self.znajdz_konto(od_kogo)
        konto_do = self.znajdz_konto(do_kogo)
        konto_od.wyplata(kwota)
        konto_do.wplata(kwota)
        transakcja = Transakcja(datetime.datetime.now(), kwota, "Przelew", od_kogo, do_kogo)
        self.transakcje.append(transakcja)

    def wyswietl_transakcje(self):
        for t in self.transakcje:
            print(f"{t.data} - {t.typ_transakcji} - {t.kwota} PLN (z {t.konto_zrodlowe} do {t.konto_docelowe})")

