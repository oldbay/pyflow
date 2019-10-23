"""Provides publishing functionality for publish/subscribe pattern

This module provides event publishers for sending notifications to subscribers. The base class basically does not send
notifications anywhere and thus can be used as a stub.

This module is an official hack. It is used just to get the system working and then the system should be replaced with
a better one where that hack is just not needed.

"""

import json

import pika


class Publisher:
    """Publishes three types of events: start, finish and error"""

    def pub_start(self, data):
        """Publishes start event

        Args:
            data: Arbitrary data to send along the event information.

        """

    def pub_finish(self, data):
        """Publishes finish event

        Args:
            data: Arbitrary data to send along the event information.

        """

    def pub_error(self, error, data):
        """Publishes error event

        Args:
            error: Error information which will be sent with the event.
            data: Arbitrary data to send along the event information.

        """


class RabbitPublisher(Publisher):
    """Publishes events to the RabbitMQ

    Args:
        **kwargs: Configuration for initializing RabbitMQ connection. Must include ``username``, ``password``, ``host``,
            ``port`` and ``exchange``. May include ``metadata``. Metadata will be appended to every event if it is
            provided.

    """

    def __init__(self, **kwargs):
        credentials = pika.PlainCredentials(kwargs['username'], kwargs['password'])
        self.connection_parameters = pika.ConnectionParameters(host=kwargs['host'],
                                                               port=kwargs['port'],
                                                               credentials=credentials)
        # Publisher expects that the target exchange is fanout so that several queues could be bound to it
        self.exchange = kwargs['exchange']
        self.metadata = kwargs.get('metadata')

    def pub_start(self, data):
        """Publishes start event to RabbitMQ attaching additional data to it

        Args:
            data: Arbitrary data to send along the event information. Data must be JSON serializable.

        """
        message = {
            'event_type': 'start',
            'data': data,
        }
        self.pub_event(message)

    def pub_finish(self, data):
        """Publishes finish event to RabbitMQ attaching additional data to it

        Args:
            data: Arbitrary data to send along the event information. Data must be JSON serializable.

        """
        message = {
            'event_type': 'finish',
            'data': data,
        }
        self.pub_event(message)

    def pub_error(self, error, data):
        """Publishes error event to RabbitMQ attaching error information and additional data to it

        Args:
            error: Error information which will be sent with the event. Must be convertible to string.
            data: Arbitrary data to send along the event information. Data must be JSON serializable.

        """
        message = {
            'event_type': 'error',
            'error': str(error),
            'data': data,
        }
        self.pub_event(message)

    def pub_event(self, event_message):
        """Boilerplate code for putting event into RabbitMQ"""
        connection = pika.BlockingConnection(self.connection_parameters)
        channel = connection.channel()

        if self.metadata is not None:
            event_message['metadata'] = self.metadata

        json_message = json.dumps(event_message, separators=(',', ':'))
        channel.basic_publish(self.exchange, '', bytes(json_message, encoding='utf-8'))

        connection.close()
