
import mock

import team_commands

def test_append_notes():
    fake_updater = mock.Mock()
    fake_responder = mock.Mock()
    fake_values = {'college': 'there',
                   'name': 'them',
                   'notes': 'Initial Notes.',
                   'present': True }
    fake_getter = mock.Mock(return_value = fake_values)
    with mock.patch('team_commands.roster.get', fake_getter), \
         mock.patch('team_commands.roster.update', fake_updater):

        options = { '<tla>': 'GMR',
                    '<note>': 'More notes' }
        team_commands.perform_append_notes(fake_responder, options)

        fake_getter.assert_called_once_with('GMR')
        expected_notes = 'Initial Notes.' + " " + 'More notes'
        fake_updater.assert_called_once_with('GMR', notes = expected_notes)
        fake_responder.assert_called_once_with('Team GMR notes updated.')
