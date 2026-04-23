# SignalForge Atlas

## Overview
SignalForge Atlas is a backend intelligence system for short-horizon crypto signal generation and risk-aware decision support. It is designed to operate on sub-hour timeframes, with a primary focus on 5-minute directional movement in Bitcoin and Ethereum markets.

The system integrates market discovery, structured data ingestion, probabilistic forecasting, LLM-assisted reasoning, and disciplined capital allocation into a single cohesive pipeline. It is engineered for clarity, reliability, and extensibility, with a strong emphasis on deterministic behavior and transparent decision-making.

## Product Vision
SignalForge Atlas is built around a simple principle:  
prediction without structured decision-making has limited value.

Instead of stopping at directional forecasts, the system produces complete, risk-adjusted signals that can be evaluated, compared, and iteratively improved. The architecture is intentionally modular, enabling seamless evolution toward more advanced models, broader market coverage, and real-time execution environments.

## Core Capabilities

- Short-horizon signal generation for BTC and ETH  
- Market-aware opportunity discovery across prediction platforms  
- Deterministic probabilistic forecasting based on time-series features  
- LLM-assisted signal validation using constrained reasoning  
- Kelly-based position sizing for disciplined exposure control  
- Persistent memory and performance tracking across runs  
- Fault-tolerant pipeline with structured logging  

## System Architecture

SignalForge Atlas is composed of independent, cooperating components that form a continuous decision loop:

1. Market Discovery Engine  
Identifies relevant short-horizon prediction markets across multiple sources and normalizes them into a unified structure.

2. Data Ingestion Layer  
Retrieves recent OHLC price data for target assets using stable public market data endpoints. Ensures consistency and low-latency access.

3. Forecasting Engine  
Produces probabilistic predictions using a deterministic momentum-volatility framework. The implementation is designed to be lightweight, interpretable, and replaceable with higher-capacity models.

4. Reasoning Layer  
Applies constrained LLM-based evaluation to refine raw predictions into actionable decisions. The model is used strictly as a decision filter, not as a data source.

5. Risk Engine  
Converts probabilistic confidence into position sizing using the Kelly criterion, with enforced caps to maintain risk discipline.

6. Evaluation and Memory System  
Stores historical signals and outcomes in append-only JSONL format, computes performance metrics, and enables feedback-driven iteration.

This architecture follows a modular agent-based pattern, where each component is independently testable and can evolve without impacting the overall system.

## Architectural Notes

Kronos Adapter Strategy  
Kronos is represented through an explicit adapter boundary so forecasting remains interface-driven and swap-ready. This keeps the prediction contract stable while enabling deterministic fallback inference when direct Kronos runtime integration is unavailable or intentionally deferred.

Hermes-Oriented Orchestration  
Hermes is implemented as an orchestration layer that coordinates modular agents across the full decision lifecycle. This reflects the intended multi-agent control pattern without coupling orchestration concerns to forecasting, reasoning, or risk logic.

Constraint-Aware API Selection  
Free public APIs are used by design to ensure local reproducibility, zero-cost execution, and predictable operational behavior. This constraint-aware approach favors transparent dependencies and removes hidden infrastructure assumptions.

Deterministic and Fallback Philosophy  
SignalForge Atlas is intentionally built around deterministic core computation and controlled degradation paths. When external systems are unavailable, safe fallbacks preserve continuity while maintaining bounded, explainable outputs.

## Design Principles

- Determinism First  
Core prediction logic is reproducible and explainable. No hidden randomness or opaque behavior.

- Separation of Concerns  
Each module has a clearly defined responsibility, enabling maintainability and extensibility.

- Controlled Use of LLMs  
The reasoning layer operates within strict boundaries and does not introduce external or fabricated data.

- Operational Reliability  
External dependencies are wrapped with timeouts, retries, and safe fallbacks to ensure consistent execution.

- Minimal Surface Area  
The system avoids unnecessary abstractions, UI layers, or external services that do not contribute to core functionality.

## Technology Stack

- Python  
- Modular agent-based architecture  
- OpenRouter (free model routing for reasoning layer)  
- Public APIs for market discovery and price data  
- Lightweight append-only JSONL storage  
- Standard logging framework for observability  

The system is designed to run fully locally without requiring paid services or proprietary infrastructure.

## Getting Started

Installation:
pip install -r requirements.txt

Environment Configuration:
Create a `.env` file:
OPENROUTER_API_KEY=your_key  
APIFY_API_TOKEN=optional  

Run:
python main.py

The system executes a full signal generation cycle and outputs structured results to the console while logging detailed execution traces.

## Example Output

=== SIGNAL OUTPUT ===
{
  "asset": "BTC",
  "prediction": "UP",
  "probability": 0.64,
  "decision": "STRONG_BUY",
  "position_size": 0.18
}

=== PERFORMANCE ===
accuracy: 0.61

## Engineering Decisions

Forecasting Strategy  
The current forecasting engine uses a deterministic momentum-volatility model designed for stability and interpretability. It is implemented behind a model interface to allow seamless replacement with higher-capacity systems without altering downstream components.

Market Data Selection  
A stable, high-availability public data source is used for OHLC ingestion to ensure consistent execution without reliance on paid APIs.

Platform Integration  
Where direct integration constraints exist, fallback mechanisms are implemented to preserve system continuity while maintaining transparency.

Reasoning Layer Boundaries  
The LLM is used strictly for bounded classification of signals and does not influence raw data or generate predictions.

## Limitations

- No direct trade execution layer  
- Simplified forecasting relative to large pretrained models  
- Limited asset coverage (BTC and ETH)  
- Outcome evaluation may rely on simulated or delayed ground truth  

These constraints are intentional to maintain a focused, reliable core system.

## Extensibility

The architecture supports straightforward expansion in several directions:

- Additional assets and markets  
- Multi-timeframe signal aggregation  
- Arbitrage detection across prediction horizons  
- Integration with higher-capacity forecasting models  
- Real-time streaming data pipelines  

## Observability and Reliability

- Structured logging across all pipeline stages  
- Graceful degradation on external API failures  
- Clear error reporting without interrupting full pipeline execution  

## Closing

SignalForge Atlas is built as a foundation for reliable, short-horizon market intelligence. It emphasizes disciplined engineering, transparent logic, and practical extensibility, making it suitable for both experimentation and evolution into more advanced systems.

## Environment Configuration

The system supports Apify-based data ingestion via an optional adapter.

To enable Apify:
- Create an Apify account
- Generate an API token
- Add it to your environment:

APIFY_API_TOKEN=your_token_here

Note:
Apify integration is optional and not required for local execution.