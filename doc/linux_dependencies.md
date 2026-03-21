# Linux dependencies

All dependencies listed below are not mandatory but useful for different purposes such as logging and monitoring.

## glances

[Glances](https://nicolargo.github.io/glances/) is a cross-platform system monitoring tool written in Python. It can be installed through the Python `pip` package manager as described in the [Install](https://glances.readthedocs.io/en/latest/install.html) page of the official documentation, or through `apt-get`.

> It's recommended to install it as a Linux service to start Glances automatically after booting the system. For more information about Linux services, refer to [`/doc/systemd_configuration.md`](/doc/systemd_configuration.md).

**After installing Glances in the Raspberry Pi, install the [Glances add-on for Home Assistant](/doc/homeassistant.md#glances) to remotely visualize the metrics.**

## loki

[Grafana Loki](https://grafana.com/docs/loki/latest/), or sometimes abbreviated as Loki, is a logging tool. The [Quick start](https://grafana.com/docs/loki/latest/get-started/quick-start/quick-start/) explains very well the common Loki-Alloy-Grafana architecture. **For SC RPi it's not necessary to install [Alloy](https://grafana.com/docs/alloy/latest/) nor other tools described in the official page, Loki is enough.**

The required steps to have Loki working correctly and as a Linux service are the following :

1. [Install Loki](#installing-loki)
2. [Configure Loki](#configure-loki)
3. [Configure Loki as a Linux service](https://medium.com/@abdullah037b/setup-loki-as-a-service-in-linux-cdf114d8e1f5)

> Configuration via YAML files and the Linux service creation is only necessary when installing manually.

**To check Loki is working correctly open http://raspberrypi.local:3100/ready or http://raspberrypi.local/metrics** (replace raspberrypi.local for the corresponding hostname). **To visualize logs remotely, install Grafana and configure the corresponding Grafana Loki datasource in the Grafana instance running with Home Assistant (refer to the [Grafana](/doc/homeassistant.md#grafana) section in [`/doc/homeassistant.md`](/doc/homeassistant.md)).**

### Installing Loki

There're many ways to install Grafana :

- [From the official GitHub](#installing-loki-from-official-github)<!---->
- [With `apt-get`](#installing-loki-with-apt-get)<!---->
- [With Docker](https://grafana.com/docs/loki/latest/get-started/quick-start/tutorial/)<!---->

> Install Loki manually only if `apt-get` brings an old version.

#### Installing Loki with `apt-get`

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

> By default configuration file will stored in `/etc/loki/config.yml`. For more information refer to [Install Grafana Loki locally](https://grafana.com/docs/loki/latest/setup/install/local/).

#### Installing Loki from official GitHub

To install Loki from the official GitHub page follow instructions in [Setup Loki as a service in Linux](https://medium.com/@abdullah037b/setup-loki-as-a-service-in-linux-cdf114d8e1f5).

> Instead of using `gunzip` for uncompressing, use `unzip`.

### Configure Loki

Create a YAML file or verify it's already created (usually named `loki-local-config.yaml`) as **it will be used for the start command**. Refer to [Setup Loki as a service in Linux](https://medium.com/@abdullah037b/setup-loki-as-a-service-in-linux-cdf114d8e1f5) to obtain a sample configuration file.

### Configure Loki as a Linux Service

Refer to [Setup Loki as a service in Linux.](https://medium.com/@abdullah037b/setup-loki-as-a-service-in-linux-cdf114d8e1f5).

## Links

- [Glances - Install](https://glances.readthedocs.io/en/latest/install.html)
- [Grafana Alloy](https://grafana.com/docs/alloy/latest/)
- [Grafana Loki](https://grafana.com/docs/loki/latest/)
- [Grafana Loki - Install Grafana Loki locally](https://grafana.com/docs/loki/latest/setup/install/local/)
- [Grafana Loki - Quick start](https://grafana.com/docs/loki/latest/get-started/quick-start/quick-start/)
- [Setup Loki as a service in Linux](https://medium.com/@abdullah037b/setup-loki-as-a-service-in-linux-cdf114d8e1f5))
- [Systemd journal access with python API](https://stackoverflow.com/questions/58753748/systemd-journal-access-with-python-api).
