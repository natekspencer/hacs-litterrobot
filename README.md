![](https://brands.home-assistant.io/_/litterrobot/icon.png)

# Litter-Robot for Home Assistant

**_This project has been integrated into the Home-Assistant core source code and is no longer actively maintained for HACS integration. Please see https://www.home-assistant.io/integrations/litterrobot/ for the official integration and use https://github.com/home-assistant/core/issues to report any issues._**

Home Assistant integration for a Litter-Robot Connect self-cleaning litter box.

# Installation

There are two main ways to install this custom component within your Home Assistant instance:

1. Using HACS (see https://hacs.xyz/ for installation instructions if you do not already have it installed):

   1. From within Home Assistant, click on the link to **HACS**
   2. Click on **Integrations**
   3. Click on the vertical ellipsis in the top right and select **Custom repositories**
   4. Enter the URL for this repository in the section that says _Add custom repository URL_ and select **Integration** in the _Category_ dropdown list
   5. Click the **ADD** button
   6. Close the _Custom repositories_ window
   7. You should now be able to see the _Litter-Robot_ card on the HACS Integrations page. Click on **INSTALL** and proceed with the installation instructions.
   8. Restart your Home Assistant instance and then proceed to the _Configuration_ section below.

2. Manual Installation:
   1. Download or clone this repository
   2. Copy the contents of the folder **custom_components/litterrobot** into the same file structure on your Home Assistant instance
      - An easy way to do this is using the [Samba add-on](https://www.home-assistant.io/getting-started/configuration/#editing-configuration-via-sambawindows-networking), but feel free to do so however you want
   3. Restart your Home Assistant instance and then proceed to the _Configuration_ section below.

While the manual installation above seems like less steps, it's important to note that you will not be able to see updates to this custom component unless you are subscribed to the watch list. You will then have to repeat each step in the process. By using HACS, you'll be able to see that an update is available and easily update the custom component.

---

## Support Me

I'm not employed by Litter-Robot, and provide this custom component purely for your own enjoyment and home automation needs.

If you don't already own a Litter-Robot, please consider using [my referral code](https://www.talkable.com/x/V7bKS2) and get $25 off your own robot (as well as a tip to me in appreciation)!

If you already own a Litter-Robot and/or want to donate to me directly, consider buying me a coffee (or beer) instead by using the link below:

<a href="https://www.buymeacoffee.com/natekspencer" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-blue.png" alt="Buy Me A Coffee" height="41" width="174"></a>
