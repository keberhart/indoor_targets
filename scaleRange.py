#!/usr/bin/env python

import math
import sys
import targets

class rangeScale(object):
    def __init__(self, paperSize=10.5, indoorRange=180, targetRange=15):
        self.paperSize = paperSize
        self.indoorRange = indoorRange
        self.targetRange = targetRange

        self.genTarget(targets.Metric)
        self.genTarget(targets.Classic)

    def genTarget(self,targetObj):
        # Find the paper size and range for a given target size and range...
        obj = targetObj(str(self.targetRange))

        # Size in inches
        targetSize = obj.height/25.4

        # Figure out the visual angle
        visualAngle = 2*math.atan(targetSize/(2*(self.targetRange*36.0)))

        # Fit the target to the paper
        paperTargetSize = math.tan(visualAngle) * self.indoorRange

        if paperTargetSize > self.paperSize:
            indoorDistance = self.paperSize / math.tan(visualAngle)
            obj.drawTarget(self.paperSize)
            obj.setText('%.2f" target at %.2f" simulates %.2fyds' % (self.paperSize, indoorDistance, self.targetRange))
            obj.showPage()
        else:
            obj.drawTarget(paperTargetSize)
            obj.setText('%.2f" target at %.2f" simulates %.2fyds' % (paperTargetSize, self.indoorRange, self.targetRange))
            obj.showPage()


if __name__ == "__main__":
    if (len(sys.argv) > 1):
        targetRange = float(sys.argv[1])
    else:
        print ("Enter virtual range in yards")
        sys.exit()

    shoot = rangeScale(targetRange=targetRange)
