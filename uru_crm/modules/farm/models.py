# -*- coding: utf-8 -*-
"""
    uru_crm.modules.farm
    ~~~~~~~~~~~~~~~~~~

    Farm model definition(s)
"""

from sqlalchemy import Column

from uru_crm.extensions import db
from uru_crm.utils import STRING_LEN
from uru_crm.modules.base import Base


class Farm(Base):
    farm = db.Column(db.String(STRING_LEN), nullable=False, unique=True)
    phone_num = Column(db.String(STRING_LEN), nullable=False, default='test')
    email = Column(db.String(STRING_LEN), nullable=False, unique=True)
    address = Column(db.String(STRING_LEN), nullable=False, default='test')
