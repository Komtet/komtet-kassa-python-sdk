# -*- coding: utf-8 -*-
from unittest import TestCase

from komtet_kassa_sdk.v1 import (Agent, AgentType)


class TestAgent(TestCase):
    def setUp(self):
        self.agent = Agent(AgentType.PAYMENT_AGENT, "+87776665544", "ООО 'Лютик'", "12345678901")

    def test_simple_agent(self):

        expected = {
            "agent_info": {
                "type": "payment_agent",
            },
            "supplier_info": {
                "phones": ["+87776665544"],
                "name": "ООО 'Лютик'",
                "inn": "12345678901"
            }
        }
        self.assertEqual(dict(self.agent), expected)

    def test_paying_agent(self):
        self.agent.set_paying_agent_info('Оплата', ['+87654443322'])

        expected = {
            "agent_info": {
                "type": "payment_agent",
                "paying_agent": {
                    "operation": "Оплата",
                    "phones": ["+87654443322"]
                }
            },
            "supplier_info": {
                "phones": ["+87776665544"],
                "name": "ООО 'Лютик'",
                "inn": "12345678901"
            }
        }
        self.assertEqual(dict(self.agent), expected)

    def test_receive_payments_operator(self):
        self.agent.set_receive_payments_operator_info(['+87654443322'])

        expected = {
            "agent_info": {
                "type": "payment_agent",
                "receive_payments_operator": {
                    "phones": ["+87654443322"]
                }
            },
            "supplier_info": {
                "phones": ["+87776665544"],
                "name": "ООО 'Лютик'",
                "inn": "12345678901"
            }
        }
        self.assertEqual(dict(self.agent), expected)

    def test_money_transfer_operator(self):
        self.agent.set_money_transfer_operator_info(
            'Оператор', ['+87654443322'], 'ул.Мира', '0123456789')

        expected = {
            "agent_info": {
                "type": "payment_agent",
                "money_transfer_operator": {
                    "name": "Оператор",
                    "phones": ["+87654443322"],
                    "address": "ул.Мира",
                    "inn": "0123456789"
                }
            },
            "supplier_info": {
                "phones": ["+87776665544"],
                "name": "ООО 'Лютик'",
                "inn": "12345678901"
            }
        }
        self.assertEqual(dict(self.agent), expected)
