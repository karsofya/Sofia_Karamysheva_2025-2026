import unittest
import streamlit
import sys
import os
import requests
from streamlit.testing.v1 import AppTest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import p2026_projekts

class IntegrationTests(unittest.TestCase):
    def test_API_call(self):
        test = p2026_projekts.weather("Rome", False)
        url = f"https://wttr.in/{"Rome"}?format=j1"
        r = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        result = test == r.json()
        self.assertTrue(result)

    def test_card_renders_correctly(self):

        at = AppTest.from_file("p2026_projekts.py").run()
        self.assertEqual(at.markdown[3].value, "### laikapstākļi")
    def test_piezímes_renders_correctly(self):

        at = AppTest.from_file("p2026_projekts.py").run()

        self.assertEqual(at.session_state.notes, streamlit.text_area("teksts", streamlit.session_state.notes, height=120))
