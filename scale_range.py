#!/usr/bin/env python

import math
import sys
import targets

class RangeScale(object):
    def __init__(self, paper_size=10.5, indoor_range=180, target_range=15):
        self.paper_size = paper_size
        self.indoor_range = indoor_range
        self.target_range = target_range

        self.gen_target(targets.Metric)
        self.gen_target(targets.Classic)
        self.gen_target(targets.SmallBore50Ft)

    def gen_target(self, target_obj):
        # Find the paper size and range for a given target size and range...
        obj = target_obj(str(self.target_range))

        # Size in inches
        target_size = obj.height/25.4

        # Figure out the visual angle
        visual_angle = 2*math.atan(target_size/(2*(self.target_range*36.0)))

        # Fit the target to the paper
        paper_target_size = math.tan(visual_angle) * self.indoor_range

        if paper_target_size > self.paper_size:
            indoor_distance = self.paper_size / math.tan(visual_angle)
            obj.drawTarget(self.paper_size)
            obj.setText('%.2f" target at %.2f" simulates %.2fyds' %
                        (self.paper_size, indoor_distance, self.target_range))
            obj.showPage()
        else:
            obj.drawTarget(paper_target_size)
            obj.setText('%.2f" target at %.2f" simulates %.2fyds' %
                        (paper_target_size, self.indoor_range, self.target_range))
            obj.showPage()


if __name__ == "__main__":
    if (len(sys.argv) > 1):
        target_range = float(sys.argv[1])
        range_len = float(sys.argv[2])
    else:
        print ("Enter virtual range in yards")
        print ("Enter actual range in inches")
        sys.exit()

    shoot = RangeScale(target_range=target_range,
                       indoor_range=range_len)
