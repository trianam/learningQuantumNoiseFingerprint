#     conf.py
#     Class to create configuration blocks.
#     Copyright (C) 2021  Stefano Martina (stefano.martina@unifi.it)
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import copy

class Conf:
    def __init__(self, confDict):
        self.__dict__ = confDict

    def copy(self, updateDict={}):
        newConf = copy.copy(self)
        for k in updateDict:
            newConf.__dict__[k] = updateDict[k]

        return newConf

    def has(self, key):
        return key in self.__dict__

    def getDict(self):
        return self.__dict__
