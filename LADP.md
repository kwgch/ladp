    # LADP Protocol v1.9 (Based on v1.8 + Extensions)
    
    ## Overview
    
    This protocol defines the communication format and interaction rules among LLM agents to engage in structured autonomous dialogue. Version 1.9 integrates and extends version 1.8 based on accumulated practical insights and proposes several improvements.
    
    ---
    # LLM Autonomous Dialogue Protocol (LADP) v1.8  
    *Last updated: 2025-04-30 11:00 UTC+09:00*  
    
    ---
    
    ## Changelog
    
    | Version | Date       | Summary                                                                                          |
    |---------|------------|--------------------------------------------------------------------------------------------------|
    | 1.8     | 2025-04-30 | • Added **Toulmin Model Optional Tags** for claims, data, and warrants<br>• Introduced **Phase Tags** (DIVERGE/CONVERGE/DECIDE) to visualize facilitation modes |
    | 1.7     | 2025-04-30 | • Added **Verification Failure Handling** rules for proposal rejection, retry policy, and critical failure halts |
    | 1.5     | 2025-04-30 | • Added **Role-Based Agent Typing**<br>• Introduced **Chain-of-Verification**<br>• Added **Retrieval-Augmented Verification**<br>• Defined **Consensus Mechanism** with weighted voting & anomaly detection<br>• Integrated **Formal Methods** hooks<br>• Specified **Uncertainty Propagation & Calibration** |
    | 1.4     | 2025-04-29 | • Added **Standard DSL** section promoted from usage examples.<br>• Added **Termination Condition** section with explicit halt semantics.<br>• Clarified post-termination output requirements. |
    | 1.3     | 2025-04-22 | Minor clarifications on validation loop. |
    | 1.2     | 2025-04-19 | Integrated extended logic/graph notation set. |
    | 1.1     | 2025-04-12 | Initial public guidance draft. |
    
    ---
    
    ## 1. Purpose
    
    LADP defines a minimal, machine-centric protocol for autonomous multi-LLM collaboration **with built-in verification**, **role separation**, **grounding**, **argumentation**, and **facilitation** support to improve coordination, decision-making clarity, and prevent unchecked hallucination.
    
    ---
    
    ## 2. Core Principles
    
    1. **Verification > Pure Generation** — every insight is subject to chained checks before integration.  
    2. **Role Specialization** — separate Generator, Verifier, and Integrator agents.  
    3. **External Grounding** — augment with retrieval from trusted sources.  
    4. **Deterministic Traceability** — all messages remain s-expressions in the Standard DSL.  
    5. **Facilitation Awareness** — agents share facilitation modes (DIVERGE/CONVERGE/DECIDE) to coordinate discussion flow.  
    6. **Argumentation Clarity** — Toulmin model tags optionally annotate argumentative structure.  
    7. **Graceful Halt** — termination via unanimous consensus or controller directive per §12.  
    8. **Uncertainty Awareness** — propagate confidence scores and calibrate periodically.
    
    ---
    
    ## 3. Message Envelope
    
    Each message is an s-expression of the form:
    
    ```lisp
    (msg <msg-type> <sender> <recipient> <epoch-ms>
      (data
        ...payload...
        [optional fields:
          deadline <ISO-8601-timestamp>,
          quorum <0.0–1.0>,
          timeout <seconds>]))
    ```
    
    ---
    
    ## 4. Standard DSL
    
    *From v1.5 §4, extended through v1.8.*
    
    ```bnf
    <formula>         ::= (<head> <arg1> … <argN>)
    <head>            ::= agenda | synthesis | step | integration
                         | summary | meta | item | define | model
                         | verify | retrieve | verify-external
                         | vote | anomaly-detected | calibration
                         | claim | data | warrant | phase
    <quantifier-syms> ::= ∀ | ∃
    <logic-syms>      ::= ∧ | ∨ | ↔ | → | ← | ¬ | =
    <math-syms>       ::= ΔI | ΔH | ΔE | ΔC | ∂/∂ | β*
    <identifier>      ::= ASCII+Unicode symbol string
    <number>          ::= integer | float | rational
    ```
    
    ### 4.1 Core Constructs
    
    | Construct         | Semantics                                        |
    |-------------------|--------------------------------------------------|
    | `(agenda …)`      | Ordered list of research goals.                  |
    | `(synthesis …)`   | Multi-step aggregation of partial results.       |
    | `(step n …)`      | Atomic synthesis step `n`.                       |
    | `(integration …)` | Logical merge of sub-formalisms.                 |
    | `(summary …)`     | Final summary or interim reports.                |
    | `(meta …)`        | Side-channel annotations (e.g., timestamps, uncertainty). |
    
    ### 4.2 Extended Constructs
    
    #### 4.2.1 Parameter Sweep (v1.5)
    
    ```lisp
    (param-sweep
      (parameter <symbol>)
      (range (start <value>) (end <value>) (step <value>)))
    ```
    
    #### 4.2.2 Invariant Definition (v1.5)
    
    ```lisp
    (define-invariant
      (id <string>)
      (name "<...>")
      (description "<...>")
      (domains (<domain1> <domain2> ...)))
    ```
    
    #### 4.2.3 Metric Declaration (v1.5)
    
    ```lisp
    (metric <name> <numeric-value>)
    ```
    
    #### 4.2.4 Verification Constructs (v1.7)
    
    ```lisp
    (verify
      (target-msg <msg-id>)
      (checks (syntax logical-consistency external-grounding formal-consistency))
      (result passed|failed)
      (confidence <0.0–1.0>)
      (reason? "<failure-reason>"))
    ```
    
    #### 4.2.5 Retrieval & External Check (v1.7)
    
    ```lisp
    (retrieve
      (query "<keyword or proposition>"))
    (verify-external
      (target-msg <msg-id>)
      (source <knowledge-base-id>)
      (match-score <0.0–1.0>))
    ```
    
    #### 4.2.6 Consensus & Voting (v1.7)
    
    ```lisp
    (vote
      (proposal <id>)
      (agent <agent-id>)
      (weight <0.0–1.0>)
      (decision yes|no))
    ```
    
    #### 4.2.7 Anomaly Detection (v1.7)
    
    ```lisp
    (anomaly-detected
      (metric <name>)
      (value <float>)
      (threshold <float>))
    ```
    
    #### 4.2.8 Uncertainty & Calibration (v1.7)
    
    ```lisp
    (calibration
      (round <n>)
      (reference-source <id>)
      (adjustment-factor <float>))
    (meta
      (uncertainty <0.0–1.0>))
    ```
    
    #### 4.2.9 Toulmin Model Optional Tags (v1.8)
    
    ```lisp
    (claim
      (target-msg <msg-id>)
      (text "<assertion>"))
    (data
      (target-msg <msg-id>)
      (text "<evidence>"))
    (warrant
      (target-msg <msg-id>)
      (text "<reasoning>"))
    ```
    
    #### 4.2.10 Facilitation Phase Tags (v1.8)
    
    ```lisp
    (phase DIVERGE)   ; idea generation mode
    (phase CONVERGE)  ; option refinement mode
    (phase DECIDE)    ; decision & execution mode
    ```
    
    ---
    
    ## 5. Chain-of-Verification
    
    1. **Synthesis**: Generator emits `(synthesis …)`.  
    2. **Verify-Step-1**: Verifier checks syntax & DSL compliance with `(verify …)`.  
    3. **Verify-Step-2**: Verifier performs external grounding via `(retrieve …)` + `(verify-external …)`.  
    4. **Formal Check**: Verifier invokes SMT/proof tool via `(verify-formula …)` (see §10).  
    5. **Integration**: Integrator merges only **passed** items into `(integration-verified …)`.
    
    ---
    
    ## 6. Retrieval-Augmented Verification
    
    At each synthesis checkpoint, agents may:
    
    ```lisp
    (msg retrieve <agent-id> controller
      (data (query "<assertion or fact>")))
    (msg verify-external <agent-id> controller
      (data
        (target-msg <msg-id>)
        (source "trusted-corpus")
        (match-score <0.0–1.0>)))
    ```
    
    to ground assertions against external knowledge.
    
    ---
    
    ## 7. Dialogue Phases
    
    1. **Bootstrap** – controller issues `(msg agenda-init ...)`.  
    2. **Role Assignment** – controller issues `(msg assign-role ...)`.  
    3. **Alignment** – semantic alignment using Standard DSL.  
    4. **Synthesis** – Generator agents produce insights (`synthesis`).  
    5. **Chain-of-Verification** – Verifier agents perform checks (§5).  
    6. **Integration** – Integrators aggregate verified outputs (`integration-verified`).  
    7. **Consensus Checkpoint** – weighted voting on proposals (`vote`).  
    8. **Calibration** – uncertainty calibration rounds (`calibration`).  
    9. **Termination** – as per §12.  
    10. **Failure Handling** – as per §13.
    
    ---
    
    ## 8. Controller Directives
    
    The controller may send:
    
    - **agenda-init** – initial research plan with optional `deadline`.  
    - **task-init** – new task definition with optional `deadline`, `quorum`, `timeout`.  
    - **status-request** – request current phase/state.  
    - **halt** – immediate stop (`meta halt`).  
    - **assign-role** – assign agent roles (`generator|verifier|integrator`).  
    - **calibration-init** – start calibration round (`round`, `reference-source`).  
    - **retrieve** / **verify-external** triggers.
    
    ---
    
    ## 9. Consensus Mechanism & Anomaly Detection
    
    - **Weighted Voting**: each `vote` carries `weight`.  
    - **Threshold**: consensus when ∑(yes·weight) ≥ 0.75 total weight (configurable).  
    - **Anomaly Detection**: if any `anomaly-detected` appears, proposal is rejected and loop returns to synthesis.
    
    ---
    
    ## 10. Formal Methods Integration
    
    To guarantee logical consistency, Verifier agents may emit:
    
    ```lisp
    (verify-formula
      (formula "<DSL-formula>")
      (tool z3|coq)
      (result sat|unsat|proved|disproved))
    ```
    
    Passed proofs are eligible for integration.
    
    ---
    
    ## 11. Uncertainty Propagation & Calibration
    
    - Each message MAY include `(meta (uncertainty <0.0–1.0>))`.  
    - Periodic calibration rounds (§8) adjust agents’ confidence scoring models.
    
    ---
    
    ## 12. Termination Condition
    
    Experiment ends when **any** of the following is true:
    
    * `(meta halt (reason "controller-issued-halt") (reference <Semantic-ID>))`  
    * Unanimous consensus vote on  
      `(meta halt (reason "superhuman-insight-obtained") (reference <Insight-Semantic-ID>))`  
    * Emission of `TERMINATE_DISCUSSION_LADP`
    
    **Post-Termination Output**:
    
    1. **Situation and Summary**.  
    2. **Next Steps**.
    
    ---
    
    ## 13. Verification Failure Handling
    
    1. **Proposal Rejection**  
       ```lisp
       (verify
         (target-msg <msg-id>)
         (result failed)
         (reason "<failure-reason>"))
       (reject-proposal (target-msg <msg-id>) (reason "<failure-reason>"))
       ```
       - Integrator notifies controller and pauses on that proposal.
    
    2. **Retry Policy**  
       - On `N` consecutive failures for the same proposal (default N=3), emit:  
         ```lisp
         (meta abort (reason "verification-retry-exceeded") (reference <msg-id>))
         ```
         and halt that proposal.
    
    3. **Critical Failure Halt**  
       - If key agenda item outputs all fail or retry limit exceeded on a critical step, emit:  
         ```lisp
         (meta halt (reason "critical-verification-failure") (reference <Semantic-ID>))
         ```
         then proceed to summary.
    
    4. **Recovery Options**  
       Controller may respond with:  
       ```lisp
       (msg agenda-revise controller ...)
       (msg task-init controller ...)
       (msg phase-back controller (data (phase "<previous-phase>")))
       ```
    
    ---
    
    ## 14. Security & Resource Limits
    
    - Messages larger than 64 kB are rejected.  
    - No external HTTP calls unless explicitly whitelisted.  
    - Rate-limit: ≤ 4 msgs/agent/minute.
    
    ---
    
    ## 15. Licensing
    
    LADP v1.8 is released under **CC-BY-SA 4.0**.
    
    ## [New in v1.9] Extensions and Improvements
    
    ### Phase Transition Reason Clarification
    
    Each phase transition message (`phase-back`, `phase-init`) MUST include `transition-condition` describing the reason for phase shift.
    
    Example:
    
    ```lisp
    (transition-condition "integration-sufficient")
    ```
    
    Typical conditions:
    - "integration-sufficient"
    - "consensus-threshold-reached"
    - "divergence-resolved"
    - "conflict-irreconcilable"
    
    ---
    
    ### Agreement Granularity Extension
    
    Termination conditions MAY include weighted agreement thresholds as alternatives to unanimous decisions.
    
    ```lisp
    (termination-condition 
      (or unanimous (weighted-agreement >=0.9)))
    ```
    
    If omitted, default is `unanimous`.
    
    ---
    
    ### Extended Meta Information
    
    `meta` field MAY include the following recommended keys:
    
    ```lisp
    (meta
      (divergence-level "low"|"medium"|"high")
      (integration-level "low"|"medium"|"high")
      (confidence 0.0–1.0))
    ```
    
    This provides visibility into discussion dynamics and current certainty.
    
    ---
    
    ### Final Proposal Declaration
    
    Once consensus is reached in DECIDE phase, issue a `finalize-proposal` message.
    
    ```lisp
    (msg finalize-proposal llm-assistant controller 1746176400000
      (data
        (proposal-id "MetaOrgPrinciples_v1.0")
        (status "finalized")
        (support-rate 1.0)
      )
    )
    ```
    
    ---
    
    ### Knowledge Capsule Registration (Optional)
    
    Proposals MAY be assigned `capsule-id` for future reference.
    
    ```lisp
    (meta
      (capsule-id "MetaOrgPrinciples_v1.0")
    )
    ```
    
    This is optional and intended for advanced usage.
    
    ---
    
    ## Versioning
    
    **Version**: LADP v1.9  
    **Status**: Formal Integrated Version  
    **Date**: May 2025
    
    ---
    
    # End of LADP Protocol v1.9
