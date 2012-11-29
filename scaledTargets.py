#!/usr/bin/env python

import sys
try:
    import wx
    import wx.lib.wxcairo
except:
    print "failed on imports"
    sys.exit()

VERSION = 1.0


class ScaleTargets(wx.Frame):

    def __init__(self):
        super(ScaleTargets, self).__init__(None)

        self.metricUnits = True
        self.rangePos = 5
        self.targetPos = 25

        self.initUI()

    def initUI(self):
        self.menubar = wx.MenuBar()
        self.fileMenuSetup()
        self.helpMenuSetup()
        self.SetMenuBar(self.menubar)

        self.panel = wx.Panel(self)
        self.GUISetup()

        self.SetSize((600, 300))
        self.SetTitle('Scale Targets')
        self.Centre()
        self.Show()

    def GUISetup(self):
        # main sizer
        vbox = wx.BoxSizer(wx.VERTICAL)

        # horizontal box for main stuff
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox, 1, flag=wx.EXPAND | wx.ALL)

        # The vbox for our controls
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        self.meterCheck = wx.RadioButton(self.panel, -1, 'Meters', (10,10), style=wx.RB_GROUP)
        self.yardCheck = wx.RadioButton(self.panel, -1, 'Yards', (10,30))
        self.Bind(wx.EVT_RADIOBUTTON, self.SetUnits, id=self.meterCheck.GetId())
        self.Bind(wx.EVT_RADIOBUTTON, self.SetUnits, id=self.yardCheck.GetId())
        hboxRadio = wx.BoxSizer(wx.HORIZONTAL)
        hboxRadio.Add(self.meterCheck)
        hboxRadio.Add(self.yardCheck)
        vbox1.Add(hboxRadio)
        self.rangeSlideText = wx.StaticText(self.panel, -1, 'Range to target board in meters.', style=wx.ALIGN_CENTRE)
        vbox1.Add(self.rangeSlideText,0)
        self.rangeSlide = wx.Slider(self.panel, -1, self.rangePos, 1, 35, (-1,-1), (250,-1), wx.SL_AUTOTICKS|wx.SL_HORIZONTAL|wx.SL_LABELS)
        self.Bind(wx.EVT_SLIDER, self.OnSlide)
        vbox1.Add(self.rangeSlide,0, wx.ALIGN_LEFT)
        self.targetSlideText = wx.StaticText(self.panel, -1, 'Simulated range to target in meters.', style=wx.ALIGN_CENTRE)
        vbox1.Add(self.targetSlideText,0)
        self.targetSlide = wx.Slider(self.panel, -1, self.targetPos, 5, 200, (-1,-1), (250,-1), wx.SL_AUTOTICKS|wx.SL_HORIZONTAL|wx.SL_LABELS)
        vbox1.Add(self.targetSlide,0, wx.ALIGN_LEFT)

        hbox.Add(vbox1,0, flag = wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)

        # The canvas to draw our example target on will be in this vbox
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        self.canvas = CairoPane(self.panel)
        vbox2.Add(self.canvas, 3, flag = wx.EXPAND)

        hbox.Add(vbox2, 1, flag = wx.EXPAND |wx.ALIGN_LEFT| wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)

        # hbox for print, save and exit buttons
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(self.panel, label='Print', size=(70,30))
        self.Bind(wx.EVT_BUTTON, self.OnPrint, id=btn1.GetId())
        hbox1.Add(btn1)
        btn2 = wx.Button(self.panel, label='Save', size=(70,30))
        self.Bind(wx.EVT_BUTTON, self.OnSave, id=btn2.GetId())
        hbox1.Add(btn2, flag=wx.LEFT|wx.BOTTOM,border=5)
        btn3 = wx.Button(self.panel, label='Quit', size=(70,30))
        self.Bind(wx.EVT_BUTTON, self.OnQuit, id=btn3.GetId())
        hbox1.Add(btn3, flag=wx.LEFT|wx.BOTTOM,border=5)
        vbox1.Add(hbox1, 0, flag=wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.RIGHT|wx.TOP,border=10)

        self.panel.SetSizer(vbox)

    def fileMenuSetup(self):
        fileMenu = wx.Menu()
        pitem = fileMenu.Append(wx.ID_PRINT, '&Print...\tCtrl-P', 'Print data')
        self.Bind(wx.EVT_MENU, self.OnPrint, pitem)
        fileMenu.AppendSeparator()
        sitem = fileMenu.Append(wx.ID_SAVE, '&Save\tCtrl-S', 'Save the target')
        self.Bind(wx.EVT_MENU, self.OnSave, sitem)
        fileMenu.AppendSeparator()
        fitem = fileMenu.Append(wx.ID_EXIT, '&Quit\tCtrl-Q', 'Quit application')
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)

        self.menubar.Append(fileMenu, '&File')

    def helpMenuSetup(self):
        helpMenu = wx.Menu()
        aitem = helpMenu.Append(wx.ID_ABOUT, '&About', 'What is this application?')
        self.Bind (wx.EVT_MENU, self.OnAbout, aitem)

        self.menubar.Append(helpMenu, '&Help')

    def OnSlide(self, e):
        self.rangePos = self.rangeSlide.GetValue()
        self.targetPos = self.targetSlide.GetValue()

    def SetUnits(self, e):
        self.metricUnits = self.meterCheck.GetValue()
        if self.metricUnits == False:
            self.rangeSlideText.SetLabel('Range to target board in yards.')
            self.targetSlideText.SetLabel('Simulated range to target in yards.')
        else:
            self.rangeSlideText.SetLabel("Range to target board in meters.")
            self.targetSlideText.SetLabel('Simulated range to target in meters.')

    def OnAbout(self, e):
        description="""Scale Targets is a program to generate IPSC and other targets for training on shorter ranges.
The targets will appear as if they are at a specific further distance.
"""

        licence="""Scale Targets is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public Licence
as published by the Free Software Foundation; either version
2 of the License, or (at your option) any later version.

Scale Targets is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY of FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details. You should have
received a copy of the GNU General Public License along with
Scale Targets; if not, write to
the Free Software Foundation, Inc., 59 Temple Place, Suite 330,
Boston, MA 02111-1307 USA
"""

        info = wx.AboutDialogInfo()
        info.SetName('Scale Targets')
        info.SetVersion(str(VERSION))
        info.SetDescription(description)
        info.SetCopyright('(C) 2012 Kyle Eberhart')
        info.SetLicence(licence)
        info.AddDeveloper('Kyle Eberhart')
        info.AddDocWriter('Kyle Eberhart')
        info.AddArtist('Kyle Eberhart')

        wx.AboutBox(info)

    def OnPrint(self, e):
        self.rangeValue = self.rangeSlide.GetValue()
        self.targetValue = self.targetSlide.GetValue()

    def OnSave(self, e):
        self.rangeValue = self.rangeSlide.GetValue()
        self.targetValue = self.targetSlide.GetValue()

    def OnQuit(self, e):
        self.Close()

class CairoPane(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SIMPLE)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.text = 'Big Fat Hat'

    def OnPaint(self, e):
        # set up the panel using wx device contexts
        dc = wx.PaintDC(self)
        width, height = self.GetClientSize()
        cr = wx.lib.wxcairo.ContextFromDC(dc)

        # do the cairo bit here
        size = min(width, height)
        cr.scale(size,size)
        cr.set_source_rgb(1,1,1)
        cr.rectangle(0,0,width,height)
        cr.fill()

        cr.set_source_rgb(0,0,0)
        cr.set_line_width(0.04)
        cr.select_font_face("Sans")
        cr.set_font_size(0.07)
        cr.move_to(0.5,0.5)
        cr.show_text(self.text)
        cr.stroke()

def main():

    ex = wx.App()
    ScaleTargets()
    ex.MainLoop()

if __name__ == "__main__":
    main()
