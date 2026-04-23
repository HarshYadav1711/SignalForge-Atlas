# SignalForge Atlas

Production-grade, agent-based crypto prediction backend (Python only), designed for local execution and internship assessment demos.

## Scope

- Hermes-style modular agent architecture with feedback loop
- OpenRouter integration using free models only
- Free/public crypto data integrations
- Polymarket and Kalshi market discovery with safe fallbacks
- Time-series prediction engine (Kronos if feasible, otherwise justified substitute)
- Kelly-criterion risk management
- Memory + evaluation loop
- Structured logging and robust error handling

## Current Progress

Step 1 complete:
- Python project scaffold
- Package layout for agents/data/markets/prediction/risk/memory/evaluation/pipeline
- Configuration and logging foundations
- CLI entrypoint

## Quick Start

1. Create virtual environment and install:
   - `python -m venv .venv`
   - `.venv\\Scripts\\activate`
   - `pip install -e .[dev]`
2. Configure environment:
   - Copy `.env.example` to `.env`
   - Fill required values
3. Run:
   - `signalforge-atlas`

## Repository Layout

- `signalforge_atlas/config.py` - strongly typed environment config
- `signalforge_atlas/logging.py` - centralized logger setup
- `signalforge_atlas/main.py` - backend CLI entrypoint
- `signalforge_atlas/*` - modular domains (agents, data sources, markets, models, risk, memory, evaluation, pipeline)

## Notes

- No frontend, no dashboards, no live trading, no paid services.
- The implementation will be built incrementally step-by-step.
