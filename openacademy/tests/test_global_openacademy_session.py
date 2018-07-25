# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger
from psycopg2 import IntegrityError

class GlobalTestOpenAcademySession(TransactionCase):
    '''
    This create global test to sessions
    '''
    def setUp(self):
        super(GlobalTestOpenAcademySession, self).setUp()
        self.session = self.env['openacademy.session']
        self.partner_vauxoo = self.env.ref('base.res_partner_1')
        self.course = self.env.ref('openacademy.course0')
        self.partner_attendee = self.env.ref('base.res_partner_2')

    def test_10_instructor_is_attende(self):
        '''
        Check that raise of 'A session's instructor can't be an attendee'
        '''
        with self.assertRaisesRegexp(
            ValidationError,
            "A session's instructor can't be an attendee"
        ):
            self.session.create({
                'name': 'Session test 1',
                'seats': 1,
                'instructor_id': self.partner_vauxoo.id,
                'attendee_ids': [(6, 0, [self.partner_vauxoo.id])],
                'course_id': self.course.id
            })

    def test_20_wkf_done(self):
        '''
        Check that the workflow work's fine!
        '''
        session_id = self.session.create({
            'name': 'Session test 1',
            'seats': 1,
            'instructor_id': self.partner_vauxoo.id,
            'attendee_ids': [(6, 0, [self.partner_attendee.id])],
            'course_id': self.course.id
        })
        self.assertTrue(self.session.search([('id', '=', "{}".format(session_id.id))]).id)

    @mute_logger('odoo.sql_db')
    def test_30_session_without_course(self):
        with self.assertRaisesRegexp(
            IntegrityError,
            'null value in column "course_id"'
            ' violates not-null constraint'
        ):
            self.session.create({
                'name': 'Session test 1',
                'seats': 1,
                'instructor_id': self.partner_vauxoo.id,
                'attendee_ids': [(6, 0, [self.partner_vauxoo.id])],
                'course_id': None
            })
