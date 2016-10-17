#!/usr/local/bin/python3
# Use C-c C-j to search
# AnnotationTester is the class - first function test_good_values

import unittest
import argparse
from collections import OrderedDict
from collections import namedtuple

from annotate_test import annotate_test

# Global variable area for constants
# debug_except = input("Debug exceptions? y/n : ")
# debug_except = str(debug_except)[0]


def debug(self, func, args, kwargs):
    with self.assertRaises(ValueError):
        try:
            func(*args, **kwargs)
        except ValueError as e:
            print("##DEBUG EXCEPTION in {} ##".format(func.__name__))
            print("Values: ", args, kwargs)
            print("ValueError returned msg")
            print(e)
            print('')
            raise


def assert_pass(self, cases):
    for answer, func, args, kwargs in cases:
        self.assertEqual(answer, func(*args, **kwargs))


def assert_fail(self, cases):
    for answer, func, args, kwargs in cases:
        if debug_except.upper() == "Y":
            debug(self, func, args, kwargs)
        self.assertRaises(ValueError, func, *args, **kwargs)


# Global variable area (for functions and classes):


class BlankClass(object):
    """This is a BlankClass to test.  It will allow an instance."""

    def __init__(self, a, b):
        self.a = a
        self.b = b

    @staticmethod
    def functiontest(a, b):
        return a + b


def basicfunc(a, b):
    return a + b


def twofuncy(c, d):
    return c + d
# Area for functions to test

# Area for namedtuple
tupname = namedtuple('tupname', ('one', 'two', 'three'))
dif_namedtuple = namedtuple('different', ('one', 'two', 'three'))

# Odd semantic testing (Complete)


@annotate_test
def missing_annotation(a, b: 'str', c: 'int'):
    return (a, b + str(c))

# bool only has type (Complete)


@annotate_test
def f_bool(a: 'bool', b: 'bool') -> 'bool':
    return a ^ b  # Return xor of a and b


@annotate_test
def f_broken_bool(a: 'bool', b: 'bool') -> 'str':
    return a ^ b

# str only has type (Complete)


@annotate_test
def f_str(a: 'str', b: 'str'='default') -> 'str':
    return a + b


# int only has type (Complete)


@annotate_test
def f_int(a: 'int', b: 'int') -> 'int':
    return a + b


# float only has type (Complete)


@annotate_test
def f_float(a: 'float', b: 'float') -> 'float':
    return a + b


# complex only has type (Complete)


@annotate_test
def f_complex(a: 'complex', b: 'complex') -> 'complex':
    return a + b

# bytes only has type (Complete)


@annotate_test
def f_bytes(a: 'bytes', b: 'bytes') -> 'bytes':
    return a + b

# bytearray only has type (Complete)


@annotate_test
def f_bytearray(a: 'bytearray', b: 'bytearray') -> 'bytearray':
    return a + b


# Class has match to a class type (Complete)


@annotate_test
def f_Class(a: 'Class BlankClass',
            b: 'Class BlankClass'
            )->'tuple[Class BlankClass, Class BlankClass]':
    return a, b


# ClassInst has match against a class

@annotate_test
def f_ClassInst(a: 'ClassInst BlankClass',
                b: 'ClassInst BlankClass'
                ) -> 'tuple[ClassInst BlankClass]':
    return a, b

# Func testing method has type and match (Completed)


@annotate_test
def f_Func_type(a: 'Func') -> 'Func':
    return a


@annotate_test
def f_Func_static(
        a: 'Func BlankClass.functiontest',
        b: 'Func BlankClass.functiontest'
) -> 'tuple[Func BlankClass.functiontest, Func BlankClass.functiontest]':
    return a, b


@annotate_test
def f_Func_match(a: 'Func basicfunc') -> 'Func basicfunc':
    return a

# tuple has type, single, positional and group (Completed)


@annotate_test
def f_tuple_t(a: 'tuple') -> 'tuple':
    return a


@annotate_test
def f_tuple_s(a: 'tuple[int]') -> 'tuple[int]':
    return a


@annotate_test
def f_tuple_p(a: 'tuple[int, str]') -> 'tuple':
    return a


@annotate_test
def f_tuple_g(a: 'tuple[int|str]') -> 'tuple[int|str]':
    return a

# frozenset has type and group (Completed)


@annotate_test
def f_frozenset_t(a: 'frozenset') -> 'frozenset':
    return a


@annotate_test
def f_frozenset_g(a: 'frozenset[int|str]') -> 'frozenset[int|str]':
    return a

# set has type and group (Completed)


@annotate_test
def f_set_t(a: 'set') -> 'set':
    return a


@annotate_test
def f_set_g(a: 'set[int|str]') -> 'set[int|str]':
    return a

