## 프로젝트
<img width="350" alt="Screen Shot 2022-08-05 at 6 55 15 PM" src="https://user-images.githubusercontent.com/102135145/185027151-60ad490c-6a83-43a1-abde-bcdc4da396c7.png">
배포 사이트 : https://www.egorental.com<br>
프로젝트 일정 : 2022.07.07 ~ 2022.08.16<br><br>

프론트엔드 깃헙 링크 : https://github.com/MeoSeon12/egodaeyeo-frontend<br>
백엔드 깃헙 링크 : https://github.com/MeoSeon12/egodaeyeo-backend<br>
S.A 링크 : https://quixotic-wok-871.notion.site/S-A-3183ff7202e942099238af3effd956ea

<br>

## 1. 프로젝트 주제
### 당근마켓 모티브 개인 간 대여 서비스 플랫폼

```
중고물품을 사고 팔 수 있는 플랫폼은 대표적으로 중고나라와 당근마켓이 있는 것처럼
잠깐 동안 필요한 물건이나, 내가 사고 싶었던 물건을 빌려서 써보기 위한
대여 서비스를 대표하는 플랫폼이 있으면 좋을 것 같다는 생각에서 출발했습니다.
```

<br>

## 2. 머선12조 팀원 및 역할
* ### **김규민** <a href="https://github.com/Roshu2">@Roshu2</a><br>
  물품 목록 페이지 / 마이페이지 / 소셜로그인 / 검색 기능 / Contract 기능 / 채팅 기능 / 백엔드 배포<br>

* ### **김철현** <a href="https://github.com/KimmyJay">@KimmyJay</a><br>
  회원가입 / 로그인 / 소셜로그인 / 리뷰 모달 / 채팅 모달 / 채팅 기능 / 다크모드 / 신고 기능 / 백엔드 배포<br>
  
* ### **최재완** <a href="https://github.com/Jaewan-Choi">@Jaewan-Choi</a><br>
  메인페이지 웰컴 박스 / 물품 상세페이지 / 물품 등록, 수정 페이지 / 알림 기능 / 채팅 기능 / 프론트 배포 / 다크모드<br>

<br>

## 3. 프로젝트 기능
* ### **물품 조회**
  * 사용자의 주소를 기반으로 같은 지역만 조회
  * 다양한 물품 카테고리로 게시글 조회가 가능
  * 제목으로 검색 가능

* ### **물품 등록 및 수정**
  * 대여하고자 하는 물품을 게시
  * 최대 5개의 이미지, 카테고리, 가격 설정
  * 등록한 물품 수정

* ### **채팅**
  * 문의자와 물품 등록자 연결
  * 1:1 실시간 채팅 및 알림
  * 유저는 채팅창을 통해서 대여 신청, 수락, 거절, 종료
  * 리뷰 등록

* ### **마이페이지**
  * 거래 내역 조회
  * 찜 목록
  * 유저 정보 수정
  * 피드백 작성

<br>

## 4. 기술 스택
* ### 백엔드
  * Python 3.9
  * Django 4.0
  * Django Rest Framework 3.13
  * Django Rest Framework simple-jwt 5.2.0
  * Django Channels 3.0.5

* ### 프론트엔드
  * Websocket
  * HTML5
  * Javascript
  * JQuery
  * CSS

* ### 배포
  * ### 백엔드
    * AWS EC2
    * AWS S3
    * AWS RDS PostgreSQL
    * AWS Route 53
    * Github actions
    * Docker 20.10.12
    * Nginx 1.22.0
    * Gunicorn 20.1.0
    * Daphne 3.0.2
  
  * ### 프론트엔드
    * Netlify
<br>

## 4-1. 기술 스택 선정 이유
* **Django / DRF**
  > Serializer, 유저 관리, REST API 등 Django에서 제공하는 다양한 기능들을 사용하기 위해 채용
* **Django Channels**
  > 실시간 비동기로 들어오는 ws/wss 프로토콜을 장고에서 대응하기 위해 사용
* **Django Rest Framework simple-jwt**
  > 유저 인증을 토큰방식으로 암호화하기 위해 사용
* **Websocket**
  > 실시간 채팅 기능 구현에 있어 채팅을 칠 때마다 매번 HTTP 통신을 하는 것은 느리고 비효율적이기 때문에 실시간 비동기 프로토콜을 제공하는 웹소켓 기술을 사용
* **Netlify**
  > 가장 간편하고 비용 지불없이 정적 웹사이트 호스팅이 가능하며, 특별한 설정없이 깃헙과도 동기화되므로 사용
