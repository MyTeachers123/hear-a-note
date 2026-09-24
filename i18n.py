"""
i18n.py — single source of truth for all UI text (12 languages)
To add any text: add the same key to every language in STRINGS, then run generate_assets.py
to write static/i18n.json, which the frontend uses automatically. check() fails on missing translations.

notes: the 7 note names each language uses (Do Re Mi… / ドレミ… / C D E… / सा रे ग…)
"""

LANGS = [  # (code, name shown in the menu — each language in its own script)
    ("en", "English"),
    ("es", "Español"),
    ("zh-Hant", "繁體中文"),
    ("zh-Hans", "简体中文"),
    ("ko", "한국어"),
    ("ja", "日本語"),
    ("vi", "Tiếng Việt"),
    ("fr", "Français"),
    ("it", "Italiano"),
    ("ru", "Русский"),
    ("de", "Deutsch"),
    ("hi", "हिन्दी"),
]

STRINGS = {
    "en": {
        "appName": "Toddler Music Box", "start": "Tap to play", "continue": "Tap to continue",
        "free": "Free play", "black": "Black keys", "staff": "Staff", "now": "Current note",
        "language": "Language", "high": "High",
        "twinkle": "Twinkle Twinkle Little Star", "mary": "Mary Had a Little Lamb",
                "song": "Song", "piano": "Play on my piano", "stop": "Stop", "listening": "Listening… play on your piano", "midi": "MIDI piano connected", "micDenied": "Microphone is off — allow it in browser settings", "great": "Great job!",
                "micTitle": "Allow the microphone", "micBody": "To hear your piano, this app needs the microphone. The sound is only analyzed on this device — nothing is recorded or uploaded.", "micAllow": "Allow microphone", "micBlocked": "The microphone is blocked. Tap the lock icon (🔒) next to the web address → Microphone → Allow, then tap Try again.", "retry": "Try again", "close": "Close",
                "treble": "Treble clef", "bass": "Bass clef", "clef": "Clef",
                "quiz": "Quiz", "quizEnd": "End quiz", "quizPraise": "All correct — amazing!", "quizTryLater": "That's okay — let's try again later!",
        "notes": ["C", "D", "E", "F", "G", "A", "B"],
    },
    "es": {
        "appName": "Caja de Música para Peques", "start": "Toca para jugar", "continue": "Toca para continuar",
        "free": "Libre", "black": "Teclas negras", "staff": "Pentagrama", "now": "Nota actual",
        "language": "Idioma", "high": "Agudo",
        "twinkle": "Estrellita, ¿dónde estás?", "mary": "María tenía un corderito",
                "song": "Canción", "piano": "Tocar en mi piano", "stop": "Parar", "listening": "Escuchando… toca tu piano", "midi": "Piano MIDI conectado", "micDenied": "Micrófono desactivado — actívalo en el navegador", "great": "¡Muy bien!",
                "micTitle": "Permite el micrófono", "micBody": "Para escuchar tu piano, la app necesita el micrófono. El sonido solo se analiza en este dispositivo: no se graba ni se sube nada.", "micAllow": "Permitir micrófono", "micBlocked": "El micrófono está bloqueado. Toca el candado (🔒) junto a la dirección web → Micrófono → Permitir, y luego toca Reintentar.", "retry": "Reintentar", "close": "Cerrar",
                "treble": "Clave de sol", "bass": "Clave de fa", "clef": "Clave",
                "quiz": "Prueba", "quizEnd": "Terminar prueba", "quizPraise": "¡Todo correcto, increíble!", "quizTryLater": "No pasa nada, ¡lo intentamos luego!",
        "notes": ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"],
    },
    "zh-Hant": {
        "appName": "寶寶音樂盒", "start": "點一下開始", "continue": "點一下繼續",
        "free": "自由彈", "black": "黑鍵", "staff": "五線譜", "now": "當前音",
        "language": "語言", "high": "高音",
        "twinkle": "小星星", "mary": "瑪莉有隻小綿羊",
                "song": "歌曲", "piano": "用我的鋼琴彈", "stop": "停止", "listening": "聆聽中…請彈你的鋼琴", "midi": "已連接 MIDI 鋼琴", "micDenied": "麥克風未開啟，請在瀏覽器設定中允許", "great": "太棒了！",
                "micTitle": "請允許使用麥克風", "micBody": "要聽到你的鋼琴，需要使用麥克風。聲音只在這台裝置上分析，不會錄音，也不會上傳。", "micAllow": "允許麥克風", "micBlocked": "麥克風被封鎖了。請點網址旁的鎖頭（🔒）→ 麥克風 → 允許，再按「再試一次」。", "retry": "再試一次", "close": "關閉",
                "treble": "高音譜號", "bass": "低音譜號", "clef": "譜號",
                "quiz": "小測驗", "quizEnd": "結束測驗", "quizPraise": "全部答對，太厲害了！", "quizTryLater": "沒關係，下次再試！",
        "notes": ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"],
    },
    "zh-Hans": {
        "appName": "宝宝音乐盒", "start": "点一下开始", "continue": "点一下继续",
        "free": "自由弹", "black": "黑键", "staff": "五线谱", "now": "当前音",
        "language": "语言", "high": "高音",
        "twinkle": "小星星", "mary": "玛丽有只小绵羊",
                "song": "歌曲", "piano": "用我的钢琴弹", "stop": "停止", "listening": "聆听中…请弹你的钢琴", "midi": "已连接 MIDI 钢琴", "micDenied": "麦克风未开启，请在浏览器设置中允许", "great": "太棒了！",
                "micTitle": "请允许使用麦克风", "micBody": "要听到你的钢琴，需要使用麦克风。声音只在这台设备上分析，不会录音，也不会上传。", "micAllow": "允许麦克风", "micBlocked": "麦克风被阻止了。请点网址旁的锁头（🔒）→ 麦克风 → 允许，再按“再试一次”。", "retry": "再试一次", "close": "关闭",
                "treble": "高音谱号", "bass": "低音谱号", "clef": "谱号",
                "quiz": "小测验", "quizEnd": "结束测验", "quizPraise": "全部答对，太厉害了！", "quizTryLater": "没关系，下次再试！",
        "notes": ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"],
    },
    "ko": {
        "appName": "아기 뮤직박스", "start": "눌러서 시작", "continue": "눌러서 계속",
        "free": "자유 연주", "black": "검은 건반", "staff": "오선보", "now": "지금 음",
        "language": "언어", "high": "높은",
        "twinkle": "반짝반짝 작은 별", "mary": "메리의 어린 양",
                "song": "노래", "piano": "내 피아노로 치기", "stop": "멈추기", "listening": "듣는 중… 피아노를 쳐 보세요", "midi": "MIDI 피아노 연결됨", "micDenied": "마이크가 꺼져 있어요 — 브라우저 설정에서 허용하세요", "great": "잘했어요!",
                "micTitle": "마이크를 허용해 주세요", "micBody": "피아노 소리를 들으려면 마이크가 필요해요. 소리는 이 기기에서만 분석되며 녹음하거나 업로드하지 않아요.", "micAllow": "마이크 허용", "micBlocked": "마이크가 차단되어 있어요. 주소 옆 자물쇠(🔒) → 마이크 → 허용을 누른 뒤 '다시 시도'를 누르세요.", "retry": "다시 시도", "close": "닫기",
                "treble": "높은음자리표", "bass": "낮은음자리표", "clef": "음자리표",
                "quiz": "퀴즈", "quizEnd": "퀴즈 끝내기", "quizPraise": "모두 맞혔어요, 최고예요!", "quizTryLater": "괜찮아요, 다음에 다시 해요!",
        "notes": ["도", "레", "미", "파", "솔", "라", "시"],
    },
    "ja": {
        "appName": "ベビーミュージックボックス", "start": "タップしてはじめる", "continue": "タップしてつづける",
        "free": "じゆうにひく", "black": "くろいけんばん", "staff": "ごせんふ", "now": "いまのおと",
        "language": "げんご", "high": "たかい",
        "twinkle": "きらきらぼし", "mary": "メリーさんのひつじ",
                "song": "うた", "piano": "じぶんのピアノでひく", "stop": "とめる", "listening": "きいています… ピアノをひいてね", "midi": "MIDIピアノにつながりました", "micDenied": "マイクがオフです（ブラウザのせっていできょかしてください）", "great": "よくできました！",
                "micTitle": "マイクをきょかしてください", "micBody": "ピアノの音をきくためにマイクをつかいます。音はこの端末の中だけで分析し、録音やアップロードはしません。", "micAllow": "マイクをきょかする", "micBlocked": "マイクがブロックされています。アドレスの横のかぎ（🔒）→ マイク → 許可 にしてから「もういちど」をおしてください。", "retry": "もういちど", "close": "とじる",
                "treble": "トおんきごう", "bass": "ヘおんきごう", "clef": "おんきごう",
                "quiz": "クイズ", "quizEnd": "クイズをおわる", "quizPraise": "ぜんぶせいかい！すごいね！", "quizTryLater": "だいじょうぶ、またやってみよう！",
        "notes": ["ド", "レ", "ミ", "ファ", "ソ", "ラ", "シ"],
    },
    "vi": {
        "appName": "Hộp Nhạc Cho Bé", "start": "Chạm để chơi", "continue": "Chạm để tiếp tục",
        "free": "Chơi tự do", "black": "Phím đen", "staff": "Khuông nhạc", "now": "Nốt hiện tại",
        "language": "Ngôn ngữ", "high": "Cao",
        "twinkle": "Ngôi sao lấp lánh", "mary": "Mary có một chú cừu non",
                "song": "Bài hát", "piano": "Chơi trên đàn của bé", "stop": "Dừng", "listening": "Đang nghe… hãy chơi đàn nhé", "midi": "Đã kết nối đàn MIDI", "micDenied": "Micrô đang tắt — hãy cho phép trong trình duyệt", "great": "Giỏi lắm!",
                "micTitle": "Cho phép micrô", "micBody": "Để nghe đàn của bé, ứng dụng cần micrô. Âm thanh chỉ được phân tích trên thiết bị này — không ghi âm, không tải lên.", "micAllow": "Cho phép micrô", "micBlocked": "Micrô đang bị chặn. Chạm biểu tượng ổ khóa (🔒) cạnh địa chỉ web → Micrô → Cho phép, rồi chạm Thử lại.", "retry": "Thử lại", "close": "Đóng",
                "treble": "Khóa Sol", "bass": "Khóa Fa", "clef": "Khóa nhạc",
                "quiz": "Đố vui", "quizEnd": "Kết thúc đố vui", "quizPraise": "Đúng hết rồi, giỏi quá!", "quizTryLater": "Không sao, lần sau thử lại nhé!",
        "notes": ["Đô", "Rê", "Mi", "Fa", "Son", "La", "Si"],
    },
    "fr": {
        "appName": "Boîte à Musique Bébé", "start": "Touche pour jouer", "continue": "Touche pour continuer",
        "free": "Jeu libre", "black": "Touches noires", "staff": "Portée", "now": "Note actuelle",
        "language": "Langue", "high": "Aigu",
        "twinkle": "Ah ! vous dirai-je, maman", "mary": "Marie avait un petit agneau",
                "song": "Chanson", "piano": "Jouer sur mon piano", "stop": "Arrêter", "listening": "À l'écoute… joue sur ton piano", "midi": "Piano MIDI connecté", "micDenied": "Micro désactivé — autorise-le dans le navigateur", "great": "Bravo !",
                "micTitle": "Autorise le micro", "micBody": "Pour entendre ton piano, l'appli a besoin du micro. Le son est analysé uniquement sur cet appareil : rien n'est enregistré ni envoyé.", "micAllow": "Autoriser le micro", "micBlocked": "Le micro est bloqué. Touche le cadenas (🔒) à côté de l'adresse → Micro → Autoriser, puis touche Réessayer.", "retry": "Réessayer", "close": "Fermer",
                "treble": "Clé de sol", "bass": "Clé de fa", "clef": "Clé",
                "quiz": "Quiz", "quizEnd": "Terminer le quiz", "quizPraise": "Tout juste, bravo !", "quizTryLater": "Ce n'est pas grave, on réessaiera plus tard !",
        "notes": ["Do", "Ré", "Mi", "Fa", "Sol", "La", "Si"],
    },
    "it": {
        "appName": "Carillon per Bimbi", "start": "Tocca per suonare", "continue": "Tocca per continuare",
        "free": "Suona libero", "black": "Tasti neri", "staff": "Pentagramma", "now": "Nota attuale",
        "language": "Lingua", "high": "Acuto",
        "twinkle": "Brilla brilla la stellina", "mary": "Maria aveva un agnellino",
                "song": "Canzone", "piano": "Suona sul mio pianoforte", "stop": "Ferma", "listening": "In ascolto… suona il tuo pianoforte", "midi": "Pianoforte MIDI collegato", "micDenied": "Microfono disattivato — consentilo nel browser", "great": "Bravissimo!",
                "micTitle": "Consenti il microfono", "micBody": "Per sentire il tuo pianoforte, l'app ha bisogno del microfono. Il suono viene analizzato solo su questo dispositivo: nulla viene registrato o caricato.", "micAllow": "Consenti microfono", "micBlocked": "Il microfono è bloccato. Tocca il lucchetto (🔒) accanto all'indirizzo → Microfono → Consenti, poi tocca Riprova.", "retry": "Riprova", "close": "Chiudi",
                "treble": "Chiave di violino", "bass": "Chiave di basso", "clef": "Chiave",
                "quiz": "Quiz", "quizEnd": "Termina il quiz", "quizPraise": "Tutto giusto, fantastico!", "quizTryLater": "Non fa niente, riproviamo più tardi!",
        "notes": ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"],
    },
    "ru": {
        "appName": "Музыкальная шкатулка", "start": "Нажми, чтобы играть", "continue": "Нажми, чтобы продолжить",
        "free": "Свободная игра", "black": "Чёрные клавиши", "staff": "Нотный стан", "now": "Текущая нота",
        "language": "Язык", "high": "Высокая",
        "twinkle": "Ты свети, звезда моя", "mary": "У Мэри был барашек",
                "song": "Песня", "piano": "Играть на моём пианино", "stop": "Стоп", "listening": "Слушаю… играй на пианино", "midi": "MIDI-пианино подключено", "micDenied": "Микрофон выключен — разрешите его в браузере", "great": "Молодец!",
                "micTitle": "Разрешите микрофон", "micBody": "Чтобы слышать ваше пианино, приложению нужен микрофон. Звук анализируется только на этом устройстве — ничего не записывается и не отправляется.", "micAllow": "Разрешить микрофон", "micBlocked": "Микрофон заблокирован. Нажмите на замок (🔒) рядом с адресом → Микрофон → Разрешить, затем нажмите «Ещё раз».", "retry": "Ещё раз", "close": "Закрыть",
                "treble": "Скрипичный ключ", "bass": "Басовый ключ", "clef": "Ключ",
                "quiz": "Викторина", "quizEnd": "Закончить", "quizPraise": "Всё правильно — здорово!", "quizTryLater": "Ничего страшного, попробуем позже!",
        "notes": ["До", "Ре", "Ми", "Фа", "Соль", "Ля", "Си"],
    },
    "de": {
        "appName": "Baby-Spieluhr", "start": "Tippen zum Spielen", "continue": "Tippen zum Weiterspielen",
        "free": "Freies Spiel", "black": "Schwarze Tasten", "staff": "Notenlinien", "now": "Aktueller Ton",
        "language": "Sprache", "high": "Hohes",
        "twinkle": "Funkel, funkel, kleiner Stern", "mary": "Maria hat ein kleines Lamm",
                "song": "Lied", "piano": "Auf meinem Klavier spielen", "stop": "Stopp", "listening": "Ich höre zu… spiel auf deinem Klavier", "midi": "MIDI-Klavier verbunden", "micDenied": "Mikrofon ist aus – bitte im Browser erlauben", "great": "Super gemacht!",
                "micTitle": "Mikrofon erlauben", "micBody": "Um dein Klavier zu hören, braucht die App das Mikrofon. Der Ton wird nur auf diesem Gerät ausgewertet – nichts wird aufgenommen oder hochgeladen.", "micAllow": "Mikrofon erlauben", "micBlocked": "Das Mikrofon ist blockiert. Tippe auf das Schloss (🔒) neben der Adresse → Mikrofon → Erlauben und dann auf „Nochmal“.", "retry": "Nochmal", "close": "Schließen",
                "treble": "Violinschlüssel", "bass": "Bassschlüssel", "clef": "Schlüssel",
                "quiz": "Quiz", "quizEnd": "Quiz beenden", "quizPraise": "Alles richtig – toll!", "quizTryLater": "Macht nichts – wir versuchen es später nochmal!",
        "notes": ["C", "D", "E", "F", "G", "A", "H"],   # German uses H for B
    },
    "hi": {
        "appName": "शिशु संगीत बॉक्स", "start": "खेलने के लिए छुएँ", "continue": "जारी रखने के लिए छुएँ",
        "free": "मुक्त वादन", "black": "काली कुंजियाँ", "staff": "स्वरलिपि", "now": "वर्तमान स्वर",
        "language": "भाषा", "high": "तार",
        "twinkle": "चमक चमक छोटा तारा", "mary": "मैरी का छोटा मेमना",
                "song": "गीत", "piano": "मेरे पियानो पर बजाएँ", "stop": "रोकें", "listening": "सुन रहे हैं… अपना पियानो बजाएँ", "midi": "MIDI पियानो जुड़ा है", "micDenied": "माइक्रोफ़ोन बंद है — ब्राउज़र में अनुमति दें", "great": "बहुत बढ़िया!",
                "micTitle": "माइक्रोफ़ोन की अनुमति दें", "micBody": "आपका पियानो सुनने के लिए ऐप को माइक्रोफ़ोन चाहिए। आवाज़ केवल इसी डिवाइस पर जाँची जाती है — कुछ भी रिकॉर्ड या अपलोड नहीं होता।", "micAllow": "माइक्रोफ़ोन की अनुमति दें", "micBlocked": "माइक्रोफ़ोन ब्लॉक है। वेब पते के पास ताले (🔒) पर टैप करें → माइक्रोफ़ोन → अनुमति दें, फिर 'फिर से कोशिश करें' दबाएँ।", "retry": "फिर से कोशिश करें", "close": "बंद करें",
                "treble": "ट्रेबल क्लेफ़", "bass": "बेस क्लेफ़", "clef": "क्लेफ़",
                "quiz": "प्रश्नोत्तरी", "quizEnd": "प्रश्नोत्तरी समाप्त करें", "quizPraise": "सब सही — शानदार!", "quizTryLater": "कोई बात नहीं, बाद में फिर कोशिश करेंगे!",
        "notes": ["सा", "रे", "ग", "म", "प", "ध", "नि"],   # Indian sargam syllables
    },
}


def check() -> None:
    """Make sure every language has every key; fail loudly on missing translations"""
    base = set(STRINGS["en"])
    for code, _ in LANGS:
        missing = base - set(STRINGS[code])
        extra = set(STRINGS[code]) - base
        if missing or extra:
            raise SystemExit(f"i18n error: {code} is missing {sorted(missing)}, has extra {sorted(extra)}")
        if len(STRINGS[code]["notes"]) != 7:
            raise SystemExit(f"i18n error: {code} notes must have exactly 7 entries")
