# -*- coding: utf-8 -*-
# (c) 2021, Alexei Znamensky <russoz@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import os
import subprocess

from andeboxlib.actions.base import AndeboxAction
from andeboxlib.exceptions import AndeboxException


def _make_default_tox_ini():
    return """; andebox tox-test's tox.ini -- this file is not overwritten by andebox
[tox]
isolated_build = true
envlist = 29, 210, 211, a3, a4, dev
skipsdist = true

[testenv]
passenv = PWD HOME
skip_install = true
allowlist_externals = andebox
deps =
  andebox
  29: ansible>=2.9,<2.10
  210: ansible-base>=2.10,<2.11
  211: ansible-core>=2.11,<2.12
  a3: ansible>=3.0.0,<4.0.0
  a4: ansible>=4.0.0,<5.0.0
  dev: https://github.com/ansible/ansible/archive/devel.tar.gz
commands = andebox test -- {posargs}
"""


class ToxTestError(AndeboxException):
    pass


class ToxTestAction(AndeboxAction):
    name = "tox-test"
    help = "runs ansible-test within tox, for testing in multiple ansible versions"
    args = [
        dict(names=("--env", "-e"),
             specs=dict(help="tox environments to run the test in")),
        dict(names=("--list", "-l"),
             specs=dict(action="store_true", help="list all tox environments (tox -a)")),
        dict(names=("ansible_test_params", ),
             specs=dict(nargs="*")),
    ]
    tox_ini_filename = ".andebox-tox-test.ini"

    def make_parser(self, subparser):
        action_parser = super().make_parser(subparser)
        action_parser.epilog = "Notice the use of '--' to delimit andebox's options from tox's"
        action_parser.usage = "%(prog)s usage: andebox tox-test [-h] [--env ENV] -- [ansible_test_params ...]"

    def run(self, args):
        if not os.path.exists(self.tox_ini_filename):
            with open(self.tox_ini_filename, "w") as tox_ini:
                tox_ini.write(_make_default_tox_ini())

        cmd_args = ["tox", "-c", self.tox_ini_filename]
        if args.list:
            cmd_args.append("-a")
        if args.env:
            cmd_args.extend(["-e", args.env])
        cmd_args.append("--")
        cmd_args.extend(args.ansible_test_params)
        rc = subprocess.call(cmd_args)

        if rc != 0:
            raise ToxTestError("Error running tox (rc={0})".format(rc))
