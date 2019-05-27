# Copyright 2011-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re

OIP_WAITING = 'waiting'
OIP_PROGRESS = 'progress'
OIP_SUCCESS = 'success'
OIP_FAIL = 'fail'

_PARSE_OIP_REGEX = re.compile(r'^(?:(\w+)\|)?(\w+)(?:;(\d+)(?:/(\d+))?)?')


class BaseOperation(object):

    def __init__(self, label=None, state=OIP_WAITING, current=None, end=None, sub_oips=None):
        self.label = label
        self.state = state
        self.current = current
        self.end = end
        self.sub_oips = sub_oips or []

    def __str__(self):
        status = '{}: {}'.format(self.label, self.state)
        if self.current and self.end:
            status += ' ({}/{})'.format(self.current, self.end)

        if self.sub_oips:
            for sub_oip in self.sub_oips:
                status += '\n  {}'.format(sub_oip)

        return status


class OperationInProgress(BaseOperation):

    def __init__(self, command, location, delete_on_exit=True):
        super(OperationInProgress, self).__init__()
        self._command = command
        self.location = location
        fixed_location = self._fix_location_url(location)
        self._url = '{base}/{location}'.format(base=self._command.base_url, location=fixed_location)
        self._delete_on_exit = delete_on_exit

        self.update()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self._delete_on_exit:
            self.delete()

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    def update(self):
        r = self._command.session.get(self._url)
        self._command.raise_from_response(r)
        base_operation = parse_operation(r.json()['status'])
        self.label = base_operation.label
        self.state = base_operation.state
        self.current = base_operation.current
        self.end = base_operation.end
        self.sub_oips = base_operation.sub_oips

    def delete(self):
        r = self._command.session.delete(self._url)
        self._command.raise_from_response(r)

    @staticmethod
    def _fix_location_url(location):
        location_parts = location.split('/')
        return '/'.join(location_parts[3:])  # We do not want /{version}/{pg,dev,cfg}_mgr/ prefix


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
        return BaseOperation(label, state, current, end, sub_oips)


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
