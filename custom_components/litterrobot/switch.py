"""Support for Litter-Robot Connected Vacuums switches."""
from datetime import timedelta

from homeassistant.helpers.entity import ToggleEntity
from pylitterbot import Robot

from . import LitterRobotEntity
from .const import _LOGGER, LITTERROBOT_DOMAIN

NIGHT_LIGHT = "Night Light"
PANEL_LOCKOUT = "Panel Lockout"


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Litter-Robot switches using config entry."""
    entities = []
    hub = hass.data[LITTERROBOT_DOMAIN][config_entry.entry_id]

    for robot in hub.account.robots:
        entities.append(LitterRobotSwitch(robot, NIGHT_LIGHT, hub))
        entities.append(LitterRobotSwitch(robot, PANEL_LOCKOUT, hub))

    if not entities:
        return

    _LOGGER.debug(f"Adding robot switches {entities}")
    async_add_entities(entities, True)


class LitterRobotSwitch(LitterRobotEntity, ToggleEntity):
    """Litter-Robot Connect Switches."""

    @property
    def is_on(self):
        """Return true if switch is on."""
        if self.type == NIGHT_LIGHT:
            return self.robot.night_light_active
        elif self.type == PANEL_LOCKOUT:
            return self.robot.panel_lock_active

    @property
    def icon(self):
        if self.type == NIGHT_LIGHT:
            return "mdi:lightbulb-on" if self.is_on else "mdi:lightbulb-off"
        elif self.type == PANEL_LOCKOUT:
            return "mdi:lock" if self.is_on else "mdi:lock-open"

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        if self.type == NIGHT_LIGHT:
            await self.perform_action_and_refresh(self.robot.set_night_light, True)
        elif self.type == PANEL_LOCKOUT:
            await self.perform_action_and_refresh(self.robot.set_panel_lockout, True)

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        if self.type == NIGHT_LIGHT:
            await self.perform_action_and_refresh(self.robot.set_night_light, False)
        elif self.type == PANEL_LOCKOUT:
            await self.perform_action_and_refresh(self.robot.set_panel_lockout, False)
