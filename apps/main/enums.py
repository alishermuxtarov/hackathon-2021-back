from django.utils.translation import ugettext as _
from django.db import models


class CargoStateType(models.TextChoices):
    NEW = 'new', _('Новый')
    EXECUTOR_CHOSEN = 'executor_chosen', _('Исполнитель выбран')
    CONTRACT_CREATED = 'contract_created', _('Контракт создан')
    CONTRACT_SIGNED = 'contract_signed', _('Контракт подписан')
    LOADED = 'loaded', _('Загружен')
    DELIVERED = 'delivered', _('Доставлен')
    CANCELLED = 'cancelled', _('Отменен')
