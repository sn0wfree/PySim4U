# coding: utf-8

import collections
import gc
import pprint
import time

import numpy as np


class cel():

    def __init__(self, location, diffusion, concentration):
        inits = collections.namedtuple(
            'Cell', ['location', 'diffusion', 'concentration'])
        self = inits(location, diffusion, concentration)


class Cell():
    # basic cell
    # provide location,concentration,status

    def __init__(self, row, column, maxrow, maxcolumn, concentration=0):
        self.concentration = concentration
        self.location = (row, column)
        self.maxrow = maxrow
        self.maxcolumn = maxcolumn
        self.diffusion = False
        self.change = 0
        # self.status = 'Dead'  # alive;equilibrium
        self.__concentrationcheck()

    def __run__(self):
        self.concentration = self.concentration + self.change
        self.change = 0

    def __concentrationcheck(self):
        if self.concentration < 0:
            self.concentration = 0
            self.status = 'Dead'

        elif self.concentration != 0 and self.status == 'Dead':
            self.status = 'Alive'
        elif self.concentration > 0:
            self.status = 'Alive'

            # concentration status changed

    def getneighbour(self):
        # obtain the neighbour
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

    def __init__(self, rownumber, columnnumber, diffusionspeed=1, diffusionsize=0.5):
        self.diffusionspeed = diffusionspeed
        self.diffusionsize = diffusionsize
        self.rownumber = rownumber
        self.columnnumber = columnnumber
        self.maxrow = self.rownumber - 1
        self.maxcolumn = self.columnnumber - 1

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
        self._detect_equilibrium(self.gridcell[row][column])

    def detect_equilibrium_all(self):
        for k, v in self.gridcell.items():
            for k2, v2 in v.items():
                self._detect_equilibrium(v2)

    def _detect_equilibrium(self, cell):
        neighbours = cell.getneighbour()
        cellstatus = 0
        for l in neighbours:  # location:(1,2)
            if self.gridcell[l[0]][l[1]].concentration < cell.concentration:
                self.gridcell[l[0]][l[1]].diffusion = cell.diffusion = True
            else:
                cellstatus += 1
        if cellstatus == len(neighbours):
            cell.diffusion = False

    def diffusionstatuslist(self):
        c = []

        for k, v in self.gridcell.items():
            for k2, v2 in v.items():
                self._detect_equilibrium(v2)
                if v2.diffusion:
                    c.append((k, k2))
        return set(c)

    def _go_(self):
        for k, v in self.gridcell.items():
            for k2, v2 in v.items():
                self.__go__(v2)
        for k, v in self.gridcell.items():
            for k2, v2 in v.items():
                v2.__run__()

    def __go__(self, cell):

        if cell.diffusion:
            neighbours = cell.getneighbour()
            # for n in neighbours:
            s = sum(self.concentration(neighbours)) + cell.concentration
            m = s / (1 + len(neighbours))
            if m >= cell.concentration:
                splitenumber = 0 * self.diffusionspeed
            else:
                splitenumber = (cell.concentration - m) * self.diffusionspeed

            sharelist = []
            totalshare = 0
            lenn = len(neighbours)
            for neighbour in neighbours:
                neighbourcell = self.gridcell[neighbour[0]][neighbour[1]]
                if neighbourcell.concentration > cell.concentration:

                    neighbourcell.concentration -= int(
                        neighbourcell.concentration - cell.concentration) / lenn
                    cell.concentration += int(neighbourcell.concentration -
                                              cell.concentration) / lenn
                elif neighbourcell.concentration < cell.concentration:
                    neighbourcell.concentration += int(
                        cell.concentration - neighbourcell.concentration) / lenn
                    cell.concentration -= int(cell.concentration -
                                              neighbourcell.concentration) / lenn

            """
                else:
                    share = cell.concentration - neighbourcell.concentration

                    change = 1  # float(share) / len(neighbours)
                    if cell.change - change <= cell.concentration:

                        cell.change = cell.change - change

                        cc = neighbour
                        self.gridcell[cc[0]][cc[1]].change = self.gridcell[
                            cc[0]][cc[1]].change + change
                    else:
                        pass"""

# single cell

    def concentration(self, locationlist):
        return [self.gridcell[location[0]][location[1]
                                           ].concentration for location in locationlist]

    def status(self):
        c = [[v2.concentration for k2, v2 in v.items()]
             for k, v in self.gridcell.items()]
        return c

    def cellprint(self):
        c = self.status()
        pprint.pprint(c, indent=1, width=10 * self.columnnumber, depth=2)


if __name__ == '__main__':
    gc.enable()
    row = 5
    column = 5
    diffusionspeed = 1
    gcs = GridCell(row, column, diffusionspeed=diffusionspeed)
    gcs.setconcentration([((0, 0), 2601)])
    last = []
    lastcount = 0

    # print gc.concentration(gc.diffusionstatuslist())
    while gcs.diffusionstatuslist() != set([]):
        # print gcs.diffusionstatuslist()
        gcs._go_()
        if last == gcs.status():
            lastcount += 1
            if lastcount > 5:
                break
        gcs.cellprint()
        last = gcs.status()
        gc.collect()

        time.sleep(.05)

    # print gc.gridcell[0][2].getneighbour()
