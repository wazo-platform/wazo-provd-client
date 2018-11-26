# Copyright (C) 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import unittest
from hamcrest import (
    assert_that,
    equal_to,
    is_,
    empty,
    has_length,
)

from wazo_provd_client.operation import parse_operation


class TestParseOperation(unittest.TestCase):

    def test_state(self):
        oip = parse_operation('state')
        assert_that(oip.label, equal_to(None))
        assert_that(oip.state, equal_to('state'))
        assert_that(oip.current, equal_to(None))
        assert_that(oip.end, equal_to(None))
        assert_that(oip.sub_oips, is_(empty()))

    def test_state_label(self):
        oip = parse_operation('label|state')
        assert_that(oip.label, equal_to('label'))
        assert_that(oip.state, equal_to('state'))
        assert_that(oip.current, equal_to(None))
        assert_that(oip.end, equal_to(None))
        assert_that(oip.sub_oips, is_(empty()))

    def test_state_current(self):
        oip = parse_operation('state;0')
        assert_that(oip.label, equal_to(None))
        assert_that(oip.state, equal_to('state'))
        assert_that(oip.current, equal_to(0))
        assert_that(oip.end, equal_to(None))
        assert_that(oip.sub_oips, is_(empty()))

    def test_state_current_end(self):
        oip = parse_operation('state;0/1')
        assert_that(oip.label, equal_to(None))
        assert_that(oip.state, equal_to('state'))
        assert_that(oip.current, equal_to(0))
        assert_that(oip.end, equal_to(1))
        assert_that(oip.sub_oips, is_(empty()))

    def test_state_current_end_label(self):
        oip = parse_operation('label|state;0/1')
        assert_that(oip.label, equal_to('label'))
        assert_that(oip.state, equal_to('state'))
        assert_that(oip.current, equal_to(0))
        assert_that(oip.end, equal_to(1))
        assert_that(oip.sub_oips, is_(empty()))

    def test_state_sub_state(self):
        oip1 = parse_operation('state1(state11)')
        assert_that(oip1.label, equal_to(None))
        assert_that(oip1.state, equal_to('state1'))
        assert_that(oip1.current, equal_to(None))
        assert_that(oip1.end, equal_to(None))
        assert_that(oip1.sub_oips, has_length(1))

        oip11 = oip1.sub_oips[0]
        assert_that(oip11.label, equal_to(None))
        assert_that(oip11.state, equal_to('state11'))
        assert_that(oip11.current, equal_to(None))
        assert_that(oip11.end, equal_to(None))
        assert_that(oip11.sub_oips, is_(empty()))

    def test_state_two_sub_state(self):
        oip1 = parse_operation('state1(state11)(state12)')
        assert_that(oip1.label, equal_to(None))
        assert_that(oip1.state, equal_to('state1'))
        assert_that(oip1.current, equal_to(None))
        assert_that(oip1.end, equal_to(None))
        assert_that(oip1.sub_oips, has_length(2))

        oip11 = oip1.sub_oips[0]
        assert_that(oip11.label, equal_to(None))
        assert_that(oip11.state, equal_to('state11'))
        assert_that(oip11.current, equal_to(None))
        assert_that(oip11.end, equal_to(None))
        assert_that(oip11.sub_oips, has_length(0))

        oip12 = oip1.sub_oips[1]
        assert_that(oip12.label, equal_to(None))
        assert_that(oip12.state, equal_to('state12'))
        assert_that(oip12.current, equal_to(None))
        assert_that(oip12.end, equal_to(None))
        assert_that(oip12.sub_oips, has_length(0))

    def test_complex(self):
        oip1 = parse_operation('label1|state1;1/1(label11|state11;11/11(label111|state111;111/111))(label12|state12;12/12)')

        assert_that(oip1.label, equal_to('label1'))
        assert_that(oip1.state, equal_to('state1'))
        assert_that(oip1.current, equal_to(1))
        assert_that(oip1.end, equal_to(1))
        assert_that(oip1.sub_oips, has_length(2))

        oip11 = oip1.sub_oips[0]
        assert_that(oip11.label, equal_to('label11'))
        assert_that(oip11.state, equal_to('state11'))
        assert_that(oip11.current, equal_to(11))
        assert_that(oip11.end, equal_to(11))
        assert_that(oip11.sub_oips, has_length(1))

        oip111 = oip11.sub_oips[0]
        assert_that(oip111.label, equal_to('label111'))
        assert_that(oip111.state, equal_to('state111'))
        assert_that(oip111.current, equal_to(111))
        assert_that(oip111.end, equal_to(111))
        assert_that(oip111.sub_oips, is_(empty()))

        oip12 = oip1.sub_oips[1]
        assert_that(oip12.label, equal_to('label12'))
        assert_that(oip12.state, equal_to('state12'))
        assert_that(oip12.current, equal_to(12))
        assert_that(oip12.end, equal_to(12))
        assert_that(oip111.sub_oips, is_(empty()))
