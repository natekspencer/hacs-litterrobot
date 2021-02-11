"""Config flow for Litter-Robot integration."""
import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from pylitterbot import Account
from pylitterbot.exceptions import LitterRobotException, LitterRobotLoginException

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class LitterRobotFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Litter-Robot config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            try:
                _LOGGER.debug("Attempting to login to Litter-Robot API.")
                account = Account()
                await account.connect(
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD],
                )
                _LOGGER.debug("Successfully logged in.")
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )
            except LitterRobotLoginException:
                errors["base"] = "cannot_connect"
            except LitterRobotException:
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_USERNAME): str, vol.Required(CONF_PASSWORD): str}
            ),
            errors=errors,
        )
