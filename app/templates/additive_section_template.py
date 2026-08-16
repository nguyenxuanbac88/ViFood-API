from app.schemas.additive_v1_schema import (
    AdditiveDetailResponse,
    AdditiveSectionResponse,
)


def build_additive_sections(
    additive: AdditiveDetailResponse,
) -> list[AdditiveSectionResponse]:
    return [
        AdditiveSectionResponse(
            section_type="overview",
            title=f"{_display_name(additive)} là gì?",
            content=_build_overview(additive),
        ),
        AdditiveSectionResponse(
            section_type="food_role",
            title="Vì sao có trong thực phẩm?",
            content=_build_food_role(additive),
        ),
        AdditiveSectionResponse(
            section_type="permitted_foods",
            title="Thường gặp ở đâu?",
            content=_build_permitted_foods(additive),
        ),
        AdditiveSectionResponse(
            section_type="sources_and_regulations",
            title="Khi đọc nhãn cần lưu ý",
            content=_build_sources_and_regulations(additive),
        ),
    ]


def _display_name(additive: AdditiveDetailResponse) -> str:
    return additive.name_vi or additive.name or additive.id


def _english_name(additive: AdditiveDetailResponse) -> str | None:
    if additive.name and additive.name != additive.name_vi:
        return additive.name
    return None


def _alias_names(additive: AdditiveDetailResponse) -> list[str]:
    aliases = [
        alias.name
        for alias in additive.aliases
        if alias.name
    ]

    if additive.ins:
        aliases.insert(0, f"INS {additive.ins}")

    return list(dict.fromkeys(aliases))


def _function_names(additive: AdditiveDetailResponse) -> list[str]:
    return list(dict.fromkeys(
        function.name[:1].lower() + function.name[1:]
        for function in additive.functions
        if function.name
    ))


def _category_names(
    additive: AdditiveDetailResponse,
    limit: int = 8,
) -> list[str]:
    names = [
        category.name_vi or category.name
        for category in additive.permitted_categories
        if category.name_vi or category.name
    ]
    return list(dict.fromkeys(names))[:limit]


def _build_overview(additive: AdditiveDetailResponse) -> str:
    name = _display_name(additive)
    sentences = [
        f"{name} là một phụ gia thực phẩm, tức là chất được thêm vào sản phẩm "
        "với một mục đích công nghệ nhất định."
    ]

    if additive.ins:
        sentences.append(f"Trên nhãn, chất này có thể được nhận diện bằng mã INS {additive.ins}.")

    english_name = _english_name(additive)
    if english_name:
        sentences.append(f"Tên tiếng Anh thường gặp là {english_name}.")

    aliases = _alias_names(additive)
    if aliases:
        sentences.append(f"Một số cách ghi khác có thể gặp là {', '.join(aliases)}.")

    return " ".join(sentences)


def _build_food_role(additive: AdditiveDetailResponse) -> str:
    name = _display_name(additive)
    functions = _function_names(additive)

    if functions:
        return (
            f"{name} thường được dùng với vai trò {', '.join(functions)}. "
            "Tùy sản phẩm, vai trò này có thể liên quan đến mùi vị, màu sắc, cấu trúc, "
            "độ ổn định hoặc thời hạn sử dụng."
        )

    return (
        f"Khi thấy {name} trên nhãn, nên hiểu đây là một phụ gia được dùng "
        "vì mục đích công nghệ của sản phẩm. "
        "Để biết chính xác vai trò, cần đọc thêm nhóm chức năng hoặc mã phụ gia đi kèm "
        "nếu nhà sản xuất có công bố."
    )


def _build_permitted_foods(additive: AdditiveDetailResponse) -> str:
    name = _display_name(additive)
    categories = _category_names(additive)

    if categories:
        return (
            f"{name} có thể xuất hiện trong các nhóm thực phẩm như {', '.join(categories)}. "
            "Điều này không có nghĩa chất này được dùng trong mọi sản phẩm thuộc các nhóm đó; "
            "việc sử dụng còn phụ thuộc công thức và giới hạn áp dụng."
        )

    return (
        f"{name} có thể được phép dùng trong một số nhóm thực phẩm nhất định. "
        "Khi cần đánh giá kỹ hơn, nên xem tên nhóm thực phẩm, hàm lượng nếu có "
        "và quy định phụ gia tương ứng."
    )


def _build_sources_and_regulations(additive: AdditiveDetailResponse) -> str:
    name = _display_name(additive)
    sentences = [
        f"Khi đọc nhãn có {name}, điều quan trọng là xem chất này xuất hiện cùng nhóm thực phẩm nào "
        "và được ghi bằng tên hay mã INS."
    ]

    references = list(dict.fromkeys(
        item
        for item in [
            *[
                source.name
                for source in additive.sources
                if source.name
            ],
            *[
                regulation.name
                for regulation in additive.regulations
                if regulation.name
            ],
        ]
        if item
    ))
    if references:
        sentences.append(f"Các thông tin liên quan có thể đối chiếu với {', '.join(references)}.")

    sentences.append(
        "Phần này chỉ giúp hiểu ý nghĩa của phụ gia trên nhãn, không tự kết luận sản phẩm "
        "là tốt hay xấu nếu thiếu bối cảnh khẩu phần và tần suất sử dụng."
    )

    return " ".join(sentences)
