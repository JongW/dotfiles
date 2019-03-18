#!/usr/bin/env python3

# This script listens for i3 events and updates workspace names to show icons
# for running programs.  It contains icons for a few programs, but more can
# easily be added by adding them to WINDOW_ICONS below.
#
# It also re-numbers workspaces in ascending order with one skipped number
# between monitors (leaving a gap for a new workspace to be created). By
# default, i3 workspace numbers are sticky, so they quickly get out of order.
#
# Installation:
# * Download this script and place it in ~/.config/i3/ (or anywhere you want)
# * Add "exec_always ~/.config/i3/i3-autoname-workspaces.py &" to your i3 config
# * Restart i3: $ i3-msg restart
#
# Configuration:
# The default i3 config's keybindings reference workspaces by name, which is an
# issue when using this script because the "names" are constantaly changing to
# include window icons.  Instead, you'll need to change the keybindings to
# reference workspaces by number.  Change lines like:
#   bindsym $mod+1 workspace 1
# To:
#   bindsym $mod+1 workspace number 1

import re
import logging
import signal
import sys

import i3ipc
import fontawesome as fa
from xcffib.xproto import WindowError
from xpybutil.icccm import (
    get_wm_class,
    get_wm_name,
)

# Add icons here for common programs you use.  The keys are the X window class
# (WM_CLASS) names (lower-cased) and the icons can be any text you want to
# display.
#
# Most of these are character codes for font awesome:
#   http://fortawesome.github.io/Font-Awesome/icons/
#

WINDOW_ICONS = {
    'google-chrome': fa.icons['globe-asia'],
    'spotify': fa.icons['music'],
    'kitty': fa.icons['terminal'],
    'urxvt': fa.icons['terminal'],
    'code': fa.icons['code'],
}

# This icon is used for any application not in the list above
DEFAULT_ICON = '~'

# https://github.com/justbuchanan/i3scripts


def focused_workspace(i3):
    return [w for w in i3.get_workspaces() if w.focused][0]


def parse_workspace_name(name):
    """Takes a workspace 'name' from i3 and splits it into three parts:
    * 'num'
    * 'shortname' - the workspace's name, assumed to have no spaces
    * 'icons' - the string that comes after the
    Any field that's missing will be None in the returned dict
    """
    return re.match('(?P<num>\d+):?(?P<shortname>\w+)? ?(?P<icons>.+)?',
                    name).groupdict()


def construct_workspace_name(parts):
    """Given a dictionary with 'num', 'shortname', 'icons', returns the
    formatted name by concatenating them together.
    """
    if parts['icons'] is not None:
        temp_icons = set(parts['icons'].split(" "))   
        parts['icons']=' '.join(temp_icons)

    new_name = str(parts['num'])
    if parts['shortname'] or parts['icons']:
        new_name += ' | '

        if parts['shortname']:
            new_name += parts['shortname']

        if parts['icons']:
            new_name += parts['icons']

    return new_name


def icon_for_window(window):
    """Try all window classes and use the first one we have an icon for."""
    name = get_wm_name(window.window).reply()
    classes = get_wm_class(window.window).reply()

    if name:
        name = name[0].split()[0]
        if name in WINDOW_ICONS:
            return WINDOW_ICONS[name]

    if classes:
        for cls in classes:
            cls = cls.lower()  # case-insensitive matching
            if cls in WINDOW_ICONS:
                return WINDOW_ICONS[cls]
    logging.info(
        'No icon available for window with classes: %s' % str(classes))
    return DEFAULT_ICON


def rename_workspaces(i3):
    """renames all workspaces based on the windows present
    also renumbers them in ascending order, with one gap left between monitors
    for example: workspace numbering on two monitors: [1, 2, 3], [5, 6]
    """
    workspace_infos = i3.get_workspaces()
    prev_output = None
    workspace_number = 1
    for workspace_index, workspace in enumerate(i3.get_tree().workspaces()):
        workspace_info = workspace_infos[workspace_index]

        name_parts = parse_workspace_name(workspace.name)
        try:
            icons = [icon_for_window(w) for w in workspace.leaves()]
        except WindowError:
            logging.info('WindowError encountered, bailing for now...')
            return
        name_parts['icons'] = ' '.join(icons)

        # As we enumerate, leave one gap in workspace numbers between each
        # monitor.
        # This leaves a space to insert a new one later.
        if prev_output and workspace_info.output != prev_output:
            workspace_number += 1
        prev_output = workspace_info.output

        # renumber workspace
        name_parts['num'] = workspace_number
        workspace_number += 1

        new_name = construct_workspace_name(name_parts)
        if workspace.name != new_name:
            i3.command('rename workspace "%s" to "%s"' % (workspace.name,
                                                          new_name))


def on_exit(i3):
    """Rename workspaces to just numbers and shortnames, removing the icons."""
    for workspace in i3.get_tree().workspaces():
        name_parts = parse_workspace_name(workspace.name)
        name_parts['icons'] = None
        new_name = construct_workspace_name(name_parts)
        if workspace.name == new_name:
            continue
        i3.command('rename workspace "%s" to "%s"' % (workspace.name,
                                                      new_name))
    i3.main_quit()
    sys.exit(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    i3 = i3ipc.Connection()

    # Exit gracefully when ctrl+c is pressed
    for sig in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig, lambda signal, frame: on_exit(i3))

    rename_workspaces(i3)

    # Call rename_workspaces() for relevant window events
    def window_event_handler(i3, e):
        if e.change in ['new', 'close', 'move']:
            rename_workspaces(i3)

    i3.on('window', window_event_handler)
    i3.main()
