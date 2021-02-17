import os
import shlex
from shutil import which
import tempfile


HERE = os.path.dirname(os.path.abspath(__file__))

def setup_desktop():
    # make a secure temporary directory for sockets
    # This is only readable, writeable & searchable by our uid
    sockets_dir = tempfile.mkdtemp()
    sockets_path = os.path.join(sockets_dir, 'vnc-socket')
    vncserver = which('vncserver')

    if vncserver:
        vnc_args = [
            vncserver,
        ]
        socket_args = []
    else:
        # Use bundled tigervnc
        vnc_args = [
            os.path.join(HERE, 'share/tigervnc/bin/vncserver'), #older tigervnc
            #os.path.join(HERE, 'share/tigervnc/bin/x0vncserver'), #fails
            '-rfbunixpath', sockets_path,
        ]
        socket_args = [
            '--unix-target', sockets_path
        ]

    vnc_command = ' '.join(shlex.quote(p) for p in (vnc_args + [
        '-verbose',
        '-xstartup', os.path.join(HERE, 'share/xstartup'),
        '-geometry', '1680x1050',
        '-SecurityTypes', 'None',
        '-fg',
        ':1',
    ]))
    return {
        'command': [
            'websockify', '-v',
            '--web', os.path.join(HERE, 'share/web/noVNC-1.1.0'), #if you want working uncomment
            #'--web', os.path.join(HERE, 'share/web/noVNC-1.2.0'),
            '--heartbeat', '30',
            '5901',
        ] + socket_args + [
            '--',
            '/bin/sh', '-c',
            f'cd {os.getcwd()} && {vnc_command}'
        ],
        'port': 5901,
        'timeout': 30,
        'mappath': {'/': '/vnc_lite.html'}, #uncomment if you want it to work (1.1.0) has websocket error w/ 1.2.0
        #'mappath': {'/': '/vnc.html'}, #fails w/ tigervnc or turbovnc regardless
        #"ws://127.0.0.1:8888/websockify"
        #some websocket error, investigate, same websocket error with 1.2.0
        #
        #'mappath': {'/': '/vnc_jose.html'},
        'new_browser_window': True
    }
