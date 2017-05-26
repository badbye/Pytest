# encoding: utf8

"""
Created on 2017.01.06

@author: yalei
"""

import numpy as np
import pandas as pd
from numpy import array


def _test_object(name, obj):
    '''test object'''
    return 'self.assertIsInstance(%s, %s)' % (name, obj)


def _test_shape(name):
    '''test shape of pd.DataFrame/np.array/np.matrix'''
    return 'self.assertEqual(%s.shape, %s)' % (name, eval('%s.shape' % name))


def _test_length(name):
    '''test length list/character'''
    return 'self.assertEqual(len(%s), %s)' % (name, eval('len(%s)' % name))


def _test_col(name, sort_col=True):
    '''test pd.DataFrame.columns'''
    col_name = eval('%s.columns.tolist()' % name)
    if sort_col:
        return 'self.assertEqual(%s.columns.tolist(), %s)' % (name, col_name)
    else:
        return 'self.assertEqual(sorted(%s.columns.tolist(), %s))' % (name, sorted(col_name))


def _test_index(name, sort_row = True):
    '''test pd.DataFrame.index'''
    index_name = eval('%s.index.tolist()' % name)
    if sort_row:
        return 'self.assertEqual(%s.index.tolist(), %s)' % (name, index_name)
    else:
        return 'self.assertEqual(sorted(%s.index.tolist()), %s)' % (name, sorted(index_name))


def _test_val(name):
    '''test list of values'''
    val = eval(name)
    if eval("type(%s[0])" % name) in [float, np.float64, np.float32]:
        return 'self.assertTrue(np.allclose(%s, %s))' % (name, val.__repr__())
    else:
        return 'self.assertEqual(%s, %s)' % (name, val.__repr__())


def test_df(df, value, sort_col = True, sort_row = True):
    assert type(df) == str
    globals()[df] = value
    code = [
        _test_object(df, 'pd.DataFrame'),
        _test_shape(df),
        _test_col(df, sort_col),
        _test_index(df, sort_row)
    ]
    # test values
    shape = value.shape
    if shape[0] >= shape[1]:
        for col in value.columns:
            if type(col) == str:
                col = '"%s"' % col
            code.append( _test_val('%s[%s].tolist()' % (df, col)) )
    else:
        for row in value.index:
            if type(row) == str:
                row = '"%s"' % row
            code.append( _test_val('%s[%s].tolist()' % (df, row)) )
    del globals()[df]
    return '\n'.join(code)


def test_numpy_array(name, value):
    assert type(name) == str
    globals()[name] = value
    code = [
        _test_object(name, 'np.array'),
        _test_shape(name)
    ]
    shape = value.shape
    if len(shape) == 1:
        code.append(
            _test_val('%s.tolist()' % name)
        )
    elif len(shape) != 2:
        pass
    elif shape[0] > shape[1]:
        for i in range(shape[1]):
            code.append( _test_val('%s[:, %s].tolist()' % (name, i)) )
    else:
        for i in range(shape[0]):
            code.append( _test_val('%s[%s, :].tolist()' % (name, i)) )
    del globals()[name]
    return '\n'.join(code)


def test_list(name, value):
    assert type(name) == str
    globals()[name] = value
    code = [
        _test_object(name, 'list'),
        _test_length(name),
        _test_val(name)
    ]
    del globals()[name]
    return '\n'.join(code)


if __name__ == '__main__':

    a = np.array([[1, 2], [3, 4], [5, 6]])
    print 'check numpy array: '
    print '=' * 50
    print 'original array: \n', a, '\n'
    print 'test code: \n', '-' * 20
    print test_numpy_array('a', a)

    print '\n' * 5

    d = pd.DataFrame({'a': [1, 2, 4], 'b': [2.1, 3.2, 4.3], 'c': ['212', '1232', 'adc']})
    print 'check pandas dataframe: '
    print '=' * 50
    print 'original dataframe: \n', d, '\n'
    print 'test code: \n', '-' * 20
    print test_df('d', d)

    l = [1, 2, 3, '4']
    print 'check list: '
    print '=' * 50
    print 'original list: \n', l, '\n'
    print 'test code: \n', '-' * 20
    print test_list('l', l)


