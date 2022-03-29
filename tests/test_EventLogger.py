import inspect

import EventLogger.EventLogger as EL
import mock

import pytest


@pytest.fixture
def event_test_fixtures():
    """
    Test fixture with eventlogger with event loaded
    :return:
    """
    test_logger = EL.eventlogger()
    params = ['ship_attack', 'Ship Attack', 'Ship1', 'Ship2']

    test_logger.add_event(params)
    return test_logger


def test_check_len_events(event_test_fixtures):
    """
    Tests that there is an event tracker in the eventlogger
    :param event_test_fixtures:
    :return assertion:
    """
    print("\nTests that there is an event tracker in the eventlogger")
    assert len(event_test_fixtures.tracked_events) == 1


def test_add_event(event_test_fixtures):
    """
    Tests that the eventlogger can add new events
    :param event_test_fixtures:
    :return:
    """

    if len(event_test_fixtures.tracked_events) != 1:
        assert False
    event_test_fixtures.add_event([f"{inspect.currentframe()}", 'Ship Attack', 'Ship1', 'Ship2'])
    print(f"\n{event_test_fixtures.tracked_events[-1]}")
    assert len(event_test_fixtures.tracked_events) == 2