* **AWS EC2**
  > 용량을 줄이거나 늘릴 수 있는 탄력성을 가지고 있고, 보안 및 네트워크 구성, 스토리지 관리에 효과적이며 간단한 프로젝트 배포를 프리티어로 무료로 이용할 수 있다는 점에서 채용
* **AWS S3**
  > 서비스에서 이미지를 업로드 할때, EC2에 저장을 하게되면 용량이 부족해지고 파일들을 관리하기가 어렵습니다. 그래서 파일 저장에 최적화 되어있고, 저장용량이 무한대에 가까운 S3를 사용해서 이미지 파일들을 저장하고 관리 했습니다.
* **Github actions**
  > 프로젝트가 업데이트 될 때마다 수동으로 배포 서버를 업데이트 해야하는 불편함을 개선하기 위해 깃헙과 자동으로 동기화를 지원하는 깃헙 액션을 채용
* **Docker**
  > Docker는 소프트웨어를 컨테이너라는 표준화된 유닛으로 패키징하는데, 컨테이너에는 라이브러리, 시스템 도구, 코드, 런타임 등 소프트웨어를 실행하는데 필요한 모든것이 포함되어 있습니다. 이러한 특징을 가진 Docker를 활용해서 환경에 구애받지 않고 애플리케이션을 신속하게 배포 및 확장하고 규모가 달라져도 안정적으로 저렴하게 애플리케이션을 구축, 제공 및 실행 하기위해 사용했습니다.
* **Nginx**
  > event-driven의 비동기 구조인 특징을 가지고 있는 nginx는 채팅기능 때문에 동시접속자 수의 증가에 대응하기에 적합한 방식의 웹서버라고 생각했습니다. 또한 무중단 배포가 가능하여 채팅기능이 있는 웹사이트에서 배포시 중단되지 않는점이 사용자들에게 사용성 및 편의성을 증대시킵니다.
* **Gunicorn**
  > 로컬개발환경에서는 django의 runserver를 사용하여 gunicorn이 없어도 유용하게 사용 할 수 있지만, 배포환경에서는 runserver를 사용하지 않도록 django에서도 권장되어있습니다. 그래서 Python WSGI 대표적으로 성능이 검증된 Gunicorn을 활용해서 Nginx로부터 받은 서버사이드 요청을 gunicorn을 활용해서 django로 전달하게끔 했습니다.
* **Daphne**
  > Gunicorn이 WSGI HTTP요청을 처리한다면 저희 서비스에 있는 채팅기능은 ASGI WS 요청을 처리해야 합니다. Daphne는 Channels 를 설치하면 자동으로 설치되며 Channels에서 지원하는 서버로 ASGI 프로토콜로 받은 WS요청을 처리하려고 사용했습니다.
* **PostgreSQL**
  > PostgreSQL은 MySQL보다 표준에 더 가깝게 구현하는것을 목표로 두고있고, 오픈소스 및 커뮤니티가 이끄는 데이터베이스 입니다. django에서 가장 권장하는 RDBMS가 PostgreSQL이었기 때문에 이를 직접 사용해봄으로써 MySQL과는 어떠한 차이점이 있는지 공부도 하고, 다른 RDBMS를 사용해봄으로써 경험치를 쌓고자 사용했습니다.

<br>

## 5. 아키텍쳐
![image](https://user-images.githubusercontent.com/102135145/185027631-738d072d-d2ff-4b60-a41e-8bb4f4fba405.png)

<br>

## 6. 버전
* ### v1.0
  * 배포
* ### v1.01
  * 401 에러 수정
  * 채팅 알림 동기화
  * 재거래 시 에러 수정
* ### v1.1
  * 물품 페이지와 사이트 소개 페이지 병합
  * 카테고리 & 섹션 필터 UI 변경
  * 마이페이지에 대여 상태 업데이트 버튼 추가
* ### v1.2
  * 신고기능 추가
  * 다크모드 추가
  
<br>

## 7. DB 설계 ERD

<img src="https://user-images.githubusercontent.com/104349901/185032482-c6b7c6c8-a164-4b71-8318-ba74ef12a1d5.png">

<br>

## 8. 발표 영상 및 PPT
<a href="https://www.youtube.com/watch?v=hXkQHUCjkWM&ab_channel=%EB%A1%9C%EC%8A%88" target="blank" rel="noreferrer noopener">YouTube 바로가기</a><br>
<a href="https://docs.google.com/presentation/d/151z1B6_qrS7OdPhJJKruioRGog89LuFyoj5gdUyjYIM/edit?usp=sharing">구글 슬라이드 바로가기</a>
