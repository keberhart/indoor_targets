#!/usr/bin/env python

import cairo

WIDTH, HEIGHT = 216, 279
POINT_TO_MM = 72/25.4
PAPER_WIDTH = WIDTH*POINT_TO_MM
PAPER_HEIGHT = HEIGHT*POINT_TO_MM
PRINT_MARGIN = 10
PRINT_WIDTH = PAPER_WIDTH-(PRINT_MARGIN*2)
PRINT_HEIGHT = PAPER_HEIGHT-(PRINT_MARGIN*2)

class Metric(object):

    def __init__(self, targetRange):
        filename = "%s_metric.pdf" % targetRange
        self.surface = cairo.PDFSurface(filename,
                PAPER_WIDTH, 
                PAPER_HEIGHT)
        self.ctx = cairo.Context(self.surface)

        self.ctx.scale(POINT_TO_MM,POINT_TO_MM)
        self.ctx.translate(PRINT_MARGIN,PRINT_MARGIN)

        self.width = 460.0
        self.height = 760.0

    def drawTarget(self, scale):
        self.ctx.save()
        self.myScale = scale
        # rescale for different range targets
        scale2 = ((scale*25.4)/self.height)
        self.ctx.scale(scale2,scale2)
        deviceWidth, deviceHeight = self.ctx.device_to_user(PRINT_WIDTH,PRINT_HEIGHT)
        if deviceHeight/4 > self.height:
            # if possible print more than one target
            chunkHeight = deviceHeight/8
            chunkWidth = deviceWidth/8
            workingHeight = chunkHeight
            while workingHeight <= deviceHeight:
                workingWidth = chunkWidth
                while workingWidth <= deviceWidth:
                    leftEdge = workingWidth - (self.width/2)
                    topEdge = workingHeight - (self.height/2)
                    self.ctx.save()
                    self.ctx.translate(leftEdge,topEdge)
                    self._plotTarget()
                    self.ctx.restore()
                    workingWidth += chunkWidth*2
                workingHeight += chunkHeight*2
            leftEdge = deviceWidth
        elif deviceHeight/3 > self.height:
            # if possible print more than one target
            chunkHeight = deviceHeight/6
            chunkWidth = deviceWidth/6
            workingHeight = chunkHeight
            while workingHeight <= deviceHeight:
                workingWidth = chunkWidth
                while workingWidth <= deviceWidth:
                    leftEdge = workingWidth - (self.width/2)
                    topEdge = workingHeight - (self.height/2)
                    self.ctx.save()
                    self.ctx.translate(leftEdge,topEdge)
                    self._plotTarget()
                    self.ctx.restore()
                    workingWidth += chunkWidth*2
                workingHeight += chunkHeight*2
            leftEdge = deviceWidth
        elif deviceHeight/2 > self.height:
            # if possible print more than one target
            chunkHeight = deviceHeight/4
            chunkWidth = deviceWidth/4
            workingHeight = chunkHeight
            while workingHeight <= deviceHeight:
                workingWidth = chunkWidth
                while workingWidth <= deviceWidth:
                    leftEdge = workingWidth - (self.width/2)
                    topEdge = workingHeight - (self.height/2)
                    self.ctx.save()
                    self.ctx.translate(leftEdge,topEdge)
                    self._plotTarget()
                    self.ctx.restore()
                    workingWidth += chunkWidth*2
                workingHeight += chunkHeight*2
            leftEdge = deviceWidth
        else:
            # center the print if the scale is to big
            leftEdge = (deviceWidth/2)-(self.width/2)
            topEdge = (deviceHeight/2)-(self.height/2)
            self.ctx.translate(leftEdge,topEdge)
            self._plotTarget()

        self.ctx.restore()

    def _plotTarget(self):

        borderWidth = 0.7
        lineWidth = 0.3
        # Metric Target
        # 0.5cm non-scoring border
        self.ctx.set_line_width(borderWidth)
        self.ctx.move_to(0,205)
        self.ctx.line_to(55,150)
        self.ctx.line_to(150,150)
        self.ctx.line_to(150,0)
        self.ctx.line_to(310,0)
        self.ctx.line_to(310,150)
        self.ctx.line_to(405,150)
        self.ctx.line_to(460,205)
        self.ctx.line_to(460,605)
        self.ctx.line_to(383,760)
        self.ctx.line_to(77,760)
        self.ctx.line_to(0,605)
        self.ctx.line_to(0,205)
        self.ctx.set_source_rgb(0,0,0)
        self.ctx.stroke()

        # D zone
        self.ctx.set_line_width(lineWidth)
        self.ctx.move_to(55,155)
        self.ctx.line_to(405,155)
        self.ctx.line_to(455,205)
        self.ctx.line_to(455,605)
        self.ctx.line_to(380,755)
        self.ctx.line_to(80,755)
        self.ctx.line_to(5,605)
        self.ctx.line_to(5,205)
        self.ctx.line_to(55,155)
        self.ctx.set_source_rgb(0,0,0)
        self.ctx.stroke()

        # C zone
        self.ctx.set_line_width(lineWidth)
        self.ctx.move_to(305,155)
        self.ctx.line_to(380,205)
        self.ctx.line_to(380,485)
        self.ctx.line_to(330,605)
        self.ctx.line_to(130,605)
        self.ctx.line_to(80,485)
        self.ctx.line_to(80,205)
        self.ctx.line_to(155,155)
        self.ctx.set_source_rgb(0,0,0)
        self.ctx.stroke()

        # B zone
        self.ctx.set_line_width(lineWidth)
        self.ctx.move_to(155,155)
        self.ctx.line_to(155,5)
        self.ctx.line_to(305,5)
        self.ctx.line_to(305,155)
        self.ctx.set_source_rgb(0,0,0)
        self.ctx.stroke()

        # A zones
        from math import pi
        radius = 10
        top = 205
        left = 155
        bottom = top + 280
        right = left + 150
        # top left corner
        self.ctx.arc(left+radius, top+radius, radius, 2*(pi/2), 3*(pi/2))
        # top right corner
        self.ctx.arc(right-radius, top+radius, radius, 3*(pi/2), 4*(pi/2))
        # bottom right corner
        self.ctx.arc(right-radius, bottom-radius, radius, 0*(pi/2), 1*(pi/2))
        # bottom left corner
        self.ctx.arc(left+radius,  bottom-radius, radius, 1*(pi/2), 2*(pi/2))
        self.ctx.close_path()
        self.ctx.set_source_rgb(0,0,0)
        self.ctx.stroke()

        top = 30
        left = 180
        bottom = top + 50
        right = left + 100
        # top left corner
        self.ctx.arc(left+radius, top+radius, radius, 2*(pi/2), 3*(pi/2))
        # top right corner
        self.ctx.arc(right-radius, top+radius, radius, 3*(pi/2), 4*(pi/2))
        # bottom right corner
        self.ctx.arc(right-radius, bottom-radius, radius, 0*(pi/2), 1*(pi/2))
        # bottom left corner
        self.ctx.arc(left+radius,  bottom-radius, radius, 1*(pi/2), 2*(pi/2))
        self.ctx.close_path()
        self.ctx.set_source_rgb(0,0,0)
        self.ctx.stroke()


    def setText(self, text):
        self.ctx.save()
        deviceWidth, deviceHeight = self.ctx.device_to_user(PRINT_WIDTH,PRINT_HEIGHT)
        self.ctx.translate(deviceWidth/2,deviceHeight)
        self.ctx.select_font_face('Sans')
        self.ctx.set_font_size(5)
        fontData =  self.ctx.text_extents(text)
        self.ctx.move_to(-(fontData[2]/2),0)
        self.ctx.set_source_rgb(0,0,0)
        self.ctx.show_text(text)
        self.ctx.restore()

    def showPage(self):
        self.ctx.show_page()

    def writePNG(self):
        self.surface.write_to_png('output.png')


