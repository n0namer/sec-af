from __future__ import annotations

import json
import time
from typing import Any, cast

from agentfield.execution_context import get_current_context

from sec_af.agents.recon.architecture import run_architecture_mapper as _run_architecture_mapper
from sec_af.agents.recon.config_scanner import run_config_scanner as _run_config_scanner
from sec_af.agents.recon.data_flow import run_data_flow_mapper as _run_data_flow_mapper
from sec_af.agents.recon.dependencies import run_dependency_auditor as _run_dependency_auditor
from sec_af.agents.recon.security_context import run_security_context_profiler as _run_security_context_profiler
from sec_af.schemas.recon import ArchitectureMap

from . import router


@router.reasoner()
async def run_architecture_mapper(repo_path: str) -> dict[str, Any]:
    runtime_router = cast(Any, router)
    runtime_router.note("Architecture mapper starting", tags=["recon", "architecture"])
    result = await _run_architecture_mapper(runtime_router, repo_path)
    return result.model_dump()


@router.reasoner()
async def run_dependency_auditor(repo_path: str) -> dict[str, Any]:
    runtime_router = cast(Any, router)
    runtime_router.note("Dependency auditor starting", tags=["recon", "dependencies"])
    result = await _run_dependency_auditor(runtime_router, repo_path)
    return result.model_dump()


def _emit_execution_event(event_type: str, *, level: str = "info", **attributes: Any) -> None:
    ctx = get_current_context()
    identity = ctx.to_log_identity() if ctx else {
        "execution_id": None,
        "workflow_id": None,
        "run_id": None,
        "root_workflow_id": None,
        "parent_execution_id": None,
        "agent_node_id": "sec-af",
        "reasoner_id": "run_config_scanner",
    }
    payload = {
        "timestamp": time.time(),
        **identity,
        "event_type": event_type,
        "source": "sec-af",
        "level": level,
        "attributes": {**(ctx.to_log_attributes() if ctx else {}), **attributes},
    }
    print(json.dumps(payload, sort_keys=True), flush=True)


@router.reasoner()
async def run_config_scanner(repo_path: str) -> dict[str, Any]:
    runtime_router = cast(Any, router)
    runtime_router.note("Config scanner starting", tags=["recon", "config"])
    _emit_execution_event("reasoner.start", repo_path=repo_path)
    started = time.monotonic()
    try:
        result = await _run_config_scanner(runtime_router, repo_path)
    except Exception as exc:
        _emit_execution_event(
            "reasoner.error",
            level="error",
            duration_ms=round((time.monotonic() - started) * 1000, 3),
            error_type=type(exc).__name__,
        )
        raise
    _emit_execution_event(
        "reasoner.complete",
        duration_ms=round((time.monotonic() - started) * 1000, 3),
    )
    return result.model_dump()


@router.reasoner()
async def run_data_flow_mapper(repo_path: str, architecture: dict[str, Any]) -> dict[str, Any]:
    runtime_router = cast(Any, router)
    runtime_router.note("Data flow mapper starting", tags=["recon", "data-flow"])
    architecture_model = ArchitectureMap(**architecture)
    result = await _run_data_flow_mapper(runtime_router, repo_path, architecture_model)
    return result.model_dump()


@router.reasoner()
async def run_security_context_profiler(repo_path: str, architecture: dict[str, Any]) -> dict[str, Any]:
    runtime_router = cast(Any, router)
    runtime_router.note("Security context profiler starting", tags=["recon", "security-context"])
    architecture_model = ArchitectureMap(**architecture)
    result = await _run_security_context_profiler(runtime_router, repo_path, architecture_model)
    return result.model_dump()
