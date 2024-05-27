# Test custom django management commands

# Mock the behaviour of the db
from unittest.mock import patch
# type of error expected from Psycopg2Error
from psycopg2 import OperationalError as Psycopg2Error
# allows to call the command tests
from django.core.management import call_command
# type of error expected
from django.db.utils import OperationalError
# type of test performed
from django.test import SimpleTestCase


# command that we are mocking
@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    # Test commands

    def test_wait_for_db_ready(self, patched_check):
        # Test if db is ready
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        # Test waiting for db when getting op error

        # The first 2 times we call the mocked method is raises a Psycopg2Error
        # The next 3 times it raises an operational error from django
        # Otherwise,
        # Values are from trial and error
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
