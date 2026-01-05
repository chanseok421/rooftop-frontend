from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    env: str = os.getenv("OKSSANGIMONG_ENV", "dev")
    data_dir: Path = Path(os.getenv("OKSSANGIMONG_DATA_DIR", "./data")).resolve()

    kakao_rest_api_key: str | None = os.getenv("KAKAO_REST_API_KEY") or None
    vworld_api_key: str | None = os.getenv("VWORLD_API_KEY") or None
    vworld_domain: str | None = os.getenv("VWORLD_DOMAIN") or None

    # 버전 관리(계수/수식/데이터)
    engine_version: str = "0.1.0"
    coefficient_set_version: str = "v1"

settings = Settings()
