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
import logging

from tatlin.lib.gl.scene import Scene
from tatlin.lib.ui.panel import Panel
from tatlin.lib.util import format_float

from .view import ViewButtons


class GcodePanel(Panel):
    def __init__(self, parent, scene: Scene):
        super(GcodePanel, self).__init__(parent, scene)

        # ----------------------------------------------------------------------
        # DIMENSIONS
        # ----------------------------------------------------------------------

        static_box_dimensions = wx.StaticBox(self, label="Dimensions")
        sizer_dimensions = wx.StaticBoxSizer(static_box_dimensions, wx.VERTICAL)

        label_width = wx.StaticText(self, label="X:")
        self.label_width_value = wx.StaticText(self)

        label_depth = wx.StaticText(self, label="Y:")
        self.label_depth_value = wx.StaticText(self)

        label_height = wx.StaticText(self, label="Z:")
        self.label_height_value = wx.StaticText(self)

        grid_dimensions = wx.GridSizer(3, 2, 5, 5)
        grid_dimensions.Add(label_width, 0, wx.ALIGN_CENTER)
        grid_dimensions.Add(self.label_width_value, 0, wx.ALIGN_CENTER)
        grid_dimensions.Add(label_depth, 0, wx.ALIGN_CENTER)
        grid_dimensions.Add(self.label_depth_value, 0, wx.ALIGN_CENTER)
        grid_dimensions.Add(label_height, 0, wx.ALIGN_CENTER)
        grid_dimensions.Add(self.label_height_value, 0, wx.ALIGN_CENTER)
        # Set minimum size to prevent GTK allocation errors
        grid_dimensions.SetMinSize((120, -1))

        sizer_dimensions.Add(grid_dimensions, 0, wx.EXPAND | wx.ALL, border=5)

        # ----------------------------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------------------------

        static_box_display = wx.StaticBox(self, label="Display")
        sizer_display = wx.StaticBoxSizer(static_box_display, wx.VERTICAL)

        label_layers = wx.StaticText(self, label="Layers")
        self.slider_layers = wx.Slider(self, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.check_arrows = wx.CheckBox(self, label="Show arrows")
        self.check_travels = wx.CheckBox(self, label="Show travels")
        self.check_grid = wx.CheckBox(self, label="Show grid")
        self.check_3d = wx.CheckBox(self, label="3D view")
        view_buttons = ViewButtons(self, scene)
        self.check_ortho = wx.CheckBox(self, label="Orthographic projection")
        
        # Set minimum sizes to prevent GTK warnings about negative size
        min_checkbox_size = (120, 30)
        for checkbox in [self.check_arrows, self.check_travels, self.check_grid,
                         self.check_3d, self.check_ortho]:
            checkbox.SetMinSize(min_checkbox_size)
        
        # Zoom controls
        self.btn_zoom_in = wx.Button(self, label="Zoom in")
        self.btn_zoom_out = wx.Button(self, label="Zoom out")
        self.btn_reset_view = wx.Button(self, label="Reset view")
        # Center view
        self.btn_center_view = wx.Button(self, label="Center view")
        
        # Set minimum sizes to prevent GTK allocation errors
        for btn in [self.btn_zoom_in, self.btn_zoom_out, self.btn_reset_view, self.btn_center_view]:
            btn.SetMinSize((100, 30))

        # Tooltips show keyboard shortcuts
        self.btn_zoom_in.SetToolTip("Zoom in (Ctrl+=)")
        self.btn_zoom_out.SetToolTip("Zoom out (Ctrl+-)")
        self.btn_reset_view.SetToolTip("Reset view (Ctrl+0)")
        self.btn_center_view.SetToolTip("Center model in the view")

        hzoom = wx.BoxSizer(wx.HORIZONTAL)
        hzoom.Add(self.btn_zoom_in, 0, wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hzoom.Add(self.btn_zoom_out, 0, wx.FIXED_MINSIZE)

        box_display = wx.BoxSizer(wx.VERTICAL)
        box_display.Add(label_layers, 0, wx.ALIGN_LEFT)
        box_display.Add(self.slider_layers, 0, wx.EXPAND | wx.TOP, border=5)
        box_display.Add(self.check_arrows, 0, wx.EXPAND | wx.TOP | wx.FIXED_MINSIZE, border=5)
        box_display.Add(self.check_travels, 0, wx.EXPAND | wx.TOP | wx.FIXED_MINSIZE, border=5)
        box_display.Add(self.check_grid, 0, wx.EXPAND | wx.TOP | wx.FIXED_MINSIZE, border=5)
        box_display.Add(self.check_3d, 0, wx.EXPAND | wx.TOP | wx.FIXED_MINSIZE, border=5)
        box_display.Add(view_buttons, 0, wx.ALIGN_CENTER | wx.TOP, border=5)
        box_display.Add(self.check_ortho, 0, wx.EXPAND | wx.TOP | wx.FIXED_MINSIZE, border=5)
        box_display.Add(hzoom, 0, wx.EXPAND | wx.TOP, border=5)

        # Small on-screen hint showing keyboard shortcuts
        hint = wx.StaticText(self, label="Shortcuts: Ctrl+=, Ctrl+-, Ctrl+0")
        font = hint.GetFont()
        # make hint a bit smaller than default
        try:
            font.SetPointSize(max(font.GetPointSize() - 1, 8))
            hint.SetFont(font)
        except Exception:
            pass
        box_display.Add(hint, 0, wx.ALIGN_LEFT | wx.TOP, border=5)

        hreset = wx.BoxSizer(wx.HORIZONTAL)
        hreset.Add(self.btn_reset_view, 0, wx.RIGHT | wx.FIXED_MINSIZE, border=5)
        hreset.Add(self.btn_center_view, 0, wx.FIXED_MINSIZE)
        box_display.Add(hreset, 0, wx.EXPAND | wx.TOP, border=5)

        sizer_display.Add(box_display, 0, wx.EXPAND | wx.ALL, border=5)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(sizer_dimensions, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, border=5)
        box.Add(sizer_display, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, border=5)

        self.SetSizer(box)
        # Set minimum width to prevent GTK allocation warnings
        self.SetMinSize((260, -1))
        # Prevent panel from shrinking below minimum size
        box.SetMinSize((260, -1))
        # Finalize layout before showing to prevent GTK sizing errors
        self.SetInitialSize(self.GetMinSize())
        self.Layout()

    def connect_handlers(self):
        if self._handlers_connected:
            return

        self.slider_layers.Bind(wx.EVT_SCROLL, self.on_slider_moved)
        self.check_arrows.Bind(wx.EVT_CHECKBOX, self.on_arrows_toggled)
        self.check_travels.Bind(wx.EVT_CHECKBOX, self.on_travels_toggled)
        self.check_grid.Bind(wx.EVT_CHECKBOX, self.on_grid_toggled)
        self.btn_reset_view.Bind(wx.EVT_BUTTON, self.on_reset_clicked)
        self.btn_center_view.Bind(wx.EVT_BUTTON, self.on_center_clicked)
        self.btn_zoom_in.Bind(wx.EVT_BUTTON, self.on_zoom_in)
        self.btn_zoom_out.Bind(wx.EVT_BUTTON, self.on_zoom_out)
        self.check_3d.Bind(wx.EVT_CHECKBOX, self.on_set_mode)
        self.check_ortho.Bind(wx.EVT_CHECKBOX, self.on_set_ortho)

        self._handlers_connected = True

    def on_slider_moved(self, event):
        self.scene.change_num_layers(event.GetEventObject().GetValue())
        self.scene.invalidate()

    def on_arrows_toggled(self, event):
        """
        Show/hide arrows on the Gcode model.
        """
        self.scene.show_arrows(event.GetEventObject().GetValue())
        self.scene.invalidate()

    def on_travels_toggled(self, event):
        """
        Show/hide travel movements (non-cutting moves) on the Gcode model.
        """
        self.scene.show_travels(event.GetEventObject().GetValue())
        self.scene.invalidate()

    def on_grid_toggled(self, event):
        """
        Show/hide the background grid and axes.
        """
        self.scene.show_grid(event.GetEventObject().GetValue())
        self.scene.invalidate()

    def on_reset_clicked(self, event):
        """
        Restore the view of the model shown on startup.
        """
        self.scene.reset_view()
        self.scene.invalidate()

    def on_center_clicked(self, event):
        """
        Center the model in the viewable area without modifying the model's vertices.
        """
        # Guard and logging for debugging
        if not getattr(self.scene, "model", None):
            logging.info("Center view requested but no model is loaded")
            return

        logging.info(
            "Center view requested; offsets before: (%s, %s, %s)",
            getattr(self.scene.model, "offset_x", None),
            getattr(self.scene.model, "offset_y", None),
            getattr(self.scene.model, "offset_z", None),
        )

        # Use scene.view_model_center which adjusts offsets for viewing only
        self.scene.view_model_center()

        logging.info(
            "Offsets after centering: (%s, %s, %s)",
            getattr(self.scene.model, "offset_x", None),
            getattr(self.scene.model, "offset_y", None),
            getattr(self.scene.model, "offset_z", None),
        )

        # Try to translate the view so the model center (after applying
        # model offsets) appears at the center of the canvas. This handles
        # both 2D (View2D) and 3D (View3D) modes.
        cur_view = self.scene.current_view
        try:
            logging.info(
                "View before centering: x=%s, y=%s, z=%s, offset_x=%s, offset_y=%s",
                getattr(cur_view, "x", None),
                getattr(cur_view, "y", None),
                getattr(cur_view, "z", None),
                getattr(cur_view, "offset_x", None),
                getattr(cur_view, "offset_y", None),
            )

            model = getattr(self.scene, "model", None)
            if model is not None:
                # If the model has offsets applied, move the view the opposite
                # direction so the model visually centers. For View2D we use
                # x/y pan variables; for View3D we use offset_x/offset_y.
                if hasattr(cur_view, "offset_x") and hasattr(cur_view, "offset_y"):
                    # 3D view has small scale differences, so use model offsets
                    cur_view.offset_x = -model.offset_x
                    cur_view.offset_y = -model.offset_y
                else:
                    # 2D view uses x/y panning
                    cur_view.x = -model.offset_x
                    cur_view.y = -model.offset_y

            logging.info(
                "View after centering: x=%s, y=%s, z=%s, offset_x=%s, offset_y=%s",
                getattr(cur_view, "x", None),
                getattr(cur_view, "y", None),
                getattr(cur_view, "z", None),
                getattr(cur_view, "offset_x", None),
                getattr(cur_view, "offset_y", None),
            )
        except Exception:
            logging.exception("Failed to adjust view to center model")

        # Try to make the centering exact using GL projection/unprojection
        try:
            # Ensure GL context is current
            try:
                self.scene.SetCurrent(self.scene.context)
            except Exception:
                pass

            from OpenGL.GL import glGetDoublev, glGetIntegerv, GL_MODELVIEW_MATRIX, GL_PROJECTION_MATRIX, GL_VIEWPORT
            from OpenGL.GLU import gluProject, gluUnProject

            # model center in model coordinates
            bbox = self.scene.model.bounding_box
            mcx = (bbox.lower_corner[0] + bbox.upper_corner[0]) / 2.0
            mcy = (bbox.lower_corner[1] + bbox.upper_corner[1]) / 2.0
            mcz = (bbox.lower_corner[2] + bbox.upper_corner[2]) / 2.0

            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            proj = glGetDoublev(GL_PROJECTION_MATRIX)
            viewport = glGetIntegerv(GL_VIEWPORT)

            winx, winy, winz = gluProject(mcx, mcy, mcz, modelview, proj, viewport)
            center_x = viewport[2] / 2.0
            center_y = viewport[3] / 2.0

            dx_pixels = center_x - winx
            dy_pixels = center_y - winy

            logging.info("Model center projected to window: (%s, %s) target: (%s, %s) delta pixels: (%s, %s)", winx, winy, center_x, center_y, dx_pixels, dy_pixels)

            # unproject two points to find world space delta at the same depth
            wx1, wy1, wz1 = gluUnProject(winx, winy, winz, modelview, proj, viewport)
            wx2, wy2, wz2 = gluUnProject(winx + dx_pixels, winy + dy_pixels, winz, modelview, proj, viewport)

            dx_world = wx2 - wx1
            dy_world = wy2 - wy1
            dz_world = wz2 - wz1

            logging.info("Computed world translation to center: (%s, %s, %s)", dx_world, dy_world, dz_world)

            cur_view = self.scene.current_view
            # apply world delta to view translation variables
            # For View3D, translating in world X/Y corresponds to offset_x/offset_y
            # For View2D we should apply an analytic translation to x/y that takes
            # zoom into account to avoid large rounding errors from gluUnProject.
            try:
                from tatlin.lib.gl.views import View2D
            except Exception:
                View2D = None

            if View2D is not None and isinstance(cur_view, View2D):
                # For 2D, world transform after model translation and scale is:
                # screen = view + zoom * (vertex + model_offset). To center the
                # model center (mc + model_offset) at screen=0, set:
                # view = -zoom * (mc + model_offset)
                bbox = self.scene.model.bounding_box
                mcx = (bbox.lower_corner[0] + bbox.upper_corner[0]) / 2.0
                mcy = (bbox.lower_corner[1] + bbox.upper_corner[1]) / 2.0
                # model offsets
                mo_x = getattr(self.scene.model, "offset_x", 0.0)
                mo_y = getattr(self.scene.model, "offset_y", 0.0)
                # The view translation should satisfy: zoom * (view.x + mc + mo) = 0
                # which simplifies to view.x = -(mc + mo). Do NOT multiply by zoom again.
                new_x = -(mcx + mo_x)
                new_y = -(mcy + mo_y)
                logging.info("View2D analytic centering -> setting x=%s y=%s (zoom=%s mc=(%s,%s) mo=(%s,%s))",
                             new_x, new_y, cur_view.zoom_factor, mcx, mcy, mo_x, mo_y)
                cur_view.x = new_x
                cur_view.y = new_y
            else:
                if hasattr(cur_view, "offset_x") and hasattr(cur_view, "offset_y"):
                    cur_view.offset_x += dx_world
                    cur_view.offset_y += dy_world
                else:
                    cur_view.x += dx_world
                    cur_view.y += dy_world

            logging.info("Applied world delta/analytic centering; new view x/y/offsets: x=%s y=%s offset_x=%s offset_y=%s",
                         getattr(cur_view, "x", None), getattr(cur_view, "y", None),
                         getattr(cur_view, "offset_x", None), getattr(cur_view, "offset_y", None))

        except Exception:
            logging.exception("Precise centering using GL projection failed; falling back")

        # Final redraw and UI feedback
        self.scene.invalidate()
        try:
            parent = self.GetParent()
            if hasattr(parent, "update_status"):
                parent.update_status("Centered model in view")
        except Exception:
            pass

    def on_zoom_in(self, event):
        """Zoom the scene in by one tick."""
        self.scene.zoom_in()
        self.scene.invalidate()

    def on_zoom_out(self, event):
        """Zoom the scene out by one tick."""
        self.scene.zoom_out()
        self.scene.invalidate()

    def on_set_mode(self, event):
        val = event.GetEventObject().GetValue()
        self.check_ortho.Enable(val)

        self.scene.mode_2d = not val
        if self.scene.initialized:
            self.scene.invalidate()

    def on_set_ortho(self, event):
        self.scene.mode_ortho = event.GetEventObject().GetValue()
        self.scene.invalidate()

    def set_initial_values(self, layers_range_max, layers_value, width, height, depth):
        if layers_range_max > 1:
            self.slider_layers.SetRange(1, layers_range_max)
            self.slider_layers.SetValue(layers_value)
            self.slider_layers.Show()
        else:
            self.slider_layers.Hide()

        self.check_arrows.SetValue(True)  # check the box
        self.check_travels.SetValue(True)  # check the box
        self.check_grid.SetValue(True)  # check the box
        self.check_3d.SetValue(True)

        self.label_width_value.SetLabel(format_float(width))
        self.label_height_value.SetLabel(format_float(height))
        self.label_depth_value.SetLabel(format_float(depth))

    def set_3d_view(self, value):
        self.check_3d.SetValue(value)
