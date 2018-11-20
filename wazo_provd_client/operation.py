# -*- coding: utf-8 -*-

# Copyright (C) 2011-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+


import re

OIP_WAITING = 'waiting'
OIP_PROGRESS = 'progress'
OIP_SUCCESS = 'success'
OIP_FAIL = 'fail'


class OperationInProgress(object):

    def __init__(self, label=None, state=OIP_WAITING, current=None, end=None, sub_oips=None):
        self.label = label
        self.state = state
        self.current = current
        self.end = end
        self.sub_oips = sub_oips or []


def _split_top_parentheses(str_):
    idx = 0
    length = len(str_)
    result = []
    while idx < length:
        if str_[idx] != '(':
            raise ValueError('invalid character: {}'.format(str_[idx]))
        start_idx = idx
        idx += 1
        count = 1
        while count:
            if idx >= length:
                raise ValueError('unbalanced number of parentheses: {}'.format(str_))
            c = str_[idx]
            if c == '(':
                count += 1
            elif c == ')':
                count -= 1
            idx += 1
        end_idx = idx
        result.append(str_[start_idx + 1:end_idx - 1])
    return result


_PARSE_OIP_REGEX = re.compile(r'^(?:(\w+)\|)?(\w+)(?:;(\d+)(?:/(\d+))?)?')


def parse_operation(operation_string):
    m = _PARSE_OIP_REGEX.search(operation_string)
    if not m:
        raise ValueError('Invalid progress string: {}'.format(operation_string))
    else:
        label, state, raw_current, raw_end = m.groups()
        raw_sub_oips = operation_string[m.end():]
        current = raw_current if raw_current is None else int(raw_current)
        end = raw_end if raw_end is None else int(raw_end)
        sub_oips = [parse_operation(sub_oip_string) for sub_oip_string in
                    _split_top_parentheses(raw_sub_oips)]
        return OperationInProgress(label, state, current, end, sub_oips)
