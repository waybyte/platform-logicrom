How to build
============

1. Install `Visual Studio Code <https://code.visualstudio.com/>`_
2. Install `PlatformIO Extension for VSCode <https://platformio.org/platformio-ide>`_
3. Install Logicrom Platform:

   * Open PlatformIO Home
   * Go to Platforms -> Embedded (Top Navigation)
   * Type "Logicrom" in the search box
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

	(c) Waybyte Solutions
	Logicrom v6.65 268a05f - Build Jan 25 2022 12:00:06
	Core firmware: WBMT2503DV01_c88ba54
	System Ready
	System Initialization finished
	SYSTEM: GSM NW State: 2
	NETWORK: SIM card ready

	Please login to access console
	Username: SYSTEM: GSM NW State: 5
	NETWORK: GSM - Registered
	NETWORK: GPRS - Registered
	NETWORK: GPRS Active 1110
	Socket connected
	Data received (12 bytes):
	Hello World
	Data send status: 0
	Data received (12 bytes):
	Hello World
	Data send status: 0
	Data send status: 0
	Data received (12 bytes):
	Hello World
	Data received (12 bytes):
	Hello World
	Data send status: 0
	Data received (12 bytes):
	Hello World
	Data send status: 0

