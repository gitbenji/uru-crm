# -*- coding: utf-8 -*-
"""
    uru_crm.modules.veggies
    ~~~~~~~~~~~~~~~~~~

    Available_Veggie model definition(s)
"""

from sqlalchemy import Column

from uru_crm.extensions import db
from uru_crm.utils import STRING_LEN
from uru_crm.modules.base import Base


class Available_Veggie(Base):
    veggie = db.Column(db.String(STRING_LEN), nullable=False)
    farm = db.Column(db.String(STRING_LEN), nullable=False)
    quantity = db.Column(db.String(STRING_LEN), nullable=False)
