"""Sensoren für Autodarts."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Sensoren initialisieren."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Hier übergeben wir KEINEN Namen mehr, nur noch den Key (z.B. "status")
    sensors = [
        AutodartsSensor(coordinator, "connection_status", "mdi:wifi-check"),
        AutodartsSensor(coordinator, "status", "mdi:state-machine"),
        AutodartsSensor(coordinator, "turn_score", "mdi:bullseye-arrow"),
        AutodartsSensor(coordinator, "num_throws", "mdi:counter"),
        AutodartsSensor(coordinator, "throw1", "mdi:numeric-1-circle-outline"),
        AutodartsSensor(coordinator, "throw2", "mdi:numeric-2-circle-outline"),
        AutodartsSensor(coordinator, "throw3", "mdi:numeric-3-circle-outline"),
    ]

    async_add_entities(sensors)

class AutodartsSensor(CoordinatorEntity, SensorEntity):
    """Ein Sensor für Autodarts."""

    def __init__(self, coordinator, key, icon):
        super().__init__(coordinator)
        self._key = key
        self._icon = icon
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{key}"
        self._attr_has_entity_name = True
        
        # Das ist das Wichtigste: Wir sagen HA, welcher Schlüssel in der JSON genutzt werden soll
        self._attr_translation_key = key
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.entry.entry_id)},
            "name": "Autodarts Board",
            "manufacturer": "Autodarts",
            "model": "Local API",
        }

    @property
    def icon(self):
        # Icon ändern wenn Offline (nur für Verbindungs-Sensor)
        if self._key == "connection_status" and self.state == "Offline":
            return "mdi:wifi-off"
        return self._icon

    @property
    def state(self):
        return self.coordinator.data.get(self._key)