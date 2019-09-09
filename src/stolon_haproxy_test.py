import unittest
import json

import stolon_haproxy


class TestStolonJson(unittest.TestCase):

    test_variants_wo_fallback = [
        {"fixture": "one-healthy-slave.json", "result": ['2.2.2.2:5432']},
        {"fixture": "some-unhealthy-slave.json", "result": ['1.1.1.1:5432']},
        {"fixture": "no-healthy-slaves.json", "result": []},
        {"fixture": "two-healthy-slaves.json", "result": ['1.1.1.1:5432', '2.2.2.2:5432']}
    ]

    test_variants_with_fallback = [
        {"fixture": "one-healthy-slave.json", "result": ['2.2.2.2:5432']},
        {"fixture": "some-unhealthy-slave.json", "result": ['1.1.1.1:5432']},
        {"fixture": "no-healthy-slaves.json", "result": ['3.3.3.3:5432']},
        {"fixture": "two-healthy-slaves.json", "result": ['1.1.1.1:5432', '2.2.2.2:5432']}
    ]

    
    def test_without_fallback(self):
        for item in self.test_variants_wo_fallback:
            with self.subTest(msg=item["fixture"]):
                with open('fixtures/'+ item["fixture"]) as json_file:
                    json_data = json.load(json_file)
                self.assertEqual(stolon_haproxy.get_stolon_servers(stolon_json=json_data, fallback_to_master=False), item["result"])

    def test_with_fallback(self):
        for item in self.test_variants_with_fallback:
            with self.subTest(msg=item["fixture"]):
                with open('fixtures/'+ item["fixture"]) as json_file:
                    json_data = json.load(json_file)
                self.assertEqual(stolon_haproxy.get_stolon_servers(stolon_json=json_data, fallback_to_master=True), item["result"])