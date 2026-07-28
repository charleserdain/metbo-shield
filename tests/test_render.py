import pytest

streamlit = pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest

def test_dashboard_renders_without_exception():
    app = AppTest.from_file("app.py")
    app.run(timeout=30)
    assert not app.exception
    titles = [item.value for item in app.title]
    assert "🛡️ METBO Shield" in titles
