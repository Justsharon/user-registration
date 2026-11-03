
import phonenumbers
from phonenumbers import PhoneNumberFormat
from pydantic import BaseModel, EmailStr, field_validator


class PhoneNumberSchema(BaseModel):
    phone_number: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str):
        try:
            number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(number):
                raise ValueError("Invalid phone number")

            normalized = phonenumbers.format_number(
                number,
                PhoneNumberFormat.E164
            )

            return normalized

        except phonenumbers.NumberParseException:
            raise ValueError("Invalid phone number")
        
    
class UserLookup(PhoneNumberSchema):
    pass

class UserCreate(PhoneNumberSchema):
    full_name: str
    email: EmailStr
    id_number: str

class UserLookupResponse(BaseModel):
    registered: bool
    message: str


class UserResponse(BaseModel):
    success: bool
    message: str

