import control
import mock

def check_showed_usage(responder):
    responder.assert_any_call('Usage: usage')

def test_usage():
    responder = mock.Mock()
    control.handle('usage', responder)
    check_showed_usage(responder)

def test_unknown():
    responder = mock.Mock()
    control.handle('hnnnng', responder)
    check_showed_usage(responder)
