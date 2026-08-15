from app.schemas.nutrient_v1_schema import (
    NutrientDetailResponse,
    NutrientSectionResponse,
)


def build_nutrient_sections(
    nutrient: NutrientDetailResponse,
) -> list[NutrientSectionResponse]:
    return [
        NutrientSectionResponse(
            section_type="overview",
            title=f"{_display_name(nutrient)} là gì?",
            content=_build_overview(nutrient),
        ),
        NutrientSectionResponse(
            section_type="common_unit",
            title="Cách đọc trên nhãn",
            content=_build_common_unit(nutrient),
        ),
        NutrientSectionResponse(
            section_type="health_note",
            title="Ý nghĩa dinh dưỡng",
            content=_build_health_note(nutrient),
        ),
        NutrientSectionResponse(
            section_type="sources_and_labeling",
            title="Ghi nhãn và tham khảo",
            content=_build_sources_and_labeling(nutrient),
        ),
    ]


def _display_name(nutrient: NutrientDetailResponse) -> str:
    return nutrient.name_vi or nutrient.name or nutrient.id


def _english_name(nutrient: NutrientDetailResponse) -> str | None:
    if nutrient.name and nutrient.name != nutrient.name_vi:
        return nutrient.name
    return None


def _build_overview(nutrient: NutrientDetailResponse) -> str:
    name = _display_name(nutrient)
    sentences = [
        f"{name} là một thành phần dinh dưỡng có thể xuất hiện trong bảng thông tin dinh dưỡng của thực phẩm đóng gói."
    ]

    english_name = _english_name(nutrient)
    if english_name:
        sentences.append(f"Trên nhãn tiếng Anh, chất này thường được ghi là {english_name}.")

    if nutrient.external_code:
        sentences.append(f"Mã tham chiếu thường dùng cho chất này là {nutrient.external_code}.")

    return " ".join(sentences)


def _build_common_unit(nutrient: NutrientDetailResponse) -> str:
    name = _display_name(nutrient)

    if nutrient.default_unit:
        return (
            f"Khi đọc nhãn, {name} thường được biểu diễn bằng đơn vị {nutrient.default_unit}. "
            "Con số này nên được xem cùng khẩu phần ăn hoặc khối lượng sản phẩm, vì cùng một hàm lượng có thể mang ý nghĩa khác nhau giữa các khẩu phần."
        )

    return (
        f"Với {name}, đơn vị có thể thay đổi tùy cách trình bày của từng nhãn thực phẩm. "
        "Người đọc nên xem kỹ phần khẩu phần, khối lượng và đơn vị đi kèm trước khi so sánh giữa các sản phẩm."
    )


def _build_health_note(nutrient: NutrientDetailResponse) -> str:
    name = _display_name(nutrient)

    claim_texts = [
        _strip_sentence_end(claim.claim_text)
        for claim in nutrient.health_claims
        if claim.claim_text
    ]
    if claim_texts:
        return (
            f"Về mặt dinh dưỡng, {name} thường được nhắc đến với các vai trò như "
            f"{'; '.join(claim_texts)}. "
            "Các thông tin này giúp hiểu ý nghĩa của chất dinh dưỡng trong khẩu phần, nhưng không thay thế tư vấn y tế cá nhân."
        )

    return (
        f"{name} nên được hiểu trong bối cảnh tổng thể của khẩu phần ăn, không chỉ bằng một con số riêng lẻ trên nhãn. "
        "Khi so sánh sản phẩm, hãy xem chất này cùng năng lượng, đường, chất béo, natri và các thành phần liên quan khác."
    )


def _build_sources_and_labeling(nutrient: NutrientDetailResponse) -> str:
    name = _display_name(nutrient)
    sentences: list[str] = []

    if nutrient.vietnam_label_requirement:
        sentences.append(
            f"Trong ghi nhãn dinh dưỡng, {name} thuộc nhóm {_label_requirement_text(nutrient.vietnam_label_requirement)} khi công bố trên sản phẩm."
        )

    source_names = list(dict.fromkeys(
        source.name
        for source in nutrient.sources
        if source.name
    ))
    if source_names:
        sentences.append(f"Thông tin tham khảo có thể đối chiếu với {', '.join(source_names)}.")

    if not sentences:
        return (
            f"Khi cần hiểu sâu hơn về {name}, nên đối chiếu thêm với bảng thành phần, khẩu phần ăn và các tài liệu dinh dưỡng đáng tin cậy."
        )

    return " ".join(sentences)


def _strip_sentence_end(value: str) -> str:
    return value.strip().rstrip(".")


def _label_requirement_text(value: str) -> str:
    mapping = {
        "required": "thường cần được thể hiện rõ",
        "conditional": "có thể cần thể hiện tùy điều kiện",
        "optional": "không phải lúc nào cũng bắt buộc",
    }
    return mapping.get(value, value)
