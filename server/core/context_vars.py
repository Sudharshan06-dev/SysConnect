from contextvars import ContextVar

user_id_ctx = ContextVar('current_user', default=None)