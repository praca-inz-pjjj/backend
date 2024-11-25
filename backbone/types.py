from django.db import models


class LogType(models.TextChoices):
    LOGIN = 'LOGIN', 'Login' # Log in
    PASSWORD_RESET = 'PASSWORD_RESET', 'Password Reset' # Reset password
    CREATE = 'CREATE', 'Create' # Create something 
    DELETE = 'DELETE', 'Delete' # Delete something
    IMPORT = 'IMPORT', 'Import' # Import data  
    HISTORY = 'HISTORY', 'History' # Access history
    SIGN = 'SIGN', 'Sign' # Sign consent
    ISSUE = 'ISSUE', 'Issue' # Decision of issuer
    WARNING = 'WARNING', 'Warning'
    ERROR = 'ERROR', 'Error'
    INFO = 'INFO', 'Info'

class ConsentType(models.TextChoices):
    INFORMATION = 'INFORMATION', 'Information'
    BIOMETRIC = 'BIOMETRIC', 'Biometric'
    # etc.

class AccessType(models.IntegerChoices):
    NONE = 0, 'None'
    PARTIAL = 1 , 'Partial'
    FULL = 2 , 'Full'

class PermissionState(models.TextChoices):
    SLEEP = 'SLEEP', 'Sleep'
    NOTIFY = 'NOTIFY', 'Notify'
    ACTIVE = 'ACTIVE', 'Active'
    CLOSED = 'CLOSED', 'Closed'
    PERMANENT = 'PERMANENT', 'Permanent'