from enum import Enum
from pydantic import BaseModel, Field


class Gender(str, Enum):
    male = "Male"
    female = "Female"


class YesNo(str, Enum):
    yes = "Yes"
    no = "No"


class InternetService(str, Enum):
    dsl = "DSL"
    fiber = "Fiber optic"
    no = "No"


class MultipleLines(str, Enum):
    yes = "Yes"
    no = "No"
    no_phone_service = "No phone service"


class ContractType(str, Enum):
    month_to_month = "Month-to-month"
    one_year = "One year"
    two_year = "Two year"


class PaymentMethod(str, Enum):
    bank_transfer = "Bank transfer (automatic)"
    credit_card = "Credit card (automatic)"
    electronic_check = "Electronic check"
    mailed_check = "Mailed check"


class Message(BaseModel):
    message: str


class Health(BaseModel):
    status: str
    model_loaded: bool
    metrics_loaded: bool
    threshold_loaded: bool


class Info(BaseModel):
    model_version: str
    trained_at: str
    threshold: float
    test_accuracy: float
    test_precision: float
    test_recall: float
    test_f1: float
    test_roc_auc: float
    test_pr_auc: float


class PredictionLabel(str, Enum):
    churn = "churn"
    not_churn = "not churn"


class PredictionResponse(BaseModel):
    churn_probability: float
    prediction: int
    label: PredictionLabel
    threshold_used: float


class CustomerRequest(BaseModel):
    gender: Gender = Field(description="Gender of the customer", examples=["Male"])

    seniorcitizen: int = Field(
        description="Whether customer is a senior citizen (0 = No, 1 = Yes)",
        ge=0,
        le=1,
        examples=[0],
    )

    partner: YesNo = Field(
        description="Whether customer has a partner", examples=["Yes"]
    )

    dependents: YesNo = Field(
        description="Whether customer has dependents", examples=["No"]
    )

    tenure: int = Field(
        description="Number of months the customer has stayed",
        ge=0,
        le=100,
        examples=[12],
    )

    phoneservice: YesNo = Field(
        description="Whether customer has phone service", examples=["Yes"]
    )

    multiplelines: MultipleLines = Field(
        description="Multiple phone lines status", examples=["No"]
    )

    internetservice: InternetService = Field(
        description="Type of internet service", examples=["DSL"]
    )

    onlinesecurity: YesNo = Field(
        description="Online security subscription", examples=["No"]
    )

    onlinebackup: YesNo = Field(
        description="Online backup subscription", examples=["Yes"]
    )

    deviceprotection: YesNo = Field(
        description="Device protection plan", examples=["No"]
    )

    techsupport: YesNo = Field(
        description="Technical support subscription", examples=["No"]
    )

    streamingtv: YesNo = Field(
        description="Streaming TV subscription", examples=["Yes"]
    )

    streamingmovies: YesNo = Field(
        description="Streaming movies subscription", examples=["No"]
    )

    contract: ContractType = Field(
        description="Type of contract", examples=["Month-to-month"]
    )

    paperlessbilling: YesNo = Field(
        description="Whether paperless billing is enabled", examples=["Yes"]
    )

    paymentmethod: PaymentMethod = Field(
        description="Customer payment method", examples=["Electronic check"]
    )

    monthlycharges: float = Field(
        description="Monthly charges billed to the customer", gt=0.0, examples=[40.35]
    )

    totalcharges: float = Field(
        description="Total charges billed to the customer", gt=0.0, examples=[165.35]
    )
