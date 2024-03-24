from pydantic import BaseModel, PastDatetime, EmailStr, Field, model_validator, field_validator, computed_field
from typing import List, Optional
import re
import json

def js_r(filename: str):
    with open(filename) as f_in:
        return json.load(f_in)


# class StudentBase(BaseModel):
#     first_name: str = Field(..., min_length=1, max_length=15, pattern=r"^[a-zA-Z]+$")
#     last_name: str = Field(..., min_length=1, max_length=15, pattern=r"^[a-zA-Z]+$")
#     check_in_time: PastDatetime = Field(...)
    
#     # @model_validator(mode='after')
#     # def check_first_equals_last(self):
#     #     if self.first_name != self.last_name:
#     #         raise ValueError("First name should equal last name.")
#     #     return self
    
#     @field_validator('last_name')
#     @classmethod
#     def check_last_is_alpha(cls, v:str) -> str:
#         pattern = r"[^a-zA-Z]"
        
#         matches = re.search(pattern, v)
        
#         if matches:
#             raise ValueError("Last name should only contain alphabetic characters.")
#         return v
    
#     @field_validator('first_name')
#     @classmethod
#     def check_last_is_alpha(cls, v:str) -> str:
#         pattern = r"[^a-zA-Z]"
        
#         matches = re.search(pattern, v)
        
#         if matches:
#             raise ValueError("Last name should only contain alphabetic characters.")
#         return v

class StudentBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=15)
    last_name: str = Field(..., min_length=1, max_length=15)
    email: EmailStr = Field(...)
    # check_in_time: Optional[PastDatetime] = None
    
    # @model_validator(mode='after')
    # def check_valid_inputs(self):
    #     if self.email.endswith('.edu'):
    #         raise ValueError("Email must be end with .edu.")
    #     return 
    
    @field_validator('email')
    @classmethod
    def check_email_is_edu(cls, v:str) -> str:
        if not v.endswith('.edu'):
            raise ValueError("Email must be end with .edu.")
        return v

    
    @field_validator('last_name')
    @classmethod
    def check_last_is_alpha(cls, v:str) -> str:
        pattern = r"[^a-zA-Z]"
        
        matches = re.search(pattern, v)
        
        if matches:
            raise ValueError("Last name should only contain alphabetic characters.")
        return v
    
    @field_validator('first_name')
    @classmethod
    def check_first_is_alpha(cls, v:str) -> str:
        pattern = r"[^a-zA-Z]"
        
        matches = re.search(pattern, v)
        
        if matches:
            raise ValueError("Last name should only contain alphabetic characters.")
        return v

class StudentOutput(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=15, pattern=r"^[a-zA-Z]+$")
    last_name: str = Field(..., min_length=1, max_length=15, pattern=r"^[a-zA-Z]+$")
    
    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
class CheckInBase(BaseModel):
    major: str = Field(...)
    email: EmailStr = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    
    # @field_validator('major')
    # @classmethod
    # def check_major_is_valid(cls, v:str) -> str:        
    #     a = js_r("majors.json")
    #     majors = [k['name'] for k in a["majors"]]
    #     if v not in majors:
    #         raise ValueError("Major must be a valid major.")
    #     return v
    
    @field_validator('email')
    @classmethod
    def check_email_is_edu(cls, v:str) -> str:
        if not v.endswith('.edu'):
            raise ValueError("Email must be end with .edu.")
        return v
    
    @field_validator('last_name')
    @classmethod
    def check_last_is_alpha(cls, v:str) -> str:
        pattern = r"[^a-zA-Z]"
        
        matches = re.search(pattern, v)
        
        if matches:
            raise ValueError("Last name should only contain alphabetic characters.")
        return v
    
    @field_validator('first_name')
    @classmethod
    def check_first_is_alpha(cls, v:str) -> str:
        pattern = r"[^a-zA-Z]"
        
        matches = re.search(pattern, v)
        
        if matches:
            raise ValueError("Last name should only contain alphabetic characters.")
        return v
    
    
    

    
    