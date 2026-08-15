from app.schemas.ingredient_v1_schema import (
    IngredientDetailResponse,
    IngredientSectionResponse,
)


def build_ingredient_sections(
    ingredient: IngredientDetailResponse,
) -> list[IngredientSectionResponse]:
    sections: list[IngredientSectionResponse] = []

    overview = _build_overview(ingredient)
    if overview:
        sections.append(
            IngredientSectionResponse(
                section_type="description",
                title=f"{_display_name(ingredient)} là gì?",
                content=overview,
            )
        )

    aliases = _build_aliases(ingredient)
    if aliases:
        sections.append(
            IngredientSectionResponse(
                section_type="aliases",
                title="Có thể được ghi bằng tên nào?",
                content=aliases,
            )
        )

    categories = _build_categories(ingredient)
    if categories:
        sections.append(
            IngredientSectionResponse(
                section_type="categories",
                title="Thuộc nhóm nào?",
                content=categories,
            )
        )

    usages = _build_usages(ingredient)
    if usages:
        sections.append(
            IngredientSectionResponse(
                section_type="usages",
                title="Thường được dùng để làm gì?",
                content=usages,
            )
        )

    sources = _build_sources(ingredient)
    if sources:
        sections.append(
            IngredientSectionResponse(
                section_type="sources",
                title="Tìm hiểu thêm",
                content=sources,
            )
        )

    return sections


def _display_name(ingredient: IngredientDetailResponse) -> str:
    return ingredient.name_vi or ingredient.name or ingredient.name_en or ingredient.id


def _english_name(ingredient: IngredientDetailResponse) -> str | None:
    if ingredient.name_en and ingredient.name_en != ingredient.name_vi:
        return ingredient.name_en
    return None


def _build_overview(ingredient: IngredientDetailResponse) -> str | None:
    name = _display_name(ingredient)
    description = ingredient.description_vi or ingredient.description_en
    sentences: list[str] = []

    if description:
        sentences.append(_ensure_sentence(description))
    else:
        sentences.append(
            f"{name} là một thành phần có thể xuất hiện trong công thức hoặc danh sách nguyên liệu của thực phẩm."
        )

    english_name = _english_name(ingredient)
    if english_name:
        sentences.append(f"Trong tài liệu hoặc nhãn tiếng Anh, thành phần này thường được gọi là {english_name}.")

    return " ".join(sentences) if sentences else None


def _build_aliases(ingredient: IngredientDetailResponse) -> str | None:
    alias_names = list(dict.fromkeys(
        alias.name
        for alias in ingredient.aliases
        if alias.name and alias.name != _display_name(ingredient)
    ))
    if not alias_names:
        return None

    return (
        f"Khi đọc nhãn, {_display_name(ingredient)} có thể xuất hiện dưới một số tên gọi khác như "
        f"{', '.join(alias_names)}. "
        "Các tên này giúp nhận ra cùng một thành phần dù cách ghi trên sản phẩm không hoàn toàn giống nhau."
    )


def _build_categories(ingredient: IngredientDetailResponse) -> str | None:
    category_names = list(dict.fromkeys(
        category.name
        for category in ingredient.categories
        if category.name
    ))
    if not category_names:
        return None

    return (
        f"Về phân loại, {_display_name(ingredient)} có liên quan đến các nhóm như "
        f"{', '.join(category_names)}. "
        "Những nhóm này giúp đặt thành phần vào bối cảnh rộng hơn khi so sánh với các nguyên liệu cùng loại."
    )


def _build_usages(ingredient: IngredientDetailResponse) -> str | None:
    usage_names = list(dict.fromkeys(
        usage.name
        for usage in ingredient.usages
        if usage.name
    ))
    if not usage_names:
        return None

    return (
        f"Trong thực phẩm, {_display_name(ingredient)} có thể liên quan đến các mục đích sử dụng như "
        f"{', '.join(usage_names)}. "
        "Ý nghĩa cụ thể còn phụ thuộc vào công thức, hàm lượng và vai trò của thành phần trong từng sản phẩm."
    )


def _build_sources(ingredient: IngredientDetailResponse) -> str | None:
    links = list(dict.fromkeys(
        link
        for link in [
            *[
                source.source_url
                for source in ingredient.sources
                if source.source_url
            ],
            ingredient.wikipedia_vi_url,
            ingredient.wikipedia_en_url,
        ]
        if link
    ))
    if not links:
        return None

    return (
        "Có thể tham khảo thêm tại "
        + ", ".join(links)
        + ". Khi cần đánh giá một sản phẩm cụ thể, nên đọc thành phần này cùng toàn bộ danh sách nguyên liệu và bảng dinh dưỡng."
    )


def _ensure_sentence(value: str) -> str:
    sentence = value.strip()
    if sentence.endswith((".", "!", "?")):
        return sentence
    return sentence + "."
