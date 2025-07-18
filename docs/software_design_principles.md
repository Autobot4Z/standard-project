# Software-Design-Prinzipien: Ein Leitfaden für Senior-Entwickler

Dieses Dokument beschreibt fundamentale Prinzipien für das Design von robuster, skalierbarer und wartbarer Software. Es dient als Leitfaden, um Code zu schreiben, der nicht nur heute funktioniert, sondern auch in Zukunft leicht verständlich, anpassbar und erweiterbar ist.

---

## 1. Separation of Concerns (Trennung der Verantwortlichkeiten)

Das vielleicht wichtigste Prinzip. Eine Anwendung sollte in verschiedene Sektionen unterteilt werden, von denen jede eine klar definierte und abgegrenzte Verantwortung hat.

-   **Was es bedeutet:** Die Logik für die Benutzeroberfläche (UI), die Geschäftslogik (Business Logic) und der Datenzugriff (Data Access) sollten voneinander getrennt sein. Ein Modul, das mit der HubSpot-API kommuniziert, sollte nichts über die Benutzeroberfläche oder die spezifischen Regeln der Terminfindungslogik wissen.
-   **Warum es wichtig ist:**
    -   **Wartbarkeit:** Änderungen in einem Bereich (z.B. ein neues Feld in der Datenbank) wirken sich nicht auf die anderen Bereiche aus.
    -   **Wiederverwendbarkeit:** Ein `EmailService` kann von verschiedenen Teilen der Anwendung genutzt werden, weil er nur für das Senden von E-Mails zuständig ist.
    -   **Testbarkeit:** Jede Komponente kann isoliert getestet werden.

## 2. KISS (Keep It Simple, Stupid)

Komplexität ist der Feind von guter Software. Die einfachste Lösung, die die Anforderungen erfüllt, ist fast immer die beste.

-   **Was es bedeutet:** Widerstehe dem Drang, übermäßig komplizierte oder "clevere" Lösungen zu bauen. Vermeide unnötige Abstraktionen, komplexe Vererbungshierarchien oder Design Patterns, wo eine einfache Funktion ausreichen würde.
-   **Warum es wichtig ist:**
    -   **Lesbarkeit:** Einfacher Code ist leichter zu verstehen, sowohl für dich in sechs Monaten als auch für neue Teammitglieder.
    -   **Fehlerreduktion:** Weniger Komplexität bedeutet weniger potenzielle Fehlerquellen.

## 3. DRY (Don't Repeat Yourself)

Wiederhole dich nicht. Jede Information oder Logik in einem System sollte eine einzige, unmissverständliche und autoritative Repräsentation haben.

-   **Was es bedeutet:** Wenn du denselben Codeblock an mehreren Stellen kopierst und einfügst, abstrahiere ihn in eine Funktion oder Klasse.
-   **Warum es wichtig ist:**
    -   **Effizienz:** Eine Änderung an der Logik muss nur an einer einzigen Stelle vorgenommen werden.
    -   **Konsistenz:** Stellt sicher, dass sich alle Teile der Anwendung gleich verhalten.

## 4. YAGNI (You Ain't Gonna Need It)

Implementiere keine Funktionalität, von der du nur *vermutest*, dass sie in Zukunft benötigt wird.

-   **Was es bedeutet:** Konzentriere dich darauf, die aktuellen Anforderungen so gut wie möglich zu erfüllen. Füge keine Features "auf Vorrat" hinzu.
-   **Warum es wichtig ist:**
    -   **Fokus:** Spart Entwicklungszeit und hält die Codebasis schlank.
    -   **Flexibilität:** Oft ändern sich die Anforderungen, und die "auf Vorrat" gebaute Funktionalität wäre entweder falsch oder müsste stark angepasst werden.

## 5. SOLID-Prinzipien

SOLID ist ein Akronym für fünf Design-Prinzipien, die zusammen eine solide Grundlage für objektorientiertes Design bilden.

-   **S - Single Responsibility Principle (SRP):** Eine Klasse oder ein Modul sollte nur einen einzigen Grund haben, sich zu ändern. Dies ist eine spezifischere Anwendung des "Separation of Concerns"-Prinzips. *Beispiel: Eine Klasse, die einen Kalender-Event erstellt, sollte nicht gleichzeitig für den Versand von E-Mails verantwortlich sein.*

-   **O - Open/Closed Principle (OCP):** Software-Entitäten (Klassen, Module, Funktionen) sollten offen für Erweiterungen, aber geschlossen für Modifikationen sein. *Beispiel: Statt eine bestehende Funktion zu ändern, um einen neuen Fall zu behandeln, sollte sie so gestaltet sein, dass man ein neues Modul für diesen Fall hinzufügen kann, ohne den alten Code anzufassen (z.B. über Plugins oder Strategie-Patterns).*

-   **L - Liskov Substitution Principle (LSP):** Objekte einer abgeleiteten Klasse müssen in der Lage sein, Objekte der Basisklasse zu ersetzen, ohne das Programm zu beeinträchtigen. *Beispiel: Wenn du eine `Vogel`-Klasse hast und eine `Pinguin`-Klasse davon erbst, darf die `fliegen()`-Methode nicht einfach eine Exception werfen, weil ein Pinguin nicht fliegen kann. Das würde das Verhalten der Basisklasse verletzen.*

-   **I - Interface Segregation Principle (ISP):** Kein Client sollte gezwungen sein, von Interfaces abhängig zu sein, die er nicht verwendet. *Beispiel: Besser mehrere kleine, spezifische Interfaces (`KannFliegen`, `KannSchwimmen`) als ein großes, generisches (`Tier-Aktionen`).*

-   **D - Dependency Inversion Principle (DIP):** High-Level-Module sollten nicht von Low-Level-Modulen abhängen. Beide sollten von Abstraktionen abhängen. Abstraktionen sollten nicht von Details abhängen. Details sollten von Abstraktionen abhängen. *Beispiel: Deine `AppointmentFinder`-Logik (High-Level) sollte nicht direkt von `GoogleCalendarService` (Low-Level) abhängen, sondern von einem abstrakten `CalendarService`-Interface. Dadurch könntest du Google Kalender später durch einen anderen Dienst ersetzen, ohne die Kernlogik zu ändern.*

---

### Fazit

Gutes Softwaredesign ist kein Selbstzweck. Es ist eine Investition, die sich durch geringere Wartungskosten, höhere Entwicklerzufriedenheit und eine längere Lebensdauer der Anwendung auszahlt. Es geht darum, Code zu schreiben, auf den man stolz sein kann – nicht nur, weil er funktioniert, sondern weil er elegant, verständlich und langlebig ist. 