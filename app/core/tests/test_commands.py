'''
Test custom Django management commands
'''

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Mock the BaseCommand.check method
# This then becomes available as an arg on the class methods
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    def test_wait_for_db_ready(self, patched_check):
        '''Test waiting for DB service'''
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    # Mock Python sleep function - actual delay not required during test
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        '''
        Test waiting for DB when getting OperationalError (i.e. not ready)
        The below raises 2 Psycopg2Errors, 3 OperationalErrors and then
        returns True - mocks waiting for Postgres DB service
        '''
        patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True] # noqa
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
