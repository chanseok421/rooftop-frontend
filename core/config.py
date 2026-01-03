from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

def _get_from_secrets(k: str) -> str | None:
    try:
        import streamlit as st
        # st.secrets 접근 시점에 예외가 날 수 있으니 여기서 잡는다
        return st.secrets.get(k)  # type: ignore[attr-defined]
    except Exception:
        return None

def _get(k: str) -> str | None:
    return os.getenv(k) or _get_from_secrets(k) or None


@dataclass(frozen=True)
class Settings:
    env: str = _get("OKSSANGIMONG_ENV") or "dev"
    data_dir: Path = Path(_get("OKSSANGIMONG_DATA_DIR") or "./data").resolve()

    kakao_rest_api_key: str | None = _get("KAKAO_REST_API_KEY")
    vworld_api_key: str | None = _get("VWORLD_API_KEY")
    vworld_domain: str | None = _get("VWORLD_DOMAIN")

    engine_version: str = "0.1.0"
    coefficient_set_version: str = "v1"


settings = Settings()
