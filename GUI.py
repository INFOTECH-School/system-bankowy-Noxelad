import tkinter as tk
from tkinter import messagebox, simpledialog
from main import Bank, Klient, Konto, KontoOszczednosciowe, NiewystarczajaceSrodki, NieprawidlowyNumerKonta

class BankGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("System Bankowy")
        self.root.geometry("500x500")

        self.bank = Bank("Mój Bank")

        self.label_info = tk.Label(root, text="System Bankowy", font=("Arial", 16))
        self.label_info.pack(pady=10)

        self.btn_dodaj_klienta = tk.Button(root, text="Dodaj klienta", command=self.dodaj_klienta)
        self.btn_dodaj_klienta.pack(pady=5)

        self.btn_usun_klienta = tk.Button(root, text="Usuń klienta", command=self.usun_klienta)
        self.btn_usun_klienta.pack(pady=5)

        self.btn_dodaj_konto = tk.Button(root, text="Dodaj konto", command=self.dodaj_konto)
        self.btn_dodaj_konto.pack(pady=5)

        self.btn_usun_konto = tk.Button(root, text="Usuń konto", command=self.usun_konto)
        self.btn_usun_konto.pack(pady=5)

        self.btn_przelew = tk.Button(root, text="Wykonaj przelew", command=self.wykonaj_przelew)
        self.btn_przelew.pack(pady=5)

        self.btn_saldo = tk.Button(root, text="Sprawdź saldo", command=self.sprawdz_saldo)
        self.btn_saldo.pack(pady=5)

        self.btn_lista_klientow = tk.Button(root, text="Wyświetl listę klientów", command=self.wyswietl_liste_klientow)
        self.btn_lista_klientow.pack(pady=5)

    def dodaj_klienta(self):
        imie = simpledialog.askstring("Dodaj klienta", "Podaj imię:")
        nazwisko = simpledialog.askstring("Dodaj klienta", "Podaj nazwisko:")
        pesel = simpledialog.askstring("Dodaj klienta", "Podaj PESEL:")
        if imie and nazwisko and pesel:
            klient = Klient(imie, nazwisko, pesel)
            self.bank.dodaj_klienta(klient)
            messagebox.showinfo("Sukces", "Dodano klienta!")
        else:
            messagebox.showerror("Błąd", "Wprowadź poprawne dane!")

    def usun_klienta(self):
        pesel = simpledialog.askstring("Usuń klienta", "Podaj PESEL klienta do usunięcia:")
        if pesel:
            self.bank.usun_klienta(pesel)
            messagebox.showinfo("Sukces", "Klient usunięty!")
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy PESEL!")

    def dodaj_konto(self):
        pesel = simpledialog.askstring("Dodaj konto", "Podaj PESEL klienta:")
        klient = next((k for k in self.bank.klienci if k.pesel == pesel), None)
        if klient:
            numer_konta = simpledialog.askstring("Dodaj konto", "Podaj numer konta:")
            saldo = float(simpledialog.askstring("Dodaj konto", "Podaj saldo początkowe:"))
            konto = Konto(numer_konta, klient, saldo)
            klient.dodaj_konto(konto)
            self.bank.konta.append(konto)
            messagebox.showinfo("Sukces", "Dodano konto!")
        else:
            messagebox.showerror("Błąd", "Nie znaleziono klienta!")

    def usun_konto(self):
        numer_konta = simpledialog.askstring("Usuń konto", "Podaj numer konta do usunięcia:")
        self.bank.konta = [k for k in self.bank.konta if k.numer_konta != numer_konta]
        messagebox.showinfo("Sukces", "Konto usunięte!")

    def wykonaj_przelew(self):
        od_konto = simpledialog.askstring("Przelew", "Podaj numer konta źródłowego:")
        do_konto = simpledialog.askstring("Przelew", "Podaj numer konta docelowego:")
        kwota = float(simpledialog.askstring("Przelew", "Podaj kwotę:"))
        try:
            self.bank.wykonaj_przelew(od_konto, do_konto, kwota)
            messagebox.showinfo("Sukces", "Przelew wykonany!")
        except (NiewystarczajaceSrodki, NieprawidlowyNumerKonta) as e:
            messagebox.showerror("Błąd", str(e))

    def sprawdz_saldo(self):
        numer_konta = simpledialog.askstring("Sprawdź saldo", "Podaj numer konta:")
        try:
            konto = self.bank.znajdz_konto(numer_konta)
            messagebox.showinfo("Saldo", f"Saldo: {konto.sprawdz_saldo()} PLN")
        except NieprawidlowyNumerKonta as e:
            messagebox.showerror("Błąd", str(e))

    def wyswietl_liste_klientow(self):
        if not self.bank.klienci:
            messagebox.showinfo("Lista klientów", "Brak klientów w systemie.")
        else:
            lista_klientow = "\n".join([f"{k.imie} {k.nazwisko} (PESEL: {k.pesel})" for k in self.bank.klienci])
            messagebox.showinfo("Lista klientów", lista_klientow)

if __name__ == "__main__":
    root = tk.Tk()
    app = BankGUI(root)
    root.mainloop()