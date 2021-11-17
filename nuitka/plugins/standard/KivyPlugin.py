#     Copyright 2021, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
""" Details see below in class definition.
"""

from nuitka.Options import isStandaloneMode
from nuitka.plugins.PluginBase import NuitkaPluginBase


class NuitkaPluginKivy(NuitkaPluginBase):
    """This class represents the main logic of the plugin."""

    plugin_name = "kivy"
    plugin_desc = "Required by kivy package"

    @staticmethod
    def isAlwaysEnabled():
        return True

    @classmethod
    def isRelevant(cls):
        """One time only check: may this plugin be required?

        Returns:
            True if this is a standalone compilation.
        """
        return isStandaloneMode()

    def _getKivyInformation(self):
        setup_codes = r"""
import kivy.core.image
"""
        info = self.queryRuntimeInformationMultiple(
            info_name="kivy_info",
            setup_codes=setup_codes,
            values=(("libs_loaded", "kivy.core.image.libs_loaded"),),
        )

        if info is None:
            self.sysexit("Error, it seems Kivy is not installed.")

        return info

    def getImplicitImports(self, module):
        full_name = module.getFullName()

        if full_name == "kivy.core.image":
            for module_name in self._getKivyInformation().libs_loaded:
                yield full_name.getChildNamed(module_name)
