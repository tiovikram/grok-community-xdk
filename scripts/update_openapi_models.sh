#!/usr/bin/env bash
set -euo pipefail

repository_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
spec_file="$(mktemp)"
trap 'rm -f "$spec_file"' EXIT

curl --fail --silent --show-error \
  https://api.x.ai/api-docs/openapi.json \
  --output "$spec_file"

"$repository_dir/venv/bin/datamodel-codegen" \
  --input "$spec_file" \
  --input-file-type openapi \
  --output "$repository_dir/src/xai_grok/schemas/openapi.py" \
  --output-model-type pydantic_v2.BaseModel \
  --use-standard-collections \
  --use-union-operator \
  --target-python-version 3.11 \
  --snake-case-field \
  --use-schema-description \
  --use-field-description \
  --enum-field-as-literal all \
  --disable-timestamp \
  --use-double-quotes
