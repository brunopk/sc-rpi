# System dependencies

In order for sc-rpi to work some system dependencies must be installed with `apt-get` or any other Linux package manager:

1. libsystemd-dev: used to send logs though the journal systemd service

In case of not being able to install Python with apt-get (`sudo apt-get install python3.8`), refer to [this](https://forums.raspberrypi.com/viewtopic.php?t=291158) thread in Raspberry forum to install it from sources.

## Links

- [Systemd journal access with python API](https://stackoverflow.com/questions/58753748/systemd-journal-access-with-python-api).
