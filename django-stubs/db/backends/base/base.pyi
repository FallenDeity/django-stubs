from collections.abc import Callable, MutableMapping
from contextlib import AbstractContextManager
from datetime import tzinfo
from logging import Logger
from typing import Any, TypeAlias

from django.db.backends.base.client import BaseDatabaseClient
from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.base.features import BaseDatabaseFeatures
from django.db.backends.base.introspection import BaseDatabaseIntrospection
from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.backends.base.validation import BaseDatabaseValidation
from django.db.backends.utils import CursorDebugWrapper, CursorWrapper
from django.db.transaction import Atomic
from django.utils.functional import cached_property
from typing_extensions import Self

NO_DB_ALIAS: str
RAN_DB_VERSION_CHECK: set[str]

logger: Logger

_ExecuteWrapper: TypeAlias = Callable[
    [Callable[[str, Any, bool, dict[str, Any]], Any], str, Any, bool, dict[str, Any]], Any
]

class BaseDatabaseWrapper:
    data_types: dict[str, str]
    data_types_suffix: dict[str, str]
    data_type_check_constraints: dict[str, str]
    vendor: str
    display_name: str
    SchemaEditorClass: type[BaseDatabaseSchemaEditor]
    client_class: type[BaseDatabaseClient]
    creation_class: type[BaseDatabaseCreation]
    features_class: type[BaseDatabaseFeatures]
    introspection_class: type[BaseDatabaseIntrospection]
    ops_class: type[BaseDatabaseOperations]
    validation_class: type[BaseDatabaseValidation]
    queries_limit: int
    connection: Any
    settings_dict: dict[str, Any]
    alias: str
    queries_log: Any
    force_debug_cursor: bool
    autocommit: bool
    in_atomic_block: bool
    savepoint_state: int
    savepoint_ids: list[str]
    commit_on_exit: bool
    needs_rollback: bool
    close_at: float | None
    closed_in_transaction: bool
    errors_occurred: bool
    run_on_commit: list[tuple[set[str], Callable[[], None]]]
    run_commit_hooks_on_set_autocommit_on: bool
    execute_wrappers: list[_ExecuteWrapper]
    client: BaseDatabaseClient
    creation: BaseDatabaseCreation
    features: BaseDatabaseFeatures
    introspection: BaseDatabaseIntrospection
    ops: BaseDatabaseOperations
    validation: BaseDatabaseValidation
    operators: MutableMapping[str, str]
    atomic_blocks: list[Atomic]
    def __init__(self, settings_dict: dict[str, Any], alias: str = "default") -> None: ...
    def ensure_timezone(self) -> bool: ...
    @cached_property
    def timezone(self) -> tzinfo | None: ...
    @cached_property
    def timezone_name(self) -> str: ...
    @property
    def queries_logged(self) -> bool: ...
    @property
    def queries(self) -> list[dict[str, str]]: ...
    def get_database_version(self) -> tuple[int, ...]: ...
    def check_database_version_supported(self) -> None: ...
    def get_connection_params(self) -> dict[str, Any]: ...
    def get_new_connection(self, conn_params: Any) -> Any: ...
    def init_connection_state(self) -> None: ...
    def create_cursor(self, name: Any | None = None) -> Any: ...
    def connect(self) -> None: ...
    def check_settings(self) -> None: ...
    def ensure_connection(self) -> None: ...
    def cursor(self) -> CursorWrapper: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...
    def close(self) -> None: ...
    def savepoint(self) -> str | None: ...
    def savepoint_rollback(self, sid: str) -> None: ...
    def savepoint_commit(self, sid: str) -> None: ...
    def clean_savepoints(self) -> None: ...
    def get_autocommit(self) -> bool: ...
    def set_autocommit(
        self, autocommit: bool, force_begin_transaction_with_broken_autocommit: bool = False
    ) -> None: ...
    def get_rollback(self) -> bool: ...
    def set_rollback(self, rollback: bool) -> None: ...
    def validate_no_atomic_block(self) -> None: ...
    def validate_no_broken_transaction(self) -> None: ...
    def constraint_checks_disabled(self) -> AbstractContextManager[None]: ...
    def disable_constraint_checking(self) -> bool: ...
    def enable_constraint_checking(self) -> None: ...
    def check_constraints(self, table_names: Any | None = None) -> None: ...
    def is_usable(self) -> bool: ...
    def close_if_health_check_failed(self) -> None: ...
    def close_if_unusable_or_obsolete(self) -> None: ...
    @property
    def allow_thread_sharing(self) -> bool: ...
    def inc_thread_sharing(self) -> None: ...
    def dec_thread_sharing(self) -> None: ...
    def validate_thread_sharing(self) -> None: ...
    def prepare_database(self) -> None: ...
    @property
    def wrap_database_errors(self) -> Any: ...
    def chunked_cursor(self) -> CursorWrapper: ...
    def make_debug_cursor(self, cursor: CursorWrapper) -> CursorDebugWrapper: ...
    def make_cursor(self, cursor: CursorWrapper) -> CursorWrapper: ...
    def temporary_connection(self) -> AbstractContextManager[CursorWrapper]: ...
    def _nodb_cursor(self) -> AbstractContextManager[CursorWrapper]: ...
    def schema_editor(self, *args: Any, **kwargs: Any) -> BaseDatabaseSchemaEditor: ...
    def on_commit(self, func: Callable[[], object], robust: bool = False) -> None: ...
    def run_and_clear_commit_hooks(self) -> None: ...
    def execute_wrapper(self, wrapper: _ExecuteWrapper) -> AbstractContextManager[None]: ...
    def copy(self, alias: str | None = None) -> Self: ...
