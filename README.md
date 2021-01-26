![](https://brands.home-assistant.io/_/litterrobot/icon.png)
# Litter-Robot for Home Assistant
Home Assistant integration for a Litter-Robot Connect self-cleaning litter box.

# Installation
There are two main ways to install this custom component within your Home Assistant instance:

1. Using HACS (see https://hacs.xyz/ for installation instructions if you do not already have it installed):
    1. From within Home Assistant, click on the link to **HACS**
    2. Click on **Integrations**
    3. Click on the vertical ellipsis in the top right and select **Custom repositories**
    4. Enter the URL for this repository in the section that says *Add custom repository URL* and select **Integration** in the *Category* dropdown list
    5. Click the **ADD** button
    6. Close the *Custom repositories* window
    7. You should now be able to see the *Litter-Robot* card on the HACS Integrations page. Click on **INSTALL** and proceed with the installation instructions.
    8. Restart your Home Assistant instance and then proceed to the *Configuration* section below.

2. Manual Installation:
    1. Download or clone this repository
    2. Copy the contents of the folder **custom_components/litterrobot** into the same file structure on your Home Assistant instance
        - An easy way to do this is using the [Samba add-on](https://www.home-assistant.io/getting-started/configuration/#editing-configuration-via-sambawindows-networking), but feel free to do so however you want
    3. Restart your Home Assistant instance and then proceed to the *Configuration* section below.

While the manual installation above seems like less steps, it's important to note that you will not be able to see updates to this custom component unless you are subscribed to the watch list. You will then have to repeat each step in the process. By using HACS, you'll be able to see that an update is available and easily update the custom component.

# Configuration

There is a config flow for this Litter-Robot integration. After installing the custom component:
1. Go to **Configuration**->**Integrations**
2. Click **+ ADD INTEGRATION** to setup a new integration
3. Search for **Litter-Robot** and click on it
4. You will be guided through the rest of the setup process via the config flow

# Services
Replace `<entity_id>` in any of the below samples with the appropriate value of your Litter-Robot vacuum entity.

## vacuum.turn_off
Supports turning off your Litter-Robot. If the unit is currently cycling, it will interrupt the cycle and stop the bonnet where it is at the time the command is received.
```yaml
service: vacuum.turn_off
entity_id: <entity_id>
```

## vacuum.turn_on
Supports turning on your Litter-Robot, initiating a clean cycle.
```yaml
service: vacuum.turn_on
entity_id: <entity_id>
```

## vacuum.send_command
### reset_waste_drawer
Resets the waste drawer gauge on the Litter-Robot. 
```yaml
service: vacuum.send_command
data:
  entity_id: <entity_id>
  command: reset_waste_drawer
```

Alternatively, you can create a script using the snippet below that can then be reused across Home Assistant.
```yaml
alias: Reset Waste Drawer
sequence:
  - service: vacuum.send_command
    data:
      entity_id: <entity_id>
      command: reset_waste_drawer
mode: single
icon: 'mdi:refresh'
```

### set_sleep_mode
Enables (with sleep time param) or disables sleep mode on the Litter-Robot.

Param      | Type   | Description
---------- | ------ | -----------
enabled    | bool   | true to enable, false to disable
sleep_time | string | time at which the unit will enter sleep mode and prevent an automatic clean cycle for 8 hours. This param uses the 24-hour format string `%H:%M:%S`, with seconds being optional, and is based on the timezone configured for your Home Assistant installation. As such, `10:30:00` would indicate 10:30 am, whereas `22:30:00` would indicate 10:30 pm. Required if the param `enabled` is set to true.

```yaml
service: vacuum.send_command
data:
  entity_id: <entity_id>
  command: set_sleep_mode
  params:
    enabled: true
    sleep_time: '22:30:00'
```

---

## Support Me
I'm not employed by Litter-Robot, and provide this custom component purely for your own enjoyment and home automation needs. 

If you don't already own a Litter-Robot, please consider using [my referal code](http://share.litter-robot.com/rmcGL) and get $25 off your own robot (as well as a tip to me in appreciation)!

If you already own a Litter-Robot and still want to donate, consider buying me a coffee (or beer) instead by using the link below:

<a href="https://www.buymeacoffee.com/natekspencer" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-blue.png" alt="Buy Me A Coffee" height="41" width="174"></a>
