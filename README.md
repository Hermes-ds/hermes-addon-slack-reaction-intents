# hermes-addon-slack-reaction-intents

A removable Hermes **addon** that turns Slack emoji reactions on Hermes bot messages into follow-up intents.

Under the hood, this addon uses the official Hermes **plugin API** and the `hermes_agent.plugins` entry-point mechanism, but the user-facing concept here is an **addon**.

## What it does

Supported reactions on Hermes-authored Slack messages:
- `thumbsup` / `+1` → approve and execute the proposal attached to the reacted message
- `question` → ask for only necessary next-step suggestions

Generated synthetic events are marked with:
- `suppress_busy_ack=true`
- `origin=slack_reaction_addon`

## Current status

This repo layout is prepared to be split into its own repository.
It assumes Hermes core already contains the required extension seam:
- `slack_reaction_added` async hook
- `gateway_pre_handle_event` hook
- `MessageEvent.flags`
- flag-based busy-ack suppression

## Layout

```text
hermes-addon-slack-reaction-intents/
├── pyproject.toml
├── plugin.yaml
├── README.md
├── LICENSE
├── .gitignore
├── slack_reaction_intents/
│   ├── __init__.py
│   ├── config.py
│   ├── handlers.py
│   ├── plugin.py
│   └── prompts.py
└── tests/
    ├── conftest.py
    ├── test_handlers.py
    └── test_placeholder.py
```

## Install

Example shared-runtime install:

```bash
source /opt/hermes-agent/venv-shared/bin/activate
pip install git+https://github.com/<org>/hermes-addon-slack-reaction-intents.git
hermes plugins enable slack-reaction-intents
systemctl restart hermes-ds-admin.service hermes-ds-default.service
```

Notes:
- The package name is `hermes-addon-slack-reaction-intents`
- The Hermes entry-point name remains `slack-reaction-intents`
- Hermes still enables/disables it through the plugin manager because that is the current official extension mechanism

## Update

```bash
source /opt/hermes-agent/venv-shared/bin/activate
pip install --upgrade git+https://github.com/<org>/hermes-addon-slack-reaction-intents.git
systemctl restart hermes-ds-admin.service hermes-ds-default.service
```

## Uninstall

```bash
source /opt/hermes-agent/venv-shared/bin/activate
hermes plugins disable slack-reaction-intents || true
pip uninstall -y hermes-addon-slack-reaction-intents
systemctl restart hermes-ds-admin.service hermes-ds-default.service
```

## Development

This addon imports Hermes modules such as `gateway.platforms.base`, so local development needs Hermes source importable.

Preferred options:

### Option A — point tests at a Hermes checkout

```bash
export HERMES_AGENT_SRC=/path/to/hermes-agent
pytest -q
```

### Option B — run tests from inside a Hermes workspace/venv

```bash
source /opt/hermes-agent/venv-shared/bin/activate
export HERMES_AGENT_SRC=/opt/hermes-agent
pytest -q .hermes/scaffolds/hermes-addon-slack-reaction-intents/tests
```

## Scope boundaries

This addon owns:
- Slack reaction → intent mapping
- bot-message validation
- reacted-message lookup
- `reactions.get` fallback
- synthetic `MessageEvent` creation

Hermes core should only own:
- hook invocation seams
- event flag plumbing
- generic busy-ack behavior

## Terminology

To avoid confusion:
- **addon** = this removable custom extension
- **plugin API** = Hermes official internal extension interface used by the addon
