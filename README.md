Regularly check the indoor air quality (AQI), and run the HVAC fan AQI exceeds a given threshold.

I use a Nest thermostat and Purple Air AQI sensor, and we can easily add modules for other devices (just need to update import statements).

It runs regularly via Github Actions - unfortunately this means it doesn't run reliably, and a commit needs to be made every 60 days in order to keep the action from auto-stopping. A better solution would be to run this on a Raspberry Pi, perhaps.
