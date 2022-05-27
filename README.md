# Logicrom Wireless IoT Platform for Platformio

[![PlatformIO Registry](https://badges.registry.platformio.org/packages/ajaybhargav/platform/logicrom.svg)](https://registry.platformio.org/platforms/ajaybhargav/logicrom)

![Examples](https://github.com/waybyte/platform-logicrom/workflows/Examples/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/logicromsdk/badge/?version=latest)](https://docs.logicrom.com)
[![Github Issues](https://img.shields.io/github/issues/waybyte/platform-logicrom.svg)](http://github.com/waybyte/platform-logicrom/issues)
[![Github Releases](https://img.shields.io/github/release/waybyte/platform-logicrom.svg)](https://github.com/waybyte/platform-logicrom/releases)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/waybyte/platform-logicrom/blob/master/LICENSE)

## Installation

1. Install [Visual Studio Code](https://code.visualstudio.com/)
2. Install [PlatformIO Extension for VSCode](https://platformio.org/platformio-ide)
3. Install Logicrom Platform:
	* Open PlatformIO Home
	* Go to Platforms -> Embedded
	* Enter in search box "Logicrom"
	* Open "Logicrom Development Platform" and hit install

## Examples

* [gpio-blink](https://github.com/waybyte/platform-logicrom/tree/master/examples/gpio-blink) - GPIO Toggle Example
* [adc-example](https://github.com/waybyte/platform-logicrom/tree/master/examples/adc-example) - ADC Read Example
* [socket-example](https://github.com/waybyte/platform-logicrom/tree/master/examples/socket-example) - TCP Socket example using RAW Socket APIs
* [ssl-socket-example](https://github.com/waybyte/platform-logicrom/tree/master/examples/ssl-socket-example) - SSL Socket example
* [ssl-socket-clientauth](https://github.com/waybyte/platform-logicrom/tree/master/examples/ssl-socket-clientauth) - SSL Socket example with client certificate authentication
* [example-os](https://github.com/waybyte/example-os) - OS API use Example
* [example-console](https://github.com/waybyte/example-console) - Console and Comamnd processor example


## Resources

* [Documentation](https://docs.logicrom.com) - Logicrom SDK documentation for latest version

# Supported Modules
## 4G LTE Cat.1 Modules

| Module Name  | Networking | BLE[^1] | GPS | GPIO | ADC | I2C | SPI | USB | LCD | Camera |
|--------------|------------|---------|-----|------|-----|-----|-----|-----|-----|--------|
| Neoway N58  | &check; | &check; | &check; | &check; | &check; | &check; | &check; | &check; | &check; | &cross; |
| Neoway N716 | &check; | &check; | &#8212; | &check; | &check; | &check; | &check; | &check; | &check; | &cross; |
| Quectel EC200U | &check; | &check; | &check; | &check; | &check; | &check; | &check; | &check; | &check; | &cross; |
| Quectel EC600U | &check; | &check; | &#8212; | &check; | &check; | &check; | &check; | &check; | &check; | &cross; |
| Quectel EG915U  | &check; | &check; | &#8212; | &check; | &check; | &check; | &check; | &check; | &check; | &cross; |
| Fibocom L610  | &check; | &check; | &#8212; | &check; | &check; | &check; | &check; | &check; | &check; | &cross; |

> DFOTA is also supported for LTE modules

## NB-IoT Modules[^2]

| Module Name  | Networking | GPS | GPIO | ADC | I2C | SPI | USB |
|--------------|------------|-----|------|-----|-----|-----|-----|
| Quectel BC66 | &check; | &#8212; | &check; | &check; | &check; | &check; | &check; |
| Quectel BC20 | &check; | &check; | &check; | &check; | &check; | &check; | &check; |

## GSM Modules

| Module Name  | Networking | BT | GPS | GPIO | ADC | I2C | SPI | USB | LCD[^3] |
|--------------|------------|----|-----|------|-----|-----|-----|-----|---------|
| Quectel M66  | &check; | &check; | &#8212; | &check; | &check; | &check; | &check; | &#8212; | &cross; |
| Quectel M66DS| &check; | &check; | &#8212; | &check; | &check; | &check; | &check; | &#8212; | &cross; |
| Quectel MC60 | &check; | &check; | &check; | &check; | &check; | &check; | &check; | &#8212; | &cross; |
| Quectel MC20 | &check; | &check; | &check; | &check; | &check; | &check; | &check; | &#8212; | &cross; |
| Quectel M56| &check; | &check; | &#8212; | &check; | &check; | &check; | &check; | &check; | &cross; |
| Quectel MC20U| &check; | &check; | &check; | &check; | &check; | &check; | &check; | &check; | &cross; |
| SIMCOM SIM868[^4]| &check; | &check; | &check; | &check; | &check; | &check; | &check; | &check; | &cross; |


[^1]: Currely only GATT Server supported and used for console purpose only.

[^2]: Updates to come

[^3]: LCD is work in progress.

[^4]: Please backup calibration during first flash via Maui Meta tool (google is your friend).
