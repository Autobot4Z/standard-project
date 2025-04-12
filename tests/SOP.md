# 🧪 SOP: Tests schreiben & nutzen (für Einsteiger)

## Warum überhaupt testen?

- Du findest Fehler sofort – **nicht erst beim Kunden**.
- Du kannst deinen Code ändern, ohne Angst zu haben, dass du etwas kaputt machst.
- Du verstehst besser, was dein Code überhaupt tun soll.

---

## Was ist ein Test?

Ein Test ist eine kleine Python-Funktion, die prüft, ob dein Code das macht, was du erwartest.

Beispiel:

```python
# Datei: tests/test_math.py
from core.logic_a import addiere

def test_addiere():
    assert addiere(2, 3) == 5
```

---

## Wie funktioniert das?

1. Du schreibst Tests in Dateien im Ordner `tests/`.
2. Du führst sie mit dem Tool `pytest` aus.
3. Pytest sagt dir, ob etwas kaputt ist.

---

## Vorbereitung (nur beim ersten Mal)

1. Öffne dein Terminal
2. Installiere `pytest`:

```bash
pip install pytest
pip install pytest-cov
pip install pytest-mock
```

---

## Test ausführen

Im Terminal:

```bash
PYTHONPATH=. pytest
```

```bash
PYTHONPATH=. pytest --cov=core --cov=services --cov-report=term-missing
```

Dann siehst du z. B.:

```
tests/test_math.py ..F
```

✅ `.` = Test bestanden  
❌ `F` = Test fehlgeschlagen

---

## Wie schreibe ich einen guten Test?

- Der Testname sollte mit `test_` anfangen
- Nutze `assert`, um zu prüfen, ob etwas stimmt
- Teste **eine Sache pro Testfunktion**

---

## Beispiel

Angenommen, du hast diese Funktion:

```python
# Datei: core/logic_a.py
def verdopple(x):
    return x * 2
```

Dann schreibst du den Test so:

```python
# Datei: tests/test_logic_a.py
from core.logic_a import verdopple

def test_verdopple():
    assert verdopple(4) == 8
```

---

## Fehler finden mit Tests

Wenn der Test fehlschlägt, bekommst du eine Meldung wie:

```
>       assert verdopple(4) == 9
E       AssertionError: assert 8 == 9
```

→ Du hast z. B. erwartet, dass 4 verdoppelt 9 ergibt – stimmt nicht.

---

## Bonus: Tests automatisch beim Commit prüfen

Installiere `pre-commit` und lass Tests automatisch vor jedem Git-Commit laufen. So hast du immer sauberen Code. (Siehe `.pre-commit-config.yaml` in deinem Projekt.)
