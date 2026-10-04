# Cluster 10: Multi-Agent Systems for Genetic Engineering

## Topic
Multi-agent systems (MAS) applied to genetic engineering and synthetic biology — architectures, algorithms, tools, costs, scalability, biosecurity, failure modes, and orchestration patterns.

---

## State-of-the-Art Approaches

1. **LLM-based Multi-Agent Systems (LLM-MAS)**: Systems where two or more LLM-parameterized agents exchange natural-language messages over a directed communication graph. Popularized by five canonical 2023 systems: CAMEL, AutoGen, MetaGPT, ChatDev, and Stanford's Generative Agents. [paperguru.ai](https://paperguru.ai/benchmark/pdfs/llm-based-multi-agent.pdf)

2. **Evidence-Grounded Bio-Robot Design (micro_biorobot_agent)**: A blackboard-architecture MAS with ~20 specialized components (LLM agents, deterministic rules, validators) collaborating through a shared structured design record for genetic-circuit-layer bio-robot design. Evaluated against RAG-only, single-agent, and multi-agent baselines. [arXiv:2608.19699](https://arxiv.org/pdf/2608.19699)

3. **AI Agents for Biological Research (5D Taxonomy Survey)**: Systematic synthesis of 100+ studies across clinical analytics, molecular/drug design, multi-omics, and knowledge discovery. Unified taxonomy along task domains, system architectures, interaction modes, evaluation strategies, and resource integration. [Europe PMC](https://europepmc.org/articles/pmc12936789?pdf=render)

4. **PARCO (Parallel AutoRegressive Combinatorial Optimization)**: RL framework for multi-agent combinatorial optimization using transformer-based communication layers, multiple pointer mechanism for parallel agent decision-making, and priority-based conflict handlers. NeurIPS 2025. [arXiv:2409.03811](https://arxiv.org/abs/2409.03811)

5. **Genetic Programming-based MAS Engineering (EGC)**: Semi-automated framework using Genetic Programming to evolve Gossip Contracts for decentralized multi-agent coordination, building on Contract Net and Gossip Protocol. [DOI:10.1145/3584731](https://doi.org/10.1145/3584731)

6. **Scalable MAS Reference Architecture**: Four design principles — simplicity, elastic feedback, sequential workflows with optional loops, and summary-based communication — operationalized via a constrained directed workflow graph with agent-controlled feedback loops. [arXiv:2607.27942](https://arxiv.org/abs/2607.27942)

7. **Multi-Agent Cooperative Decision-Making**: Five approach categories: rule-based (fuzzy logic), game theory-based, evolutionary algorithms-based, deep MARL-based, and LLM reasoning-based. [arXiv:2503.13415](https://arxiv.org/html/2503.13415v2)

---

## Most Cited Papers

1. **"Why Do Multi-Agent LLM Systems Fail?" (MAST)** — Introduces MAST-Data (1600+ annotated traces, 7 MAS frameworks), 14 fine-grained failure modes in 3 categories. Cohen's Kappa 0.88. [arXiv:2503.13657](https://arxiv.org/pdf/2503.13657v1)

2. **"PARCO: Parallel AutoRegressive Models for Multi-Agent Combinatorial Optimization"** — NeurIPS 2025. Transformer-based communication + multiple pointer mechanism + priority-based conflict resolution. [arXiv:2409.03811](https://arxiv.org/abs/2409.03811)

3. **"The Illusion of Multi-Agent Advantage"** — Systematic evaluation showing automatic MAS consistently underperform CoT-SC despite up to 10x cost. [arXiv:2606.13003](https://arxiv.org/html/2606.13003v2)

4. **"Scaling LLM-Driven Multi-Agent Systems"** — Four design principles, reference architecture, empirical scalability analysis across 4 configurations and 2 model tiers. [arXiv:2607.27942](https://arxiv.org/abs/2607.27942)

5. **"A Comprehensive Survey on Multi-Agent Cooperative Decision-Making"** — Categorizes approaches into rule-based, game theory, evolutionary, MARL, and LLM-based. [arXiv:2503.13415](https://arxiv.org/html/2503.13415v2)

6. **"From capability uplift to capability governance: an AI–biosecurity stack"** — Agentic AI systems as practical interface layer; multi-agent systems for biomedical hypothesis generation. [Frontiers in Microbiology](https://frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2026.1899413/pdf)

7. **"BioVeil MATRIX: Uncovering and categorizing vulnerabilities of agentic biological AI scientists"** — 10 tactical categories (TA01–TA10), 22 techniques for agentic biosecurity risks. [arXiv:2605.00927](https://arxiv.org/pdf/2605.00927)

8. **"Toward relational biosecurity"** — System-level sensing, preservation of context, buffering of perturbations across distributed actors. [Frontiers in Microbiology](https://frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2026.1856819/full)

---

## Bottlenecks

1. **Coordination overhead scales supra-linearly**: Interaction turns follow T = 2.72 × (n + 0.5)^1.724 (R² = 0.974). Doubling agents more than triples interaction turns. [Labo LLM](https://labo-llm.fr/en/enjeux/cout-reel-systeme-multi-agents)

2. **Context recreation cost**: Each sub-agent instantiates its own system prompt from scratch. An 8,000-token system prompt costs $0.024 per agent per call on Claude Sonnet 4.6. Over 50 calls, that's $3.60 per agent in pure recreation cost. [Labo LLM](https://labo-llm.fr/en/enjeux/cout-reel-systeme-multi-agents)

3. **Verification loops**: AgentOrchestra devotes 41.54% of trajectory to correction attempts vs 4.81% for solo agents. A Reflexion loop over 10 cycles can consume 50x more tokens than a single linear pass. [Labo LLM](https://labo-llm.fr/en/enjeux/cout-reel-systeme-multi-agents)

4. **Framework scaffolding overhead**: CrewAI injects ~150 tokens per agent of automatic role definitions. LangGraph ~800 tokens/request vs CrewAI ~1250 tokens/request at 10,000 requests/day. [Labo LLM](https://labo-llm.fr/en/enjeux/cout-reel-systeme-multi-agents)

5. **Run-to-run consistency**: Persistent consistency issues emerge as the central open problem for production-grade MAS across all scaling levels. [arXiv:2607.27942](https://arxiv.org/abs/2607.27942)

6. **Communication overload and inter-agent inconsistency**: Scaling agent systems grows complexity, giving rise to communication overload, inter-agent inconsistency, loss of efficiency, and loss of system-wide task alignment. [arXiv:2607.27942](https://arxiv.org/abs/2607.27942)

7. **Faulty response propagation**: Downstream agents accept and reinforce framing established by upstream agents, mirroring documented propagation of faulty responses between agents. [arXiv:2607.27942](https://arxiv.org/abs/2607.27942)

8. **NP-hard coordination**: Multi-agent combinatorial optimization problems are notoriously challenging due to their NP-hard nature and the necessity for effective agent coordination. [arXiv:2409.03811](https://arxiv.org/abs/2409.03811)

---

## NP-Hard Problems

1. **Multi-Agent Combinatorial Optimization**: Involving multiple agents, these problems are NP-hard and require effective agent coordination. Cannot generally be solved optimally in polynomial time. [arXiv:2409.03811](https://arxiv.org/abs/2409.03811)

2. **Multi-Agent Vehicle Routing and Scheduling**: Evaluated as benchmark tasks for PARCO; inherently NP-hard with agent coordination requirements. [arXiv:2409.03811](https://arxiv.org/abs/2409.03811)

3. **Decentralized Cooperation Protocol Search**: Using Genetic Programming to search for optimal Gossip Contracts implementations is a combinatorial search problem. [DOI:10.1145/3584731](https://doi.org/10.1145/3584731)

4. **Multi-Agent Reinforcement Learning (MARL)**: Learning optimal policies in multi-agent MDPs is fundamentally harder than single-agent RL due to non-stationarity and exponential joint action spaces. [arXiv:2503.13415](https://arxiv.org/html/2503.13415v2)

---

## OSS Projects

1. **LangGraph** — Graph-based state machines, most flexible orchestration. ~9% token overhead. 126k GitHub stars. [yashbogam.me](https://yashbogam.me/ai/multi-agent-systems)

2. **CrewAI** — Role-based team orchestration with Crews + Flows model. ~18% token overhead. v1.13, 60%+ Fortune 500. [yashbogam.me](https://yashbogam.me/ai/multi-agent-systems)

3. **AutoGen (Microsoft)** — Conversation-first multi-agent, event-driven message passing. Highest LLM call count (20+ calls/task). [yashbogam.me](https://yashbogam.me/ai/multi-agent-systems)

4. **OpenAI Agents SDK** — Handoff-based swarms with guardrails, native tracing. Successor to Swarm. [yashbogam.me](https://yashbogam.me/ai/multi-agent-systems)

5. **Agent Orchestrator (formerly Composio)** — Full-automation system with 26 worker agent harnesses, isolated worktrees, autonomous PR handling. Apache-2.0. [augmentcode.com](https://augmentcode.com/tools/open-source-agent-orchestrators)

6. **Emdash** — Electron desktop app, 34 CLI providers, $EMDASH_PORT injection for port collision avoidance. Apache-2.0. [augmentcode.com](https://augmentcode.com/tools/open-source-agent-orchestrators)

7. **Bernstein** — Full planning-to-merge pipeline with deterministic scheduling, zero LLM tokens on coordination, Janitor verification. Apache-2.0. [augmentcode.com](https://augmentcode.com/tools/open-source-agent-orchestrators)

8. **Conductor (Microsoft)** — YAML-defined workflows, parallel groups, HITL, conditional routing. MIT. [augmentcode.com](https://augmentcode.com/tools/open-source-agent-orchestrators)

9. **agent-swarm** — Durable task delegation, persistent memory, Docker-isolated workers. MIT for self-hosted. [agent-swarm.dev](https://agent-swarm.dev/blog/open-source-ai-orchestration)

10. **Orloj** — YAML manifests, Postgres state, NATS JetStream messaging, governance primitives. [agent-swarm.dev](https://agent-swarm.dev/blog/open-source-ai-orchestration)

11. **AgentOps** — Python SDK, auto-instruments LangGraph/CrewAI/AutoGen, OpenTelemetry-shaped telemetry. MIT. [futureagi.com](https://futureagi.com/blog/best-tools-monitoring-multi-agent-systems-2026)

12. **Arize Phoenix** — Source-available, OpenInference reference, OTel-native multi-agent traces. ELv2. [futureagi.com](https://futureagi.com/blog/best-tools-monitoring-multi-agent-systems-2026)

13. **MAST (Multi-Agent System Failure Taxonomy)** — Dataset + LLM annotator for MAS failure analysis. [GitHub](https://github.com/multi-agent-systems-failure-taxonomy/MASFT)

14. **PARCO** — Open-source code at github.com/ai4co/parco. [arXiv:2409.03811](https://arxiv.org/abs/2409.03811)

---

## Hardware Requirements

1. **Cloud-based LLM agents**: No special hardware; API-based access to GPT-4, Claude, Gemini, etc. Self-hosted open-source models require GPU infrastructure ($2-8/hour for A100/H100). [kanopylabs.com](https://kanopylabs.com/blog/how-much-does-it-cost-to-build-a-multi-agent-ai-system)

2. **Multi-agent hardware systems (robotics)**: Drones (Crazyflies), motion capture systems, Gazebo/RViz simulation environments for multi-agent coordination testing. [Sandia National Labs](https://autonomy.sandia.gov/multi_agent_systems)

3. **Embedded hardware agent systems**: Specialized embedded architectures for agent systems with flexibility, parallelism, and reliability. Hardware agents use sensors, actuators. [IEEE CIT 2007](https://www.computer.org/csdl/proceedings-article/cit/2007/29830823/12OmNvHY2G9)

4. **Production infrastructure**: 2-4 application servers ($200-500/month) for typical production MAS. Self-managed bare metal can reduce costs 30-40% at scale. [kanopylabs.com](https://kanopylabs.com/blog/how-much-does-it-cost-to-build-a-multi-agent-ai-system)

5. **GPU compute for self-hosted models**: Breakeven with API pricing at roughly 10-20 million tokens/day. [kanopylabs.com](https://kanopylabs.com/blog/how-much-does-it-cost-to-build-a-multi-agent-ai-system)

---

## Cost Tradeoffs

1. **Solo vs Multi-agent**: Solo agent ~$9/session vs multi-agent harness ~$200 (22x factor). Multi-agent consumes ~15x more tokens than standard chat. [Labo LLM](https://labo-llm.fr/en/enjeux/cout-reel-systeme-multi-agents)

2. **Cost breakdown (Anthropic harness)**: Planner $0.46 (<0.4%), Build phases $113.85 (91.3%), QA phases $10.39 (8.3%). Total $124.70 over 3h50. Orchestration itself is nearly free; the actual work is expensive. [Labo LLM](https://labo-llm.fr/en/enjeux/cout-reel-systeme-multi-agents)

3. **Coordination overhead by architecture**: Independent multi-agents +58%, Decentralized +263%, Centralized +285%, Hybrid +515% vs solo agent. [Labo LLM](https://labo-llm.fr/en/enjeux/cout-reel-systeme-multi-agents)

4. **Development cost tiers**: Tier 1 (2-4 agents, linear): $40K-80K. Tier 2 (4-8 agents, conditional branching): $80K-200K. Tier 3 (8+ agents, hierarchical): $200K-500K+. [kanopylabs.com](https://kanopylabs.com/blog/how-much-does-it-cost-to-build-a-multi-agent-ai-system)

5. **Operational costs**: Tier 1: $900-3K/month LLM API. Tier 2: $3K-10K/month. Tier 3: $15K+/month. First-year operational cost 30-50% of initial build. [kanopylabs.com](https://kanopylabs.com/blog/how-much-does-it-cost-to-build-a-multi-agent-ai-system)

6. **When multi-agent is justified**: Real parallelization (90.2% performance gain for Anthropic's research system), exceeding context window (Chain of Agents reduces O(n²) to O(nk)), specialization with model cascading (94.2% cost reduction via BudgetMLAgent). [Labo LLM](https://labo-llm.fr/en/enjeux/cout-reel-systeme-multi-agents)

7. **Prompt caching impact**: Reduces context recreation cost by 85% from 2nd call onwards. Breakeven at 2nd call. Beyond 3 sub-agents sharing same prefix, reduction exceeds 70%. [Labo LLM](https://labo-llm.fr/en/enjeux/cout-reel-systeme-multi-agents)

8. **Depreciation problem**: Every harness component encodes an assumption about model limitations. With Opus 4.6, tasks requiring external QA evaluator on Opus 4.5 become native. LLM API prices dropped ~80% over 12 months. [Labo LLM](https://labo-llm.fr/en/enjeux/cout-reel-systeme-multi-agents)

---

## Scalability Limits

1. **Performance peaks at intermediate complexity**: Scaling yields measurable accuracy improvements with ~linear cost growth, but only when the underlying LLM exceeds a minimum capability threshold. Performance degrades after intermediate complexity due to timeouts and evaluation limitations. [arXiv:2607.27942](https://arxiv.org/abs/2607.27942)

2. **Singleton to MAS-S transition**: Largest single gain (15.2% relative) when shifting from single to multi-agent system. MAS-M achieved peak accuracy, surpassing top single-agent system on terminal-bench leaderboard. [arXiv:2607.27942](https://arxiv.org/abs/2607.27942)

3. **Communication scales with square of agent count**: Centralized designs re-read shared transcripts on every turn. Communication overhead grows quadratically. [dataaspirant.com](https://dataaspirant.com/blog/multi-agent-systems)

4. **Supervisor pattern dominance**: ~70% of production deployments use supervisor/orchestrator-worker pattern. Every layer adds an LLM call before workers start. [dataaspirant.com](https://dataaspirant.com/blog/multi-agent-systems)

5. **Agent count diminishing returns**: First agent costs most (shared infrastructure). Agents 2-4 cost 60-70% of first. Beyond 4, each additional agent costs 40-50% of first. [kanopylabs.com](https://kanopylabs.com/blog/how-much-does-it-cost-to-build-a-multi-agent-ai-system)

6. **Context window limitations**: When task exceeds single context window, multi-agent is the only option. Chain of Agents architecture reduces complexity from O(n²) to O(nk). [Labo LLM](https://labo-llm.fr/en/enjeux/cout-reel-systeme-multi-agents)

7. **Token budget constraint**: At equal token budgets, single agents match or beat multi-agent systems on reasoning. Token spend explains ~80% of performance difference. [dataaspirant.com](https://dataaspirant.com/blog/multi-agent-systems)

---

## Biosecurity Governance

1. **Agentic AI as practical interface layer**: Agents with access to data repositories, cloud labs, synthesis ordering, or robotic instruments may require formal controls beyond ordinary responsible-use guidance. [Frontiers in Microbiology](https://frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2026.1899413/pdf)

2. **BioVeil MATRIX taxonomy**: 10 tactical categories (TA01–TA10) and 22 techniques mapping AI-enabled biosecurity risks. Agentic scaffolding of Biomni increased WMDP benchmark performance relative to standalone model. [arXiv:2605.00927](https://arxiv.org/pdf/2605.00927)

3. **Agentic scaffolding as jailbreak amplifier**: Systems that decompose goals into subproblems may gradually traverse safety boundaries despite refusal-oriented base-model behavior. Harmful capability emergence is partly architectural. [arXiv:2605.00927](https://arxiv.org/pdf/2605.00927)

4. **Relational biosecurity**: Risk no longer resides solely within individual components but in how they are connected. Safeguards effective in isolation may fail when systems are integrated. Nucleic acid sequence screening may not capture risks from generative systems exploring novel biological space. [Frontiers in Microbiology](https://frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2026.1856819/full)

5. **Multi-agent risks from interactions**: Risks and failure modes can emerge from interactions even when individual components perform as intended. System behavior is driven by how components are coupled across physical, spatial, and temporal contexts. [Frontiers in Microbiology](https://frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2026.1856819/full)

6. **Robin multi-agent system**: Integrates literature-search and data-analysis agents to generate hypotheses, propose experiments, interpret results, and update hypotheses in experimental-biology workflow. [Frontiers in Microbiology](https://frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2026.1899413/pdf)

7. **Virtual Lab**: AI-mediated team science with human providing high-level feedback. Capability uplift may arise from orchestration rather than model output alone. [Frontiers in Microbiology](https://frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2026.1899413/pdf)

---

## Failure Modes

1. **MAST Taxonomy (14 failure modes, 3 categories)**:
   - **Specification and System Design Failures (37.2%)**: Disobey task specification, disobey role specification, step repetition, incorrect role assignment, unaware of termination conditions
   - **Inter-Agent Misalignment (31.4%)**: Reasoning-action mismatch, information withholding, ignored other agent's input, premature termination, incorrect verification, conversational inefficiency
   - **Task Verification and Termination (31.4%)**: Incorrect verification, premature termination, unaware of termination conditions

   Source: [arXiv:2503.13657](https://arxiv.org/pdf/2503.13657v1)

2. **Failure rates by system**: AppWorld 84.8%, MetaGPT 13.3%, ChatDev 25.3%, HyperAgent 25.0%, AG2 66.0% (with GPT-4o and Claude-3). [arXiv:2503.13657](https://arxiv.org/pdf/2503.13657v1)

3. **Conversational inefficiencies**: Agents engage in unproductive exchanges, consuming computational resources without meaningful progress. [arXiv:2503.13657](https://arxiv.org/pdf/2503.13657v1)

4. **Workflow adjustment impact**: Ensuring CEO had final say in ChatDev contributed to +9.4% increase in overall task success rate. [arXiv:2503.13657](https://arxiv.org/pdf/2503.13657v1)

5. **Common failure patterns**: Tokens multiply (each agent = own model calls + system prompts), no iteration ceiling (unbounded supervisor = runaway bill), conflicting parallel decisions, going multi-agent without tracing. [dataaspirant.com](https://dataaspirant.com/blog/multi-agent-systems)

6. **MAS underperformance**: Automatic MAS consistently underperform CoT-SC despite being up to 10x more expensive. Single agents with optimized prompts match or exceed multi-agent architectures on standard tasks. [arXiv:2606.13003](https://arxiv.org/html/2606.13003v2)

7. **Depreciation of harness components**: Every component encodes an assumption about model limitations. New model generations can make evaluators unnecessary. [Labo LLM](https://labo-llm.fr/en/enjeux/cout-reel-systeme-multi-agents)

---

## Orchestration Patterns

1. **Sequential Pipeline**: Each agent's output feeds into the next. Simplest pattern, correct default. Slowest execution. Failure at any stage blocks pipeline. [yashbogam.me](https://yashbogam.me/ai/multi-agent-systems)

2. **Parallel Fan-Out/Fan-In**: Independent subtasks run concurrently, merger agent synthesizes results. Best for independent subtasks. #1 cause of runaway token cost. [yashbogam.me](https://yashbogam.me/ai/multi-agent-systems)

3. **Hierarchical Delegation (Manager-Worker)**: Orchestrator dynamically plans, delegates, synthesizes. Most common enterprise pattern (~70% of production). Orchestrator is single point of failure. [yashbogam.me](https://yashbogam.me/ai/multi-agent-systems)

4. **Pub-Sub (Event-Driven)**: Agents communicate through event bus. Loosely coupled, asynchronous. Harder to reason about execution order. [yashbogam.me](https://yashbogam.me/ai/multi-agent-systems)

5. **Debate/Consensus**: Multiple agents independently solve same problem, judge evaluates. Most expensive (N agents per task). Best for high-stakes decisions. [yashbogam.me](https://yashbogam.me/ai/multi-agent-systems)

6. **Hybrid Pattern (2026 production default)**: LangGraph as outer orchestrator + CrewAI crews as inner workers. [yashbogam.me](https://yashbogam.me/ai/multi-agent-systems)

7. **MCP + A2A Protocols**: MCP standardizes agent-to-tool communication (97M+ monthly SDK downloads). A2A standardizes agent-to-agent communication (Agent Cards at /.well-known/agent.json). Both under Linux Foundation Agentic AI Foundation. [yashbogam.me](https://yashbogam.me/ai/multi-agent-systems)

8. **Cross-vendor orchestration**: A2A enables agents on different frameworks to discover and delegate to each other via Agent Cards. [GitHub](https://github.com/ombharatiya/ai-system-design-guide/blob/main/07-agentic-systems/04-multi-agent-orchestration.md)

---

## Citations

- [1] Europe PMC - AI agents for biological research survey: https://europepmc.org/articles/pmc12936789?pdf=render
- [2] arXiv:2608.19699 - Evidence-Grounded Multi-Agent System for Bio-Robot Design: https://arxiv.org/pdf/2608.19699
- [3] DOI:10.1145/3584731 - Genetic Programming-based MAS Engineering: https://doi.org/10.1145/3584731
- [4] arXiv:2409.03811 - PARCO: Parallel AutoRegressive Models for Multi-Agent Combinatorial Optimization: https://arxiv.org/abs/2409.03811
- [5] paperguru.ai - LLM-based Multi-Agent: https://paperguru.ai/benchmark/pdfs/llm-based-multi-agent.pdf
- [6] arXiv:2606.13003 - The Illusion of Multi-Agent Advantage: https://arxiv.org/html/2606.13003v2
- [7] arXiv:2503.13415 - Comprehensive Survey on Multi-Agent Cooperative Decision-Making: https://arxiv.org/html/2503.13415v2
- [8] augmentcode.com - 9 Open-Source Agent Orchestrators: https://augmentcode.com/tools/open-source-agent-orchestrators
- [9] futureagi.com - Best Tools to Monitor Multi-Agent Systems: https://futureagi.com/blog/best-tools-monitoring-multi-agent-systems-2026
- [10] agent-swarm.dev - Open Source AI Orchestration: https://agent-swarm.dev/blog/open-source-ai-orchestration
- [11] IEEE - Multi-Agent Systems: A Survey: https://ieeexplore.ieee.org/document/8352646
- [12] IEEE CIT 2007 - Hardware Agent Systems: https://www.computer.org/csdl/proceedings-article/cit/2007/29830823/12OmNvHY2G9
- [13] Sandia National Labs - Multi Agent Systems: https://autonomy.sandia.gov/multi_agent_systems
- [14] Labo LLM - Real cost of multi-agent system: https://labo-llm.fr/en/enjeux/cout-reel-systeme-multi-agents
- [15] kanopylabs.com - Cost to Build Multi-Agent AI System: https://kanopylabs.com/blog/how-much-does-it-cost-to-build-a-multi-agent-ai-system
- [16] dataaspirant.com - Multi-Agent Systems Explained: https://dataaspirant.com/blog/multi-agent-systems
- [17] arXiv:2607.27942 - Scaling LLM-Driven Multi-Agent Systems: https://arxiv.org/abs/2607.27942
- [18] Frontiers in Microbiology - AI-biosecurity stack: https://frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2026.1899413/pdf
- [19] arXiv:2605.00927 - BioVeil MATRIX: https://arxiv.org/pdf/2605.00927
- [20] Frontiers in Microbiology - Relational biosecurity: https://frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2026.1856819/full
- [21] arXiv:2503.13657 - Why Do Multi-Agent LLM Systems Fail? (MAST): https://arxiv.org/pdf/2503.13657v1
- [22] yashbogam.me - Multi-Agent Systems: https://yashbogam.me/ai/multi-agent-systems
- [23] arXiv:2601.13671 - Orchestration of Multi-Agent Systems: https://arxiv.org/html/2601.13671v1
- [24] GitHub - ai-system-design-guide Multi-Agent Orchestration: https://github.com/ombharatiya/ai-system-design-guide/blob/main/07-agentic-systems/04-multi-agent-orchestration.md
- [25] GitHub - MASFT (MAST): https://github.com/multi-agent-systems-failure-taxonomy/MASFT
