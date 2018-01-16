# coding: utf-8

import collections
import pprint


class Cell():
    # basic cell
    # provide location,concentration,status

    def __init__(self, row, column, maxrow, maxcolumn):
        self.status = 'Dead'  # alive;equilibrium
        self.concentration = 0
        self.location = (row, column)
        self.maxrow = maxrow
        self.maxcolumn = maxcolumn
        self.diffusion = False

    def __concentrationcheck(self):
        if self.concentration < 0:
            self.concentration = 0

        elif self.concentration != 0 and self.status == 'Dead':
            self.status = 'Alive'
            # concentration status changed

    def getneighbour(self):
        row = self.location[0]
        column = self.location[1]
        if row - 1 < 0:
            initrow = 0
        else:
            initrow = row - 1
        if column - 1 < 0:
            initcolumn = 0
        else:
            initcolumn = column - 1
        if row + 1 >= self.maxrow:
            maxrow = self.maxrow
        else:
            maxrow = row + 1
        if column + 1 >= self.maxcolumn:
            maxcolumn = self.maxcolumn
        else:
            maxcolumn = column + 1

        return [(x, y) for x in xrange(initrow, maxrow + 1) for y in xrange(initcolumn, maxcolumn + 1) if (x, y) != self.location]

        #     WN  N  NE
        #     W       E
        #     WS  S  SE


class GridCell():

    def __init__(self, rownumber, columnnumber, diffusionspeed=0.5, diffusionsize=0.5):
        self.diffusionspeed = diffusionspeed
        self.diffusionsize = diffusionsize
        self.maxrow = rownumber - 1
        self.maxcolumn = columnnumber - 1
        self.rownumber = rownumber
        self.columnnumber = columnnumber
        self.gridcell = collections.OrderedDict()
        for row in xrange(self.rownumber):
            rowdict = collections.OrderedDict()
            for column in xrange(self.columnnumber):
                rowdict[column] = Cell(
                    row, column, self.maxrow, self.maxcolumn)
            self.gridcell[row] = rowdict

    def setconcentration(self, lc, printout=True):
        if isinstance(lc, list):
            for l, c in lc:
                self._setconcentration(l, c, printout=False)
        else:
            print 'Unknown loaction,ingore!!!'

        if printout:
            self.cellprint()
        self.detect_equilibrium_all()

    def _setconcentration(self, location, concentration, printout=True):
        row = location[0]
        column = location[1]
        # print self.gridcell[row][column]
        self.gridcell[row][column].concentration = concentration
        if printout:
            self.cellprint()
        self.detect_equilibrium_all()

    def detect_equilibrium_all(self):
        for k, v in self.gridcell.items():
            for k2, v2 in v.items():
                self._detect_equilibrium(v2)

    def _detect_equilibrium(self, cell):
        neighbours = cell.getneighbour()
        for l in neighbours:  # location:(1,2)
            if self.gridcell[l[0]][l[1]].concentration != cell.concentration:
                self.gridcell[l[0]][l[1]].diffusion = cell.diffusion = True

    def diffusionstatuslist(self):
        c = []

        for k, v in self.gridcell.items():
            for k2, v2 in v.items():
                if v2.diffusion:
                    c.append((k, k2))
        return set(c)

    def concentration(self, locationlist):
        return [self.gridcell[location[0]][location[1]
                                           ].concentration for location in locationlist]

    def cellprint(self):
        c = [[v2.concentration for k2, v2 in v.items()]
             for k, v in self.gridcell.items()]

        pprint.pprint(c, indent=5, width=10 * self.columnnumber, depth=2)


if __name__ == '__main__':
    row = 5
    column = 4
    gc = GridCell(row, column)
    gc.setconcentration([((1, 2), 3), ((2, 2), 2)])

    print gc.concentration(gc.diffusionstatuslist())

    # print gc.gridcell[0][2].getneighbour()
