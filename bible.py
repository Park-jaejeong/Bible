import os
import sys
import json
import re
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

# 성경 66권 약어 및 이름 매핑 정의
BIBLE_BOOKS = [
    ('창', '창세기', ['창세기', '창']),
    ('출', '출애굽기', ['출애굽기', '출']),
    ('레', '레위기', ['레위기', '레']),
    ('민', '민수기', ['민수기', '민']),
    ('신', '신명기', ['신명기', '신']),
    ('수', '여호수아', ['여호수아', '수']),
    ('삿', '사사기', ['사사기', '삿']),
    ('룻', '룻기', ['룻기', '룻']),
    ('삼상', '사무엘상', ['사무엘상', '삼상']),
    ('삼하', '사무엘하', ['사무엘하', '삼하']),
    ('왕상', '열왕기상', ['열왕기상', '왕상']),
    ('왕하', '열왕기하', ['열왕기하', '왕하']),
    ('대상', '역대상', ['역대상', '대상']),
    ('대하', '역대하', ['역대하', '대하']),
    ('스', '에스라', ['에스라', '스']),
    ('느', '느헤미야', ['느헤미야', '느']),
    ('에', '에스더', ['에스더', '에']),
    ('욥', '욥기', ['욥기', '욥']),
    ('시', '시편', ['시편', '시']),
    ('잠', '잠언', ['잠언', '잠']),
    ('전', '전도서', ['전도서', '전']),
    ('아', '아가', ['아가서', '아가', '아']),
    ('사', '이사야', ['이사야', '사']),
    ('렘', '예레미야', ['예레미야', '렘']),
    ('애', '예레미야애가', ['예레미야애가', '애가', '애']),
    ('겔', '에스겔', ['에스겔', '겔']),
    ('단', '다니엘', ['다니엘', '단']),
    ('호', '호세아', ['호세아', '호']),
    ('욜', '요엘', ['요엘', '욜']),
    ('암', '아모스', ['아모스', '암']),
    ('옵', '오바댜', ['오바댜', '옵']),
    ('욘', '요나', ['요나', '욘']),
    ('미', '미가', ['미가', '미']),
    ('나', '나훔', ['나훔', '나']),
    ('합', '하박국', ['하박국', '합']),
    ('습', '스바냐', ['스바냐', '습']),
    ('학', '학개', ['학개', '학']),
    ('슥', '스가랴', ['스가랴', '슥']),
    ('말', '말라기', ['말라기', '말']),
    ('마', '마태복음', ['마태복음', '마태', '마']),
    ('막', '마가복음', ['마가복음', '마가', '막']),
    ('눅', '누가복음', ['누가복음', '누가', '눅']),
    ('요', '요한복음', ['요한복음', '요한', '요']),
    ('행', '사도행전', ['사도행전', '행전', '행']),
    ('롬', '로마서', ['로마서', '로마', '롬']),
    ('고전', '고린도전서', ['고린도전서', '고전']),
    ('고후', '고린도후서', ['고린도후서', '고후']),
    ('갈', '갈라디아서', ['갈라디아서', '갈라디아', '갈']),
    ('엡', '에베소서', ['에베소서', '에베소', '엡']),
    ('빌', '빌립보서', ['빌립보서', '빌립보', '빌']),
    ('골', '골로새서', ['골로새서', '골로새', '골']),
    ('살전', '데살로니가전서', ['데살로니가전서', '살전']),
    ('살후', '데살로니가후서', ['데살로니가후서', '살후']),
    ('딤전', '디모데전서', ['디모데전서', '딤전']),
    ('딤후', '디모데후서', ['디모데후서', '딤후']),
    ('딛', '디도서', ['디도서', '디도', '딛']),
    ('몬', '빌레몬서', ['빌레몬서', '빌레몬', '몬']),
    ('히', '히브리서', ['히브리서', '히브리', '히']),
    ('약', '야고보서', ['야고보서', '야고보', '약']),
    ('벧전', '베드로전서', ['베드로전서', '벧전']),
    ('벧후', '베드로후서', ['베드로후서', '벧후']),
    ('요일', '요한일서', ['요한일서', '요한1서', '요일']),
    ('요이', '요한이서', ['요한이서', '요한2서', '요이']),
    ('요삼', '요한삼서', ['요한삼서', '요한3서', '요삼']),
    ('유', '유다서', ['유다서', '유다', '유']),
    ('계', '요한계시록', ['요한계시록', '계시록', '계']),
]

