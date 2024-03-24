from pydantic import BaseModel, PastDatetime, EmailStr, Field, model_validator, field_validator, computed_field
from typing import List, Optional
import re
import json


class StudentBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=15)
    last_name: str = Field(..., min_length=1, max_length=15)
    email: EmailStr = Field(...)
    

    
    