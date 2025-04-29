# Convertor de Expresii Regulate în DFA

## Structura Proiectului

- `regex_to_postfix.py`: Convertește expresii regulate în notație postfixată folosind algoritmul Shunting-Yard
- `postfix_to_nfa.py`: Construiește un NFA din expresii postfixate folosind algoritmul Thompson
- `nfa_to_dfa.py`: Convertește NFA în DFA folosind metoda de subset construction
- `dfa_simulator.py`: Simulează un DFA pentru a verifica dacă un string este acceptat
- `test_runner.py`: Rulează cazuri de test dintr-un fișier JSON
- `main.py`: Punctul principal de intrare cu interfață pentru utilizator
- `tests.json`: Conține cazuri de test pentru validarea implementării

## Cum se rulează programul

Proiectul poate fi rulat în două moduri:

### Modul 1: Conversie de la Regex la DFA

```bash
python3 main.py
```

Introduceți `1` ca mod. Apoi:
1. Introduceți o expresie regulată
2. Programul o va converti în notație postfixată, va construi un NFA, va vizualiza NFA-ul, va converti în DFA și va vizualiza DFA-ul
3. Introduceți un string pentru a fi testat
4. Programul spune dacă stringul este acceptat sau respins

### Modul 2: Testare

```bash
python3 main.py
```

Introduceți `2` ca mod, apoi introduceți fișierul de teste: `tests.json`

Aceasta va rula toate cazurile din fișierul JSON și va afișa rezultatele.

## Detalii de Implementare

### Conversie de la Regex la Postfix
- Operatori suportați: `*` (zero or more), `+` (one or more), `?` (optional), `.` (concatenation), `|` (alternation)
- Operatorii de concatenare sunt introduși automat acolo unde este necesar
- Precedența operatorilor: `*`,`+`,`?` > `.` > `|`

### Thompson (Postfix la NFA)
- NFA este reprezentat ca fragmente cu stări de început și acceptare
- Fiecare fragment este construit urmând regulile lui Thompson pentru operațiile de bază
- Folosește tranziții epsilon (ε) pentru a conecta fragmentele între ele

### Construcția prin mulțimi (NFA la DFA)
- Folosește operațiile de epsilon-închidere și mutare pentru a determina tranzițiile între stări
- Mapează seturi de stări NFA la stări DFA
- Identifică automat stările de acceptare bazate pe starea de acceptare a NFA-ului

### Vizualizare
- Atât NFA cât și DFA pot fi vizualizate folosind NetworkX, Matplotlib și Graphviz
- Stările de început sunt afișate în verde, stările de acceptare în roșu, iar celelalte stări în albastru deschis

## Dependențe

Proiectul necesită:
- Python 3.x
- NetworkX (pentru vizualizare)
- Matplotlib (pentru vizualizare)
- Graphviz (pentru vizualizare)
