How to build
============

1. Install `Visual Studio Code <https://code.visualstudio.com/>`_
2. Install `PlatformIO Extension for VSCode <https://platformio.org/platformio-ide>`_
3. Install LOGICROM Platform:

   * Open PlatformIO Home
   * Go to Platforms -> Advanced Installation
   * Paste repository link https://github.com/waybyte/platform-logicrom.git
   * Click Install

4. Download and Extract examples from github https://github.com/waybyte/platform-logicrom/archive/master.zip
5. Extract and Open example folder with *VSCode*
6. Run following command:

.. code-block:: bash

   # Build Project
   $ platformio run

   # Upload Project
   $ platformio run --target upload

Example Output
--------------

.. code-block::

	(c) 2021 WAYBYTE
	LOGICROM v6.62 ea61103 - Build Apr 19 2021 19:58:05
	Core firmware: WBMT2503DV01_c70a56b
	System Ready
	System Initialization finished
	SYSTEM: GSM NW State: 2
	NETWORK: SIM card ready

	Please login to access console
	Username: ADC Channel 0: 572, 1565.56mV
	ADC Channel 1: 932, 2550.88mV
	ADC Channel 2: 13, 35.58mV
	ADC Channel 0: 571, 1562.83mV
	ADC Channel 1: 932, 2550.88mV
	ADC Channel 2: 12, 32.84mV
	ADC Channel 0: 573, 1568.30mV
	ADC Channel 1: 931, 2548.15mV
	ADC Channel 2: 13, 35.58mV
	ADC Channel 0: 572, 1565.56mV
	ADC Channel 1: 931, 2548.15mV
	ADC Channel 2: 13, 35.58mV
	ADC Channel 0: 571, 1562.83mV
	ADC Channel 1: 931, 2548.15mV
	ADC Channel 2: 12, 32.84mV
	SYSTEM: GSM NW State: 5
	ADC Channel 0: 572, 1565.56mV
	ADC Channel 1: 932, 2550.88mV
	ADC Channel 2: 12, 32.84mV
	NETWORK: GSM - Registered
	ADC Channel 0: 571, 1562.83mV
	ADC Channel 1: 932, 2550.88mV
	ADC Channel 2: 13, 35.58mV
	ADC Channel 0: 570, 1560.09mV
	ADC Channel 1: 931, 2548.15mV
	ADC Channel 2: 13, 35.58mV
	ADC Channel 0: 572, 1565.56mV
	ADC Channel 1: 932, 2550.88mV
	ADC Channel 2: 13, 35.58mV
	ADC Channel 0: 571, 1562.83mV
	ADC Channel 1: 932, 2550.88mV
	ADC Channel 2: 13, 35.58mV