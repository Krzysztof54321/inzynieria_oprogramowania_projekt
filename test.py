# test_month.py

class Budget:
    def __init__(self, category, amount, month, year):
        self.category = category
        self.amount = amount
        self.month = month
        self.year = year

    @property
    def month_name(self):
        months = {
            1: "Styczeń",
            2: "Luty",
            3: "Marzec",
            4: "Kwiecień",
            5: "Maj",
            6: "Czerwiec",
            7: "Lipiec",
            8: "Sierpień",
            9: "Wrzesień",
            10: "Październik",
            11: "Listopad",
            12: "Grudzień"
        }
        return months.get(self.month)

    def __repr__(self):
        return f'<Budget {self.category}>'


if __name__ == "__main__":
    print("=== month = 5, różne sposoby wywołania ===")

    b = Budget("Jedzenie", 500.00, 5, 2026)

    # 1. Przez właściwość (tak jak w Jinja: {{ b.month_name }})
    print("b.month         =", b.month)
    print("b.month_name    =", b.month_name)

    # 2. Przez property.getter — pokazuje, że to getter
    print("getter(b)       =", Budget.month_name.fget(b))

    # 3. Próba wywołania jak metody — błąd, bo to nie funkcja
    print("\n=== próba b.month_name() — powinno wywalić TypeError ===")
    try:
        b.month_name()
    except TypeError as e:
        print("TypeError:", e)

    # 4. repr
    print("\nrepr(b)         =", repr(b))

    # 5. Zmiana month i ponowne odczytanie
    print("\n=== zmiana month ===")
    for m in [1, 5, 8, 12]:
        b.month = m
        print(f"month={m:2} -> month_name={b.month_name}")

    # 6. Wartości brzegowe / dziwne
    print("\n=== wartości dziwne ===")
    for m in [0, 13, None]:
        b.month = m
        print(f"month={m!r:6} -> month_name={b.month_name!r}")