# Grafana via NGINX Design

## Goal

Expose Grafana to the internet by IP address under `http://<server-ip>/grafana/` without introducing a domain name.

## Chosen Approach

Add a dedicated `nginx` container on port `80` and proxy `/grafana/` traffic to the internal `grafana:3000` service over the existing Docker network.

## Why This Approach

- Keeps Grafana off a directly published host port.
- Supports a stable subpath deployment under `/grafana/`.
- Leaves room to add more reverse-proxied routes later without changing the public entry point.

## Configuration Changes

### Docker Compose

- Add an `nginx` service based on `nginx:alpine`.
- Publish host port `80` to container port `80`.
- Mount a custom `nginx.conf`.
- Make `nginx` depend on `grafana`.
- Remove the direct `3000:3000` port mapping from Grafana.

### Grafana

Set:

- `GF_SERVER_ROOT_URL=%(protocol)s://%(domain)s/grafana/`
- `GF_SERVER_SERVE_FROM_SUB_PATH=true`

This ensures redirects, static assets, and API calls work correctly from the `/grafana/` subpath.

### NGINX

- Redirect `/grafana` to `/grafana/`.
- Proxy all `/grafana/` requests to `grafana:3000`.
- Forward the standard proxy headers and websocket upgrade headers.
- Return `404` for unrelated root-level paths.

## Verification

- `docker compose config` validates the compose file.
- `http://<server-ip>/grafana/` should load the Grafana login screen.
- `http://<server-ip>/` should return `404`.

## Notes

- This change does not add HTTPS.
- Prometheus and Loki remain directly published as before.
