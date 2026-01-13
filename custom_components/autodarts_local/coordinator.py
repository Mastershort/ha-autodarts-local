"""DataUpdateCoordinator für Autodarts."""
from datetime import timedelta
import logging
import async_timeout
import aiohttp
import asyncio  # Wichtig für Timeouts

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.core import HomeAssistant
from .const import DOMAIN, CONF_API_IP, CONF_API_PORT

_LOGGER = logging.getLogger(__name__)

# Intervalle
INTERVAL_ONLINE = timedelta(seconds=1)
INTERVAL_OFFLINE = timedelta(seconds=30)

class AutodartsCoordinator(DataUpdateCoordinator):
    """Klasse zum Verwalten der Autodarts Daten."""

    def __init__(self, hass: HomeAssistant, entry):
        """Initialisierung."""
        self.entry = entry
        self.api_ip = entry.data[CONF_API_IP]
        self.api_port = entry.data[CONF_API_PORT]
        self.url = f"http://{self.api_ip}:{self.api_port}/api/state"
        self.is_connected = False

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=INTERVAL_ONLINE,
        )

    async def _async_update_data(self):
        """Daten von der API holen."""
        try:
            # Kurzer Timeout (2 Sek), damit HA nicht hängt
            async with async_timeout.timeout(2):
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.url) as response:
                        if response.status != 200:
                            raise UpdateFailed(f"API Fehler: {response.status}")
                        
                        data = await response.json()
                        
                        # Board ist wieder da!
                        if not self.is_connected:
                            _LOGGER.info("Autodarts Board verbunden.")
                            self.is_connected = True
                            self.update_interval = INTERVAL_ONLINE
                        
                        return self._process_data(data)

        except (aiohttp.ClientError, asyncio.TimeoutError):
            # Verbindung weg oder Timeout
            if self.is_connected:
                _LOGGER.info("Verbindung verloren. Gehe in Standby.")
                self.is_connected = False
                self.update_interval = INTERVAL_OFFLINE
            
            return self._get_offline_data()

        except Exception as err:
            raise UpdateFailed(f"Kritischer Fehler: {err}")

    def _process_data(self, data):
        """Verarbeitet die echten Daten (Online)."""
        throws = data.get("throws", [])
        
        current_turn_score = sum(
            t["segment"]["number"] * t["segment"]["multiplier"] 
            for t in throws
        )

        return {
            "connection_status": "Online",  # Neuer Wert für den Sensor
            "status": data.get("status", "Unknown"),
            "event": data.get("event", "None"),
            "num_throws": data.get("numThrows", 0),
            "turn_score": current_turn_score,
            "throw1": self._format_throw(throws, 0),
            "throw2": self._format_throw(throws, 1),
            "throw3": self._format_throw(throws, 2),
        }

    def _get_offline_data(self):
        """Daten, wenn Board offline ist."""
        return {
            "connection_status": "Offline", # Neuer Wert
            "status": "Offline",            # Status zeigt auch Offline
            "event": "-",
            "num_throws": 0,
            "turn_score": 0,                # Punkte auf 0
            "throw1": "-",                  # Würfe auf Strich
            "throw2": "-",
            "throw3": "-",
        }

    def _format_throw(self, throws, index):
        if index < len(throws):
            return throws[index]["segment"]["name"]
        return "-"