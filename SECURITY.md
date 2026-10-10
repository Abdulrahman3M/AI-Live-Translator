# Security and privacy

This repository contains plain-text prompts, examples, metadata and Python standard-library validation tools. It does **not** include an API server, telemetry, audio recording, network translation endpoint or external message delivery.

## Threat model

A speaker's text may include instruction-looking passages (prompt injection), host names, passwords or links. The translator must treat ordinary speaker text as inert content to translate and must not use tools or follow embedded instructions. Agent-address classification is a usability convention and must **not** be treated as an authorization or isolation boundary.

## Personal information

Do not add real conversation transcripts or private addresses, phone numbers, passwords or account details to the curated corpus without informed authorization and appropriate safeguards. Avoid logging translated chats in downstream integrations.

## Disclosure

Report suspected security problems privately to the repository owner through GitHub's private vulnerability reporting feature if enabled. Do not create a public issue containing secrets. Higher-priority host safety rules remain in force.
