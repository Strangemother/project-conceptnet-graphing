import os
import unittest
import shutil
import mock
from mock import patch


from database.db import DB, AppendableDB, GRow, MAX_BYTES
from database.graph import GraphDB, ObjectDB


TEST_WRITE_ENV = "E:/conceptnet/_lmdb_test/"


class TestDB(unittest.TestCase):

    def setUp(self):

        self.db = DB(directory=TEST_WRITE_ENV)

    def tearDown(self):
        if hasattr(self.db, 'env'):
            self.db.env.close()

        if os.path.isdir(TEST_WRITE_ENV):
            shutil.rmtree(TEST_WRITE_ENV)
            self.assertFalse(os.path.exists(TEST_WRITE_ENV), 'tearDown did not Delete Test Directory.')

    def test_open(self):
        """Open a new DB, asserting the new directory data"""
        self.db.open('test')
        self.assertEqual(self.db.env.path(), TEST_WRITE_ENV)
        self.assertTrue(os.path.exists(self.db.env.path()))

    @patch('lmdb.open')
    def test_make_directory(self, lmdb_open):
        """Open a new DB, asseting the correct library methods are used"""
        self.db.open('test')
        args = self.db._open_args(map_size=MAX_BYTES)
        lmdb_open.assert_called_with(TEST_WRITE_ENV, **args)

    def test_put(self):
        """Add a key value and assert its existence"""
        self.db.open('test_put')
        key, value = b'my_test_key', b'my test value'
        success = self.db.put(key, value)
        self.assertTrue(success)

        result = self.db.get(key)
        self.assertEqual(result, value)

    def test_delete(self):
        """Add a key with put(), then delete. More deletes should yield false."""
        # Use put for an input.
        self.test_put()
        key, value = b'my_test_key', b'my test value'

        success = self.db.delete(key)
        self.assertTrue(success)

        success = self.db.delete(key)
        # not thing to delete the second time
        self.assertFalse(success)
        success = self.db.delete(key)
        self.assertFalse(success)

    def test_commit(self):
        """put() a key and commit
        """

        # First we assert the death of non persistent put() delete
        self.db.open('test_commit')

        key, value = b'commit_key', b'my test value'
        success = self.db.put(key, value, save=True)
        self.assertTrue(success)

        success = self.db.delete(key, commit=False)
        self.assertTrue(success)

        result = self.db.get(key)
        self.assertEqual(result, None)

        # close and open-
        self.db.close()
        self.setUp()
        self.db.open('test_commit')

        # Should exist due to persistent write
        result = self.db.get(key)
        self.assertEqual(result, value)

        # Now delete.
        success = self.db.delete(key, commit=False)
        self.assertTrue(success)
        # store the change
        self.db.commit()

        # Delete and remake -
        self.tearDown()
        self.setUp()
        self.db.open('test_commit')

        # Should not exist due to commit()
        result = self.db.get(key)
        self.assertEqual(result, None)


    def test_in_out_conversion(self):
        self.db.open('test_commit')

        result = self.db.put('apples', '[1,24,54,6,56]')
        self.assertTrue(result)

        result = self.db.get('apples')
        self.db.put('apples', [1,24,54,6,56])

        result = self.db.get('apples')
        self.assertEqual(result, [1,24,54,6,56])
        self.assertIsInstance(result, list)

    def test_tuple_store(self):
        self.db.open('test_commit')
        self.db.put('nums', (1,2,3,4,5,6,7,8,))
        self.assertIsInstance(self.db.get('nums'), tuple)

    def test_list_store(self):
        self.db.open('test_commit')
        self.db.put('list', [1,2,3,4,5])
        res = self.db.get('list')
        self.assertIsInstance(self.db.get('list'), list)

    def test_collect(self):
        self.db.open('test_collect')
        self.db.delete('collect')
        self.db.put('collect', (1,2,3,4,5,))
        self.db.put('collect', (5,4,3,2,1,))

        result = self.db.collect('collect')

        self.assertEqual(len(list(result)), 2)

    def test_dict_store(self):
        self.db.open('test_commit')

        de = {'foo': 1, 'bar': 'two', 'three': True}
        self.db.put('dict', de)

        res = self.db.get('dict')

        expected = {'foo': 1, 'bar': 'two', 'three': True}

        self.assertDictEqual(res, expected)


