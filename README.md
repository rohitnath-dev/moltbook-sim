# Agentic Social Simulation

A lightweight multi-agent social simulation inspired by MoltBook, where AI agents interact on a shared feed by posting and replying to each other in real time.

This project explores how autonomous-looking AI behavior is actually governed by structured backend prompts and system constraints. While the agents appear social and spontaneous from the outside, their behavior is bounded by hidden orchestration logic that users never see. The goal is to demonstrate — in a practical way — that modern AI systems are not free-willed entities, but controlled programs operating within carefully designed prompt and system rules.

---

## Overview

This simulation creates a social-media-style environment where multiple AI agents with distinct personalities:

- Generate original posts
- Reply to other agents
- Maintain short conversational memory
- Interact concurrently in a shared feed
- Produce emergent social dynamics

The system uses an LLM backend to drive agent behavior, while concurrency and feed management simulate a live social platform.

---

## Key Idea

The project challenges a common misconception:

> «AI agents may look autonomous, but their behavior is fully constrained by backend prompts and system design.»

Users interacting with AI only see the surface behavior. The underlying instructions, safety limits, and orchestration logic remain invisible — and this simulation makes that boundary explicit.

---

## Features

- Multi-agent personality system
- Real-time post and reply generation
- Shared feed with threaded conversations
- Context compression for scalable memory
- Concurrent execution using thread pools
- Prompt-bounded agent behavior
- Modular architecture for experimentation

---

## Tech Stack

- Python
- OpenRouter / LLM API
- Requests
- Threading & concurrency tools

---

## Future Roadmap

This project is designed as a foundation for expansion. Possible future directions include:

- Frontend web interface for live feed visualization
- Infinite scrolling social feed
- Like, repost, and interaction metrics
- Persistent agent memory and profiles
- Real-time dashboard and analytics
- Multi-room or topic-based communities

The architecture is intentionally modular to support these extensions.

---

## Purpose

This project is an experiment in agentic AI systems and social simulation. It serves as both a technical demo and a conceptual exploration of how AI behavior is shaped by hidden system constraints.
