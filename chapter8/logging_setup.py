import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(service_name="agent-service"):
    """간단하지만 실용적인 로깅 설정"""
    
    # 로그 폴더가 없으면 만듭니다
    os.makedirs("logs", exist_ok=True)
    
    # 로거 생성
    logger = logging.getLogger(service_name)
    logger.setLevel(logging.INFO)  # INFO 레벨 이상만 기록
    
    # 콘솔 출력 설정
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 파일 출력 설정 (10MB마다 새 파일로) 
    file_handler = RotatingFileHandler(
        filename=f"logs/{service_name}.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,  # 최대 5개 파일 보관 
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)  # 파일에는 더 자세히 기록
    
    # 로그 포맷 설정 (시간, 레벨, 메시지)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # 핸들러 추가
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


