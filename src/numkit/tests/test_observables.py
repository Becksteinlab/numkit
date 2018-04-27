# -*- coding: utf-8 -*-
# numkit.integration test cases
# Part of GromacsWrapper
# Copyright (c) Oliver Beckstein <orbeckst@gmail.com>
# Published under the Modified BSD Licence.

"""
===================================
 Test cases for numkit.observables
====================================

"""
from __future__ import division

import numkit.observables

import numpy as np
from numpy.testing import assert_equal, assert_almost_equal

import pytest


class TestQID(object):
    @staticmethod
    def test_None():
        q = numkit.observables.QID()
        assert q is None

    @staticmethod
    @pytest.mark.parametrize("identifiers", [
        (0, 1, 42), 42, ("a", "b", "a"), ("aba", ), "aba",
        ])
    def test_create(identifiers):
        q = numkit.observables.QID(identifiers)
        assert q == set(numkit.observables.asiterable(identifiers))

    @staticmethod
    def test_union():
        q1 = numkit.observables.QID([1, 2, 3])
        q2 = numkit.observables.QID([4, 2, 3, 5])

        q3 = q1.union(q2)

        assert isinstance(q3, frozenset)
        assert q3 == set([1, 2, 3, 4, 2, 3, 5])

@pytest.fixture
def Q1():
    return numkit.observables.QuantityWithError(1.0, 0.5)

@pytest.fixture
def Q1b():
    return numkit.observables.QuantityWithError(1.0, 0.5)


@pytest.fixture
def Q2():
    return numkit.observables.QuantityWithError(-1.0, 1.0)

@pytest.fixture()
def Q(Q1, Q1b, Q2):
    return {'Q1': Q1, 'Q1b': Q1b, 'Q2': Q2}

class TestQuantityWithError(object):
    def test_astuple(self, Q1):
        assert Q1.astuple() == (Q1.value, Q1.error)

    def test_astuple_other_Q(self, Q1, Q2, ref=(-1.0, 1.0)):
        self._test_astuple_other(Q1, Q2, ref)

    def test_astuple_other_float(self, Q1, other=22.3, ref=(22.3, 0)):
        self._test_astuple_other(Q1, other, ref)

    def _test_astuple_other(self, q, other, ref):
        val, err, qid = q._astuple(other)
        assert_almost_equal((val, err), ref)
        if hasattr(other, "qid"):
            assert qid == other.qid

    def test_error(self, Q1):
        assert_almost_equal(Q1.variance, Q1.error**2)

    def test_set_error(self, Q2, error=2.0):
        Q2.error = error
        assert Q2.variance == error**2

    @pytest.mark.parametrize("q1,q2,same", [
        ("Q1", "Q1", True),
        ("Q1", "Q1b", False),
        ("Q1", "Q2", False),
        ("Q2", "Q2", True),
    ])
    def test_sameness(self, Q, q1, q2, same):
        assert (Q[q1].isSame(Q[q2])) == same

    @pytest.mark.parametrize("q1,q2,same", [
        ("Q1", "Q1", True),
        ("Q1", "Q1b", True),
        ("Q1", "Q2", False),
        ("Q2", "Q2", True),
    ])
    def test_equality(self, Q, q1, q2, same):
        assert (Q[q1] == Q[q2]) == same

    @pytest.mark.parametrize("op,ref",
                             [("Q1 {} Q2".format(op),
                               "Q1.value {} Q2.value".format(op)) for op in
                              (">", ">=", "<", "<=", "==")])
    def test_comparisons(self, Q1, Q2, op, ref):
        assert eval(op) == eval(ref)


    @pytest.mark.parametrize("op,value", [
        (lambda x, y: 5*x, True),
        (lambda x, y: x*5, True),
        (lambda x, y: -x, True),
        (lambda x, y: abs(x), True),
        (lambda x, y: x + x, True),
        (lambda x, y: x - x, True),
        (lambda x, y: x * x, True),
        (lambda x, y: x * x * x, True),
        (lambda x, y: x / x, True),
        (lambda x, y: 5 + x, True),
        (lambda x, y: 5 - x, True),
        (lambda x, y: x - 5, True),
        (lambda x, y: x**x, True),
        pytest.param(lambda x, y: x**3, True,
                     marks=pytest.mark.xfail),  # need to fix
        (lambda x, y: x - 5*y, False),
        (lambda x, y: x * y, False),
        (lambda x, y: y / x, False),
        (lambda x, y: x**y, False),
    ]   )
    def test_sameness_algebra(self, Q1, Q2, op, value):
        assert Q1.isSame(op(Q1, Q2)) == value

    def test_copy(self, Q1):
        other = Q1.copy()
        assert not Q1.isSame(other)

    def test_deepcopy(self, Q1):
        other = Q1.deepcopy()
        assert Q1.isSame(other)