class Classic(object):

    def __init__(self, targetRange):
        filename = "%s_classic.pdf" % targetRange
        self.surface = cairo.PDFSurface(filename,
                PAPER_WIDTH,
                PAPER_HEIGHT)
        self.ctx = cairo.Context(self.surface)

        self.ctx.scale(POINT_TO_MM,POINT_TO_MM)
        self.ctx.translate(PRINT_MARGIN,PRINT_MARGIN)

        self.width = 460.0
        self.height = 580.0

    def drawTarget(self, scale):
        self.ctx.save()
        self.myScale = scale
        # rescale for different range targets
        scale2 = ((scale*25.4)/self.height)
        self.ctx.scale(scale2,scale2)
        deviceWidth, deviceHeight = self.ctx.device_to_user(PRINT_WIDTH,PRINT_HEIGHT)
        if deviceHeight/4 > self.height:
            # if possible print more than one target
            chunkHeight = deviceHeight/8
            chunkWidth = deviceWidth/8
            workingHeight = chunkHeight
            while workingHeight <= deviceHeight:
                workingWidth = chunkWidth
                while workingWidth <= deviceWidth:
                    leftEdge = workingWidth - (self.width/2)
                    topEdge = workingHeight - (self.height/2)
                    self.ctx.save()
                    self.ctx.translate(leftEdge,topEdge)
                    self._plotTarget()
                    self.ctx.restore()
                    workingWidth += chunkWidth*2
                workingHeight += chunkHeight*2
            leftEdge = deviceWidth
        elif deviceHeight/3 > self.height:
            # if possible print more than one target
            chunkHeight = deviceHeight/6
            chunkWidth = deviceWidth/6
            workingHeight = chunkHeight
            while workingHeight <= deviceHeight:
                workingWidth = chunkWidth
                while workingWidth <= deviceWidth:
                    leftEdge = workingWidth - (self.width/2)
                    topEdge = workingHeight - (self.height/2)
                    self.ctx.save()
                    self.ctx.translate(leftEdge,topEdge)
                    self._plotTarget()
                    self.ctx.restore()
                    workingWidth += chunkWidth*2
                workingHeight += chunkHeight*2
            leftEdge = deviceWidth
        elif deviceHeight/2 > self.height:
            print '/2 >'
            # if possible print more than one target
            chunkHeight = deviceHeight/4
            chunkWidth = deviceWidth/4
            workingHeight = chunkHeight
            while workingHeight <= deviceHeight:
                workingWidth = chunkWidth
                while workingWidth <= deviceWidth:
                    leftEdge = workingWidth - (self.width/2)
                    topEdge = workingHeight - (self.height/2)
                    self.ctx.save()
                    self.ctx.translate(leftEdge,topEdge)
                    self._plotTarget()
                    self.ctx.restore()
                    workingWidth += chunkWidth*2
                workingHeight += chunkHeight*2
            leftEdge = deviceWidth
        else:
            print 'else'
            # center the print if the scale is to big
            leftEdge = (deviceWidth/2)-(self.width/2)
            topEdge = (deviceHeight/2)-(self.height/2)
            self.ctx.translate(leftEdge,topEdge)
            self._plotTarget()

        self.ctx.restore()

    def _plotTarget(self):

        borderWidth = 0.7
        lineWidth = 0.3
        # Classic Target
        # 0.5cm non-scoring border
        self.ctx.set_line_width(borderWidth)
        self.ctx.move_to(155,0)
        self.ctx.line_to(305,0)
        self.ctx.line_to(460,195)
        self.ctx.line_to(460,385)
        self.ctx.line_to(305,580)
        self.ctx.line_to(155,580)
        self.ctx.line_to(0,385)
        self.ctx.line_to(0,195)
        self.ctx.line_to(155,0)
        self.ctx.stroke()

        # D zone
        self.ctx.set_line_width(lineWidth)
        self.ctx.move_to(155,5)
        self.ctx.line_to(305,5)
        self.ctx.line_to(455,195)
        self.ctx.line_to(455,385)
        self.ctx.line_to(305,575)
        self.ctx.line_to(155,575)
        self.ctx.line_to(5,385)
        self.ctx.line_to(5,195)
        self.ctx.line_to(155,5)
        self.ctx.stroke()

        # C zone
        self.ctx.set_line_width(lineWidth)
        self.ctx.move_to(155,5)
        self.ctx.line_to(80,195)
        self.ctx.line_to(80,340)
        self.ctx.line_to(180,455)
        self.ctx.line_to(280,455)
        self.ctx.line_to(380,340)
        self.ctx.line_to(380,195)
        self.ctx.line_to(305,5)
        self.ctx.stroke()

        # A zone
        self.ctx.set_line_width(lineWidth)
        self.ctx.move_to(205,30)
        self.ctx.line_to(255,30)
        self.ctx.line_to(305,195)
        self.ctx.line_to(305,280)
        self.ctx.line_to(255,355)
        self.ctx.line_to(205,355)
        self.ctx.line_to(155,280)
        self.ctx.line_to(155,195)
        self.ctx.line_to(205,30)
        self.ctx.stroke()

    def setText(self, text):
        self.ctx.save()
        deviceWidth, deviceHeight = self.ctx.device_to_user(PRINT_WIDTH,PRINT_HEIGHT)
        self.ctx.translate(deviceWidth/2,deviceHeight)
        self.ctx.select_font_face('Sans')
        self.ctx.set_font_size(5)
        fontData =  self.ctx.text_extents(text)
        self.ctx.move_to(-(fontData[2]/2),0)
        self.ctx.set_source_rgb(0,0,0)
        self.ctx.show_text(text)
        self.ctx.restore()

    def showPage(self):
        self.ctx.show_page()

    def writePNG(self):
        self.surface.write_to_png('output.png')



if __name__ == "__main__":
    hat = Metric()
    hat.drawTarget(7)
    hat.setText('Whatever')
    hat.showPage()