NAME_TO_ABBR = {}
ABBR_TO_FULL = {}
for abbr, fullname, aliases in BIBLE_BOOKS:
    ABBR_TO_FULL[abbr] = fullname
    for name in aliases:
        NAME_TO_ABBR[name] = abbr

# 긴 이름부터 매칭되도록 정렬
SORTED_NAMES = sorted(NAME_TO_ABBR.keys(), key=lambda x: -len(x))

# ==========================================
# 실시간 한글 2벌식 분해 및 조합 엔진
# ==========================================
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
JONGSUNG_LIST = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

DOUBLE_JUNG = {'ㅗㅏ': 'ㅘ', 'ㅗㅐ': 'ㅙ', 'ㅗㅣ': 'ㅚ', 'ㅜㅓ': 'ㅝ', 'ㅜㅔ': 'ㅞ', 'ㅜㅣ': 'ㅟ', 'ㅡㅣ': 'ㅢ'}
DOUBLE_JONG = {'ㄱㅅ': 'ㄳ', 'ㄴㅈ': 'ㄵ', 'ㄴㅎ': 'ㄶ', 'ㄹㄱ': 'ㄺ', 'ㄹㅁ': 'ㄻ', 'ㄹㅂ': 'ㄼ', 'ㄹㅅ': 'ㄽ', 'ㄹㅌ': 'ㄾ', 'ㄹㅍ': 'ㄿ', 'ㄹㅎ': 'ㅀ', 'ㅂㅅ': 'ㅄ'}

DECOMPOSE_JUNG = {'ㅘ': ('ㅗ', 'ㅏ'), 'ㅙ': ('ㅗ', 'ㅐ'), 'ㅚ': ('ㅗ', 'ㅣ'), 'ㅝ': ('ㅜ', 'ㅓ'), 'ㅞ': ('ㅜ', 'ㅔ'), 'ㅟ': ('ㅜ', 'ㅣ'), 'ㅢ': ('ㅡ', 'ㅣ')}
DECOMPOSE_JONG = {'ㄳ': ('ㄱ', 'ㅅ'), 'ㄵ': ('ㄴ', 'ㅈ'), 'ㄶ': ('ㄴ', 'ㅎ'), 'ㄺ': ('ㄹ', 'ㄱ'), 'ㄻ': ('ㄹ', 'ㅁ'), 'ㄼ': ('ㄹ', 'ㅂ'), 'ㄽ': ('ㄹ', 'ㅅ'), 'ㄾ': ('ㄹ', 'ㅌ'), 'ㄿ': ('ㄹ', 'ㅍ'), 'ㅀ': ('ㄹ', 'ㅎ'), 'ㅄ': ('ㅂ', 'ㅅ')}

ENG_TO_JAMO = {
    'q': 'ㅂ', 'Q': 'ㅃ', 'w': 'ㅈ', 'W': 'ㅉ', 'e': 'ㄷ', 'E': 'ㄸ', 'r': 'ㄱ', 'R': 'ㄲ', 't': 'ㅅ', 'T': 'ㅆ',
    'y': 'ㅛ', 'u': 'ㅕ', 'i': 'ㅑ', 'o': 'ㅐ', 'O': 'ㅒ', 'p': 'ㅔ', 'P': 'ㅖ',
    'a': 'ㅁ', 's': 'ㄴ', 'd': 'ㅇ', 'f': 'ㄹ', 'g': 'ㅎ',
    'h': 'ㅗ', 'j': 'ㅓ', 'k': 'ㅏ', 'l': 'ㅣ',
    'z': 'ㅋ', 'x': 'ㅌ', 'c': 'ㅊ', 'v': 'ㅍ', 'b': 'ㅠ', 'n': 'ㅜ', 'm': 'ㅡ'
}

