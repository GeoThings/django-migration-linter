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

import unittest

from django_migration_linter.utils import split_path


class SplitPathTest(unittest.TestCase):
    def test_split_path(self):
        split = split_path('foo/bar/fuz.py')
        self.assertEqual(split, ["foo", "bar", "fuz.py"])

    def test_split_full_path(self):
        split = split_path('/foo/bar/fuz.py')
        self.assertEqual(split, ["/", "foo", "bar", "fuz.py"])

    def test_split_folder_path(self):
        split = split_path('/foo/bar')
        self.assertEqual(split, ["/", "foo", "bar"])

    def test_split_folder_path_trailing_slash(self):
        split = split_path('/foo/bar/')
        self.assertEqual(split, ["/", "foo", "bar"])

    def test_split_folder_path_trailing_slashes(self):
        split = split_path('/foo/bar///')
        self.assertEqual(split, ["/", "foo", "bar"])
