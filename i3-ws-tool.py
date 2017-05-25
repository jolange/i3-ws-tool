#!/usr/bin/env python3

# Tool to handle, manipulate and modify i3 workspaces.

# Copyright 2017 Johannes Lange
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

try:
    import i3ipc
except ImportError:
    print("You need to install i3ipc: https://github.com/acrisci/i3ipc-python")
    raise

import argparse
import subprocess as sp

i3 = i3ipc.Connection()


def main():
    parser = argparse.ArgumentParser(
        description='Tool to handle, manipulate and modify i3 workspaces.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    run_opts = ['menu', 'switch', 'next-empty', 'move-next-empty', 'rename']

    parser.add_argument('run', type=str, nargs='?', default='menu',
                        choices=run_opts,
                        help='help!')
    args = parser.parse_args()

    while args.run == 'menu':
        args.run = call_menu(action_opts, prompt='action:', selected='switch', no_custom=True)

    if args.run == 'switch':
        i3.command('workspace %s' % call_menu(get_workspaces_names(), selected=get_focused_workspace_name(),
                                              prompt='Switch to workspace:'))
    elif args.run == 'next-empty':
        i3.command('workspace %s' % get_next_empty_workspace())
    elif args.run == 'move-next-empty':
        i3.command('move container to workspace %s' % get_next_empty_workspace())
    elif args.run == 'rename':
        i3.command('rename workspace to %s' %
                   call_menu(preselection=get_focused_workspace_name(), prompt='Rename workspace to:'))
    else:
        raise ValueError("Option %s is unkown." % args.run)


def call_menu(opt_list=[], preselection=None, selected=None, prompt='input:', msg=None, no_custom=False):
    cmd = ['rofi', '-dmenu']
    if preselection:
        cmd += ['-filter', preselection]
    if msg:
        cmd += ['-mesg', msg]
    if no_custom:
        cmd += ['-no-custom']
    if selected:
        cmd += ['-select', selected]
    cmd += ['-p', prompt]
    choice = sp.check_output(cmd, input=bytearray('\n'.join(opt_list), 'utf-8'))
    return choice.strip().decode('utf-8')


def get_workspaces_names():
    return [ws['name'] for ws in i3.get_workspaces()]


def get_focused_workspace_name():
    for ws in i3.get_workspaces():
        if ws['focused']:
            return ws['name']


def get_numbered_workspaces():
    for ws in i3.get_workspaces():
        if ws['num'] >= 0:
            yield ws['num']


def get_next_empty_workspace():
    for num, ws in enumerate(get_numbered_workspaces(), 1):
        if num != ws:
            return num
    return ws + 1


if __name__ == '__main__':
    main()
