# -*- coding: utf-8 -*-
# Copyright (C) 2011 Denis Kobozev
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import wx


class ViewButtons(wx.FlexGridSizer):
    def __init__(self, parent, scene):
        super(ViewButtons, self).__init__(rows=3, cols=3, vgap=3, hgap=3)

        self.scene = scene
        
        # Set minimum size for all buttons immediately upon creation
        min_button_size = (65, 32)

        self.btn_front = wx.Button(parent, label="Front", size=min_button_size)
        self.btn_front.SetMinSize(min_button_size)
        self.btn_front.SetInitialSize(min_button_size)
        
        self.btn_back = wx.Button(parent, label="Back", size=min_button_size)
        self.btn_back.SetMinSize(min_button_size)
        self.btn_back.SetInitialSize(min_button_size)
        
        self.btn_left = wx.Button(parent, label="Left", size=min_button_size)
        self.btn_left.SetMinSize(min_button_size)
        self.btn_left.SetInitialSize(min_button_size)
        
        self.btn_right = wx.Button(parent, label="Right", size=min_button_size)
        self.btn_right.SetMinSize(min_button_size)
        self.btn_right.SetInitialSize(min_button_size)

        self.btn_top = wx.Button(parent, label="Top", size=min_button_size)
        self.btn_top.SetMinSize(min_button_size)
        self.btn_top.SetInitialSize(min_button_size)
        
        self.btn_bottom = wx.Button(parent, label="Bottom", size=min_button_size)
        self.btn_bottom.SetMinSize(min_button_size)
        self.btn_bottom.SetInitialSize(min_button_size)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.btn_top, 0, wx.FIXED_MINSIZE)
        vbox.Add(self.btn_bottom, 0, wx.FIXED_MINSIZE)
        
        # Use minimum size spacers instead of (0,0) to prevent GTK negative allocation
        min_spacer = (15, 15)
        self.Add(min_spacer, 0, wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
        self.Add(self.btn_back, 0, wx.FIXED_MINSIZE)
        self.Add(min_spacer, 0, wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
        self.Add(self.btn_left, 0, wx.FIXED_MINSIZE)
        self.Add(vbox, 0, wx.FIXED_MINSIZE)
        self.Add(self.btn_right, 0, wx.FIXED_MINSIZE)
        self.Add(min_spacer, 0, wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
        self.Add(self.btn_front, 0, wx.FIXED_MINSIZE)
        self.Add(min_spacer, 0, wx.RESERVE_SPACE_EVEN_IF_HIDDEN)
        
        # Set minimum size on the sizer itself to prevent GTK negative allocation
        self.SetMinSize((200, 100))

        # connect handlers
        self.btn_front.Bind(wx.EVT_BUTTON, self.on_view_front)
        self.btn_back.Bind(wx.EVT_BUTTON, self.on_view_back)
        self.btn_left.Bind(wx.EVT_BUTTON, self.on_view_left)
        self.btn_right.Bind(wx.EVT_BUTTON, self.on_view_right)
        self.btn_top.Bind(wx.EVT_BUTTON, self.on_view_top)
        self.btn_bottom.Bind(wx.EVT_BUTTON, self.on_view_bottom)

    def on_view_front(self, event):
        self.scene.rotate_view(0, 0)

    def on_view_back(self, event):
        self.scene.rotate_view(180, 0)

    def on_view_left(self, event):
        self.scene.rotate_view(90, 0)

    def on_view_right(self, event):
        self.scene.rotate_view(-90, 0)

    def on_view_top(self, event):
        self.scene.rotate_view(0, -90)

    def on_view_bottom(self, event):
        self.scene.rotate_view(0, 90)
