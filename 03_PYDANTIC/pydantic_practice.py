from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator


class AIModel(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    provider: str = Field(min_length=2, max_length=50)
    category: str = Field(min_length=2, max_length=30)
    max_tokens: int = Field(default=4096, gt=0, le=1000000) 
    description: str | None  = Field(default=None, max_length=300)


model = AIModel(
    name="GPT-X",
    provider="OpenAI",
    category="llm",
    max_tokens=8192,
)

print(model)

print(model.name)
print(model.provider)
print(model.max_tokens)
print(model.description)


model1 = AIModel(
    name="A",
    provider="OpenAI",
    category="llm",
)

print(model1)


# ===== 5. Type coercion: compatible string -> int =====

model_name = "GPT-X" *100

model2 = AIModel(
    name=model_name,
    provider="OpenAI",
    category="llm",
    max_tokens="8192",
)

print(model2.max_tokens)
print(type(model2.max_tokens))


# ===== 6. Impossible coercion: incompatible string -> int =====

model3 = AIModel(
    name="GPT-X",
    provider="OpenAI",
    category="llm",
    max_tokens="1000001",
)

print(model3.max_tokens)



model_description = "description" * 450
model3 = AIModel(
    name="GPT-X",
    provider="OpenAI",
    category="llm",
    max_tokens="1000001",
    description=model_description
)

print(model3.max_tokens)




# ===== 7. Optional vs default-None distinction =====

class RequiredButNullable(BaseModel):
    description: str | None


class OptionalWithDefault(BaseModel):
    description: str | None = None


# description is required here, but None is an accepted value
print(RequiredButNullable(description=None))

# omitting description entirely works only for the second model
print(OptionalWithDefault())




class Provider(BaseModel):
    name: str = Field(min_length=2)
    country: str = Field(min_length=2)

    @field_validator("name")
    @classmethod
    def strip_and_require_nonempty(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("name must not be empty or whitespace-only")
        return cleaned


class Pricing(BaseModel):
    type : str
    price : float = Field(ge=0)


class AdvancedAIModel(BaseModel):
    name: str
    category: Literal["llm", "embedding", "reranker"]
    provider: Provider
    capabilities: list[str]
    pricing: list[Pricing]
    tags: list[str] = Field(default_factory=list)

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(cls, value: str) -> str:
        return value.lower()


payload = {
    "name": "GPT-X",
    "category": "llm",
    "provider": {
        "name": "OpenAI",
        "country": "USA",
    },
    "capabilities": [
        "chat",
        "vision",
        "tool-calling",
    ],
    "pricing": [
        {
            "type": "input",
            "price": 1.25,
        },
        {
            "type": "output",
            "price": 5.0,
        },
    ],
}

advanced_model = AdvancedAIModel.model_validate(payload)

print(advanced_model)
print(advanced_model.provider)
print(type(advanced_model.provider))
print(advanced_model.pricing)
print(type(advanced_model.pricing))
print(advanced_model.pricing[0])
print(type(advanced_model.pricing[0]))
print(advanced_model.tags)


===== Failure tests =====
Each is run independently (try/except) so one failure doesn't stop the others.

----- Test 1: missing nested field (provider.country) -----

bad_payload_1 = {
    "name": "GPT-X",
    "category": "llm",
    "provider": {
        "name": "OpenAI",
        # "country" omitted on purpose
    },
    "capabilities": ["chat"],
    "pricing": [{"type": "input", "price": 1.25}],
}

try:
    AdvancedAIModel.model_validate(bad_payload_1)
except ValidationError as e:
    print("\n--- Test 1: missing provider.country ---")
    print(e)


----- Test 2: invalid nested price (price = -1) -----

bad_payload_2 = {
    "name": "GPT-X",
    "category": "llm",
    "provider": {"name": "OpenAI", "country": "USA"},
    "capabilities": ["chat"],
    "pricing": [{"type": "input", "price": -1}],
}

try:
    AdvancedAIModel.model_validate(bad_payload_2)
except ValidationError as e:
    print("\n--- Test 2: invalid price (-1) ---")
    print(e)


----- Test 3: invalid list item (pricing[1] missing "type") -----

bad_payload_3 = {
    "name": "GPT-X",
    "category": "llm",
    "provider": {"name": "OpenAI", "country": "USA"},
    "capabilities": ["chat"],
    "pricing": [
        {"type": "input", "price": 1.25},
        {"price": 5.0},  # "type" omitted on purpose
    ],
}

try:
    AdvancedAIModel.model_validate(bad_payload_3)
except ValidationError as e:
    print("\n--- Test 3: pricing[1] missing 'type' ---")
    print(e)


===== field_validator tests =====

----- Test A: valid normalization (whitespace stripped, category lowercased) -----

normalization_payload = {
    "name": "GPT-X",
    "category": "LLM",
    "provider": {"name": "  OpenAI  ", "country": "USA"},
    "capabilities": ["chat"],
    "pricing": [{"type": "input", "price": 1.25}],
}

normalized_model = AdvancedAIModel.model_validate(normalization_payload)
print("\n--- Test A: valid normalization ---")
print(repr(normalized_model.provider.name))
print(repr(normalized_model.category))


----- Test B: whitespace-only provider name -----

whitespace_payload = {
    "name": "GPT-X",
    "category": "llm",
    "provider": {"name": "      ", "country": "USA"},
    "capabilities": ["chat"],
    "pricing": [{"type": "input", "price": 1.25}],
}

try:
    AdvancedAIModel.model_validate(whitespace_payload)
except ValidationError as e:
    print("\n--- Test B: whitespace-only provider.name ---")
    print(e)


----- Test C: already-clean input -----

clean_payload = {
    "name": "GPT-X",
    "category": "embedding",
    "provider": {"name": "Cohere", "country": "Canada"},
    "capabilities": ["embed"],
    "pricing": [{"type": "input", "price": 0.1}],
}

clean_model = AdvancedAIModel.model_validate(clean_payload)
print("\n--- Test C: already-clean input ---")
print(repr(clean_model.provider.name))
print(repr(clean_model.category))



===================================

class ModelLimits(BaseModel):
    min_tokens: int = Field(ge=1)
    max_tokens: int = Field(ge=1)

    @model_validator(mode="after")
    def check_token_limits(self):
        if self.min_tokens >= self.max_tokens:
            raise ValueError("min_tokens must be strictly less than max_tokens")
        return self


class ModelPricingPlan(BaseModel):
    input_price: float = Field(ge=0)
    output_price: float = Field(ge=0)
    discounted_price: float | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def check_discounted_price(self):
        if self.discounted_price is not None and self.discounted_price > self.input_price:
            raise ValueError("discounted_price cannot be greater than input_price")
        return self


===== ModelLimits tests =====

----- Valid: 1000 < 8000 -----

limits_valid = ModelLimits(min_tokens=1000, max_tokens=8000)
print("\n--- ModelLimits valid ---")
print(limits_valid)

# ----- Invalid: min > max -----

try:
    ModelLimits(min_tokens=8000, max_tokens=4000)
except ValidationError as e:
    print("\n--- ModelLimits invalid: min_tokens > max_tokens ---")
    print(e)

# ----- Invalid: min == max -----

try:
    ModelLimits(min_tokens=5000, max_tokens=5000)
except ValidationError as e:
    print("\n--- ModelLimits invalid: min_tokens == max_tokens ---")
    print(e)


===== ModelPricingPlan tests =====

----- Valid: discounted_price provided and <= input_price -----

plan_valid_discount = ModelPricingPlan(input_price=5, output_price=10, discounted_price=4)
print("\n--- ModelPricingPlan valid: discounted_price=4 ---")
print(plan_valid_discount)

# ----- Valid: discounted_price omitted (None) -----

plan_valid_no_discount = ModelPricingPlan(input_price=5, output_price=10, discounted_price=None)
print("\n--- ModelPricingPlan valid: discounted_price=None ---")
print(plan_valid_no_discount)

# ----- Invalid: discounted_price > input_price -----

try:
    ModelPricingPlan(input_price=5, output_price=10, discounted_price=7)
except ValidationError as e:
    print("\n--- ModelPricingPlan invalid: discounted_price=7 > input_price=5 ---")
    print(e)


===== model_dump() =====

class ModelVendor(BaseModel):
    name: str
    region: str


class PriceTier(BaseModel):
    label: str
    price: float = Field(ge=0)


class ModelCard(BaseModel):
    name: str
    category: Literal["llm", "embedding", "reranker"]
    vendor: ModelVendor
    tiers: list[PriceTier]
    tags: list[str] = Field(default_factory=list)
    notes: str | None = None


# ----- Basic serialization: object vs dict vs JSON string -----

card = ModelCard(
    name="GPT-X",
    category="llm",
    vendor=ModelVendor(name="OpenAI", region="US"),
    tiers=[PriceTier(label="input", price=1.25), PriceTier(label="output", price=5.0)],
    tags=["chat", "vision"],
    notes="flagship model",
)

print("\n--- Pydantic object ---")
print(card)

dumped_dict = card.model_dump()
print("\n--- model_dump() ---")
print(dumped_dict)
print(type(dumped_dict))

dumped_json = card.model_dump_json()
print("\n--- model_dump_json() ---")
print(dumped_json)
print(type(dumped_json))


# ----- exclude_none=True (notes is None here) -----

card_no_notes = ModelCard(
    name="GPT-X",
    category="llm",
    vendor=ModelVendor(name="OpenAI", region="US"),
    tiers=[PriceTier(label="input", price=1.25)],
)

print("\n--- model_dump() without exclude_none ---")
print(card_no_notes.model_dump())

print("\n--- model_dump(exclude_none=True) ---")
print(card_no_notes.model_dump(exclude_none=True))


----- Nested serialization -----

dumped = card.model_dump()

print("\n--- Nested model_dump() ---")
print(type(dumped))
print(type(dumped["vendor"]))
print(type(dumped["tiers"]))
print(type(dumped["tiers"][0]))


===== ConfigDict =====

class APIModelCreate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str
    provider: str
    category: str
    max_tokens: int


# ----- Test 1: whitespace stripping -----

whitespace_model = APIModelCreate(
    name="  GPT-X  ",
    provider=" OpenAI ",
    category=" llm ",
    max_tokens=8192,
)

print("\n--- Test 1: whitespace stripping ---")
print(repr(whitespace_model.name))
print(repr(whitespace_model.provider))
print(repr(whitespace_model.category))


# ----- Test 2: extra field rejected -----

try:
    APIModelCreate(
        name="GPT-X",
        provider="OpenAI",
        category="llm",
        max_tokens=8192,
        secret_key="abc",
    )
except ValidationError as e:
    print("\n--- Test 2: extra field 'secret_key' ---")
    print(e)


# ----- Test 3: coercion without strict, then with strict -----

coerced_model = APIModelCreate(
    name="GPT-X",
    provider="OpenAI",
    category="llm",
    max_tokens="8192",
)

print("\n--- Test 3: max_tokens='8192' without strict ---")
print(coerced_model.max_tokens)
print(type(coerced_model.max_tokens))


class StrictTokens(BaseModel):
    model_config = ConfigDict(strict=True)

    max_tokens: int


try:
    StrictTokens(max_tokens="8192")
except ValidationError as e:
    print("\n--- Test 3: max_tokens='8192' with strict=True ---")
    print(e)


# ===== Request schema vs response schema =====

class ModelBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    provider: str
    category: Literal["llm", "embedding", "reranker"]


class ModelCreate(ModelBase):
    pass


class ModelResponse(ModelBase):
    id: int


# ----- Flow: ModelCreate -> model_dump() -> dict -> add id -> ModelResponse -----

model_create = ModelCreate(
    name="GPT-X",
    provider="OpenAI",
    category="llm",
)

print("\n--- ModelCreate instance ---")
print(model_create)

create_data = model_create.model_dump()
print("\n--- model_dump() ---")
print(create_data)

create_data["id"] = 9

model_response = ModelResponse.model_validate(create_data)
print("\n--- ModelResponse built from dict + id ---")
print(model_response)


# ----- Second test: contracts differ -----

try:
    ModelCreate(
        name="GPT-X",
        provider="OpenAI",
        category="llm",
        id=999,
    )
except ValidationError as e:
    print("\n--- ModelCreate rejects client-supplied id ---")
    print(e)

try:
    ModelResponse(
        name="GPT-X",
        provider="OpenAI",
        category="llm",
    )
except ValidationError as e:
    print("\n--- ModelResponse requires id ---")
    print(e)