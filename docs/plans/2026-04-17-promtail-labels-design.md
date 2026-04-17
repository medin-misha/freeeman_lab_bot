# Promtail Label Fix Design

## Goal

Stop `promtail` from sending unlabeled log streams to Loki and remove noise from containers outside this Docker Compose project.

## Chosen Approach

Restrict `promtail` discovery to containers from the `freeeman_lab_bot` compose project and add a guaranteed static label.

## Changes

- Keep only containers with `com.docker.compose.project=freeeman_lab_bot`.
- Add `job=docker` as a guaranteed label for every discovered stream.
- Relax the container name regex from `/(.*)` to `/?(.*)` so the `container` label is preserved consistently.
- Keep dropping monitoring services themselves to avoid ingest noise.

## Expected Result

- Loki no longer rejects batches with `error at least one label pair is required per stream`.
- Promtail stops collecting unrelated Docker containers.
- Existing Grafana queries by `service=...` continue to work for application services in this project.
