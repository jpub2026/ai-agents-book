from langdetect import detect, DetectorFactory
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import json

DetectorFactory.seed = 42

class LanguageConfig(BaseModel):
    """언어별 설정을 관리하는 모델입니다."""
    ko_style: str = Field(
        default="• 불릿 3개 이내 요약, 공손체 유지, 문장 끝 일관성",
        description="한국어 스타일 가이드"
    )
    en_style: str = Field(
        default="Concise, active voice, max 3 bullets, clear takeaway",
        description="영어 스타일 가이드"
    )
    ja_style: str = Field(
        default="です/ます調、簡潔に、箇条書き3点以内",
        description="일본어 스타일 가이드"
    )
    max_response_length: int = Field(default=500, ge=100, le=2000)
