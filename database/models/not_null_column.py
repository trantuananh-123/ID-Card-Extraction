from sqlalchemy import Column
from database.sql_alchemy_init import db


def NotNullColumn(*args, **kwargs):
    kwargs["nullable"] = kwargs.get("nullable", False)
    return Column(*args, **kwargs)
