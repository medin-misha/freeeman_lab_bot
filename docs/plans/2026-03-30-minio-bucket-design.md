## Goal

Ensure the MinIO bucket `freeman-bucket` is created automatically when the local stack starts.

## Chosen Approach

Use a one-shot Docker Compose service based on `minio/mc`.

## Why

- Keeps bucket bootstrap in infrastructure rather than backend application code.
- Works for fresh environments without requiring a manual `mc mb` step.
- `mc mb --ignore-existing` makes repeated starts safe.

## Design

- Add a `freeman-minio-init` service to `docker-compose.yml`.
- Run it on the same `freeeman-network` as MinIO.
- Wait until `freeman-minio` accepts S3 API requests.
- Configure an `mc` alias pointed at `http://freeman-minio:9000`.
- Create `freeman-bucket` with `mc mb --ignore-existing`.
- Keep the service one-shot with `restart: "no"`.

## Risks

- If MinIO credentials diverge from the values used by the init service, bucket creation will fail.
- Backend still depends on the bucket name staying aligned with `backend/.env`.

## Validation

- `docker compose up -d freeman-minio freeman-minio-init`
- `docker compose logs freeman-minio-init`
- Optional: inspect the bucket in the MinIO console on port `9001`
