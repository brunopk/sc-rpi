# Linux dependencies

All dependencies listed below are not mandatory but useful for different purposes such as logging and monitoring.

## glances

[Glances](https://nicolargo.github.io/glances/) is a cross-platform system monitoring tool written in Python. It can be installed through the Python `pip` package manager as described in the [Install](https://glances.readthedocs.io/en/latest/install.html) page of the official documentation, or through `apt-get`.

> It's recommended to install it as a Linux service to start Glances automatically after booting the system. For more information about Linux services, refer to [`/doc/systemd_configuration.md`](/doc/systemd_configuration.md).

Install the [Glances add-on for Home Assistant](/doc/homeassistant.md#glances) to remotely visualize the metrics.

## libsystemd-dev

libsystemd-dev used to send logs though the journal systemd service. It can be installed through `apt-get`.

## loki

[Grafana Loki](https://grafana.com/docs/loki/latest/), or sometimes abbreviated as Loki, is a tool stack for logging. The full Grafana Loki stack can be installed with Docker as described in the [Loki Tutorial](https://grafana.com/docs/loki/latest/get-started/quick-start/tutorial/) page of the official Grafana Loki documentation, but for simplicity, it's **recommended** to install it through `apt-get` by following instructions described in the [Install Grafana Loki locally](https://grafana.com/docs/loki/latest/setup/install/local/) page, also from the official documentation.

> For SC RPi it's not necessary to install Alloy nor other tools described in the official documentation. With Grafana Loki is enough for SC RPi.

To visualize logs, install Grafana and configure the corresponding Grafana Loki datasource. To install Grafana as a Home Assistant add-on, refer to the [Grafana](/doc/homeassistant.md#grafana) section in [`/doc/homeassistant.md`](/doc/homeassistant.md).

## python

In case of not being able to install the correct Python version with `apt-get`, refer to [this](https://forums.raspberrypi.com/viewtopic.php?t=291158) thread in Raspberry forum to install it from sources.

## Links

- [Glances - Install](https://glances.readthedocs.io/en/latest/install.html)
- [Grafana Loki](https://grafana.com/docs/loki/latest/)
- [Grafana Loki - Install Grafana Loki locally](https://grafana.com/docs/loki/latest/setup/install/local/)
- [Systemd journal access with python API](https://stackoverflow.com/questions/58753748/systemd-journal-access-with-python-api).