# list has type, positional, single and group (Completed)


@annotate_test
def f_list_t(a: 'list') -> 'list':
    return a


@annotate_test
def f_list_p(a: 'list[int, str]') -> 'list':
    return a


@annotate_test
def f_list_g(a: 'list[int|str]') -> 'list':
    return a

# OrderedDict has type, positional, grouped, key only and value only
# (Completed)


@annotate_test
def f_OrderedDict_t(a: 'OrderedDict') -> 'OrderedDict':
    return a


@annotate_test
def f_OrderedDict_p(a: 'OrderedDict[str=int,bytes=str]') -> 'OrderedDict':
    return a


@annotate_test
def f_OrderedDict_g(a: 'OrderedDict[str|bytes=bytes|int') -> 'OrderedDict':
    return a


@annotate_test
def f_OrderedDict_key_only(a: 'OrderedDict[str|bytes]') -> 'OrderedDict':
    return a


@annotate_test
def f_OrderedDict_value_only(a: 'OrderedDict[=int|bytes]') -> 'OrderedDict':
    return a


# dict has type, group, key only and value only
#   (group is done only against values as keys are hashable)
# (Completed)


@annotate_test
def f_dict_t(a: 'dict') -> 'dict':
    return a


@annotate_test
def f_dict_g(a: 'dict[str=int]') -> 'dict':
    return a


@annotate_test
def f_dict_key_only(a: 'dict[str|bytes') -> 'dict':
    return a


@annotate_test
def f_dict_value_only(a: 'dict[=int|bytes') -> 'dict':
    return a


# namedtuple has type, positional and group
# (Completed)


@annotate_test
def f_namedtuple_t(a: 'namedtuple'):
    """This is to match namedtuple type"""
    return a


@annotate_test
def f_namedtuple_n(a: 'namedtuple(tupname)'):
    """This is to match name of tuple"""
    return a


@annotate_test
def f_namedtuple_p(a: 'namedtuple(tupname[int, bytes, str])'):
    return a


@annotate_test
def f_namedtuple_g(a: 'namedtuple(tupname[int|str])'):
    return a


