# LOGICROM for Platformio

![Examples](https://github.com/waybyte/platform-logicrom/workflows/Examples/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/logicromsdk/badge/?version=latest)](https://docs.logicrom.com)
[![Github Issues](https://img.shields.io/github/issues/waybyte/platform-logicrom.svg)](http://github.com/waybyte/platform-logicrom/issues)
[![Github Releases](https://img.shields.io/github/release/waybyte/platform-logicrom.svg)](https://github.com/waybyte/platform-logicrom/releases)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/waybyte/platform-logicrom/blob/master/LICENSE)

## Installation

1. Install [Visual Studio Code](https://code.visualstudio.com/)
2. Install [PlatformIO Extension for VSCode](https://platformio.org/platformio-ide)
3. Install LOGICROM Platform:
	* Open PlatformIO Home
	* Go to Platforms -> Embedded
	* Enter in search box "Logicrom"
	* Open "LOGICROM Development Platform" and hit install

## Examples

* [gpio-blink](https://github.com/waybyte/platform-logicrom/tree/master/examples/gpio-blink) - GPIO Toggle Example
* [adc-example](https://github.com/waybyte/platform-logicrom/tree/master/examples/adc-example) - ADC Read Example
* [socket-example](https://github.com/waybyte/platform-logicrom/tree/master/examples/socket-example) - TCP Socket example using RAW Socket APIs
* [ssl-socket-example](https://github.com/waybyte/platform-logicrom/tree/master/examples/ssl-socket-example) - SSL Socket example
* [ssl-socket-clientauth](https://github.com/waybyte/platform-logicrom/tree/master/examples/ssl-socket-clientauth) - SSL Socket example with client certificate authentication

## Resources

* [Documentation](https://docs.logicrom.com) - LOGICROM SDK documentation for latest version

# Supported Modules
## GSM Modules

| Module Name  | Networking | BT | GPS | GPIO | ADC | I2C | SPI | USB | LCD[^1] |
|--------------|------------|----|-----|------|-----|-----|-----|-----|---------|
| Quectel M66  | :heavy_check_mark: | :heavy_check_mark: | :heavy_minus_sign: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_minus_sign: | :x: |
| Quectel M66DS| :heavy_check_mark: | :heavy_check_mark: | :heavy_minus_sign: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_minus_sign: | :x: |
| Quectel MC60 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_minus_sign: | :x: |
| Quectel MC20 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_minus_sign: | :x: |
| Quectel M56| :heavy_check_mark: | :heavy_check_mark: | :heavy_minus_sign: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x: |
| Quectel MC20U| :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x: |
| SIMCOM SIM868[^2]| :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x: |

## 4G LTE Cat.1 Modules

| Module Name  | Networking | BLE[^3] | GPS | GPIO | ADC | I2C | SPI | USB | LCD | Camera |
|--------------|------------|---------|-----|------|-----|-----|-----|-----|-----|--------|
| Neoway N58  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: |
| Neoway N716 | :heavy_check_mark: | :heavy_check_mark: | :heavy_minus_sign: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: |
| Quectel EC200 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: |
| Quectel EC600 | :heavy_check_mark: | :heavy_check_mark: | :heavy_minus_sign: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x: | :x: |

DFOTA is also supported of on above mentioned LTE modules

## NB-IoT Modules[^4]

| Module Name  | Networking | GPS | GPIO | ADC | I2C | SPI | USB |
|--------------|------------|-----|------|-----|-----|-----|-----|
| Quectel BC66 | :heavy_check_mark: | :heavy_minus_sign: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Quectel BC20 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |

[^1]: LCD is work in progress.
[^2]: Please backup calibration during first flash via Maui Meta tool (google is your friend).
[^3]: Currely only GATT Server supported and used for console purpose only.
[^4]: Updates to come
