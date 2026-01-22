# Linux dependencies

All dependencies listed below are not mandatory but useful for different purposes such as logging and monitoring.

## glances

[Glances](https://nicolargo.github.io/glances/) is a cross-platform system monitoring tool written in Python. It can be installed through the Python `pip` package manager as described in the [Install](https://glances.readthedocs.io/en/latest/install.html) page of the official documentation, or through `apt-get`.

> It's recommended to install it as a Linux service to start Glances automatically after booting the system. For more information about Linux services, refer to [`/doc/systemd_configuration.md`](/doc/systemd_configuration.md).

Install the [Glances add-on for Home Assistant](/doc/homeassistant.md#glances) to remotely visualize the metrics.

## libsystemd-dev

libsystemd-dev used to send logs though the journal systemd service. It can be installed through `apt-get`.

## loki

[Grafana Loki](https://grafana.com/docs/loki/latest/), or sometimes abbreviated as Loki, is a logging tool.

> For SC RPi it's not necessary to install Alloy nor other tools described in the official page, Loki is enough.

The required steps to have Loki working correctly and automatically started after system boot :

1. [Install Loki](#installing-loki)
2. [Configure Loki (only necessary when installing manually)](#configure-loki)
3. [Configure Loki as a Linux service (only necessary when installing manually)](https://medium.com/@abdullah037b/setup-loki-as-a-service-in-linux-cdf114d8e1f5)

Then to visualize logs, install Grafana and configure the corresponding Grafana Loki datasource (refer to the [Grafana](/doc/homeassistant.md#grafana) section in [`/doc/homeassistant.md`](/doc/homeassistant.md)).

### Installing Loki

There're many ways to install Grafana :

- [From the official Loki GitHub page](#installing-loki-from-the-official-loki-github-page)<!---->
- [With `apt-get`](#installing-loki-with-apt-get)<!---->
- [With Docker](https://grafana.com/docs/loki/latest/get-started/quick-start/tutorial/)<!---->

Try installing Loki with `apt-get`, if it installs an old version go for the GitHub option. After installing Loki, configure it as a Linux **service** following instructions in [Setup Loki as a service in Linux](https://medium.com/@abdullah037b/setup-loki-as-a-service-in-linux-cdf114d8e1f5)).

#### Installing Loki with `apt-get`

More information: [Install Grafana Loki locally](https://grafana.com/docs/loki/latest/setup/install/local/)

1. Add GPG keys for official repos :

    ```bash
    mkdir -p /etc/apt/keyrings/
    wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor > /etc/apt/keyrings/grafana.gpg
    echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | tee /etc/apt/sources.list.d/grafana.list
    ```

2. Update `apt-get` local registries :

    ```bash
    sudo apt-get update
    ```

3. Install `loki` package :
  
    ```bash
    sudo apt-get install loki
    ```

> By default configuration file will stored in `/etc/loki/config.yml`. The default port is 3100.

#### Installing Loki from the official Loki GitHub page

> Install from GitHub in case the official `apt-get` installs an old version.

To install Loki from the official GitHub page follow instructions in [Setup Loki as a service in Linux.](https://medium.com/@abdullah037b/setup-loki-as-a-service-in-linux-cdf114d8e1f5).

> Instead of using `gunzip` for uncompressing, use `unzip`.

### Configure Loki

To start Loki, set the `loki-local-config.yaml` configuration file as **it will be used for the start command**. Take a look at [Setup Loki as a service in Linux.](https://medium.com/@abdullah037b/setup-loki-as-a-service-in-linux-cdf114d8e1f5) obtain an example of a Loki configuration file.

## python

In case of not being able to install the correct Python version with `apt-get`, refer to [this](https://forums.raspberrypi.com/viewtopic.php?t=291158) thread in Raspberry forum to install it from sources.

## Links

- [Glances - Install](https://glances.readthedocs.io/en/latest/install.html)
- [Grafana Loki](https://grafana.com/docs/loki/latest/)
- [Grafana Loki - Install Grafana Loki locally](https://grafana.com/docs/loki/latest/setup/install/local/)
- [Setup Loki as a service in Linux](https://medium.com/@abdullah037b/setup-loki-as-a-service-in-linux-cdf114d8e1f5))
- [Systemd journal access with python API](https://stackoverflow.com/questions/58753748/systemd-journal-access-with-python-api).
