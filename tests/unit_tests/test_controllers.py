import pytest
from simple_app.controllers import simpleIntentClassifier, intent_map, keywords_to_regex, match_intent_keywords_and_msg


def create_intent_classification_test_data():
    data = list()
    for intent, intent_info in intent_map.items():
        for kw in intent_info['keywords']:
            data.append((f"{kw} USER_INPUT", intent))
    return data


def create_confused_input():
    return [
        ("!幫助找地點", "主頁選單"),
        ("幫我找Arduino", "找地點"),
        ("幫我找", "找地點"),
        ("跟我聊聊Arduino", "聊天"),
        ("你知道Arduino嗎？", "聊天"),
        ("Arduino幫我找", "找地點"),
        ("我好餓哦", "default")
    ]


def create_keyword_to_regex_test():
    return [
        (["幫我找", "幫忙找", "!找", "!find"], r"(幫我找|幫忙找|!找|!find)+[ ]*([^ ]*)"),
        (["!車輛控制", "!Arduino"], r"(!車輛控制|!Arduino)+[ ]*([^ ]*)"),
        (["跟我聊聊", "你知道什麼是", "你知道", "聊聊"], r"(跟我聊聊|你知道什麼是|你知道|聊聊)+[ ]*([^ ]*)"),
        (["生成圖片", "一張圖包含"], r"(生成圖片|一張圖包含)+[ ]*([^ ]*)")
    ]


def create_regex_matcher_input():
    return [
        # user_msg,
        # regex_pattern,
        # intent_keyword,
        # message
        (
            "!車輛控制 靠左",
            keywords_to_regex(["!車輛控制", "!Arduino"]),
            "!車輛控制", "靠左"),
        (
            "!幫我找地點",
            keywords_to_regex(["幫我找", "幫忙找", "!幫我找", "!找", "!find"]),
            "!幫我找", "地點"),
        (
            "!Arduino 幫我找 車子",
            keywords_to_regex(["!車輛控制", "!Arduino"]),
            "!Arduino", "幫我找"),
        (
            "你知道Arduino嗎?",
            keywords_to_regex(["跟我聊聊", "你知道什麼是", "你知道", "聊聊"]),
            "你知道", "Arduino嗎?")
    ]


class TestKeywordsToRegex():
    @pytest.mark.parametrize('kws,expected_pattern', create_keyword_to_regex_test())
    def test_keywords_to_pattern(self, kws, expected_pattern):
        result = keywords_to_regex(kws)
        assert result.pattern == expected_pattern

    @pytest.mark.parametrize('user_msg,regex_pattern,intent_keyword,intent_msg', create_regex_matcher_input())
    def test_regex_matcher(self, user_msg, regex_pattern, intent_keyword, intent_msg):
        result = match_intent_keywords_and_msg(user_msg, regex_pattern)

        assert result[0] == intent_keyword
        assert result[1] == intent_msg


class TestSimpleIntentClassifier():
    @pytest.mark.parametrize('msg,expected_intent', create_intent_classification_test_data())
    def test_intent_classifer(self, msg, expected_intent):
        result = simpleIntentClassifier("TEST", msg)
        assert result["intentType"] == expected_intent

    @pytest.mark.parametrize('msg,expected_intent', create_confused_input())
    def test_confused_input(self, msg, expected_intent):
        result = simpleIntentClassifier("TEST", msg)
        assert result["intentType"] == expected_intent
