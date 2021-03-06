import pytest

import numpy as np

import pandas.util.testing as tm
from pandas import (TimedeltaIndex, timedelta_range, Int64Index, Float64Index,
                    Index, Timedelta, NaT)


class TestTimedeltaIndex(object):
    _multiprocess_can_split_ = True

    def test_astype(self):
        # GH 13149, GH 13209
        idx = TimedeltaIndex([1e14, 'NaT', NaT, np.NaN])

        result = idx.astype(object)
        expected = Index([Timedelta('1 days 03:46:40')] + [NaT] * 3,
                         dtype=object)
        tm.assert_index_equal(result, expected)

        result = idx.astype(int)
        expected = Int64Index([100000000000000] + [-9223372036854775808] * 3,
                              dtype=np.int64)
        tm.assert_index_equal(result, expected)

        result = idx.astype(str)
        expected = Index(str(x) for x in idx)
        tm.assert_index_equal(result, expected)

        rng = timedelta_range('1 days', periods=10)
        result = rng.astype('i8')
        tm.assert_index_equal(result, Index(rng.asi8))
        tm.assert_numpy_array_equal(rng.asi8, result.values)

    def test_astype_timedelta64(self):
        # GH 13149, GH 13209
        idx = TimedeltaIndex([1e14, 'NaT', NaT, np.NaN])

        result = idx.astype('timedelta64')
        expected = Float64Index([1e+14] + [np.NaN] * 3, dtype='float64')
        tm.assert_index_equal(result, expected)

        result = idx.astype('timedelta64[ns]')
        tm.assert_index_equal(result, idx)
        assert result is not idx

        result = idx.astype('timedelta64[ns]', copy=False)
        tm.assert_index_equal(result, idx)
        assert result is idx

    @pytest.mark.parametrize('dtype', [
        float, 'datetime64', 'datetime64[ns]'])
    def test_astype_raises(self, dtype):
        # GH 13149, GH 13209
        idx = TimedeltaIndex([1e14, 'NaT', NaT, np.NaN])
        msg = 'Cannot cast TimedeltaIndex to dtype'
        with tm.assert_raises_regex(TypeError, msg):
            idx.astype(dtype)
