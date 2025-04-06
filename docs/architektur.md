# Architektur

Projektstruktur und Abläufe.

my_project/
│
├── .env               # Sensible Daten (nicht in Git)
├── config.py          # Zentrale Konfig (zieht .env rein)
├── requirements.txt   # Abhängigkeiten
├── main.py            # Einstiegspunkt
│
├── /core/             # Business-Logik
│   ├── logic_a.py     
│   ├── logic_b.py     
│
├── /services/         # Externe APIs, Datenquellen
│   ├── billbee_api.py
│   ├── email_client.py
│
├── /utils/            # Hilfsfunktionen, Logging, Timer
│   ├── logger.py
│   ├── retry.py
│
├── /tests/            # Unittests / Integrationstests
│   ├── test_logic_a.py
│
├── /docs/             # Projektbeschreibung, SOPs
│   └── architektur.md
│
├── README.md
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
└── .gitignore