def decompose_hangul(text):
    """완성형 한글을 자모 단위로 완전 분해"""
    res = []
    for ch in text:
        code = ord(ch)
        if 0xAC00 <= code <= 0xD7A3:
            syl = code - 0xAC00
            cho = syl // (21 * 28)
            jung = (syl % (21 * 28)) // 28
            jong = syl % 28
            res.append(CHOSUNG_LIST[cho])
            jung_char = JUNGSUNG_LIST[jung]
            if jung_char in DECOMPOSE_JUNG:
                res.extend(DECOMPOSE_JUNG[jung_char])
            else:
                res.append(jung_char)
            if jong > 0:
                jong_char = JONGSUNG_LIST[jong]
                if jong_char in DECOMPOSE_JONG:
                    res.extend(DECOMPOSE_JONG[jong_char])
                else:
                    res.append(jong_char)
        else:
            res.append(ch)
    return res

def compose_hangul(jamos):
    """자모 배열을 온전한 한글 음절로 조합"""
    res = []
    i = 0
    n = len(jamos)
    while i < n:
        c1 = jamos[i]
        if c1 in CHOSUNG_LIST:
            if i + 1 < n and jamos[i+1] in JUNGSUNG_LIST:
                cho = c1
                jung = jamos[i+1]
                i += 2
                if i < n and (jung + jamos[i]) in DOUBLE_JUNG:
                    jung = DOUBLE_JUNG[jung + jamos[i]]
                    i += 1
                jong = ''
                if i < n and jamos[i] in JONGSUNG_LIST:
                    if i + 1 < n and jamos[i+1] in JUNGSUNG_LIST:
                        pass
                    else:
                        jong = jamos[i]
                        i += 1
                        if i < n and (jong + jamos[i]) in DOUBLE_JONG:
                            if i + 1 < n and jamos[i+1] in JUNGSUNG_LIST:
                                pass
                            else:
                                jong = DOUBLE_JONG[jong + jamos[i]]
                                i += 1
                c_idx = CHOSUNG_LIST.index(cho)
                j_idx = JUNGSUNG_LIST.index(jung)
                t_idx = JONGSUNG_LIST.index(jong)
                res.append(chr(0xAC00 + (c_idx * 21 + j_idx) * 28 + t_idx))
            else:
                res.append(c1)
                i += 1
        else:
            res.append(c1)
            i += 1
    return ''.join(res)

def instant_hangul(text):
    """영문 키 입력 발생 시 화면에 즉시 한글로 나타나도록 변환"""
    if not text:
        return ""
    decomposed = decompose_hangul(text)
    converted = [ENG_TO_JAMO.get(ch, ch) for ch in decomposed]
    return compose_hangul(converted)


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def load_bible_data():
    data_path = os.path.join(get_base_dir(), 'bible_data.json')
    if not os.path.exists(data_path):
        return {}
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_query(query):
    q = query.strip()
    if not q:
        return None

    # 혹시 모를 영문 키 입력도 한글로 즉시 변환
    if re.search(r'[a-zA-Z]', q):
        q = instant_hangul(q)

    found_abbr = None
    rest = ''
    for name in SORTED_NAMES:
        if q.startswith(name):
            found_abbr = NAME_TO_ABBR[name]
            rest = q[len(name):].strip()
            break

    if not found_abbr:
        return None

    patterns = [
        r'^(\d+)\s*[:\.]\s*(\d+)(?:\s*[-~]\s*(\d+))?$',
        r'^(\d+)\s*(?:장|편)\s*(\d+)\s*절?(?:\s*[-~]\s*(\d+)\s*절?)?$',
        r'^(\d+)\s+(\d+)(?:\s*[-~]\s*(\d+))?$',
        r'^(\d+)\s*(?:장|편)?$'
    ]

    for p in patterns:
        m = re.match(p, rest)
        if m:
            groups = m.groups()
            chap = int(groups[0])
            if len(groups) >= 2 and groups[1] is not None:
                v_start = int(groups[1])
                v_end = int(groups[2]) if len(groups) >= 3 and groups[2] is not None else v_start
                return found_abbr, chap, v_start, v_end, q
            return found_abbr, chap, None, None, q

    return None


