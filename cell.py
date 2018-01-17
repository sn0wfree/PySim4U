# coding: utf-8

import collections
import gc
import pprint
import time

import numpy as np


class Cell():
    # Basic Cell class, contain the base information including:

    # location,
    # concentration,
    # status:
    #       diffusion and change

    def __init__(self, row, column, maxrow, maxcolumn, concentration=0):
        self.concentration = concentration
        self.location = (row, column)

        self.diffusion = False
        self.change = 0  # depredated parameter
        self.status = 'Dead'  # alive;equilibrium
        self.maxrow = maxrow
        self.maxcolumn = maxcolumn
        self.__concentrationcheck()

    def __run__(self):
        # depredated function
        self.concentration = self.concentration + self.change
        self.change = 0

    def __concentrationcheck(self):
        # self status check ,useless
        if self.concentration < 0:
            self.concentration = 0
            self.status = 'Dead'

        elif self.concentration != 0 and self.status == 'Dead':
            self.status = 'Alive'
        elif self.concentration > 0:
            self.status = 'Alive'

            # concentration status changed

    def getneighbour(self):
        # this function is for obtain the neighbors around this cell
        # return the list of the location of neighbors

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
    # this is gridcell function :main function to hold all cells in one dict

    def __init__(self, rownumber, columnnumber, diffusionspeed=1, diffusionsize=0.5):
        # initial gridcell
        #
        self.diffusionspeed = diffusionspeed  # diffusion speed; depredated parameters
        self.diffusionsize = diffusionsize  # diffusion size; depredated parameters
        self.rownumber = rownumber  # define the number of row
        self.columnnumber = columnnumber  # define the number of column

        self.maxrow = self.rownumber - 1
        # define the max of rownumber in python math system:the first number in
        # python is zero

        self.maxcolumn = self.columnnumber - 1
        # define the max of columnnumber in python math system:the first number
        # in python is zero

        # initial contain for collecting cells
        self.gridcell = collections.OrderedDict()
        # now mapping cell and put them into gridcell
        for row in xrange(self.rownumber):
            rowdict = collections.OrderedDict()
            for column in xrange(self.columnnumber):
                rowdict[column] = Cell(
                    row, column, self.maxrow, self.maxcolumn)
            self.gridcell[row] = rowdict

    # setup function for cell concentration
    def setconcentration(self, lc, printout=True):
        # this function need input with list type
        if isinstance(lc, list):
            for l, c in lc:
                self._setconcentration(l, c, printout=False)
        else:
            print 'Unknown loaction,ingore!!!'

        if printout:
            self.cellprint()
        self.detect_equilibrium_all()  # equilibrium check function for all

    def _setconcentration(self, location, concentration, printout=True):
        # setup subfunction for cell concentration
        # need input location;concentration
        row = location[0]
        column = location[1]

        self.gridcell[row][column].concentration = concentration
        if printout:
            self.cellprint()

        # equilibrium check function for single cell
        self._detect_equilibrium(self.gridcell[row][column])

    def detect_equilibrium_all(self):  # equilibrium check function for all
        # mapping all
        for k, v in self.gridcell.items():
            for k2, v2 in v.items():
                self._detect_equilibrium(v2)

    def _detect_equilibrium(self, cell):
        # equilibrium check function for single function
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
        # this function is for collecting diffusion status;return set
        c = []

        for k, v in self.gridcell.items():
            for k2, v2 in v.items():
                self._detect_equilibrium(v2)
                if v2.diffusion:
                    c.append((k, k2))
        return set(c)

    def _go_(self):  # diffusion function.

        for k, v in self.gridcell.items():
            for k2, v2 in v.items():
                self.__go__(v2)
        # depredated function should be used with cell.__run__ function
        """for k, v in self.gridcell.items():
            for k2, v2 in v.items():
                v2.__run__()"""

    def __go__(self, cell):  # depredated function. should be used with cell.__run__ function

        if cell.diffusion:
            neighbours = cell.getneighbour()  # getneighbou
            # for n in neighbours:
            # this part is to collection diffusionspeed but useless here
            """s = sum(self.concentration(neighbours)) + cell.concentration
            m = s / (1 + len(neighbours))
            if m >= cell.concentration:
                splitenumber = 0 * self.diffusionspeed
            else:
                splitenumber = (cell.concentration - m) * self.diffusionspeed"""

            #sharelist = []
            #totalshare = 0
            # get number of neighbours and add 1 for itself
            lenn = len(neighbours) + 1
            # mapping neighbours:
            for neighbour in neighbours:
                neighbourcell = self.gridcell[neighbour[0]][
                    neighbour[1]]  # get neighbours cell
                if neighbourcell.concentration > cell.concentration:  # compare two cells
                    # get the different between two cell and spilt it into lenn
                    # shares; get int number
                    tempint = int(neighbourcell.concentration -
                                  cell.concentration) / lenn
                    if tempint >= 1:
                        pass

                    else:
                        tempint = 1
                    neighbourcell.concentration -= tempint  # change
                    cell.concentration += tempint

                elif neighbourcell.concentration < cell.concentration:
                    tempint = int(
                        cell.concentration - neighbourcell.concentration) / lenn
                    if tempint >= 1:
                        pass
                    else:
                        tempint = 1
                    neighbourcell.concentration += tempint
                    cell.concentration -= tempint

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

    def concentration(self, locationlist):  # obtain concentrationlist base on loaction
        return [self.gridcell[location[0]][location[1]
                                           ].concentration for location in locationlist]

    def status(self):  # obtain all concentration
        c = [[v2.concentration for k2, v2 in v.items()]
             for k, v in self.gridcell.items()]
        return c

    def cellprint(self):  # print out
        c = self.status()
        pprint.pprint(c, indent=1, width=10 * self.columnnumber, depth=2)


if __name__ == '__main__':
    gc.enable()
    row = 10
    column = 10
    diffusionspeed = 1
    initvalue = row * column + 1
    initlocation = (0, 0)
    gcs = GridCell(row, column, diffusionspeed=diffusionspeed)
    gcs.setconcentration([(initlocation, initvalue)])
    last = []
    lastcount = 0
    c = 0
    # print gc.concentration(gc.diffusionstatuslist())
    while gcs.diffusionstatuslist() != set([]):  # while loop
        # print gcs.diffusionstatuslist()
        gcs._go_()
        if last == gcs.status():
            lastcount += 1
            if lastcount > 5:
                break
        gcs.cellprint()
        last = gcs.status()
        gc.collect()

        time.sleep(.5)

    # print gc.gridcell[0][2].getneighbour()
