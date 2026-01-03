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
from wx import glcanvas


class BaseScene(glcanvas.GLCanvas):
    def __init__(self, parent):
        try:  # the new way
            super(BaseScene, self).__init__(parent, self._get_display_attributes())
        except AttributeError:  # the old way
            super(BaseScene, self).__init__(parent, attribList=self._get_attrib_list())

        self.Hide()

        self.initialized = False
        self.context = glcanvas.GLContext(self)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self._on_erase_background)
        self.Bind(wx.EVT_SIZE, self._on_size)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self._on_mouse_down)
        # also bind right and middle button down so panning/offset works when
        # user starts dragging with those buttons
        self.Bind(wx.EVT_RIGHT_DOWN, self._on_mouse_down)
        self.Bind(wx.EVT_MIDDLE_DOWN, self._on_mouse_down)
        self.Bind(wx.EVT_MOTION, self._on_mouse_motion)

        # make it unnecessary for the scene to be in focus to respond to the
        # mouse wheel by binding the mouse wheel event to the parent; if we
        # bound the event to the scene itself, the user would have to click on
        # the scene before scrolling each time the scene loses focus (users who
        # have the fortune of being able to use a window manager that has a
        # setting for focus-follows-mouse wouldn't care either way, since their
        # wm would handle it for them)
        parent.Bind(wx.EVT_MOUSEWHEEL, self._on_mouse_wheel)

        methods = [
            "init",
            "display",
            "reshape",
            "button_press",
            "button_motion",
            "wheel_scroll",
        ]
        for method in methods:
            if not hasattr(self, method):
                raise Exception("Method %s() is not implemented" % method)

    @staticmethod
    def _get_display_attributes():
        """Get the display attributes when using wxPython 4.1 or later."""
        for depth in [32, 24, 16, 8]:
            dispAttrs = glcanvas.GLAttributes()
            dispAttrs.PlatformDefaults().DoubleBuffer().Depth(depth).EndList()

            if glcanvas.GLCanvas.IsDisplaySupported(dispAttrs):
                return dispAttrs
        else:
            raise Exception("No suitable depth buffer value found")

    @staticmethod
    def _get_attrib_list():
        """Get the display attributes when using wxPython 4.0 or earlier."""
        for depth in [32, 24, 16, 8]:
            attrib_list = [
                glcanvas.WX_GL_RGBA,
                glcanvas.WX_GL_DOUBLEBUFFER,
                glcanvas.WX_GL_DEPTH_SIZE,
                depth,
                0,
            ]

            if glcanvas.GLCanvas.IsDisplaySupported(attrib_list):
                return attrib_list
        else:
            raise Exception("No suitable depth buffer value found")

    def invalidate(self):
        self.Refresh(False)

    def _on_erase_background(self, event):
        pass  # Do nothing, to avoid flashing on MSW. Doesn't seem to be working, though :(

    def _on_size(self, event):
        # Use CallAfter to prevent GTK allocation errors during resize
        if self and not self.IsBeingDeleted():
            wx.CallAfter(self._set_viewport)
        event.Skip()

    def _set_viewport(self):
        """Set GL viewport using physical framebuffer size (DPI aware).

        wx returns logical client size via GetClientSize(); on HiDPI displays
        the actual framebuffer size may be scaled by a content scale factor.
        Use GetContentScaleFactor() when available to compute the physical
        dimensions for glViewport and the projection matrices.
        """
        self.SetCurrent(self.context)
        size = self.GetClientSize()
        try:
            scale = 1.0
            if hasattr(self, "GetContentScaleFactor"):
                try:
                    scale = self.GetContentScaleFactor()
                except Exception:
                    scale = 1.0
            phys_w = int(size.width * scale)
            phys_h = int(size.height * scale)
            import logging

            logging.info(
                "BaseScene._set_viewport logical size: (%s, %s) scale: %s phys: (%s, %s)",
                size.width,
                size.height,
                scale,
                phys_w,
                phys_h,
            )
        except Exception:
            phys_w, phys_h = size.width, size.height
        self.reshape(phys_w, phys_h)

    def _on_paint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.initialized:
            self.init()
            self.initialized = True
        size = self.GetClientSize()
        # Account for display scaling (HiDPI) when calling display so the
        # projection and viewport are set to the physical framebuffer size
        try:
            scale = 1.0
            if hasattr(self, "GetContentScaleFactor"):
                try:
                    scale = self.GetContentScaleFactor()
                except Exception:
                    scale = 1.0
            phys_w = int(size.width * scale)
            phys_h = int(size.height * scale)
            import logging

            logging.info(
                "BaseScene._on_paint logical size: (%s, %s) scale: %s phys: (%s, %s)",
                size.width,
                size.height,
                scale,
                phys_w,
                phys_h,
            )
        except Exception:
            phys_w, phys_h = size.width, size.height
        self.display(phys_w, phys_h)
        self.SwapBuffers()

    def _on_mouse_down(self, event):
        self.SetFocus()
        x, y = event.GetPosition()
        # Convert to physical coordinates if content-scale factor is present
        try:
            if hasattr(self, "GetContentScaleFactor"):
                scale = self.GetContentScaleFactor()
                x = int(x * scale)
                y = int(y * scale)
        except Exception:
            pass
        self.button_press(x, y)

    def _on_mouse_motion(self, event):
        x, y = event.GetPosition()
        left = event.LeftIsDown()
        middle = event.MiddleIsDown()
        right = event.RightIsDown()
        try:
            if hasattr(self, "GetContentScaleFactor"):
                scale = self.GetContentScaleFactor()
                x = int(x * scale)
                y = int(y * scale)
        except Exception:
            pass
        self.button_motion(x, y, left, middle, right)

    def _on_mouse_wheel(self, event):
        self.wheel_scroll(event.GetWheelRotation())
