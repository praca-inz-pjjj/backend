from backbone.models import CustomUser

class UserValidator:
    @staticmethod
    def is_email_taken(email: str) -> bool:
        return CustomUser.objects.filter(email=email).exists()
    
    @staticmethod
    def is_phone_taken(phone: str) -> bool:
        return CustomUser.objects.filter(phone_number=phone).exists()
