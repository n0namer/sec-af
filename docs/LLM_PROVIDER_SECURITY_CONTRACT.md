# SEC-AF — LLM Provider & Security Profile

Status: canonical repo-local provider profile
Cross-component contract: `n0namer/universal-solver:main/docs/architecture/llm-provider-security-contract.md`

## Current source contract

`agentfield-package.yaml` currently declares:
- required `OPENROUTER_API_KEY`;
- optional `HARNESS_PROVIDER`;
- optional `HARNESS_MODEL`;
- optional `AI_MODEL` for direct AI calls;
- AgentField control-plane credentials separately.

The current manifest is therefore **OpenRouter-centric**. Do not infer Gonka/OpenAI-compatible support from fleet conventions alone.

## Provider rule

SEC-AF may use two LLM paths:
1. coding-agent harness path (`HARNESS_PROVIDER` + `HARNESS_MODEL`);
2. direct AI path (`AI_MODEL` plus the provider configuration used by code/runtime).

These paths MUST be verified independently. A working harness call does not prove the direct AI path, and vice versa.

## Gonka/OpenAI-compatible adoption rule

If SEC-AF is migrated to Gonka/OpenAI-compatible routing, prove before changing the manifest that:
- source/runtime supports `OPENAI_API_KEY` and `OPENAI_BASE_URL` end-to-end;
- selected models use the intended OpenAI-compatible namespace;
- harness and direct-AI paths both preserve the custom base URL where applicable;
- no unintended OpenRouter fallback occurs.

Until then, current OpenRouter requirements remain source truth.

## Security requirements

- Never commit/log raw provider or AgentField credentials.
- Report only presence/config state and redacted provider/model identity.
- Repository/workspace scan data may contain sensitive code; do not expose it unnecessarily in logs/evidence.
- LLM credentials, AgentField credentials, and repository/workspace access are separate capabilities.
- Unexpected fallback to another provider is a functional failure.

## Acceptance ladder

1. Exact SEC-AF source/runtime identity known.
2. Package starts and node registers.
3. Intended harness provider/model resolves.
4. Intended direct-AI provider/model resolves if that path is exercised.
5. Minimal real model/harness call succeeds.
6. Provider evidence shows the intended endpoint/provider with no unintended fallback.
7. Security scan canary produces a semantically valid, code-grounded result.

Health/registration alone is not provider or semantic PASS.

## Failure classes

Use: `BOOTSTRAP_ADMISSION`, `MODEL_RESOLUTION`, `ENV_PROPAGATION`, `BASE_URL_LOSS`, `AUTH`, `FALLBACK`, `TRANSPORT`, `SEMANTIC`.

Patch the first failing layer only.
