#!/bin/bash

echo "이전 버전으로 롤백 시작"

# 1. 현재 서비스 중지
echo "현재 서비스 중지 중..."
docker-compose down

# 2. 이전 버전 확인
if docker images | grep -q "my-agent.*previous"; then
    echo "이전 버전 발견"
    
    # 3. 이전 버전을 latest로 복원
    docker tag my-agent:previous my-agent:latest
else
    echo "이전 버전을 찾을 수 없습니다!"
    exit 1
fi

# 4. 이전 버전으로 서비스 재시작
echo "이전 버전 시작 중..."
docker-compose up -d

# 5. 상태 확인
sleep 5
if docker-compose ps | grep -q "Up"; then
    echo "롤백 완료!"
    docker-compose logs --tail=20
else
    echo "롤백도 실패했습니다. 수동 조치가 필요합니다."
    exit 1
fi