class BibleApp(tk.Tk):
    """모든 교인을 위한 초경량 개역개정 성경 뷰어"""

    def __init__(self):
        super().__init__()
        self.title("개역개정 성경 본문 뷰어")
        self.geometry("760x780")
        self.minsize(520, 440)
        self.configure(bg="#F1F5F9")

        self.font_size = 17
        self.is_fullscreen = False
        self.bible_data = load_bible_data()
        self.current_result_text = ""
        self._updating_entry = False

        self._setup_ui()
        self._setup_events()

    def _setup_ui(self):
        # 상단 검색 바 컨테이너
        self.top_frame = tk.Frame(self, bg="#FFFFFF", padx=16, pady=12)
        self.top_frame.pack(fill=tk.X, side=tk.TOP)

        self.entry_var = tk.StringVar()
        self.entry_var.trace_add("write", self._on_entry_input)
        self.entry = tk.Entry(
            self.top_frame,
            textvariable=self.entry_var,
            font=("맑은 고딕", 16),
            relief=tk.SOLID,
            bd=1,
            highlightthickness=2,
            highlightcolor="#2563EB",
            highlightbackground="#CBD5E1"
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 8))

        # 찾기 버튼
        self.search_btn = tk.Button(
            self.top_frame,
            text=" 🔍 찾기 ",
            command=self.search,
            font=("맑은 고딕", 12, "bold"),
            bg="#2563EB",
            fg="#FFFFFF",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=4
        )
        self.search_btn.pack(side=tk.RIGHT)

        # 구분선
        self.sep = tk.Frame(self, bg="#CBD5E1", height=2)
        self.sep.pack(fill=tk.X)

        # 컨트롤 헤더 영역
        self.header_frame = tk.Frame(self, bg="#F1F5F9", padx=16, pady=10)
        self.header_frame.pack(fill=tk.X)

        self.title_label = tk.Label(
            self.header_frame,
            text="원하는 성경 장절을 입력하고 Enter를 누르세요",
            font=("맑은 고딕", 12, "bold"),
            bg="#F1F5F9",
            fg="#0F172A"
        )
        self.title_label.pack(side=tk.LEFT)

        # 우측 컨트롤 그룹
        right_ctrl_frame = tk.Frame(self.header_frame, bg="#F1F5F9")
        right_ctrl_frame.pack(side=tk.RIGHT)

        # 글자크기 축소 (-)
        self.btn_font_minus = tk.Button(
            right_ctrl_frame,
            text=" － ",
            command=self.decrease_font_size,
            font=("맑은 고딕", 12, "bold"),
            bg="#E2E8F0",
            fg="#0F172A",
            relief=tk.GROOVE,
            cursor="hand2",
            padx=5,
            pady=1
        )
        self.btn_font_minus.pack(side=tk.LEFT, padx=2)

        # 글자 크기 표시 및 직접 숫자 입력
        self.font_size_var = tk.StringVar(value=str(self.font_size))
        self.font_size_entry = tk.Entry(
            right_ctrl_frame,
            textvariable=self.font_size_var,
            font=("맑은 고딕", 11, "bold"),
            bg="#FFFFFF",
            fg="#2563EB",
            width=3,
            justify="center",
            relief=tk.SOLID,
            bd=1
        )
        self.font_size_entry.pack(side=tk.LEFT, padx=2)
        self.font_size_entry.bind("<Return>", lambda e: self._on_font_entry_change())
        self.font_size_entry.bind("<FocusOut>", lambda e: self._on_font_entry_change())
        self.font_size_entry.bind("<FocusIn>", lambda e: self.font_size_entry.select_range(0, tk.END))

        self.font_unit_label = tk.Label(
            right_ctrl_frame,
            text="pt",
            font=("맑은 고딕", 10),
            bg="#F1F5F9",
            fg="#64748B"
        )
        self.font_unit_label.pack(side=tk.LEFT, padx=(0, 2))

        # 글자크기 확대 (+)
        self.btn_font_plus = tk.Button(
            right_ctrl_frame,
            text=" ＋ ",
            command=self.increase_font_size,
            font=("맑은 고딕", 12, "bold"),
            bg="#E2E8F0",
            fg="#0F172A",
            relief=tk.GROOVE,
            cursor="hand2",
            padx=5,
            pady=1
        )
        self.btn_font_plus.pack(side=tk.LEFT, padx=2)

        # 🖥️ 스크린모드 (전체화면) 버튼
        self.screen_btn = tk.Button(
            right_ctrl_frame,
            text=" 🖥️ 스크린 모드 ",
            command=self.toggle_fullscreen,
            font=("맑은 고딕", 10, "bold"),
            bg="#059669",
            fg="#FFFFFF",
            activebackground="#047857",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=8,
            pady=2
        )
        self.screen_btn.pack(side=tk.LEFT, padx=(8, 2))

        # 본문 복사 버튼
        self.copy_btn = tk.Button(
            right_ctrl_frame,
            text="본문 복사",
            command=self.copy_to_clipboard,
            font=("맑은 고딕", 9),
            bg="#E2E8F0",
            fg="#334155",
            relief=tk.GROOVE,
            cursor="hand2",
            padx=6,
            pady=2
        )
        self.copy_btn.pack(side=tk.LEFT, padx=(4, 0))

        # 스크린 모드용 상단 고정 헤더 바 (본문 스크롤 시에도 맨 위에 항상 고정 표시)
        self.screen_header_frame = tk.Frame(self, bg="#FFFFFF", padx=24, pady=12)
        self.screen_header_sep = tk.Frame(self, bg="#2563EB", height=3)

        self.screen_title_label = tk.Label(
            self.screen_header_frame,
            text="",
            font=("맑은 고딕", 22, "bold"),
            bg="#FFFFFF",
            fg="#0F172A"
        )
        self.screen_title_label.pack(side=tk.LEFT)

        self.screen_exit_btn = tk.Button(
            self.screen_header_frame,
            text=" ✕ 일반 화면 (ESC) ",
            command=self.toggle_fullscreen,
            font=("맑은 고딕", 11, "bold"),
            bg="#DC2626",
            fg="#FFFFFF",
            activebackground="#B91C1C",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=4
        )
        self.screen_exit_btn.pack(side=tk.RIGHT)

        # 본문 출력 텍스트 영역
        self.content_frame = tk.Frame(self, bg="#F1F5F9", padx=16, pady=2)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        self.text_area = ScrolledText(
            self.content_frame,
            wrap=tk.WORD,
            font=("맑은 고딕", self.font_size),
            bg="#FFFFFF",
            fg="#0F172A",
            padx=24,
            pady=24,
            relief=tk.SOLID,
            bd=1,
            spacing1=2,
            spacing2=4,
            spacing3=8
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self._update_tag_fonts()

        # 하단 도움말 바
        self.bottom_frame = tk.Frame(self, bg="#E2E8F0", padx=12, pady=6)
        self.bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)

        guide_text = "입력 예시:  창 1:1  |  요 3:16  |  시편 23편  |  스크린 모드(F11 또는 🖥️)"
        guide_label = tk.Label(
            self.bottom_frame,
            text=guide_text,
            font=("맑은 고딕", 9),
            bg="#E2E8F0",
            fg="#64748B"
        )
        guide_label.pack(side=tk.LEFT)

        self._show_initial_guide()

    def _on_entry_input(self, *args):
        """영문 입력 시 즉시 한글로 화면에 표시"""
        if getattr(self, '_updating_entry', False):
            return
        cur_val = self.entry_var.get()
        converted = instant_hangul(cur_val)
        if cur_val != converted:
            self._updating_entry = True
            cursor_pos = self.entry.index(tk.INSERT)
            diff = len(converted) - len(cur_val)
            self.entry_var.set(converted)
            new_pos = max(0, cursor_pos + diff)
            self.entry.icursor(new_pos)
            self._updating_entry = False

    def _setup_events(self):
        self.entry.bind("<Return>", lambda e: self.search())
        self.after(100, lambda: self.entry.focus_set())
        self.entry.bind("<Control-a>", self._select_all_entry)

        # 전체화면 토글 (F11 및 ESC)
        self.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.bind("<Escape>", lambda e: self.exit_fullscreen())

        # 마우스 휠 및 키보드로 글자 크기 조절
        self.bind("<Control-MouseWheel>", self._on_ctrl_wheel)
        self.bind("<Control-plus>", lambda e: self.increase_font_size())
        self.bind("<Control-equal>", lambda e: self.increase_font_size())
        self.bind("<Control-minus>", lambda e: self.decrease_font_size())

        # 시작 시 기본 한글 성경 구절 바로 표시
        self.entry_var.set("창 1:1-5")
        self.search()

    def toggle_fullscreen(self):
        """전교인 스크린 모드 (전체화면 토글)"""
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        if self.is_fullscreen:
            self.screen_btn.config(text=" ✕ 일반 화면 (ESC) ", bg="#DC2626")
            self.top_frame.pack_forget()
            self.sep.pack_forget()
            self.header_frame.pack_forget()
            self.content_frame.pack_forget()
            self.bottom_frame.pack_forget()

            # 스크린 모드: 상단에 성경 장절 바를 고정 배치하고 그 아래 본문 배치 (스크롤 시에도 항상 상단 고정)
            self.screen_header_frame.pack(fill=tk.X, side=tk.TOP)
            self.screen_header_sep.pack(fill=tk.X, side=tk.TOP)
            self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            self._update_screen_header_font()
            # 본문 스크롤을 맨 위(1절)로 초기화
            self.text_area.yview_moveto(0.0)
        else:
            self.screen_btn.config(text=" 🖥️ 스크린 모드 ", bg="#059669")
            self.screen_header_frame.pack_forget()
            self.screen_header_sep.pack_forget()
            self.content_frame.pack_forget()

            self.top_frame.pack(fill=tk.X, side=tk.TOP)
            self.sep.pack(fill=tk.X)
            self.header_frame.pack(fill=tk.X)
            self.content_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 6))
            self.bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)

    def exit_fullscreen(self):
        if self.is_fullscreen:
            self.toggle_fullscreen()

    def _on_ctrl_wheel(self, event):
        if event.delta > 0:
            self.increase_font_size()
        else:
            self.decrease_font_size()

    def _select_all_entry(self, event):
        self.entry.select_range(0, tk.END)
        return "break"

    def increase_font_size(self):
        if self.font_size < 80:
            self.font_size += 2
            self._apply_font_size()

    def decrease_font_size(self):
        if self.font_size > 11:
            self.font_size -= 2
            self._apply_font_size()

    def _on_font_entry_change(self):
        try:
            val = int(self.font_size_var.get().strip())
            if 10 <= val <= 150:
                self.font_size = val
                self._apply_font_size()
            else:
                self.font_size_var.set(str(self.font_size))
        except ValueError:
            self.font_size_var.set(str(self.font_size))

    def _update_screen_header_font(self):
        header_size = max(18, min(42, int(self.font_size * 1.15)))
        self.screen_title_label.config(font=("맑은 고딕", header_size, "bold"))

    def _apply_font_size(self):
        self.font_size_var.set(str(self.font_size))
        self._update_tag_fonts()
        self._update_screen_header_font()

    def _update_tag_fonts(self):
        num_size = max(10, self.font_size - 1)
        header_size = max(16, int(self.font_size * 1.2))
        self.text_area.tag_config("verse_num", foreground="#2563EB", font=("맑은 고딕", num_size, "bold"))
        self.text_area.tag_config("body_text", foreground="#0F172A", font=("맑은 고딕", self.font_size))
        self.text_area.tag_config("header_title", foreground="#1E40AF", font=("맑은 고딕", header_size, "bold"), underline=True)
        self.text_area.tag_config("notice", foreground="#64748B", font=("맑은 고딕", self.font_size))

    def _show_initial_guide(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        intro = (
            "📖 개역개정 성경 본문 뷰어\n\n"
            "상단 입력창에 성경 장절을 입력한 뒤 [Enter]를 누르세요.\n\n"
            "■ 주요 편의 기능:\n"
            "  • 글자 크기 조절 [ ＋ ] / [ － ]: 모든 교인들이 멀리서도 잘 보이도록 확대할 수 있습니다.\n"
            "  • [ 🖥️ 스크린 모드 ]: 클릭하거나 F11 키를 누르면 예배당 빔프로젝터용 전체화면으로 전환됩니다.\n"
        )
        self.text_area.insert(tk.END, intro, "notice")
        self.text_area.config(state=tk.DISABLED)

    def search(self):
        raw_query = self.entry_var.get().strip()
        if not raw_query:
            return

        parsed = parse_query(raw_query)
        if not parsed:
            self._show_not_found(f"'{raw_query}' 형식을 인식할 수 없습니다.\n예: 창 1:1, 요 3:16, 시 23")
            return

        abbr, chap, v_start, v_end, converted_query = parsed

        # 영타였던 경우 입력창을 한글로 갱신
        if converted_query != raw_query:
            self.entry_var.set(converted_query)

        full_name = ABBR_TO_FULL.get(abbr, abbr)

        results = []
        if v_start is None:
            v = 1
            while True:
                key = f"{abbr}{chap}:{v}"
                if key in self.bible_data:
                    results.append((v, self.bible_data[key]))
                    v += 1
                else:
                    break
            range_desc = f"{full_name} {chap}장 전체 (총 {len(results)}절)"
        else:
            if v_start > v_end:
                v_start, v_end = v_end, v_start

            for v in range(v_start, v_end + 1):
                key = f"{abbr}{chap}:{v}"
                if key in self.bible_data:
                    results.append((v, self.bible_data[key]))

            if v_start == v_end:
                range_desc = f"{full_name} {chap}장 {v_start}절"
            else:
                range_desc = f"{full_name} {chap}장 {v_start}~{v_end}절 (총 {len(results)}절)"

        if not results:
            self._show_not_found(f"'{raw_query}'에 해당하는 성경 본문을 찾지 못했습니다.\n(장 또는 절 번호를 확인해 주세요)")
            return

        self.title_label.config(text=f"📖 {range_desc}", fg="#0F172A")
        self.screen_title_label.config(text=f"📖 {range_desc}")

        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)

        copy_lines = [f"[{range_desc}]"]

        for v_num, text in results:
            self.text_area.insert(tk.END, f"{v_num} ", "verse_num")
            self.text_area.insert(tk.END, f"{text}\n", "body_text")
            copy_lines.append(f"{v_num} {text}")

        self.text_area.config(state=tk.DISABLED)
        self.current_result_text = "\n".join(copy_lines)
        self.entry.select_range(0, tk.END)

    def _show_not_found(self, msg):
        self.title_label.config(text="검색 결과 없음", fg="#DC2626")
        self.screen_title_label.config(text="검색 결과 없음")
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, f"\n{msg}\n", "notice")
        self.text_area.config(state=tk.DISABLED)
        self.current_result_text = ""

    def copy_to_clipboard(self):
        if not self.current_result_text:
            return
        self.clipboard_clear()
        self.clipboard_append(self.current_result_text)
        self.copy_btn.config(text="✓ 복사됨")
        self.after(1500, lambda: self.copy_btn.config(text="본문 복사"))


def main():
    app = BibleApp()
    app.mainloop()


if __name__ == "__main__":
    main()
