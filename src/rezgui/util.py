# Copyright Contributors to the Rez project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from Qt import QtWidgets, QtGui
from rez.utils.formatting import readable_time_duration
import os.path
import time


def create_pane(widgets, horizontal, parent_widget=None, compact=False,
                compact_spacing=2):
    """Create a widget containing an aligned set of widgets.

    Args:
        widgets (list of `QWidget`).
        horizontal (bool).
        align (str): One of:
            - 'left', 'right' (horizontal);
            - 'top', 'bottom' (vertical)
        parent_widget (`QWidget`): Owner widget, QWidget is created if this
            is not provided.

    Returns:
        `QWidget`
    """
    pane = parent_widget or QtWidgets.QWidget()
    type_ = QtWidgets.QHBoxLayout if horizontal else QtWidgets.QVBoxLayout
    layout = type_()
    if compact:
        layout.setSpacing(compact_spacing)
        layout.setContentsMargins(compact_spacing, compact_spacing,
                                  compact_spacing, compact_spacing)

    for widget in widgets:
        stretch = 0
        if isinstance(widget, tuple):
            widget, stretch = widget

        if isinstance(widget, int):
            layout.addSpacing(widget)
        elif widget:
            layout.addWidget(widget, stretch)
        else:
            layout.addStretch()

    pane.setLayout(layout)
    return pane


icons = {}


def get_icon(name, as_qicon=False):
    """Returns a `QPixmap` containing the given image, or a QIcon if `as_qicon`
    is True"""
    filename = name + ".png"
    icon = icons.get(filename)
    if not icon:
        path = os.path.dirname(__file__)
        path = os.path.join(path, "icons")
        filepath = os.path.join(path, filename)
        if not os.path.exists(filepath):
            filepath = os.path.join(path, "pink.png")

        icon = QtGui.QPixmap(filepath)
        icons[filename] = icon

    return QtGui.QIcon(icon) if as_qicon else icon


def get_icon_widget(filename, tooltip=None):
    icon = get_icon(filename)
    icon_label = QtWidgets.QLabel()
    icon_label.setPixmap(icon)
    if tooltip:
        icon_label.setToolTip(tooltip)
    return icon_label


def get_timestamp_str(timestamp):
    now = int(time.time())
    release_time = time.localtime(timestamp)
    release_time_str = time.strftime('%d %b %Y %H:%M:%S', release_time)
    ago = readable_time_duration(now - timestamp)
    return "%s (%s ago)" % (release_time_str, ago)


def add_menu_action(menu, label, slot=None, icon_name=None, group=None,
                    parent=None):
    nargs = []
    if icon_name:
        icon = get_icon(icon_name, as_qicon=True)
        nargs.append(icon)
    nargs += [label, menu]
    if parent:
        nargs.append(parent)

    action = QtWidgets.QAction(*nargs)
    if slot:
        action.triggered.connect(slot)
    if group:
        action.setCheckable(True)
        group.addAction(action)
    menu.addAction(action)
    return action


def interp_color(a, b, f):
    """Interpolate between two colors.

    Returns:
        `QColor` object.
    """
    a_ = (a.redF(), a.greenF(), a.blueF())
    b_ = (b.redF(), b.greenF(), b.blueF())
    a_ = [x * (1 - f) for x in a_]
    b_ = [x * f for x in b_]
    c = [x + y for x, y in zip(a_, b_)]
    return QtGui.QColor.fromRgbF(*c)


def create_toolbutton(entries, parent=None):
    """Create a toolbutton.

    Args:
        entries: List of (label, slot) tuples.

    Returns:
        `QtWidgets.QToolBar`.
    """
    btn = QtWidgets.QToolButton(parent)
    menu = QtWidgets.QMenu()
    actions = []

    for label, slot in entries:
        action = add_menu_action(menu, label, slot)
        actions.append(action)

    btn.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
    btn.setDefaultAction(actions[0])
    btn.setMenu(menu)
    return btn, actions


def update_font(widget, italic=None, bold=None, underline=None):
    font = widget.font()
    if italic is not None:
        font.setItalic(italic)
    if bold is not None:
        font.setBold(bold)
    if underline is not None:
        font.setUnderline(underline)
    widget.setFont(font)
