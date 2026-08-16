from pydantic import BaseModel, Field


class IngredientNodeResponse(BaseModel):
    id: str
    name: str | None = None
    name_vi: str | None = None
    name_en: str | None = None
    wikidata_id: str | None = None
    description_vi: str | None = None
    description_en: str | None = None
    wikipedia_vi_url: str | None = None
    wikipedia_en_url: str | None = None
    status: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class IngredientAliasResponse(BaseModel):
    id: str | None = None
    name: str | None = None
    language: str | None = None


class IngredientCategoryResponse(BaseModel):
    id: str | None = None
    name: str | None = None
    wikidata_id: str | None = None


class IngredientUsageResponse(BaseModel):
    id: str | None = None
    name: str | None = None
    wikidata_id: str | None = None


class IngredientSourceResponse(BaseModel):
    id: str | None = None
    name: str | None = None
    source_url: str | None = None


class IngredientSectionResponse(BaseModel):
    section_type: str
    title: str
    content: str


class IngredientDetailResponse(IngredientNodeResponse):
    aliases: list[IngredientAliasResponse] = Field(default_factory=list, exclude=True)
    categories: list[IngredientCategoryResponse] = Field(default_factory=list, exclude=True)
    usages: list[IngredientUsageResponse] = Field(default_factory=list, exclude=True)
    sources: list[IngredientSourceResponse] = Field(default_factory=list, exclude=True)
    sections: list[IngredientSectionResponse] = Field(default_factory=list)


class IngredientListApiResponse(BaseModel):
    message: str
    data: list[IngredientNodeResponse]


class IngredientDetailApiResponse(BaseModel):
    message: str
    data: IngredientDetailResponse
