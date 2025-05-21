# WorstBuy – Terminalbaserat butikssystem

WorstBuy är en terminalapplikation skriven i Python där du kan söka efter produkter (via Best Buy API), lägga till dem i en kundvagn, ta bort produkter, genomföra köp och se din orderhistorik. All data sparas i JSON-filer så att din kundvagn och orderhistorik finns kvar mellan sessionerna.

## Funktioner

- **Sök produkter:** Sök efter produkter via Best Buy API direkt från terminalen.
- **Kundvagn:** Lägg till och ta bort produkter i din kundvagn.
- **Kassa:** Genomför köp och spara ordern i orderhistoriken.
- **Orderhistorik:** Se tidigare köp med datum, produkter och totalpris.
- **Spara/Ladda:** Kundvagn och orderhistorik sparas automatiskt i JSON-filer.


### Förutsättningar

- Python 3.7+
- [requests](https://pypi.org/project/requests/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [colorama](https://pypi.org/project/colorama/)

Installera beroenden:
pip install requests python-dotenv colorama
