# 개역개정 성경 웹앱 배포 가이드

본 프로그램의 `index.html`은 별도의 데이터베이스나 백엔드 서버 없이도 동작하는 **순수 정적 웹 애플리케이션(Static Web App)**입니다.
따라서 무료 호스팅 서비스(GitHub Pages, Vercel, Netlify 등) 어디에든 단 몇 분 만에 배포하여 모든 교인들에게 링크를 공유할 수 있습니다.

---

## 1. Vercel로 배포하기 (가장 추천 - 1분 완료)

1. [Vercel](https://vercel.com)에 로그인합니다 (GitHub 계정 연동 추천).
2. 'Add New...' -> 'Project'를 클릭합니다.
3. 이 폴더(`f:\프로그램\성경`)를 GitHub 저장소에 올린 후 연결하거나, Vercel CLI로 배포합니다:
   ```bash
   npx vercel
   ```
4. 배포가 완료되면 `https://your-bible-app.vercel.app` 과 같은 무료 전용 도메인이 생성되어 교인들에게 즉시 공유할 수 있습니다.

---

## 2. GitHub Pages로 배포하기 (무료 및 영구 소장)

1. GitHub에서 새로운 저장소(예: `bible-viewer`)를 생성합니다.
2. 현재 폴더의 파일들을 커밋하고 푸시합니다:
   ```bash
   git init
   git add .
   git commit -m "초경량 개역개정 성경 뷰어 웹앱"
   git remote add origin https://github.com/사용자아이디/bible-viewer.git
   git branch -M main
   git push -u origin main
   ```
3. GitHub 저장소의 **Settings** -> **Pages** 메뉴로 이동합니다.
4. 'Branch'를 `main` 브랜치, 폴더를 `/(root)`로 지정하고 **Save**를 누릅니다.
5. 1~2분 뒤 `https://사용자아이디.github.io/bible-viewer/` 주소로 전 세계 어디서나 접속 가능합니다!

---

## 3. Netlify로 배포하기 (드래그 앤 드롭)

1. [Netlify](https://www.netlify.com)에 로그인합니다.
2. Netlify 대시보드의 'Sites' 탭에서 **'Drag & drop your site output folder here'** 영역을 찾습니다.
3. 이 폴더(`f:\프로그램\성경`) 자체를 웹 브라우저 창으로 드래그하여 떨어뜨립니다.
4. 즉시 업로드 및 배포가 완료되어 고유 웹 링크가 발급됩니다.

---

## 교인 및 대형 화면(빔프로젝터/TV) 활용 팁

- **글자 크기 조절**: 상단의 `＋`, `－` 버튼을 눌러서 원하는 크기로 키울 수 있습니다 (설정값은 자동 저장됩니다).
- **🖥️ 스크린 모드**: 상단의 `🖥️ 스크린 모드` 버튼을 누르면 검색창과 하단 바가 숨겨지고, 말씀 본문만 화면 가득 정갈하게 출력되어 빔프로젝터나 강대상 TV 화면 송출에 최적화됩니다 (ESC 키로 복귀).
- **스마트폰/태블릿**: 모바일 브라우저(사파리, 크롬)에서 접속 후 **'홈 화면에 추가'**를 누르면 앱처럼 설치되어 아이콘 하나로 바로 켤 수 있습니다.
