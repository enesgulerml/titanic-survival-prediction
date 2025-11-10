# app/schema.py
from pydantic import BaseModel, Field
from typing import Optional

# The data model that our API will receive from outside
class Passenger(BaseModel):
    Pclass: int = Field(..., description="Passenger Class (1, 2, or 3)")
    Sex: str = Field(..., description="Sex ('male' or 'female')")
    Age: Optional[float] = Field(None, description="Age in years")
    SibSp: int = Field(..., description="Number of Siblings/Spouses Aboard")
    Parch: int = Field(..., description="Number of Parents/Children Aboard")
    Fare: float = Field(..., description="Passenger Fare")
    Embarked: Optional[str] = Field(None, description="Port of Embarkation (C, Q, or S)")



# The response model that our API will send out
class PredictionResponse(BaseModel):
    PassengerId: Optional[int] = None
    Survived: int