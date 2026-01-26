"""Aktionen für Autodarts."""
import aiohttp
import logging

from .const import CONF_API_IP, CONF_API_PORT, DOMAIN

from homeassistant.components.button import ButtonEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Knöpfe Initialisieren."""

    buttons = [
        AutodartsButton(entry, "start_detection", "mdi:play-circle", "/api/start"),
        AutodartsButton(entry, "stop_detection", "mdi:stop-circle", "/api/stop"),
        AutodartsButton(entry, "reset_detection", "mdi:restore", "/api/reset")
    ]

    async_add_entities(buttons)

class AutodartsButton(ButtonEntity):
    """
    Aktionen für Autodarts.
    """

    def __init__(self, entry, key, icon, endpoint):
        self._key = key
        self._icon = icon
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_has_entity_name = True

        self.api_endpoint = endpoint
        self.api_ip = entry.data[CONF_API_IP]
        self.api_port = entry.data[CONF_API_PORT]
        self.url = f"http://{self.api_ip}:{self.api_port}{endpoint}"
        
        # Das ist das Wichtigste: Wir sagen HA, welcher Schlüssel in der JSON genutzt werden soll
        self._attr_translation_key = key
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Autodarts Board",
            "manufacturer": "Autodarts",
            "model": "Local API",
        }

    async def async_press(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.put(self.url) as response:
                if response.status != 200:
                    _LOGGER.info(f"API Fehler: {self.url} antwortet mit {response.status}")
                