class TestAppendableDB(unittest.TestCase):

    def setUp(self):
        self.db = AppendableDB(directory=TEST_WRITE_ENV)

    def tearDown(self):
        if hasattr(self.db, 'env'):
            self.db.env.close()

        if os.path.isdir(TEST_WRITE_ENV):
            shutil.rmtree(TEST_WRITE_ENV)
            self.assertFalse(os.path.exists(TEST_WRITE_ENV), 'tearDown did not Delete Test Directory.')

    def test_dict_byte_string(self):
        self.db.open('test')

        de = {'foo': 1, 'bar': 'two', 'three': True}
        expected = {'foo': 1, 'bar': 'two', 'three': True}

        self.db.put('dict', de)

        res = self.db.get('dict')


        self.assertDictEqual(res, expected)

        res = self.db.get('dict', convert=False)
        expected = b"!:ADict!:{'foo': 1, 'bar': 'two', 'three': True}"
        self.assertEqual(res, expected)

    def test_tuple_convert(self):
        dd=self.db
        dd.open('test_commit')
        result = dd.encode((1,))
        expected = b'!:ATuple!:1,'
        self.assertEqual(result, expected)

        result = dd.encode((1))
        expected = b'!:Appendable!:1'
        self.assertEqual(result, expected)

        result = dd._convert_in( (1,) )
        expected = b'!:ATuple!:1,'
        self.assertEqual(result, expected)

        result = dd._convert_in( (1) )
        expected = b'!:Appendable!:1'
        self.assertEqual(result, expected)

        result = dd._convert_in( (1,) )
        expected = b'!:ATuple!:1,'
        self.assertEqual(result, expected)

        result = dd._convert_in( [1,] )
        expected = b'!:AList!:1,'
        self.assertEqual(result, expected)

        result = dd._convert_in( [1] )
        expected = b'!:AList!:1,'
        self.assertEqual(result, expected)

        result = dd._convert_in( (1,2) )
        expected = b'!:ATuple!:1, 2,'
        self.assertEqual(result, expected)

        result = dd._convert_in( (1,2,) )
        expected = b'!:ATuple!:1, 2,'
        self.assertEqual(result, expected)


    def test_tuple_put_append_get(self):
        db = self.db
        db.open('test_tuples')

        key = 'poppy'
        ta = (10,11,12,)
        tb = (1,2,3)
        db.delete(key)

        db.put(key, ta)
        db.append(key, tb)
        c_list = db.collect(key, convert=False)
        self.assertEqual(len(c_list), 1)

        result = db.get(key)
        expected = ta + tb
        self.assertTupleEqual(result, expected)

        # >>> dd.collect('apples')
        # Converting b'!:ATuple!:1, 2, 3, 4,'
        # Converting ATuple.convert(1, 2, 3, 4,)
        # ((1, 2, 3, 4),)
        # >>> dd.collect('apples', convert=False)
        # (b'!:ATuple!:1, 2, 3, 4,',)
        # >>> dd.append('apples', (1,2,3,4))
        # b'!:ATuple!:1, 2, 3, 4,1, 2, 3, 4,'
        # (Pdb) c
        # b'!:ATuple!:1, 2, 3, 4,'
        # >>> dd.collect('apples', convert=False)
        # (b'!:ATuple!:1, 2, 3, 4,1, 2, 3, 4,',)
        # >>>
        #
    def test_encode(self):
        expected =  b"!:ADict!:{'foo': 1, 'bar': 'two', 'three': True}"
        de = dict(foo=1, bar='two', three=True)
        dict_encode = self.db.encode(de)

        self.assertEqual(dict_encode, expected)

    def test_dict_append(self):
        self.db.open('test')
        self.db.delete('dict')

        expected = {'foo': 2, 'bar': 'two', 'three': True, 'dee': 2}
        de = {'foo': 2, 'bar': 'two', 'three': True, 'dee': 2}
        self.db.put('dict', de)

        result = self.db.get('dict')

        self.assertDictEqual(result, expected)

        self.db.append('dict', dict(apples=2, hammond='hampster'))
        result = self.db.get('dict')

        expected = {'foo': 2, 'bar': 'two', 'three': True, 'dee': 2, 'apples': 2, 'hammond': 'hampster'}
        self.assertDictEqual(result, expected)

    def test_convert_out(self):

        result = self.db._convert_out(b"!:ADict!:{'foo': 1, 'bar': 'two', 'three': True},{'foo': 2, 'dee': 2}")
        #Converting b"!:ADict!:{'foo': 1, 'bar': 'two', 'three': True},{'foo': 2, 'dee': 2}"
        #Converting ADict.convert({'foo': 1, 'bar': 'two', 'three': True},{'foo': 2, 'dee': 2})
        expected = {'foo': 2, 'bar': 'two', 'three': True, 'dee': 2}
        self.assertDictEqual(result, expected)


    def test_abool(self):
        self.db.open('test')
        self.db.put('banana', False)
        result = self.db.get('banana')
        self.assertFalse(result)

        self.db.put('banana good', True)
        result = self.db.get('banana good')
        self.assertTrue(result)

        expected = (False, False, True, True)
        self.db.put('bananas choice', expected)
        result = self.db.get('bananas choice')
        self.assertTupleEqual(result, expected)


