"""The Litter-Robot integration."""
import asyncio
import datetime
import logging
from datetime import timedelta
from typing import Any, Dict, Optional

import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util
import voluptuous as vol
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from pylitterbot import Account
from pylitterbot.exceptions import LitterRobotException, LitterRobotLoginException

from .const import DOMAIN, REFRESH_WAIT_TIME

PLATFORMS = ["sensor", "switch", "vacuum"]
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Setup the Litter-Robot component."""
    hass.data[DOMAIN] = {}

    if DOMAIN not in config:
        return True

    for entry in config[DOMAIN]:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": SOURCE_IMPORT}, data=entry
            )
        )


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up config entry."""
    hub = LitterRobotHub(hass, entry.data)

    await hub.login()
    if not hub.logged_in:
        _LOGGER.debug("Failed to login to Litter-Robot API")
        return False

    hass.data[DOMAIN][entry.entry_id] = hub

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class LitterRobotHub:
    """A Litter-Robot hub wrapper class."""

    def __init__(self, hass, domain_config):
        """Initialize the Litter-Robot hub."""
        self.config = domain_config
        self._hass = hass
        self.account = None
        self.logged_in = False

        async def async_update_data():
            """Update all device states from the Litter-Robot API."""
            await self.account.refresh_robots()
            return True

        self.coordinator = DataUpdateCoordinator(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_method=async_update_data,
            update_interval=timedelta(minutes=1),
        )

    async def login(self):
        """Login to Litter-Robot."""
        _LOGGER.debug("Trying to connect to Litter-Robot API")
        try:
            self.account = Account()
            await self.account.connect(
                username=self.config[CONF_USERNAME],
                password=self.config[CONF_PASSWORD],
                load_robots=True,
            )
        except LitterRobotException as ex:
            if isinstance(ex, LitterRobotLoginException):
                _LOGGER.error("Invalid credentials")
            else:
                _LOGGER.error("Unable to connect to Litter-Robot API")
                raise ConfigEntryNotReady from ex
            self.logged_in = False
            return

        self.logged_in = True
        _LOGGER.debug("Successfully connected to Litter-Robot API")


class LitterRobotEntity(CoordinatorEntity):
    """Generic Litter-Robot entity representing common data and methods"""

    def __init__(self, robot, type, hub: LitterRobotHub):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(hub.coordinator)
        self.robot = robot
        self.type = type if type else ""
        self.hub = hub

    @property
    def name(self):
        """Return the name of this entity."""
        return f"{self.robot.name} {self.type}"

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self.robot.serial}-{self.type}"

    @property
    def available(self):
        """Return availability."""
        return self.hub.logged_in

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return the device information for a Litter-Robot."""
        return {
            "identifiers": {(DOMAIN, self.robot.serial)},
            "name": self.robot.name,
            "manufacturer": "Litter-Robot",
            "model": "Litter-Robot 3 Connect"
            if self.robot.serial.startswith("LR3C")
            else "unknown",
        }

    async def perform_action_and_refresh(self, action, *args):
        """Performs an action and initiates a refresh of the robot data after a few seconds."""
        await action(*args)
        await asyncio.sleep(REFRESH_WAIT_TIME)
        await self.hub.coordinator.async_refresh()

    @staticmethod
    def parse_time_at_default_timezone(time_str: str) -> Optional[datetime.time]:
        time = dt_util.parse_time(time_str)
        return (
            None
            if time is None
            else datetime.time(
                hour=time.hour,
                minute=time.minute,
                second=time.second,
                tzinfo=dt_util.DEFAULT_TIME_ZONE,
            )
        )
