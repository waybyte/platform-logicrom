# Logicrom OpenCPU Development Platform for Platformio IDE

[![PlatformIO Registry](https://badges.registry.platformio.org/packages/waybyte/platform/logicrom.svg)](https://registry.platformio.org/platforms/waybyte/logicrom)

![Examples](https://github.com/waybyte/platform-logicrom/workflows/Examples/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/logicromsdk/badge/?version=latest)](https://docs.logicrom.com)
[![Github Issues](https://img.shields.io/github/issues/waybyte/platform-logicrom.svg)](http://github.com/waybyte/platform-logicrom/issues)
[![Github Releases](https://img.shields.io/github/release/waybyte/platform-logicrom.svg)](https://github.com/waybyte/platform-logicrom/releases)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/waybyte/platform-logicrom/blob/master/LICENSE)

## Quick Installation

1. Install [Visual Studio Code](https://code.visualstudio.com/)
2. Install [PlatformIO Extension for VSCode](https://platformio.org/platformio-ide)
3. Install Logicrom Platform:
	* Open PlatformIO Home
	* Go to Platforms -> Embedded
	* Enter in search box "Logicrom"
	* Open "Logicrom Development Platform" and hit install

For complete installation guide visit: [Installing Logicrom on PlatformIO](https://docs.logicrom.com/en/latest/book/quick_start/setup_platformio.html)

## Examples

1. [Hello World](https://github.com/waybyte/hello-world-logicrom)
2. [OS Example](https://github.com/waybyte/example-os)
3. [Console example](https://github.com/waybyte/example-console)
4. [Timer example](https://github.com/waybyte/example-timer)
5. [GPIO example](https://github.com/waybyte/example-gpio)
6. [UART example](https://github.com/waybyte/example-uart)
7. [ADC example](https://github.com/waybyte/example-adc)
8. [PWM example](https://github.com/waybyte/example-pwm)
9. [SPI example](https://github.com/waybyte/example-spi)
10. [I2C example](https://github.com/waybyte/example-i2c)
11. [Display example](https://github.com/waybyte/example-display)
12. [GPS/GNSS example](https://github.com/waybyte/example-gps)
13. [Socket example](https://github.com/waybyte/example-socket)
14. [SSL Socket example](https://github.com/waybyte/example-ssl-socket)
15. [SSL Socket with Client Authentication](https://github.com/waybyte/example-ssl-socket-clientauth)
16. [HTTP Client example](https://github.com/waybyte/example-httpclient)


## Resources

* [Documentation](https://docs.logicrom.com) - Logicrom OpenCPU SDK documentation for latest version


# Licensing

Logicrom is available in dual-license:

- **Logicrom Personal License** - Free for Personal use or Evaluation
- **Logicrom Commercial License** - Commercial Use


## Personal vs Commercial License

|              |  Personal |  Commercial  |
| -------------| ------------------ | -------------------- |
| License | [MIT](https://github.com/waybyte/platform-logicrom/blob/master/LICENSE) | Commercial - [contact us](https://waybyte.in/contact) |
| Limitations | 1 License per user | None  |
| Price  | Free | Paid, see [details](https://waybyte.in/pricing) |
| functionality  | Full | Full |
| Technical support  | Community support via [Github](https://github.com/orgs/waybyte/discussions) | Commercial Email Support |

## Get Free Personal License

Following are simple steps to activate your device.

1. Register account on [waybyte.in](https://waybyte.in/register)
2. Click on [Register Free Device](https://waybyte.in/devices/register) from left menu
3. Enter device details
4. Flash Logicrom core firmware
5. Put a valid SIM card in device
6. Turn on the device, It should accquire the license\
   If device fail to do so, run "getlic" command from device console Port (USB Port 0 or Main UART) to try again.

If you face any issue, Please feel free to contact us @ support@waybyte.in or post your issue on github.

# Supported Modules

| Name              | Vendor   | SoC/Chipset | Supported Peripherals                              | APP RAM / ROM   |
|-------------------|----------|-------------|----------------------------------------------------|-----------------|
| EC200U-XX-YY [^1] | Quectel  | RDA8910     |  UART, USB, SPI, I2C, ADC, LCD, BT [^2], GNSS [^3] | 500 KB / 1 MB   |
| EC600U-XX-YY [^1] | Quectel  | RDA8910     |                                                    | 500 KB / 1 MB   |
| EC600U-XX-YY [^1] | Quectel  | RDA8910     |                                                    | 500 KB / 1 MB   |
| EG915U-XX-YY [^1] | Quectel  | RDA8910     |                                                    | 500 KB / 1 MB   |
| N58-CA            | Neoway   | RDA8910     |                                                    | 500 KB / 1 MB   |
| N716-CA           | Neoway   | RDA8910     |                                                    | 500 KB / 1 MB   |
| EC100N-XX-XX      | Quectel  | ASR1603     |  UART, USB, SPI, I2C, ADC                          | 512 KB / 1 MB   |
| EC200N-CN-AA      | Quectel  | ASR1603     |                                                    | 512 KB / 512 KB |
| EC600N-CN-AA      | Quectel  | ASR1603     |                                                    | 512 KB / 1 MB   |
| EG912Y-EU-YY      | Quectel  | ASR1603     |                                                    | 512 KB / 1 MB   |
| EG915N-EU-YY      | Quectel  | ASR1603     |                                                    | 512 KB / 512 KB |
| EC100Y-CN-YY      | Quectel  | ASR1601     |  UART, USB, SPI, I2C, ADC                          | 512 KB / 512 KB |
| EC100S-CN-YY      | Quectel  | ASR1601     |                                                    | 512 KB / 1 MB   |
| EC600S-CN-YY      | Quectel  | ASR1601     |                                                    | 512 KB / 1 MB   |
| AC7670C           | SIMCOM   | ASR1601     |                                                    | 512 KB / 1 MB   |
| MC20, MC60, MC20U | Quectel  | MT2503      |  UART, USB, SPI, I2C, ADC, GNSS                    | 94 KB / 256 KB  |
| SIM868[^4]        | SIMCOM   | MT2503      |                                                    | 94 KB / 256 KB  |
| M66, M26, M56     | Quectel  | MT6261      |  UART, USB, SPI, I2C, ADC                          | 94 KB / 256 KB  |
| SIM800[^4]        | SIMCOM   | MT6261      |                                                    | 94 KB / 256 KB  |
| MC65              | Quectel  | RDA8955     |  UART, USB, SPI, I2C, ADC, GNSS [^3], LCD          | 1 MB / 576 KB   |
| M590              | Neoway   | RDA8955     |                                                    | 1 MB / 576 KB   |
| A9, A9G           | AiThinker| RDA8955     |                                                    | 1 MB / 576 KB   |

[^1]: XX can be CN/AU/EU, YY can be AA/AB/AC

[^2]: Currely only GATT Server supported and used for console purpose only

[^3]: Supported on module with GNSS

[^4]: IMEI need to be configured when core is flashed for first time, use AT+EGMR=1,7,"imei"


> DFOTA is also supported for LTE modules