class AnnotationTester(unittest.TestCase):
    """AnnotationTester will test simple and complex annotation
syntax.  Tests will be built from simple to complex cases."""

    # Return testing / broken

    def test_broken_return(self):
        """Return value exceptions"""
        known_exceptions = (
            (True, f_broken_bool, (True, True), dict()),
        )
        assert_fail(self, known_exceptions)

    # Odd semantic testing
    def test_good_missing_annotation(self):
        """This tests for semantic issues around missing annotations"""
        known_good = (
            (('Hello', 'Next5'), missing_annotation,
             ('Hello', 'Next'), dict(c=5)),
            (('Why', 'Now10'), missing_annotation,
             ('Why',), dict(c=10, b='Now'))
        )
        assert_pass(self, known_good)

    def test_except_missing_annotation(self):
        known_exceptions = (
            ('n/a', missing_annotation, (4, 5), dict()),
            ('n/a', missing_annotation, (), dict(a='No', c=40, b=20))
        )
        assert_fail(self, known_exceptions)

    # bool has type only (Complete)

    def test_good_bool(self):
        """Bool known good"""
        known_good = (
            (True, f_bool, (True, False), dict()),
            (False, f_bool, (False,), dict(b=False))
        )
        assert_pass(self, known_good)

    def test_except_bool(self):
        """Bool exceptions"""
        known_exceptions = (
            (True, f_bool, (3, False), dict()),  # With int in args
            (True, f_bool, (True,), dict(b=3)),  # With int in keyword
        )
        assert_fail(self, known_exceptions)

    # str has type only (Complete)
    def test_good_str(self):
        """String known good"""
        known_good = (
            ('yesno', f_str, ('yes', 'no'), dict()),
            ('yesno', f_str, ('yes', ), dict(b='no')),
            ('yesno', f_str, (), dict(a='yes', b='no')),
        )
        assert_pass(self, known_good)

    def test_except_str(self):
        """String exceptions"""
        known_exceptions = (
            ('n/a', f_str, (3, 'no'), dict()),
            ('n/a', f_str, ('no',), dict(b=3)),
            ('n/a', f_str, (), dict(a='no', b=3))
        )
        assert_fail(self, known_exceptions)

    # int has type only (Complete)
    def test_good_int(self):
        """Int known good"""
        known_good = (
            (20, f_int, (7, 13), dict()),
            (20, f_int, (12,), dict(b=8)),
            (20, f_int, (), dict(a=-22, b=42))
        )
        assert_pass(self, known_good)

    def test_except_int(self):
        """Int exceptions"""
        known_exceptions = (
            ('n/a', f_int, ('ten', 10), dict()),
            ('n/a', f_int, (19,), dict(b=True)),
            ('n/a', f_int, (), dict(a=True, b=False))
        )
        assert_fail(self, known_exceptions)

    # float has type only (Complete)
    def test_good_float(self):
        """Float known good"""
        known_good = (
            (4.5, f_float, (2.0, 2.5), dict()),
            (4.5, f_float, (1.3,), dict(b=3.2)),
            (4.5, f_float, (), dict(a=5.9, b=-1.4))
        )
        assert_pass(self, known_good)

    def test_except_float(self):
        """Float exceptions"""
        known_exceptions = (
            ('n/a', f_float, (3, 4.0), dict()),
            ('n/a', f_float, (3.5,), dict(b=10)),
            ('n/a', f_float, (), dict(a=3, b='str'))
        )
        assert_fail(self, known_exceptions)

    # complex has type only (Complete)
    def test_good_complex(self):
        """Complex known good"""
        known_good = (
            (5 + 6j, f_complex, (3 + 3j, 2 + 3j), dict()),
            (5 + 6j, f_complex, (3 + 3j,), dict(b=2 + 3j)),
            (5 + 6j, f_complex, (), dict(a=3 + 3j, b=2 + 3j))
        )
        assert_pass(self, known_good)

    def test_except_complex(self):
        """Complex exceptions"""
        known_exceptions = (
            ('n/a', f_complex, (4, 3 + 10j), dict()),
            ('n/a', f_complex, (4,), dict(b=3 + 10j)),
            ('n/a', f_complex, (), dict(a=3 + 4j, b=True))
        )
        assert_fail(self, known_exceptions)

    # bytes has type only (Complete)
    def test_good_bytes(self):
        """Bytes known good"""
        known_good = (
            (b'test yes', f_bytes, (b'test', b' yes'), dict()),
            (b'test yes', f_bytes, (b'test',), dict(b=b' yes')),
            (b'test yes', f_bytes, (), dict(a=b'test', b=b' yes'))
        )
        assert_pass(self, known_good)

    def test_except_bytes(self):
        """Bytes exceptions"""
        known_exceptions = (
            ('n/a', f_bytes, (4, b'yes'), dict()),
            ('n/a', f_bytes, (b'test',), dict(b=' yes')),
            ('n/a', f_bytes, (), dict(a=b'test', b=True))
        )
        assert_fail(self, known_exceptions)

    # bytearray has type only (Complete)
    def test_good_bytearray(self):
        """Bytearray known good"""
        known_good = (
            (bytearray(b'test yes'), f_bytearray,
             (bytearray(b'test'), bytearray(b' yes')), dict()),
            (bytearray(b'test yes'), f_bytearray,
             (bytearray(b'test '),), dict(b=bytearray(b'yes'))),
            (bytearray(b'test yes'), f_bytearray,
             (), dict(a=bytearray(b'test'), b=bytearray(b' yes')))
        )
        assert_pass(self, known_good)

    def test_except_bytearray(self):
        """Bytearray exceptions"""
        known_exceptions = (
            (bytearray(b'n/a'), f_bytearray,
             (bytes(b'test'), bytearray(b' yes')), dict()),
            (bytearray(b'n/a'), f_bytearray,
             (bytearray(b'test '),), dict(b=bytes(b'yes'))),
            (bytearray(b'n/a'), f_bytearray,
             (), dict(a=b'test', b=bytearray(b' yes')))
        )
        assert_fail(self, known_exceptions)
    # Class has type and match only (Complete)
    # Note: that can't type check except with match

    def test_good_class(self):
        """Class known good"""
        t = BlankClass
        known_good = (
            ((t, t), f_Class, (BlankClass, BlankClass), dict()),
            ((t, t), f_Class, (BlankClass,), dict(b=BlankClass)),
            ((t, t), f_Class, (), dict(a=BlankClass, b=BlankClass))
        )
        assert_pass(self, known_good)

    def test_except_class(self):
        """Class exceptions"""
        known_exceptions = (
            ('n/a', f_Class, (BlankClass(3, 5),), dict(b=BlankClass)),
            ('n/a', f_Class, (4,), dict(b=6)),
            ('n/a', f_Class, (), dict(a=BlankClass, b=BlankClass(4, 5)))
        )
        assert_fail(self, known_exceptions)

    # ClassInst has type and match (Complete)
    # Note: can only check type against a match
    def test_good_classInst(self):
        """ClassInst known good"""
        t = BlankClass(30, 20)
        s = BlankClass(10, 20)
        known_good = (
            ((s, s), f_ClassInst,
             (t,), dict(b=t)),
            ((s, s), f_ClassInst,
             (t, t), dict()),
            ((s, s), f_ClassInst,
             (), dict(a=t, b=t))
        )
        for answer, func, args, kwargs in known_good:
            # Mapping needed to test that all instances from the same class
            l = list(map(lambda x, y: (x, y), answer, func(*args, **kwargs)))
            for results in l:
                self.assertEqual(results[0].__class__, results[1].__class__)

    def test_except_classInst(self):
        """ClassInst exceptions"""
        known_exceptions = (
            ('n/a', f_ClassInst, (BlankClass,), dict()),
            ('n/a', f_ClassInst, (5,), dict()),
            ('n/a', f_ClassInst, (BlankClass.functiontest(3, 5),), dict())
        )
        assert_fail(self, known_exceptions)

    # Func has type and match (Complete)

    def test_good_func_type(self):
        """Test checking if value is a function type"""
        known_good = (
            (basicfunc, f_Func_type, (basicfunc,), dict()),
            (twofuncy, f_Func_type, (), dict(a=twofuncy))
        )
        assert_pass(self, known_good)

    def test_except_func_type(self):
        """Test to check for exceptions on Func type"""
        known_exceptions = (
            ('n/a', f_Func_type, (4,), dict()),
            ('n/a', f_Func_type, (), dict(a=b'Hello'))
        )
        assert_fail(self, known_exceptions)

    def test_good_static_func(self):
        """Static Function known good"""
        t = BlankClass.functiontest
        known_good = (
            ((BlankClass.functiontest, BlankClass.functiontest), f_Func_static,
             (BlankClass.functiontest, BlankClass.functiontest), dict()),
            ((BlankClass.functiontest, BlankClass.functiontest), f_Func_static,
             (t,), dict(b=BlankClass.functiontest)),
            ((BlankClass.functiontest, BlankClass.functiontest), f_Func_static,
             (), dict(a=t, b=t))
        )
        assert_pass(self, known_good)

    def test_except_static_func(self):
        """Static Function exceptions"""
        known_exceptions = (
            ('n/a', f_Func_static,
             (BlankClass.functiontest, basicfunc), dict()),
            ('n/a', f_Func_static,
             (basicfunc, ), dict(b=BlankClass.functiontest))
        )
        assert_fail(self, known_exceptions)

    def test_good_functions(self):
        """Func known good"""
        t = basicfunc
        known_good = (
            (basicfunc, f_Func_match, (basicfunc,), dict()),
            (basicfunc, f_Func_match, (t,), dict()),
            (basicfunc, f_Func_match, (), dict(a=t))
        )
        assert_pass(self, known_good)

    def test_except_functions(self):
        """Func exceptions"""
        known_exceptions = (
            ('n/a', f_Func_match, (3,), dict()),
            ('n/a', f_Func_match, (), dict(a='failstring'))
        )
        assert_fail(self, known_exceptions)

    # Tuple has type, single, positional and group (Complete)
    def test_good_tuple_type(self):
        """Single Tuple (Without describing type)"""
        tup_test = tuple((4, 6, 7))
        known_good = (
            ((4, 6, 7), f_tuple_t, (tup_test,), dict()),
            ((4, 6, 7), f_tuple_t, (), dict(a=tup_test))
        )
        assert_pass(self, known_good)

    def test_except_tuple_type(self):
        """Single tuple exceptions"""
        known_exceptions = (
            ('n/a', f_tuple_t, ('ten'), dict()),
            ('n/a', f_tuple_t, (), dict(a='ten'))
        )
        assert_fail(self, known_exceptions)

    def test_good_tuple_single(self):
        """This tests a single int type within a tuple"""
        known_good = (
            ((4, 6, 7), f_tuple_s, ((4, 6, 7),), dict()),
            ((4, 6, 7), f_tuple_s, (), dict(a=(4, 6, 7)))
        )
        assert_pass(self, known_good)

    def test_except_tuple_single(self):
        """This tests failures for single int type within a tuple"""
        known_exceptions = (
            ('n/a', f_tuple_s, ((4, 6, 'string'),), dict()),
            ('n/a', f_tuple_s, (), dict(a=(4, 6, 'string')))
        )
        assert_fail(self, known_exceptions)

    def test_good_tuple_positional(self):
        """This tests positional annotation for tuples"""
        known_good = (
            ((10, 'Hello'), f_tuple_p, ((10, 'Hello'),), dict()),
            ((50, 'Yup!'), f_tuple_p, (), dict(a=(50, 'Yup!')))
        )
        assert_pass(self, known_good)

    def test_except_tuple_positional(self):
        """This tests failures for positional annotation for tuples"""
        known_exceptions = (
            ('n/a', f_tuple_p, (('Test broken', 20),), dict()),
            ('n/a', f_tuple_p, (), dict(a=(20, 30)))
        )
        assert_fail(self, known_exceptions)

    def test_good_tuple_multi(self):
        """This tests multiple types (int and str) in a tuple."""
        known_good = (
            ((4, 'Hello', 6), f_tuple_g, ((4, 'Hello', 6),), dict()),
            ((4, 'Hello', 6), f_tuple_g, (), dict(a=(4, 'Hello', 6)))
        )
        assert_pass(self, known_good)

    def test_except_tuple_multi(self):
        """This tests multiple type exceptions (int, str) in a tuple."""
        byte_string = 'Hello'.encode()
        known_exceptions = (
            ('n/a', f_tuple_g, ((4, byte_string, 6),), dict()),
            ('n/a', f_tuple_g, (), dict(a=(4, byte_string, 6)))
        )
        assert_fail(self, known_exceptions)

    # frozenset has type single and multiple (Complete)
    def test_good_frozenset_single_type(self):
        """This tests that the input was a frozenset"""
        default = frozenset([4, 5, 6, 'testing', b'byte_testing'])
        known_good = (
            (frozenset([4, 5, 6]), f_frozenset_t,
             (frozenset([4, 5, 6]),), dict()),
            (frozenset([4, 5, 6]), f_frozenset_t,
             (), dict(a=frozenset([4, 5, 6]))),
            (default, f_frozenset_t, (default, ), dict()),
            (default, f_frozenset_t, (), dict(a=default))
        )
        assert_pass(self, known_good)

    def test_except_frozenset_single_type(self):
        """This tests for frozenset single_type exceptions"""
        default = int(20)
        known_exceptions = (
            ('n/a', f_frozenset_t, (default,), dict()),
            ('n/a', f_frozenset_t, (), dict(a=default))
        )
        assert_fail(self, known_exceptions)

    def test_good_frozenset_multi_type(self):
        """This tests that the input was frozenset multi_type[int|str]"""
        default = frozenset([4, 5, 6, 'testing'])
        known_good = (
            (frozenset([4, 5, 6]), f_frozenset_g,
             (frozenset([4, 5, 6]),), dict()),
            (frozenset([4, 5, 6]), f_frozenset_g,
             (), dict(a=frozenset([4, 5, 6]))),
            (default, f_frozenset_g, (default, ), dict()),
            (default, f_frozenset_g, (), dict(a=default))
        )
        assert_pass(self, known_good)

    def test_except_frozenset_multi_type(self):
        """This tests for frozenset multi_type exceptions[int|str]"""
        default = int(20)
        known_exceptions = (
            ('n/a', f_frozenset_g, (default,), dict()),
            ('n/a', f_frozenset_g, (), dict(a=default))
        )
        assert_fail(self, known_exceptions)

    # Set has type and group (Complete)
    def test_good_set_single_type(self):
        """This tests that the input was a set"""
        default = set([4, 5, 6, 'testing', b'byte_testing'])
        known_good = (
            (set([4, 5, 6]), f_set_t, (set([4, 5, 6]),), dict()),
            (set([4, 5, 6]), f_set_t, (), dict(a=set([4, 5, 6]))),
            (default, f_set_t, (default, ), dict()),
            (default, f_set_t, (), dict(a=default))
        )
        assert_pass(self, known_good)

    def test_except_set_single_type(self):
        """This tests for set single_type exceptions"""
        default = int(20)
        known_exceptions = (
            ('n/a', f_set_t, (default,), dict()),
            ('n/a', f_set_t, (), dict(a=default))
        )
        assert_fail(self, known_exceptions)

    def test_good_set_multi_type(self):
        """This tests that the input was a set[int|str]"""
        default = set(['4', 5, 6, 'testing'])
        known_good = (
            (set([4, 'Hello', 6]), f_set_g, (set([4, 'Hello', 6]),), dict()),
            (set([4, 'Hello', 6]), f_set_g, (), dict(a=set([4, 'Hello', 6]))),
            (default, f_set_g, (default, ), dict()),
            (default, f_set_g, (), dict(a=default))
        )
        assert_pass(self, known_good)

    def test_except_set_multi_type(self):
        """This tests for set multi_type exceptions[int|str]"""
        default = set([4, 5, 6, 'testing', b'byte_testing'])
        known_exceptions = (
            ('n/a', f_set_g, (default,), dict()),
            ('n/a', f_set_g, (), dict(a=default))
        )
        assert_fail(self, known_exceptions)

    # List has type and group (Complete)
    def test_good_list_type(self):
        """This tests for list type"""
        known_good = (
            ([4, 5, 6], f_list_t, ([4, 5, 6],), dict()),
            (['4', '5', '6'], f_list_t, (), dict(a=['4', '5', '6']))
        )
        assert_pass(self, known_good)

    def test_except_list_type(self):
        """This tests list type for exceptions"""
        known_exceptions = (
            ('n/a', f_list_t, (5,), dict()),
            ('n/a', f_list_t, (), dict(a='string'))
        )
        assert_fail(self, known_exceptions)

    def test_good_list_p(self):
        """This tests for list positional"""
        known_good = (
            ([4, 'hello'], f_list_p, ([4, 'hello'],), dict()),
            ([10, 'string'], f_list_p, (), dict(a=[10, 'string']))
        )
        assert_pass(self, known_good)

    def test_except_list_p(self):
        """This tests exceptions for list positional annotations"""
        known_exceptions = (
            ('n/a', f_list_p, (['Wrong', 5],), dict()),
            ('n/a', f_list_p, (), dict(a=[4, 5]))
        )
        assert_fail(self, known_exceptions)

    def test_good_list_g(self):
        """This tests list type for iterating over types"""
        known_good = (
            ([4, 'Hello', 'World'], f_list_g,
             ([4, 'Hello', 'World'],), dict()),
        )
        assert_pass(self, known_good)

    def test_except_list_g(self):
        """This tests exceptions to the list types"""
        known_exceptions = (
            ('n/a', f_list_g, ([4, 'Hello', bytes(b'Test')],), dict()),
            ('n/a', f_list_g, (), dict(a=[4, 'Hello', 4.0]))
        )
        assert_fail(self, known_exceptions)

    def test_good_OrderedDict_t(self):
        """This tests OrderedDict types"""
        a = OrderedDict()
        for i, k in zip('abcdef', 'ghijk'):
            a.update({i: k})
        known_good = (
            (a, f_OrderedDict_t, (a,), dict()),
            (a, f_OrderedDict_t, (), dict(a=a)),
            # Confirm a is the first key (dict give 'd' first)
            # f_str takes (a, b='default') so result should be adefault
            ('adefault', f_str, ((a.__iter__().__next__()),), dict())
        )
        assert_pass(self, known_good)

    def test_except_OrderedDict_t(self):
        """This tests for exceptions of OrderedDict types"""
        known_exceptions = (
            ('n/a', f_OrderedDict_t, (45,), dict()),
            ('n/a', f_OrderedDict_t, (), dict(a=b'Testing'))
        )
        assert_fail(self, known_exceptions)

    # def f_OrderedDict_p(a: 'OrderedDict[str=int,bytes=str]')
    def test_good_OrderedDict_p(self):
        """This tests good ordering for OrderedDict positional"""
        a = OrderedDict()
        a.update({'string': 20})
        a.update({b'byteshash': 'Did you work?'})

        known_good = (
            (a, f_OrderedDict_p, (a,), dict()),
            (a, f_OrderedDict_p, (), dict(a=a))
        )
        assert_pass(self, known_good)

    def test_except_OrderedDict_p(self):
        """Checking for known exceptions in OrderedDict positional"""
        a = OrderedDict()
        a.update({b'bytes should fail': 20})
        a.update({b'byteshash': 'Did you work?'})
        b = OrderedDict()
        b.update({'works': 20})
        b.update({b'Should fail': 30})

        known_exceptions = (
            # Test for KEY testing fail
            ('n/a', f_OrderedDict_p, (a,), dict()),
            ('n/a', f_OrderedDict_p, (), dict(a=a)),
            # Test for VALUE testing fail
            ('n/a', f_OrderedDict_p, (b,), dict()),
            ('n/a', f_OrderedDict_p, (), dict(a=b))
        )
        assert_fail(self, known_exceptions)

    def test_good_OrderedDict_g(self):
        """Tests OrderedDict group arguments."""
        # def f_OrderedDict_g(a: 'OrderedDict[str|bytes = bytes|int')
        a = OrderedDict()
        a.update({'First String': b'Bytes'})
        a.update({b'Bytes hash': 20})
        a.update({'String and int': 23})

        known_good = (
            (a, f_OrderedDict_g, (a, ), dict()),
            (a, f_OrderedDict_g, (), dict(a=a))
        )
        assert_pass(self, known_good)

    def test_except_OrderedDict_g(self):
        """Checking for known exceptions in OrderedDict Group check"""
        a = OrderedDict()
        a.update({'Value String': 'Hello string fail'})
        a.update({10: b'Should fail on Key'})

        known_exceptions = (
            ('n/a', f_OrderedDict_g, (a,), dict()),
            ('n/a', f_OrderedDict_g, (), dict(a=a))
        )
        assert_fail(self, known_exceptions)

    def test_good_OrderedDict_key_only(self):
        """Tests OrderedDict for key only group"""
        a = OrderedDict()
        a.update({'String': 50})
        a.update({b'Bytes': b'Bytes again'})
        known_good = (
            (a, f_OrderedDict_key_only, (a,), dict()),
            (a, f_OrderedDict_key_only, (), dict(a=a))
        )
        assert_pass(self, known_good)

    def test_except_OrderedDict_key_only(self):
        """Tests exceptions for OrderedDict key only"""
        a = OrderedDict()
        a.update({40: 'int'})
        b = OrderedDict()
        b.update({'String': 'next fails'})
        b.update({50: 'This should fail'})

        known_exceptions = (
            ('n/a', f_OrderedDict_key_only, (a,), dict()),
            ('n/a', f_OrderedDict_key_only, (b,), dict()),
            ('n/a', f_OrderedDict_key_only, (), dict(a=a)),
            ('n/a', f_OrderedDict_key_only, (), dict(a=b))
        )
        assert_fail(self, known_exceptions)

    def test_good_OrderedDict_value_only(self):
        """Tests OrderedDict for value only group"""
        a = OrderedDict()
        a.update({50: 50})
        a.update({60: b'bytes should work'})

        known_good = (
            (a, f_OrderedDict_value_only, (a,), dict()),
            (a, f_OrderedDict_value_only, (), dict(a=a))
        )
        assert_pass(self, known_good)

    def test_except_OrderedDict_value_only(self):
        """Tests OrdererDict exceptions fro value only group"""
        a = OrderedDict()
        b = OrderedDict()
        a.update({'String': 'Fail String'})
        b.update({'String': b'Successful'})
        b.update({'Fail key': 'Fail String'})

        known_exceptions = (
            ('n/a', f_OrderedDict_value_only, (a,), dict()),
            ('n/a', f_OrderedDict_value_only, (b,), dict()),
            ('n/a', f_OrderedDict_value_only, (), dict(a=a)),
            ('n/a', f_OrderedDict_value_only, (), dict(a=b))
        )
        assert_fail(self, known_exceptions)

    def test_good_dict_t(self):
        """Test dict for type."""
        a = {}
        for i, k in zip('abcdefg', 'hijkmn'):
            a.update({i: k})

        known_good = (
            (a, f_dict_t, (a,), dict()),
            (a, f_dict_t, (), dict(a=a))
        )
        assert_pass(self, known_good)

    def test_except_dict_t(self):
        """Test dict exceptions for type."""
        known_exceptions = (
            ('n/a', f_dict_t, (b'Fail bytes',), dict()),
            ('n/a', f_dict_t, (), dict(a='l33t fail'))
        )
        assert_fail(self, known_exceptions)

    def test_good_dict_group(self):
        """Test dict groups for dict[str=int]"""
        a = {}
        a.update({'Should be good': 200})
        a.update({'Redirect': 304})

        known_good = (
            (a, f_dict_g, (a,), dict()),
            (a, f_dict_g, (), dict(a=a))
        )
        assert_pass(self, known_good)

    def test_except_dict_group(self):
        """Test exceptions for dict groups for dict[str=int]"""
        a = {}
        a.update({'This shouldn\'t fail': 200})
        a.update({'This should fail': b'Broken'})

        known_exceptions = (
            ('n/a', f_dict_g, (a,), dict()),
            ('n/a', f_dict_g, (), dict(a=a))
        )
        assert_fail(self, known_exceptions)

    def test_good_dict_key_only(self):
        """Tests dict for key only check dict[str|bytes]"""
        a = {}
        a.update({'This should work': 200})
        a.update({b'Now bytes': b'Does not check'})

        known_good = (
            (a, f_dict_key_only, (a,), dict()),
            (a, f_dict_key_only, (), dict(a=a))
        )
        assert_pass(self, known_good)

    def test_except_dict_key_only(self):
        """Tests exceptions for key only check dict[str|bytes]"""
        a = {}
        a.update({'Should not fail': 200})
        a.update({401: 'This one fails'})

        known_exceptions = (
            ('n/a', f_dict_key_only, (a,), dict()),
            ('n/a', f_dict_key_only, (), dict(a=a))
        )
        assert_fail(self, known_exceptions)

    def test_good_dict_value_only(self):
        """Tests dict for value only checks dict[=int|bytes]"""
        a = {}
        for i, k in zip('abcd', [10, b'bytes', 200, b'Next bytes']):
            a.update({i: k})

        known_good = (
            (a, f_dict_value_only, (a,), dict()),
            (a, f_dict_value_only, (), dict(a=a))
        )
        assert_pass(self, known_good)

    def test_except_dict_value_only(self):
        """Tests exceptions for value only checks dict[=int|bytes]"""
        a = {}
        for i, k in zip('abcd', [10, 20, 30, 'Add string to break']):
            a.update({i: k})

        known_exceptions = (
            ('n/a', f_dict_value_only, (a,), dict()),
            ('n/a', f_dict_value_only, (), dict(a=a))
        )
        assert_fail(self, known_exceptions)

    def test_good_namedtuple_t(self):
        """Tests namedtuple type check"""
        n = tupname(1, 2, 3)
        m = tupname('Hello', 'Next', 'Third')
        known_good = (
            (n, f_namedtuple_t, (n,), dict()),
            (n, f_namedtuple_t, (), dict(a=n)),
            (m, f_namedtuple_t, (m,), dict()),
            (m, f_namedtuple_t, (), dict(a=m))
        )
        assert_pass(self, known_good)

    def test_except_namedtuple_t(self):
        """Tests exceptions for type check"""
        n = (4, 5, 6)
        m = ['String', 'Next']
        known_exceptions = (
            ('n/a', f_namedtuple_t, (n,), dict()),
            ('n/a', f_namedtuple_t, (m,), dict()),
            ('n/a', f_namedtuple_t, (), dict(a=n)),
            ('n/a', f_namedtuple_t, (), dict(a=m))
        )
        assert_fail(self, known_exceptions)

    def test_good_namedtuple_n(self):
        """Tests namedtuple matching tupname check"""
        tupname = namedtuple('tupname', ('one', 'two', 'three'))
        n = tupname(1, 2, 3)
        known_good = (
            (n, f_namedtuple_n, (n,), dict()),
            (n, f_namedtuple_n, (), dict(a=n))
        )
        assert_pass(self, known_good)

    def test_except_namedtuple_n(self):
        """Tests exceptions for namedtuple name check"""
        n = dif_namedtuple(4, 5, 6)
        m = ['String', 'Next']
        known_exceptions = (
            ('n/a', f_namedtuple_n, (n,), dict()),
            ('n/a', f_namedtuple_n, (m,), dict()),
            ('n/a', f_namedtuple_n, (), dict(a=n)),
            ('n/a', f_namedtuple_n, (), dict(a=m))
        )
        assert_fail(self, known_exceptions)

    def test_good_namedtuple_p(self):
        """Tests namedtuple with positional arguments"""
        n = tupname(1, b'2', '3')
        m = tupname(200, b'Next', 'Third')
        known_good = (
            (n, f_namedtuple_p, (n,), dict()),
            (n, f_namedtuple_p, (), dict(a=n)),
            (m, f_namedtuple_p, (m,), dict()),
            (m, f_namedtuple_p, (), dict(a=m))
        )
        assert_pass(self, known_good)

    def test_except_namedtuple_p(self):
        """Tests exceptions for namedtuple with positional type check"""
        n = tupname(1.2, b'2', '3')
        m = tupname(200, b'Next', b'Third')
        known_exceptions = (
            ('n/a', f_namedtuple_p, (n,), dict()),
            ('n/a', f_namedtuple_p, (m,), dict()),
            ('n/a', f_namedtuple_p, (), dict(a=n)),
            ('n/a', f_namedtuple_p, (), dict(a=m))
        )
        assert_fail(self, known_exceptions)

    def test_good_namedtuple_g(self):
        """Tests namedtuple with group arguments"""
        n = tupname(1, '2', '3')
        m = tupname('200', 300, 'Third')
        known_good = (
            (n, f_namedtuple_g, (n,), dict()),
            (n, f_namedtuple_g, (), dict(a=n)),
            (m, f_namedtuple_g, (m,), dict()),
            (m, f_namedtuple_g, (), dict(a=m))
        )
        assert_pass(self, known_good)

    def test_except_namedtuple_g(self):
        """Tests exceptions for namedtuple with group type check"""
        n = tupname(1.2, b'2', '3')
        m = tupname(200, b'Next', b'Third')
        known_exceptions = (
            ('n/a', f_namedtuple_g, (n,), dict()),
            ('n/a', f_namedtuple_g, (m,), dict()),
            ('n/a', f_namedtuple_g, (), dict(a=n)),
            ('n/a', f_namedtuple_g, (), dict(a=m))
        )
        assert_fail(self, known_exceptions)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Unit Tests for annotate_test.')
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='Debug of returns from exceptions')

    args = parser.parse_args()
    print(args)
    if args.debug is True:
        debug_except = 'Y'
    else:
        debug_except = 'N'

    del args
    #    unittest.main() - Previous command before fixing unittest
    # Below is needed because unittest tries to resolve custom args.

    runner = unittest.TextTestRunner()
    itersuite = unittest.TestLoader().loadTestsFromTestCase(AnnotationTester)
    runner.run(itersuite)
