import os
import unittest
import shutil
import mock
from mock import patch, Mock, call

from v4.bridge import get_siblings as get
from v4.wordnet import get_word, caller, NOUN, VERB, ADJ, ALL


class TestWordnet(unittest.TestCase):

    @patch('v4.wordnet.subprocess')
    def test_caller_setup_call(self, subproc):

        app_path = "app_path"
        out_base = "/output-dir"

        get = caller(['ALL'], app_path=app_path, output_dir=out_base)

        res1 = get('egg', to_file=None)
        res2 = get('egg', to_file=False)
        res3 = get('egg', to_file=True)
        res4 = get('egg', to_file='egg.txt')

        result = subproc.run.call_args_list
        expected = [
            call(['app_path', 'egg', '-ALL', '>', 'C:\\output-dir\\egg-ALL.txt'],
                shell=True,
                stderr=subproc.PIPE,
                stdout=subproc.PIPE,
                timeout=5),

             call(['app_path', 'egg', '-ALL'],
                shell=True,
                stderr=subproc.PIPE,
                stdout=subproc.PIPE,
                timeout=5),

             call(['app_path', 'egg', '-ALL', '>', '/output-dir\\egg-ALL.txt'],
                shell=True,
                stderr=subproc.PIPE,
                stdout=subproc.PIPE,
                timeout=5),

             call(['app_path', 'egg', '-ALL', '>', '/output-dir\\egg.txt'],
                shell=True,
                stderr=subproc.PIPE,
                stdout=subproc.PIPE,
                timeout=5),
        ]

        #for index, item in enumerate(expected):
        #    self.assertTrue(item in expected, 'Test call {}'.format(index))

        self.assertEqual(subproc.run.call_count, 4)
        self.assertListEqual(result, expected)
