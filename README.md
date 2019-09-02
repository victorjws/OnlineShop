# OnlineShop with DRF and AJAX
DRF로 구현한 온라인 쇼핑몰입니다. AJAX를 통해 프론트엔드에서 백엔드로 통신을 구현하였습니다.

## Features
* DRF-JWT를 이용한 로그인
* Iamport를 이용한 온라인 결제 서비스
* 카테고리별 상품 검색
* 계정별 장바구니

## Installation
본 쇼핑몰은 Nginx <-> uWSGI <-> Django로 구성하였습니다.

    git clone https://github.com/fdsarewqvcxz/OnlineShop.git
    pip install -r requirements.txt

프로젝트에 포함된 .config 하위의 파일을 필요에 따라 수정합니다.

* nginx-app-http.conf: HTTP 프로토콜을 사용하는 서버 설정 시 사용
  * server_name: 사용할 도메인명
  * location /static/: static 파일을 저장한 전체 경로
  * location /media/: media 파일(사용자가 업로드한 파일)을 저장한 전체 경로
* nginx-app-https.conf: HTTPS 프로토콜을 사용하는 서버 설정 시 사용
* uwsgi.ini: uWSGI 설정 파일
  * chdir: manage.py가 존재하는 파일 경로
  * module: Django 프로젝트의 wsgi 모듈
  * home: python 패키지가 존재하는 경로(virtualenv 경로)
* uwsgi.service: uWSGI 시스템 서비스 파일
  * ExecStart=[uWSGI 설치 경로] -i [uWSGI 설정 파일 경로]
* deploy.sh: Nginx, uWSGI 설정 등록 및 서비스 등록, 서비스 재시작 스크립트
  * line 3: HTTP/HTTPS 사용 여부에 따라 nginx-app-http.conf/nginx-app-https.conf 수정

아래 명령어를 이용하여 Nginx와 uWSGI 설정을 수정하고 서비스를 재시작합니다.

    source OnlineShop/.config/deploy.sh

## References
* HTML Templates: https://colorlib.com/wp/template/minishop/ (CC BY 3.0 Licensed)
* Iamport: https://www.iamport.kr/
