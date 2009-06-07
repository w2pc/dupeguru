#!/usr/bin/env python
# Unit Name: details_table
# Created By: Virgil Dupras
# Created On: 2009-05-17
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

from PyQt4.QtCore import Qt, SIGNAL, QAbstractTableModel, QVariant
from PyQt4.QtGui import QHeaderView, QTableView

HEADER = ['Attribute', 'Selected', 'Reference']

class DetailsModel(QAbstractTableModel):
    def __init__(self, app):
        QAbstractTableModel.__init__(self)
        self._app = app
        self._data = app.data
        self._dupe_data = None
        self._ref_data = None
        self.connect(app, SIGNAL('duplicateSelected()'), self.duplicateSelected)
    
    def columnCount(self, parent):
        return len(HEADER)
    
    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        if role != Qt.DisplayRole:
            return QVariant()
        column = index.column()
        row = index.row()
        if column == 0:
            return QVariant(self._data.COLUMNS[row]['display'])
        elif column == 1 and self._dupe_data:
            return QVariant(self._dupe_data[row])
        elif column == 2 and self._ref_data:
            return QVariant(self._ref_data[row])
        return QVariant()
    
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(HEADER):
            return QVariant(HEADER[section])
        return QVariant()
    
    def rowCount(self, parent):
        return len(self._data.COLUMNS)
    
    #--- Events
    def duplicateSelected(self):
        dupe = self._app.selected_dupe
        group = self._app.results.get_group_of_duplicate(dupe)
        ref = group.ref
        self._dupe_data = self._data.GetDisplayInfo(dupe, group)
        self._ref_data = self._data.GetDisplayInfo(ref, group)
        self.reset()
    

class DetailsTable(QTableView):
    def __init__(self, *args):
        QTableView.__init__(self, *args)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setShowGrid(False)
    
    def setModel(self, model):
        QTableView.setModel(self, model)
        # The model needs to be set to set header stuff
        hheader = self.horizontalHeader()
        hheader.setHighlightSections(False)
        hheader.setStretchLastSection(False)
        hheader.resizeSection(0, 100)
        hheader.setResizeMode(0, QHeaderView.Fixed)
        hheader.setResizeMode(1, QHeaderView.Stretch)
        hheader.setResizeMode(2, QHeaderView.Stretch)
        vheader = self.verticalHeader()
        vheader.setVisible(False)
        vheader.setDefaultSectionSize(18)
    