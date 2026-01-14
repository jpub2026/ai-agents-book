# Docker 공식 설치 스크립트 다운로드
curl -fsSL https://get.docker.com -o get-docker.sh

# 스크립트 실행으로 Docker 설치
sudo sh get-docker.sh

# 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER
