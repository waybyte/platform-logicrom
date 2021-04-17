# Copyright 2021 WAYBYTE Solutions
#
# SPDX-License-Identifier: MIT
#

from platform import system
from platformio.managers.platform import PlatformBase

class LogicromPlatform(PlatformBase):
    def configure_default_packages(self, variables, target):
        return PlatformBase.configure_default_packages(self, variables,
                                                       target)
