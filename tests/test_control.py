
import control
import mock

def test_usage():
    responder = mock.Mock()
    control.handle('usage', responder)
    responder.assert_any_call('Usage: usage')

def test_unknown():
    responder = mock.Mock()
    cmd = 'hnnnng'
    control.handle(cmd, responder)
    responder.assert_called_with("Command '{0}' not recognised. Check 'usage' for accepted commands.".format(cmd))
