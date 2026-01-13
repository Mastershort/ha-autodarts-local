"""Config flow für Autodarts Local Integration."""
import voluptuous as vol
import aiohttp
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONF_API_IP, CONF_API_PORT, DEFAULT_PORT

# Schema für das Formular
DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_API_IP): str,
    vol.Required(CONF_API_PORT, default=DEFAULT_PORT): int,
})

async def validate_input(hass: HomeAssistant, data: dict) -> dict:
    """Überprüfe, ob die Verbindung klappt."""
    url = f"http://{data[CONF_API_IP]}:{data[CONF_API_PORT]}/api/state"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=5) as response:
                if response.status != 200:
                    raise CannotConnect
        except Exception:
            raise CannotConnect

    return {"title": f"Autodarts ({data[CONF_API_IP]})"}

class AutodartsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Autodarts Local."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Der erste Schritt: Formular anzeigen."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

class CannotConnect(HomeAssistantError):
    """Fehler, wenn Verbindung nicht möglich."""