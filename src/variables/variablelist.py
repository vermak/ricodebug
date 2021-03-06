# ricodebug - A GDB frontend which focuses on visually supported
# debugging using data structure graphs and SystemC features.
#
# Copyright (C) 2011  The ricodebug project team at the
# Upper Austrian University Of Applied Sciences Hagenberg,
# Department Embedded Systems Design
#
# This file is part of ricodebug.
#
# ricodebug is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# For further information see <http://syscdbg.hagenberg.servus.at/>.

from PyQt4.QtCore import QObject


class VariableList(QObject):
    """
    holds variablewrappers that are generated by the given factory
    """

    def __init__(self, factory, distributedObjects):
        """ Constructor
        @param factory               variables.varwrapperfactory.VarWrapperFactory,
                                     WrapperFactory of the Module using the VariableList
        @param distributedObjects    distributedobjects.DistributedObjects, the DistributedObjects-Instance """
        QObject.__init__(self)
        self.varPool = distributedObjects.variablePool
        self.factory = factory
        self.list = []

    def addVarByName(self, varName):
        """ adds new VariableWrapper for given varName and returns this newly added VariableWrapper
        @param varName    string, the name of the Variable to add  """
        var = self.varPool.getVar(str(varName))
        vw = var.makeWrapper(self.factory)
        self.list.append(vw)
        return vw

    def addVar(self, varWrapper):
        """ adds VariableWrapper varWrapper to the list
        @param varWrapper    variables.variablewrapper.VariableWrapper, VariableWrapper to add to the list """
        self.list.append(varWrapper)
    
    def reloadLocals(self):
        self.clear()
        for var in self.varPool.reloadLocals():
            vw = var.makeWrapper(self.factory)
            self.list.append(vw)
            
    def addLocals(self):
        for var in self.varPool.addLocals():
            vw = var.makeWrapper(self.factory)
            self.list.append(vw)
        
    def removeVar(self, varWrapper):
        """ removes VariableWrapper varWrapper from the list
        @param varWrapper    variables.variablewrapper.VariableWrapper, VariableWrapper to remove from the list """
        if varWrapper in self.list:
            self.list.remove(varWrapper)
            varWrapper.die()

    def clear(self):
        """ Clears the whole VariableList. """
        for vw in self.list:
            vw.die()
        self.list = []

    def getVariableWrapper(self, var):
        return self.list[self.list.index(var)]

    def __getitem__(self, key):
        return self.list[key]

    def __setitem__(self, key, item):
        self.list[key] = item

    def __len__(self):
        return len(self.list)

    def __delitem__(self, key):
        del self.list[key]
