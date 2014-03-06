
import mock

import team_db

def test_add():
    fake_connection = mock.Mock()
    fake_connection.set = mock.Mock()
    fake_connection.publish = mock.Mock()
    roster = team_db.TeamDB(fake_connection)

    roster.add('aaa', college = 'St. Pony College', name = 'Team Pony')
    fake_connection.set.assert_has_calls([mock.call('team:aaa:college',
                                                    'St. Pony College'),
                                          mock.call('team:aaa:name',
                                                    'Team Pony'),
                                          mock.call('team:aaa:notes',
                                                    ''),
                                          mock.call('team:aaa:present',
                                                    False)],
                                         any_order = True)
    fake_connection.publish.assert_called_once_with('team:update', 'update')

def test_delete():
    fake_connection = mock.Mock()
    fake_connection.delete = mock.Mock()
    fake_connection.publish = mock.Mock()
    roster = team_db.TeamDB(fake_connection)

    roster.delete('aaa')
    fake_connection.delete.assert_has_calls([mock.call('team:aaa:college'),
                                             mock.call('team:aaa:name'),
                                             mock.call('team:aaa:notes'),
                                             mock.call('team:aaa:present')],
                                            any_order = True)
    fake_connection.publish.assert_called_once_with('team:update', 'update')

def test_mark_present():
    fake_connection = mock.Mock()
    fake_connection.set = mock.Mock()
    fake_connection.publish = mock.Mock()
    roster = team_db.TeamDB(fake_connection)

    roster.mark_present('aaa')
    fake_connection.set.assert_called_once_with('team:aaa:present',
                                                True)
    fake_connection.publish.assert_called_once_with('team:update', 'update')

def test_mark_absent():
    fake_connection = mock.Mock()
    fake_connection.set = mock.Mock()
    fake_connection.publish = mock.Mock()
    roster = team_db.TeamDB(fake_connection)

    roster.mark_absent('aaa')
    fake_connection.set.assert_called_once_with('team:aaa:present',
                                                False)
    fake_connection.publish.assert_called_once_with('team:update', 'update')

def test_update():
    fake_connection = mock.Mock()
    fake_connection.set = mock.Mock()
    fake_connection.publish = mock.Mock()
    roster = team_db.TeamDB(fake_connection)

    roster.update('aaa',
                  college = 'St. Eyes College',
                  name = 'Pony Gravity',
                  notes = 'free form text')
    fake_connection.set.assert_has_calls([mock.call('team:aaa:college',
                                                    'St. Eyes College'),
                                          mock.call('team:aaa:name',
                                                    'Pony Gravity'),
                                          mock.call('team:aaa:notes',
                                                    'free form text')],
                                         any_order = True)
    fake_connection.publish.assert_called_once_with('team:update', 'update')

def test_list():
    fake_connection = mock.Mock()
    fake_keys = ['team:aaa:college', 'team:bbb2:college']
    fake_connection.keys = mock.Mock(return_value = fake_keys)
    roster = team_db.TeamDB(fake_connection)

    actual = roster.list()
    fake_connection.keys.assert_called_once_with('team:*:college')
    assert actual == ['aaa', 'bbb2']

def test_get():
    fake_connection = mock.Mock()
    fake_values = ['College', 'Name', 'Notes', True]
    fake_connection.mget = mock.Mock(return_value = fake_values)
    roster = team_db.TeamDB(fake_connection)

    actual = roster.get('aaa')
    fake_connection.mget.assert_called_once_with('team:aaa:college',
                                                 'team:aaa:name',
                                                 'team:aaa:notes',
                                                 'team:aaa:present')
    expected = {'college': 'College',
                'name': 'Name',
                'notes': 'Notes',
                'present': True}
    assert actual == expected
