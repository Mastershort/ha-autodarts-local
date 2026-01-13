"""Sensoren für Autodarts."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Sensoren initialisieren."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        # Der neue Sensor für Online/Offline
        AutodartsSensor(coordinator, "connection_status", "Verbindung", "mdi:wifi-check"),
        
        AutodartsSensor(coordinator, "status", "Status", "mdi:state-machine"),
        AutodartsSensor(coordinator, "turn_score", "Aktuelle Aufnahme", "mdi:bullseye-arrow"),
        AutodartsSensor(coordinator, "num_throws", "Anzahl Würfe", "mdi:counter"),
        AutodartsSensor(coordinator, "throw1", "Wurf 1", "mdi:numeric-1-circle-outline"),
        AutodartsSensor(coordinator, "throw2", "Wurf 2", "mdi:numeric-2-circle-outline"),
        AutodartsSensor(coordinator, "throw3", "Wurf 3", "mdi:numeric-3-circle-outline"),
    ]

    async_add_entities(sensors)

class AutodartsSensor(CoordinatorEntity, SensorEntity):
    """Ein Sensor für Autodarts."""

    def __init__(self, coordinator, key, name, icon):
        super().__init__(coordinator)
        self._key = key
        self._name = name
        self._icon = icon
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{key}"
        self._attr_has_entity_name = True
        
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.entry.entry_id)},
            "name": "Autodarts Board",
            "manufacturer": "Autodarts",
            "model": "Local API",
        }

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        # Optional: Icon ändern wenn Offline
        if self._key == "connection_status" and self.state == "Offline":
            return "mdi:wifi-off"
        return self._icon

    @property
    def state(self):
        return self.coordinator.data.get(self._key)