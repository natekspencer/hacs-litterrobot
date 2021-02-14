"""A wrapper 'hub' for the Litter-Robot API and base entity for common attributes."""
import asyncio
import logging
from datetime import time, timedelta
from types import MethodType
from typing import Any, Optional

import homeassistant.util.dt as dt_util
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from pylitterbot import Account, Robot
from pylitterbot.exceptions import LitterRobotException, LitterRobotLoginException

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

REFRESH_WAIT_TIME = 12
UPDATE_INTERVAL = 10


class LitterRobotHub:
    """A Litter-Robot hub wrapper class."""

    def __init__(self, hass: HomeAssistant, data: dict):
        """Initialize the Litter-Robot hub."""
        self._data = data
        self.account = None
        self.logged_in = False

        async def _async_update_data():
            """Update all device states from the Litter-Robot API."""
            await self.account.refresh_robots()
            return True

        self.coordinator = DataUpdateCoordinator(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_method=_async_update_data,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def login(self, load_robots: bool = False):
        """Login to Litter-Robot."""
        self.logged_in = False
        try:
            self.account = Account()
            await self.account.connect(
                username=self._data[CONF_USERNAME],
                password=self._data[CONF_PASSWORD],
                load_robots=load_robots,
            )
            self.logged_in = True
            return self.logged_in
        except LitterRobotLoginException as ex:
            _LOGGER.error("Invalid credentials")
            raise ex
        except LitterRobotException as ex:
            _LOGGER.error("Unable to connect to Litter-Robot API")
            raise ex


class LitterRobotEntity(CoordinatorEntity):
    """Generic Litter-Robot entity representing common data and methods."""

    def __init__(self, robot: Robot, entity_type: str, hub: LitterRobotHub):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(hub.coordinator)
        self.robot = robot
        self.entity_type = entity_type if entity_type else ""
        self.hub = hub

    @property
    def name(self):
        """Return the name of this entity."""
        return f"{self.robot.name} {self.entity_type}"

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self.robot.serial}-{self.entity_type}"

    @property
    def available(self):
        """Return availability."""
        return self.hub.logged_in

    @property
    def device_info(self):
        """Return the device information for a Litter-Robot."""
        return {
            "identifiers": {(DOMAIN, self.robot.serial)},
            "name": self.robot.name,
            "manufacturer": "Litter-Robot",
            "model": "Litter-Robot 3 Connect"
            if self.robot.serial.startswith("LR3C")
            else "Other Litter-Robot Connected Device",
        }

    async def perform_action_and_refresh(self, action: MethodType, *args: Any):
        """Perform an action and initiates a refresh of the robot data after a few seconds."""
        await action(*args)
        await asyncio.sleep(REFRESH_WAIT_TIME)
        await self.hub.coordinator.async_refresh()

    @staticmethod
    def parse_time_at_default_timezone(time_str: str) -> Optional[time]:
        """Parse a time string and add default timezone."""
        parsed_time = dt_util.parse_time(time_str)
        return (
            None
            if parsed_time is None
            else time(
                hour=parsed_time.hour,
                minute=parsed_time.minute,
                second=parsed_time.second,
                tzinfo=dt_util.DEFAULT_TIME_ZONE,
            )
        )
