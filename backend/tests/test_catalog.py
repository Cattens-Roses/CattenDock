from app.core import catalog


def test_load_apps_returns_list():
    apps = catalog.load_apps()
    assert isinstance(apps, list)
    assert all("id" in a for a in apps)


def test_load_app_unknown_returns_none():
    assert catalog.load_app("does-not-exist") is None


def test_expand_defaults():
    spec = {"docker": {"volumes": ["${CONFIG_PATH}/x:/config"]}}
    out = catalog.expanded_docker_spec(spec)
    assert out["volumes"][0].startswith("/")
