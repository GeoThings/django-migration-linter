# Copyright 2019 3YOURMIND GmbH

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import os
import sys
import re

from .constants import MIGRATION_FOLDER_NAME


def is_django_project(path):
    django_manage_file = os.path.join(path, "manage.py")
    return os.path.isfile(django_manage_file)


def is_directory(path):
    return os.path.isdir(path)


def print_stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def find_project_settings_module(path):
    """Explore path recursively to the first settings.py file
    and translate the name to package notation 'mysite.settings'
    """
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name == "settings.py":
                return (
                    os.path.join(root.replace(path, ""), file_name)
                    .replace(os.sep, ".")
                    .rstrip(".py")
                )


def split_path(path):
    decomposed_path = []
    while 1:
        head, tail = os.path.split(path)
        if head == path:  # sentinel for absolute paths
            decomposed_path.insert(0, head)
            break
        elif tail == path:  # sentinel for relative paths
            decomposed_path.insert(0, tail)
            break
        else:
            path = head
            decomposed_path.insert(0, tail)

    if not decomposed_path[-1]:
        decomposed_path = decomposed_path[:-1]
    return decomposed_path


def split_migration_path(migration_path):
    decomposed_path = split_path(migration_path)
    for i, p in enumerate(decomposed_path):
        if p == MIGRATION_FOLDER_NAME:
            return decomposed_path[i - 1], os.path.splitext(decomposed_path[i + 1])[0]


def compose_migration_path(django_folder, app_name, migration):
    return os.path.join(
        django_folder, app_name, MIGRATION_FOLDER_NAME, "{0}.py".format(migration)
    )


def clean_bytes_to_str(byte_input):
    return byte_input.decode("utf-8").strip()


def parse_unapplied_migrations(filename):
    target = {}
    app_name = None
    migrations = []

    with open(filename, 'r') as migration_file:
        for line in [line.strip() for line in migration_file.readlines()]:
            app_name_match = re.match(r"^([a-zA-Z0-9_\.]*)$", line)
            migration_name_match = re.match(r"^\s*\[\s\]\s*([a-zA-Z0-9_\.]*)$", line)

            if app_name_match and len(app_name_match.groups()) == 1:
                if app_name and len(migrations) > 0:
                    target[app_name] = migrations
                    migrations = []

                app_name = app_name_match.groups()[0]
            elif migration_name_match and len(migration_name_match.groups()) == 1:
                migrations.append(migration_name_match.groups()[0])

    if app_name and len(migrations) > 0:
        target[app_name] = migrations
    return target
