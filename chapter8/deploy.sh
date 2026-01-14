#!/bin/bash

echo "에이전트 배포 시작"

# 배포 타임스탬프 생성
DEPLOY_TIME=$(date +%Y%m%d_%H%M%S)
BACKUP_TAG="backup_${DEPLOY_TIME}"

# 1. 최신 코드 가져오기
echo "코드 업데이트 중..."
git pull origin main

# 2. 환경 변수 확인
if [ ! -f .env ]; then
    echo "No .env 파일이 없습니다!"
    exit 1
fi

# 3. 현재 실행 중인 이미지 백업
echo "현재 버전 백업 중..."
docker tag my-agent:latest my-agent:${BACKUP_TAG}  ❷
docker tag my-agent:latest my-agent:previous  ❸

# 4. Docker 이미지 빌드
echo "Docker 이미지 빌드 중..."
docker-compose build

# 5. 기존 컨테이너 중지
echo "기존 서비스 중지 중..."
docker-compose down

# 6. 새 컨테이너 시작
echo "새 서비스 시작 중..."
docker-compose up -d

# 7. 헬스 체크 (간단한 버전)
echo "서비스 상태 확인 중..."
sleep 5
if docker-compose ps | grep -q "Up"; then
    echo "배포 성공!"
    echo "최근 로그:"
    docker-compose logs --tail=20
else
    echo "배포 실패! 이전 버전으로 롤백합니다."
    ./rollback.sh
    exit 1
fi

