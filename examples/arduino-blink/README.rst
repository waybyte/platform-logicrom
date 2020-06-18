How to build
============

1. Install `Visual Studio Code <https://code.visualstudio.com/>`_
2. Install `PlatformIO Extension for VSCode <https://platformio.org/platformio-ide>`_
3. Install SiWi GSM Platform:

   * Open PlatformIO Home
   * Go to Platforms -> Advanced Installation
   * Paste repository link https://github.com/siwiembedded/platform-siwigsm.git
   * Click Install

4. Download and Extract examples from github https://github.com/siwiembedded/siwigsm/archive/master.zip
5. Extract and Open example folder with *VSCode*
6. Run following command:

.. code-block:: bash

   # Build Project
   $ platformio run

   # Upload Project
   $ platformio run --target upload

