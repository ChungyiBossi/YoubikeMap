import pytest
from simple_app.controllers import simpleIntentClassifier, intent_map


def create_test_data():
    data = list()
    for intent, intent_info in intent_map.items():
        for kw in intent_info['keywords']:
            data.append((f"{kw} USER_INPUT", intent))
    return data


def create_confused_input():
    return [
        ("!幫助找地點", "主頁選單"),
        ("幫我找Arduino", "找地點"),
        ("Arduino幫我找", "找地點")
    ]


class TestSimpleIntentClassifier():
    @pytest.mark.parametrize('msg,expected_intent', create_test_data())
    def test_intent_classifer(self, msg, expected_intent):
        result = simpleIntentClassifier("TEST", msg)
        assert result["intentType"] == expected_intent

    @pytest.mark.parametrize('msg,expected_intent', create_confused_input())
    def test_confused_input(self, msg, expected_intent):
        result = simpleIntentClassifier("TEST", msg)
        assert result["intentType"] == expected_intent
