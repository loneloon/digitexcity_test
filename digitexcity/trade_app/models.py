from django.db import models
from patterns.reused_models import SimpleBankBase
from .urls import app_name
from patterns.reused_models import AppRegister


class TradeBalance(SimpleBankBase):
    """
    All app balance models are created with a Base class located in patterns package
    """
    pass
