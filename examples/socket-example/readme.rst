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

	(c) 2020 WAYBYTE
	Firmware Lib v6.49 0b5247c - Build Jun  7 2020 14:10:11
	Core firmware: SC20UCB01A02_SIWI_759fd68
	System Ready
	System Initialization finished
	SYSTEM: GSM NW State: 2
	NETWORK: SIM card ready
	  ______ _ _  _  _ _
	 / _____|_|_)(_)(_|_)
	( (____  _ _  _  _ _
	 \____ \| | || || | |
	 _____) ) | || || | |
	(______/|_|\_____/|_|


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

