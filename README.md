# Autodarts Local Integration 🎯

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![maintainer](https://img.shields.io/badge/maintainer-Mastershort-green?style=for-the-badge)](https://github.com/Mastershort)

**[🇬🇧 English](#-english) | [🇩🇪 Deutsch](#-deutsch)**

---

## 🇬🇧 English

A local Home Assistant integration for [Autodarts.io](https://autodarts.io).
This integration reads the raw status directly from your Autodarts Board Manager (Port 3180) via the local network.

**✨ Why use this?**
* **Instant Feedback:** Perfect for controlling room lights based on hits (Throwing/Takeout).
* **Privacy:** Runs locally. No cloud data required for the sensors to work.
* **Silent Mode:** When your darts PC is off, the integration goes into "Offline" mode without spamming your Home Assistant logs with errors.

### Features
* 🔌 **Connection Monitor:** Shows if your Board is Online or Offline.
* 🚦 **Status:** Detects game state (Throwing, Takeout, Game Won).
* 🎯 **Turn Score:** Shows the total score of the current 3 darts.
* 1️⃣ **Individual Darts:** Sensors for every single throw (e.g., "T20", "S5").
* ⚡ **Performance:** Zero cloud latency.

### Installation

**Option 1: The Easy Way (My Home Assistant)**
Click the button below to add this repository to HACS directly:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Mastershort&repository=ha-autodarts-local&category=integration)

**Option 2: Manual HACS Installation**
1. Open HACS in Home Assistant.
2. Go to "Integrations" > Top right menu (3 dots) > "Custom repositories".
3. URL: `https://github.com/Mastershort/ha-autodarts-local`
4. Category: **Integration**
5. Click "Add" and then install "Autodarts Local".
6. Restart Home Assistant.

### Configuration
1. Go to **Settings** > **Devices & Services**.
2. Click **Add Integration** and search for **Autodarts Local**.
3. Enter the **IP Address** of your Autodarts PC (Port is 3180 by default).

---

## 🇩🇪 Deutsch

Eine lokale Home Assistant Integration für [Autodarts.io](https://autodarts.io).
Diese Integration liest den Status direkt vom Autodarts Board Manager (Port 3180) über das lokale Netzwerk aus.

**✨ Warum diese Integration?**
* **Sofortige Reaktion:** Perfekt um Lichteffekte im Raum zu steuern (z.B. Licht an beim Pfeile ziehen).
* **Lokal:** Läuft komplett lokal. Keine Cloud-Verbindung nötig.
* **Silent Mode:** Wenn der Darts-PC aus ist, geht die Integration in den "Offline"-Modus, ohne das Home Assistant Log mit Fehlern vollzuschreiben.

### Funktionen
* 🔌 **Verbindungs-Monitor:** Zeigt an, ob das Board Online oder Offline ist.
* 🚦 **Status:** Erkennt den Spielstatus (Werfen, Pfeile ziehen / Takeout).
* 🎯 **Aufnahme-Punkte:** Zeigt die Punkte der aktuellen 3 Pfeile.
* 1️⃣ **Einzelwürfe:** Sensoren für jeden einzelnen Pfeil (z.B. "T20", "S5").
* ⚡ **Performance:** Keine Cloud-Verzögerung.

### Installation

**Option 1: Der einfache Weg**
Klicke auf den Button, um das Repository direkt zu HACS hinzuzufügen:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Mastershort&repository=ha-autodarts-local&category=integration)

**Option 2: Manuelle HACS Installation**
1. Öffne HACS in Home Assistant.
2. Gehe zu "Integrationen" > Menü oben rechts (3 Punkte) > "Benutzerdefinierte Repositories".
3. URL: `https://github.com/Mastershort/ha-autodarts-local`
4. Kategorie: **Integration**
5. Klicke auf "Hinzufügen" und installiere "Autodarts Local".
6. Starte Home Assistant neu.

### Konfiguration
1. Gehe zu **Einstellungen** > **Geräte & Dienste**.
2. Klicke auf **Integration hinzufügen** und suche nach **Autodarts Local**.
3. Gib die **IP-Adresse** deines Autodarts-PCs ein.

---

### 💡 Example Automation / Beispiel Automatisierung

**Turn on bright lights when retrieving darts / Helles Licht beim Pfeile ziehen:**

```yaml
alias: "Darts: Takeout Light"
description: "Makes room bright when player retrieves darts"
trigger:
  - platform: state
    entity_id: sensor.autodarts_board_status
    to: "Takeout"
    id: "takeout"
  - platform: state
    entity_id: sensor.autodarts_board_status
    from: "Takeout"
    id: "throwing"
action:
  - choose:
      - conditions:
          - condition: trigger
            id: "takeout"
        sequence:
          - service: light.turn_on
            target:
              entity_id: light.dart_room_main
            data:
              brightness_pct: 100
      - conditions:
          - condition: trigger
            id: "throwing"
        sequence:
          - service: light.turn_on
            target:
              entity_id: light.dart_room_main
            data:
              brightness_pct: 30
              color_name: "blue"