# Technical Document
## Let's Encrypt를 이용한 SSL 적용
### 도메인(domain) 발급
[freenom](https://www.freenom.com)을 통해 무료 도메인 발급

freenom의 DNS 서버에 도메인과 AWS EC2의 IP주소 연결
### Let's Encrypt 설치

    sudo apt-get install letsencrypt
    sudo apt-get install python3-certbot-nginx

nginx-app.conf의 80 포트(port) 부분에 추가

    location ^~ /.well-known/acme-challenge/ {
        allow all;
    }

nginx 재시작 후 아래 명령어를 통해 SSL 발급

    certbot --nginx -d [등록할 도메인:onlineshopdemo.tk]

nginx-app.conf의 443 포트 부분에 추가

    ssl_certificate /etc/letsencrypt/live/[등록한 도메인:onlineshopdemo.tk]/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/[등록한 도메인:onlineshopdemo.tk]/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

nginx 재시작
