from datetime import date
from types import SimpleNamespace

from app.services.v1.search_service_v1 import SearchServiceV1


def make_item(item_id: str, name: str):
    return SimpleNamespace(
        id=item_id,
        name=name,
    )


def make_service(items):
    service = SearchServiceV1.__new__(SearchServiceV1)
    service._get_all_nodes = lambda: items
    return service


def test_daily_feature_is_stable_for_the_same_day():
    service = make_service([
        make_item("NUTRIENT:protein", "Protein"),
        make_item("INGREDIENT:sugar", "Sugar"),
        make_item("ADDITIVE:e100", "E100"),
    ])

    first = service.get_daily_feature(target_date=date(2026, 8, 14))
    second = service.get_daily_feature(target_date=date(2026, 8, 14))

    assert first.id == second.id


def test_daily_feature_changes_by_calendar_day_when_multiple_items_exist():
    service = make_service([
        make_item("NUTRIENT:protein", "Protein"),
        make_item("INGREDIENT:sugar", "Sugar"),
        make_item("ADDITIVE:e100", "E100"),
    ])

    today = service.get_daily_feature(target_date=date(2026, 8, 14))
    tomorrow = service.get_daily_feature(target_date=date(2026, 8, 15))

    assert today.id != tomorrow.id


def test_search_list_order_is_stable_for_the_same_day():
    service = make_service([
        make_item("NUTRIENT:protein", "Protein"),
        make_item("INGREDIENT:sugar", "Sugar"),
        make_item("ADDITIVE:e100", "E100"),
        make_item("NUTRIENT:fat", "Fat"),
        make_item("ADDITIVE:e200", "E200"),
    ])

    first = service.get_all(limit=5, target_date=date(2026, 8, 14))
    second = service.get_all(limit=5, target_date=date(2026, 8, 14))

    assert [item.id for item in first] == [item.id for item in second]


def test_search_list_order_changes_by_calendar_day():
    service = make_service([
        make_item("NUTRIENT:protein", "Protein"),
        make_item("INGREDIENT:sugar", "Sugar"),
        make_item("ADDITIVE:e100", "E100"),
        make_item("NUTRIENT:fat", "Fat"),
        make_item("ADDITIVE:e200", "E200"),
    ])

    today = service.get_all(limit=5, target_date=date(2026, 8, 14))
    tomorrow = service.get_all(limit=5, target_date=date(2026, 8, 15))

    assert [item.id for item in today] != [item.id for item in tomorrow]
