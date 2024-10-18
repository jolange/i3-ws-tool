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
    print("You need to install i3ipc: https://github.com/altdesktop/i3ipc-python")
    raise

import argparse
import subprocess as sp

i3 = i3ipc.Connection()


def main():
    parser = argparse.ArgumentParser(
        description='Tool to handle, manipulate and modify i3 workspaces.',
        formatter_class=argparse.RawTextHelpFormatter,  # allow newlines
    )

    action_desc = {
        'menu': 'Show a menu and choose an action',
        'switch': 'Switch to a workspace chosen from a menu or a new one',
        'next-empty': 'Focus the next empty, numbered  workspace',
        'move': 'Move container to a workspace chosen from a menu or a new one',
        'move-next-empty': 'Move the focused container to the next empty, numbered  workspace',
        'rename': 'Rename the focused workspace',
        'clear-output': 'Move all workspaces from the active output to a different one',
        'move-to-single-output': 'Move all existing workspaces to a single output'
    }
    action_opts = action_desc.keys()

    parser.add_argument('run', type=str, nargs='?', default='menu',
                        choices=action_opts, metavar='ACTION',
                        help='Choose one of these actions:\n' + '\n'.join('- %s: %s' % (k, v) for k, v in action_desc.items()))
    parser.add_argument('--dest', type=str, metavar='DEST', nargs='?', help='Destination for move-to-single-output')

    args = parser.parse_args()
    if args.dest is not None and args.run != 'move-to-single-output':
        parser.error('DEST argument is only implemented for move-to-single-output')

    while args.run == 'menu':
        args.run = call_menu(action_opts, prompt='action', selected='switch', no_custom=True)

    if args.run == 'switch':
        i3.command('workspace %s' % call_menu(get_workspaces_names(), selected=get_focused_workspace().name,
                                              prompt='Switch to workspace'))
    elif args.run == 'next-empty':
        i3.command('workspace %s' % get_next_empty_workspace())
    elif args.run == 'move':
        i3.command('move container to workspace %s' % call_menu(get_workspaces_names(), prompt='Move to workspace'))
    elif args.run == 'move-next-empty':
        i3.command('move container to workspace %s' % get_next_empty_workspace())
    elif args.run == 'rename':
        i3.command('rename workspace to "%s"' %
                   call_menu(preselection=get_focused_workspace().name, prompt='Rename workspace to'))
    elif args.run == 'clear-output':
        output = get_focused_output()
        target = call_menu(get_output_names(), selected=output,
                           prompt=f'Move all workspaces of {output} to output')
        for ws in get_workspaces_on_output(output):
            i3.command(f'[workspace="{ws.name}"] move workspace to output {target}')
    elif args.run == 'move-to-single-output':
        target = args.dest or call_menu(get_output_names(), selected=get_focused_output(),
                                        prompt=f'Move all workspaces to output')
        focused_ws = get_focused_workspace().name
        for wsname in get_workspaces_names():
            i3.command(f'[workspace="{wsname}"] move workspace to output {target}')
        i3.command('workspace --no-auto-back-and-forth %s' % focused_ws)
    else:
        raise ValueError("Action %s is unkown." % args.run)


def call_menu(opt_list=[], preselection=None, selected=None, prompt='input', msg=None, no_custom=False):
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
    for ws in i3.get_workspaces():
        yield ws.name


def get_focused_workspace():
    for ws in i3.get_workspaces():
        if ws.focused:
            return ws


def get_numbered_workspaces():
    for ws in i3.get_workspaces():
        if ws.num >= 0:
            yield ws.num


def get_next_empty_workspace():
    # fallback: if no numbered workspaces exist, "1" is the next empty
    ws = 0
    for num, ws in enumerate(sorted(get_numbered_workspaces()), 1):
        if num != ws:
            return num
    return ws + 1


def get_workspaces_on_output(output):
    for ws in i3.get_workspaces():
        if ws.output == output:
            yield ws


def get_focused_output():
    return get_focused_workspace().output


def get_output_names():
    for o in i3.get_outputs():
        if o.active:
            yield o.name


if __name__ == '__main__':
    main()
