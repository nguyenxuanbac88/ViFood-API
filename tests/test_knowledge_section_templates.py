from app.schemas.additive_v1_schema import (
    AdditiveAliasResponse,
    AdditiveDetailResponse,
    AdditiveFoodCategoryResponse,
    AdditiveFunctionResponse,
)
from app.schemas.ingredient_v1_schema import (
    IngredientAliasResponse,
    IngredientCategoryResponse,
    IngredientDetailResponse,
    IngredientUsageResponse,
)
from app.schemas.nutrient_v1_schema import (
    NutrientDetailResponse,
    NutrientHealthClaimResponse,
)
from app.templates.additive_section_template import build_additive_sections
from app.templates.ingredient_section_template import build_ingredient_sections
from app.templates.nutrient_section_template import build_nutrient_sections


MECHANICAL_WORDS = (
    "ViFood",
    "hệ thống",
    "dữ liệu hiện tại",
    "nguồn dữ liệu",
    "được ghi nhận trong dữ liệu",
)


def assert_natural_content(sections) -> None:
    assert sections
    combined = " ".join(section.content for section in sections)

    for word in MECHANICAL_WORDS:
        assert word not in combined


def test_nutrient_sections_read_like_user_knowledge() -> None:
    nutrient = NutrientDetailResponse(
        id="NUTRIENT:PROTEIN",
        name="Protein",
        name_vi="Chất đạm",
        external_code="INFOODS:PROCNT",
        default_unit="g",
        vietnam_label_requirement="required",
        health_claims=[
            NutrientHealthClaimResponse(
                claim_text="góp phần xây dựng và duy trì khối cơ",
            )
        ],
    )

    sections = build_nutrient_sections(nutrient)

    assert_natural_content(sections)
    assert sections[0].title == "Chất đạm là gì?"
    assert "khẩu phần" in sections[1].content
    assert "không thay thế tư vấn y tế cá nhân" in sections[2].content


def test_additive_sections_read_like_user_knowledge() -> None:
    additive = AdditiveDetailResponse(
        id="ADDITIVE:E330",
        name="Citric acid",
        name_vi="Axit citric",
        ins="330",
        aliases=[
            AdditiveAliasResponse(name="E330"),
        ],
        functions=[
            AdditiveFunctionResponse(name="Chất điều chỉnh độ acid"),
        ],
        permitted_categories=[
            AdditiveFoodCategoryResponse(name_vi="Đồ uống"),
        ],
    )

    sections = build_additive_sections(additive)

    assert_natural_content(sections)
    assert sections[0].title == "Axit citric là gì?"
    assert "mục đích công nghệ" in sections[0].content
    assert "Đồ uống" in sections[2].content


def test_ingredient_sections_read_like_user_knowledge() -> None:
    ingredient = IngredientDetailResponse(
        id="INGREDIENT:Q11002",
        name="đường",
        name_vi="đường",
        name_en="sugar",
        wikidata_id="Q11002",
        description_vi="hợp chất hóa học ở dạng tinh thể thuộc nhóm phân tử cacbohydrat",
        aliases=[
            IngredientAliasResponse(name="chất đường", language="vi"),
        ],
        categories=[
            IngredientCategoryResponse(name="carbohydrat", wikidata_id="Q11358"),
        ],
        usages=[
            IngredientUsageResponse(name="chất tạo ngọt", wikidata_id="Q193619"),
        ],
        wikipedia_vi_url="https://vi.wikipedia.org/wiki/Duong",
    )

    sections = build_ingredient_sections(ingredient)

    assert_natural_content(sections)
    assert sections[0].title == "đường là gì?"
    assert "tên gọi khác" in sections[1].content
    assert "toàn bộ danh sách nguyên liệu" in sections[-1].content