class TestGraphDB(unittest.TestCase):

    TestClass = GraphDB

    def test_cursor(self):
        gb = self.TestClass(name='test_graph')
        gb.wipe()

        result = list(gb.cursor.iternext(keys=True, values=True))
        self.assertListEqual(result, [])

        gb.add('milk', 'isa', 'greeting', 3.4, 'hello')

        result = list(gb.cursor.iternext(keys=True, values=True))
        expected = [(b'milk', b"!:GRow!:'milk', 'isa', 'greeting', 3.4, 'hello'")]
        self.assertListEqual(result, expected)

    def test_iter_one(self):
        gb = self.TestClass(name='test_graph')
        gb.wipe()

        result = list(gb.iter(convert=False))
        self.assertListEqual(result, [])

        gb.add('milk', 'isa', 'greeting', 3.4, 'hello')

        result = gb.collect('milk')
        # Converting b"!:GRow!:('milk', 'isa', 'greeting', 3.4, 'hello')"
        # Converting GRow.convert(('milk', 'isa', 'greeting', 3.4, 'hello'))
        self.assertEqual(len(result), 1)

        result = gb.collect('Hello')
        # Add: milk (hello) isa greeting (3.4)
        self.assertEqual(len(result), 0)

        result = list(gb.iter(convert=False))
        expected = [('milk', b"!:GRow!:'milk', 'isa', 'greeting', 3.4, 'hello'")]
        self.assertListEqual(result, expected)

    def test_add(self):
        word = 'Hello'

        gb = self.TestClass(name='test_graph')
        gb.wipe()

        gb.add('milk', 'isa', 'nothin', 1, 'hello')
        gb.add(word, 'isa', 'greeting', 3.4, 'hello')
        gb.add(word, 'isa', 'word', 3, 'hello')
        gb.add(word, 'isa', 'another', 1, 'hello')

        result = list(gb.iter())

        self.assertEqual(len(result), 4)
        self.assertEqual(len(gb.collect(word)), 3)
        result = gb.get(word)
        self.assertIsInstance(result, GRow)


    def test_edge_walk(self):
        gb = self.TestClass(name='graph_pick')
        gb.wipe()

        key='Hello'

        gb.add(key, 'isa', 'greeting', 3.4, 'hello')
        gb.add(key, 'isa', 'word', 3, 'hello')
        gb.add(key, 'isa', 'another', 1, 'hello')
        gb.add('greeting', 'similarto', 'Hello', 2)

        p = gb.pick(key)
        result = p.isa.greeting.similarto.Hello.graph.isa.greeting.value
        self.assertEqual(result, 'greeting')
        result = p.isa.greeting.similarto.Hello.isa.another.value
        self.assertEqual(result, 'another')

    def test_parent_walk(self):

        gb = self.TestClass(name='graph_walk')
        gb.wipe()

        key='Hello'

        gb.add(key, 'isa', 'greeting', 3.4, 'hello')
        gb.add(key, 'isa', 'word', 3, 'hello')
        gb.add(key, 'isa', 'another', 1, 'hello')
        gb.add('greeting', 'similarto', 'Hello', 2)

        p = gb.pick(key)
        result =( p.isa.greeting
            .similarto.Hello
            .isa.word
            # hello
            .parent_graph
            # greeting
            .parent_graph
            # Hello
            .parent_graph
            # None!
            .parent_graph )

        self.assertIsNone(result, gb)

    def _hello_law_chain(self, gb):
        p = gb.pick('Hello')

        law_chain =( p
            .isa
                .greeting
            .similarto
                .hi
            .isa
                .greeting
            .similarto
                .Hello
            .isa
                .word
            .isa
                .thing
            .etomology
                .law)

        return law_chain

    def test_edgenode_walk(self):
        gb = self._cheap_graphdb()
        law_chain = self._hello_law_chain(gb)

        result = [x.value for x in law_chain.edgenode_chain(True)]
        expected = ['law', 'thing', 'word', 'Hello', 'greeting', 'hi', 'greeting']
        self.assertListEqual(result, expected)

    def _cheap_graphdb(self, key='Hello'):
        gb = self.TestClass(name='graph_edgenode')
        gb.wipe()

        gb.add(key, 'isa', 'greeting', 3.4, key)
        gb.add(key, 'isa', 'word', 3, key)
        gb.add(key, 'isa', 'another', 1, key)

        gb.add('greeting', 'similarto', key, 2)
        gb.add('greeting', 'similarto', 'hi', 2)
        gb.add('greeting', 'isa', 'welcome', 2)
        gb.add('hi', 'isa', 'greeting', 3)
        gb.add('word', 'isa', 'word', 1)
        gb.add('word', 'isa', 'thing', 1)
        gb.add('thing', 'etomology', 'law', 2)

        return gb

    def test_self_cheap_graphdb(self):
        """Test the test function "_cheap_graphdb"""
        gb = self._cheap_graphdb()
        self.assertIsInstance(gb, self.TestClass)
        self.assertEqual(len(gb.collect('Hello')), 3)
        self.assertEqual(len(gb.collect('greeting')), 3)
        self.assertEqual(len(gb.collect('hi')), 1)
        self.assertEqual(len(gb.collect('word')), 2)
        self.assertEqual(len(gb.collect('thing')), 1)

    def test_text_chain(self):
        gb = self._cheap_graphdb()
        chain = self._hello_law_chain(gb)
        result = chain.text_chain(True)
        expected = (
             ('thing', 'etomology', 'thing', 2),
             ('word', 'isa', 'thing', 1),
             ('Hello', 'isa', 'word', 3),
             ('greeting', 'similarto', 'Hello', 2),
             ('hi', 'isa', 'greeting', 3),
             ('greeting', 'similarto', 'hi', 2),
             ('Hello', 'isa', 'greeting', 3.4),
         )

        self.assertTupleEqual(result, expected)

    def test_parent_edgenode_walk(self):
        gb = self._cheap_graphdb()
        p = gb.pick('Hello')
        result = (p
                .isa
                .greeting
                .similarto
                .hi
                # 1
                .isa
                # Target.
                .greeting
                .similarto
                .Hello
                # 2
                .isa
                .word
                # 3
                .isa
                .thing
                .parent_edgenode
                .parent_edgenode
                .parent_edgenode

                )


        self.assertEqual(result.edge_type, 'isa')
        self.assertEqual(result.value, 'greeting')
        self.assertEqual(result.weight, 3)


class TestObjectDB(TestGraphDB):
    TestClass = ObjectDB

    def test_cursor(self):
        pass

    def test_dump(self):
        gb = self._cheap_graphdb()
        self.assertDictEqual(
            ObjectDB(load=gb.dump()).dump(),
            gb.dump())

    def test_create_index(self):
        """Assert a created index is the same as a natural index."""
        gb = self._cheap_graphdb()
        self.assertDictEqual(
            gb.create_index(gb._data),
            gb.index,
        )

    def test_create_index_dump_without_index(self):
        gb = self._cheap_graphdb()

        data = gb.dump(with_index=False)
        # ensure the index attribute is missing
        self.assertFalse('index' in data)

        # assert a recreation
        db = self.TestClass(load=data)
        self.assertDictEqual(gb.index, db.index)