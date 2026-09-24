"""
i18n.py - single source of truth for all UI text (12 languages)
To add any text: add the same key to every language in STRINGS, then run generate_assets.py
to write static/i18n.json, which the frontend uses automatically. check() fails on missing translations.

Non-English text is stored as \\uXXXX escapes so every file in the repository is plain ASCII.
Python and JSON decode them automatically; the app shows the real characters.

notes: the 7 note names each language uses (Do Re Mi... / C D E... in each language)
"""

LANGS = [  # (code, name shown in the menu, in its own script)
    ("en", "English"),
    ("es", "Espa\u00f1ol"),
    ("zh-Hant", "\u7e41\u9ad4\u4e2d\u6587"),
    ("zh-Hans", "\u7b80\u4f53\u4e2d\u6587"),
    ("ko", "\ud55c\uad6d\uc5b4"),
    ("ja", "\u65e5\u672c\u8a9e"),
    ("vi", "Ti\u1ebfng Vi\u1ec7t"),
    ("fr", "Fran\u00e7ais"),
    ("it", "Italiano"),
    ("ru", "\u0420\u0443\u0441\u0441\u043a\u0438\u0439"),
    ("de", "Deutsch"),
    ("hi", "\u0939\u093f\u0928\u094d\u0926\u0940"),
]

STRINGS = {
    "en": {
        "appName": "Toddler Music Box", "start": "Tap to play", "continue": "Tap to continue",
        "free": "Free play", "black": "Black keys", "staff": "Staff", "now": "Current note",
        "language": "Language", "high": "High",
        "twinkle": "Twinkle Twinkle Little Star", "mary": "Mary Had a Little Lamb",
                "song": "Song", "piano": "Play on my piano", "stop": "Stop", "listening": "Listening\u2026 play on your piano", "midi": "MIDI piano connected", "micDenied": "Microphone is off \u2014 allow it in browser settings", "great": "Great job!",
                "micTitle": "Allow the microphone", "micBody": "To hear your piano, this app needs the microphone. The sound is only analyzed on this device \u2014 nothing is recorded or uploaded.", "micAllow": "Allow microphone", "micBlocked": "The microphone is blocked. Tap the lock icon (\U0001f512) next to the web address \u2192 Microphone \u2192 Allow, then tap Try again.", "retry": "Try again", "close": "Close",
                "treble": "Treble clef", "bass": "Bass clef", "clef": "Clef",
                "quiz": "Quiz", "quizEnd": "End quiz", "quizPraise": "All correct \u2014 amazing!", "quizTryLater": "That's okay \u2014 let's try again later!",
        "notes": ["C", "D", "E", "F", "G", "A", "B"],
    },
    "es": {
        "appName": "Caja de M\u00fasica para Peques", "start": "Toca para jugar", "continue": "Toca para continuar",
        "free": "Libre", "black": "Teclas negras", "staff": "Pentagrama", "now": "Nota actual",
        "language": "Idioma", "high": "Agudo",
        "twinkle": "Estrellita, \u00bfd\u00f3nde est\u00e1s?", "mary": "Mar\u00eda ten\u00eda un corderito",
                "song": "Canci\u00f3n", "piano": "Tocar en mi piano", "stop": "Parar", "listening": "Escuchando\u2026 toca tu piano", "midi": "Piano MIDI conectado", "micDenied": "Micr\u00f3fono desactivado \u2014 act\u00edvalo en el navegador", "great": "\u00a1Muy bien!",
                "micTitle": "Permite el micr\u00f3fono", "micBody": "Para escuchar tu piano, la app necesita el micr\u00f3fono. El sonido solo se analiza en este dispositivo: no se graba ni se sube nada.", "micAllow": "Permitir micr\u00f3fono", "micBlocked": "El micr\u00f3fono est\u00e1 bloqueado. Toca el candado (\U0001f512) junto a la direcci\u00f3n web \u2192 Micr\u00f3fono \u2192 Permitir, y luego toca Reintentar.", "retry": "Reintentar", "close": "Cerrar",
                "treble": "Clave de sol", "bass": "Clave de fa", "clef": "Clave",
                "quiz": "Prueba", "quizEnd": "Terminar prueba", "quizPraise": "\u00a1Todo correcto, incre\u00edble!", "quizTryLater": "No pasa nada, \u00a1lo intentamos luego!",
        "notes": ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"],
    },
    "zh-Hant": {
        "appName": "\u5bf6\u5bf6\u97f3\u6a02\u76d2", "start": "\u9ede\u4e00\u4e0b\u958b\u59cb", "continue": "\u9ede\u4e00\u4e0b\u7e7c\u7e8c",
        "free": "\u81ea\u7531\u5f48", "black": "\u9ed1\u9375", "staff": "\u4e94\u7dda\u8b5c", "now": "\u7576\u524d\u97f3",
        "language": "\u8a9e\u8a00", "high": "\u9ad8\u97f3",
        "twinkle": "\u5c0f\u661f\u661f", "mary": "\u746a\u8389\u6709\u96bb\u5c0f\u7dbf\u7f8a",
                "song": "\u6b4c\u66f2", "piano": "\u7528\u6211\u7684\u92fc\u7434\u5f48", "stop": "\u505c\u6b62", "listening": "\u8046\u807d\u4e2d\u2026\u8acb\u5f48\u4f60\u7684\u92fc\u7434", "midi": "\u5df2\u9023\u63a5 MIDI \u92fc\u7434", "micDenied": "\u9ea5\u514b\u98a8\u672a\u958b\u555f\uff0c\u8acb\u5728\u700f\u89bd\u5668\u8a2d\u5b9a\u4e2d\u5141\u8a31", "great": "\u592a\u68d2\u4e86\uff01",
                "micTitle": "\u8acb\u5141\u8a31\u4f7f\u7528\u9ea5\u514b\u98a8", "micBody": "\u8981\u807d\u5230\u4f60\u7684\u92fc\u7434\uff0c\u9700\u8981\u4f7f\u7528\u9ea5\u514b\u98a8\u3002\u8072\u97f3\u53ea\u5728\u9019\u53f0\u88dd\u7f6e\u4e0a\u5206\u6790\uff0c\u4e0d\u6703\u9304\u97f3\uff0c\u4e5f\u4e0d\u6703\u4e0a\u50b3\u3002", "micAllow": "\u5141\u8a31\u9ea5\u514b\u98a8", "micBlocked": "\u9ea5\u514b\u98a8\u88ab\u5c01\u9396\u4e86\u3002\u8acb\u9ede\u7db2\u5740\u65c1\u7684\u9396\u982d\uff08\U0001f512\uff09\u2192 \u9ea5\u514b\u98a8 \u2192 \u5141\u8a31\uff0c\u518d\u6309\u300c\u518d\u8a66\u4e00\u6b21\u300d\u3002", "retry": "\u518d\u8a66\u4e00\u6b21", "close": "\u95dc\u9589",
                "treble": "\u9ad8\u97f3\u8b5c\u865f", "bass": "\u4f4e\u97f3\u8b5c\u865f", "clef": "\u8b5c\u865f",
                "quiz": "\u5c0f\u6e2c\u9a57", "quizEnd": "\u7d50\u675f\u6e2c\u9a57", "quizPraise": "\u5168\u90e8\u7b54\u5c0d\uff0c\u592a\u53b2\u5bb3\u4e86\uff01", "quizTryLater": "\u6c92\u95dc\u4fc2\uff0c\u4e0b\u6b21\u518d\u8a66\uff01",
        "notes": ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"],
    },
    "zh-Hans": {
        "appName": "\u5b9d\u5b9d\u97f3\u4e50\u76d2", "start": "\u70b9\u4e00\u4e0b\u5f00\u59cb", "continue": "\u70b9\u4e00\u4e0b\u7ee7\u7eed",
        "free": "\u81ea\u7531\u5f39", "black": "\u9ed1\u952e", "staff": "\u4e94\u7ebf\u8c31", "now": "\u5f53\u524d\u97f3",
        "language": "\u8bed\u8a00", "high": "\u9ad8\u97f3",
        "twinkle": "\u5c0f\u661f\u661f", "mary": "\u739b\u4e3d\u6709\u53ea\u5c0f\u7ef5\u7f8a",
                "song": "\u6b4c\u66f2", "piano": "\u7528\u6211\u7684\u94a2\u7434\u5f39", "stop": "\u505c\u6b62", "listening": "\u8046\u542c\u4e2d\u2026\u8bf7\u5f39\u4f60\u7684\u94a2\u7434", "midi": "\u5df2\u8fde\u63a5 MIDI \u94a2\u7434", "micDenied": "\u9ea6\u514b\u98ce\u672a\u5f00\u542f\uff0c\u8bf7\u5728\u6d4f\u89c8\u5668\u8bbe\u7f6e\u4e2d\u5141\u8bb8", "great": "\u592a\u68d2\u4e86\uff01",
                "micTitle": "\u8bf7\u5141\u8bb8\u4f7f\u7528\u9ea6\u514b\u98ce", "micBody": "\u8981\u542c\u5230\u4f60\u7684\u94a2\u7434\uff0c\u9700\u8981\u4f7f\u7528\u9ea6\u514b\u98ce\u3002\u58f0\u97f3\u53ea\u5728\u8fd9\u53f0\u8bbe\u5907\u4e0a\u5206\u6790\uff0c\u4e0d\u4f1a\u5f55\u97f3\uff0c\u4e5f\u4e0d\u4f1a\u4e0a\u4f20\u3002", "micAllow": "\u5141\u8bb8\u9ea6\u514b\u98ce", "micBlocked": "\u9ea6\u514b\u98ce\u88ab\u963b\u6b62\u4e86\u3002\u8bf7\u70b9\u7f51\u5740\u65c1\u7684\u9501\u5934\uff08\U0001f512\uff09\u2192 \u9ea6\u514b\u98ce \u2192 \u5141\u8bb8\uff0c\u518d\u6309\u201c\u518d\u8bd5\u4e00\u6b21\u201d\u3002", "retry": "\u518d\u8bd5\u4e00\u6b21", "close": "\u5173\u95ed",
                "treble": "\u9ad8\u97f3\u8c31\u53f7", "bass": "\u4f4e\u97f3\u8c31\u53f7", "clef": "\u8c31\u53f7",
                "quiz": "\u5c0f\u6d4b\u9a8c", "quizEnd": "\u7ed3\u675f\u6d4b\u9a8c", "quizPraise": "\u5168\u90e8\u7b54\u5bf9\uff0c\u592a\u5389\u5bb3\u4e86\uff01", "quizTryLater": "\u6ca1\u5173\u7cfb\uff0c\u4e0b\u6b21\u518d\u8bd5\uff01",
        "notes": ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"],
    },
    "ko": {
        "appName": "\uc544\uae30 \ubba4\uc9c1\ubc15\uc2a4", "start": "\ub20c\ub7ec\uc11c \uc2dc\uc791", "continue": "\ub20c\ub7ec\uc11c \uacc4\uc18d",
        "free": "\uc790\uc720 \uc5f0\uc8fc", "black": "\uac80\uc740 \uac74\ubc18", "staff": "\uc624\uc120\ubcf4", "now": "\uc9c0\uae08 \uc74c",
        "language": "\uc5b8\uc5b4", "high": "\ub192\uc740",
        "twinkle": "\ubc18\uc9dd\ubc18\uc9dd \uc791\uc740 \ubcc4", "mary": "\uba54\ub9ac\uc758 \uc5b4\ub9b0 \uc591",
                "song": "\ub178\ub798", "piano": "\ub0b4 \ud53c\uc544\ub178\ub85c \uce58\uae30", "stop": "\uba48\ucd94\uae30", "listening": "\ub4e3\ub294 \uc911\u2026 \ud53c\uc544\ub178\ub97c \uccd0 \ubcf4\uc138\uc694", "midi": "MIDI \ud53c\uc544\ub178 \uc5f0\uacb0\ub428", "micDenied": "\ub9c8\uc774\ud06c\uac00 \uaebc\uc838 \uc788\uc5b4\uc694 \u2014 \ube0c\ub77c\uc6b0\uc800 \uc124\uc815\uc5d0\uc11c \ud5c8\uc6a9\ud558\uc138\uc694", "great": "\uc798\ud588\uc5b4\uc694!",
                "micTitle": "\ub9c8\uc774\ud06c\ub97c \ud5c8\uc6a9\ud574 \uc8fc\uc138\uc694", "micBody": "\ud53c\uc544\ub178 \uc18c\ub9ac\ub97c \ub4e4\uc73c\ub824\uba74 \ub9c8\uc774\ud06c\uac00 \ud544\uc694\ud574\uc694. \uc18c\ub9ac\ub294 \uc774 \uae30\uae30\uc5d0\uc11c\ub9cc \ubd84\uc11d\ub418\uba70 \ub179\uc74c\ud558\uac70\ub098 \uc5c5\ub85c\ub4dc\ud558\uc9c0 \uc54a\uc544\uc694.", "micAllow": "\ub9c8\uc774\ud06c \ud5c8\uc6a9", "micBlocked": "\ub9c8\uc774\ud06c\uac00 \ucc28\ub2e8\ub418\uc5b4 \uc788\uc5b4\uc694. \uc8fc\uc18c \uc606 \uc790\ubb3c\uc1e0(\U0001f512) \u2192 \ub9c8\uc774\ud06c \u2192 \ud5c8\uc6a9\uc744 \ub204\ub978 \ub4a4 '\ub2e4\uc2dc \uc2dc\ub3c4'\ub97c \ub204\ub974\uc138\uc694.", "retry": "\ub2e4\uc2dc \uc2dc\ub3c4", "close": "\ub2eb\uae30",
                "treble": "\ub192\uc740\uc74c\uc790\ub9ac\ud45c", "bass": "\ub0ae\uc740\uc74c\uc790\ub9ac\ud45c", "clef": "\uc74c\uc790\ub9ac\ud45c",
                "quiz": "\ud034\uc988", "quizEnd": "\ud034\uc988 \ub05d\ub0b4\uae30", "quizPraise": "\ubaa8\ub450 \ub9de\ud614\uc5b4\uc694, \ucd5c\uace0\uc608\uc694!", "quizTryLater": "\uad1c\ucc2e\uc544\uc694, \ub2e4\uc74c\uc5d0 \ub2e4\uc2dc \ud574\uc694!",
        "notes": ["\ub3c4", "\ub808", "\ubbf8", "\ud30c", "\uc194", "\ub77c", "\uc2dc"],
    },
    "ja": {
        "appName": "\u30d9\u30d3\u30fc\u30df\u30e5\u30fc\u30b8\u30c3\u30af\u30dc\u30c3\u30af\u30b9", "start": "\u30bf\u30c3\u30d7\u3057\u3066\u306f\u3058\u3081\u308b", "continue": "\u30bf\u30c3\u30d7\u3057\u3066\u3064\u3065\u3051\u308b",
        "free": "\u3058\u3086\u3046\u306b\u3072\u304f", "black": "\u304f\u308d\u3044\u3051\u3093\u3070\u3093", "staff": "\u3054\u305b\u3093\u3075", "now": "\u3044\u307e\u306e\u304a\u3068",
        "language": "\u3052\u3093\u3054", "high": "\u305f\u304b\u3044",
        "twinkle": "\u304d\u3089\u304d\u3089\u307c\u3057", "mary": "\u30e1\u30ea\u30fc\u3055\u3093\u306e\u3072\u3064\u3058",
                "song": "\u3046\u305f", "piano": "\u3058\u3076\u3093\u306e\u30d4\u30a2\u30ce\u3067\u3072\u304f", "stop": "\u3068\u3081\u308b", "listening": "\u304d\u3044\u3066\u3044\u307e\u3059\u2026 \u30d4\u30a2\u30ce\u3092\u3072\u3044\u3066\u306d", "midi": "MIDI\u30d4\u30a2\u30ce\u306b\u3064\u306a\u304c\u308a\u307e\u3057\u305f", "micDenied": "\u30de\u30a4\u30af\u304c\u30aa\u30d5\u3067\u3059\uff08\u30d6\u30e9\u30a6\u30b6\u306e\u305b\u3063\u3066\u3044\u3067\u304d\u3087\u304b\u3057\u3066\u304f\u3060\u3055\u3044\uff09", "great": "\u3088\u304f\u3067\u304d\u307e\u3057\u305f\uff01",
                "micTitle": "\u30de\u30a4\u30af\u3092\u304d\u3087\u304b\u3057\u3066\u304f\u3060\u3055\u3044", "micBody": "\u30d4\u30a2\u30ce\u306e\u97f3\u3092\u304d\u304f\u305f\u3081\u306b\u30de\u30a4\u30af\u3092\u3064\u304b\u3044\u307e\u3059\u3002\u97f3\u306f\u3053\u306e\u7aef\u672b\u306e\u4e2d\u3060\u3051\u3067\u5206\u6790\u3057\u3001\u9332\u97f3\u3084\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u306f\u3057\u307e\u305b\u3093\u3002", "micAllow": "\u30de\u30a4\u30af\u3092\u304d\u3087\u304b\u3059\u308b", "micBlocked": "\u30de\u30a4\u30af\u304c\u30d6\u30ed\u30c3\u30af\u3055\u308c\u3066\u3044\u307e\u3059\u3002\u30a2\u30c9\u30ec\u30b9\u306e\u6a2a\u306e\u304b\u304e\uff08\U0001f512\uff09\u2192 \u30de\u30a4\u30af \u2192 \u8a31\u53ef \u306b\u3057\u3066\u304b\u3089\u300c\u3082\u3046\u3044\u3061\u3069\u300d\u3092\u304a\u3057\u3066\u304f\u3060\u3055\u3044\u3002", "retry": "\u3082\u3046\u3044\u3061\u3069", "close": "\u3068\u3058\u308b",
                "treble": "\u30c8\u304a\u3093\u304d\u3054\u3046", "bass": "\u30d8\u304a\u3093\u304d\u3054\u3046", "clef": "\u304a\u3093\u304d\u3054\u3046",
                "quiz": "\u30af\u30a4\u30ba", "quizEnd": "\u30af\u30a4\u30ba\u3092\u304a\u308f\u308b", "quizPraise": "\u305c\u3093\u3076\u305b\u3044\u304b\u3044\uff01\u3059\u3054\u3044\u306d\uff01", "quizTryLater": "\u3060\u3044\u3058\u3087\u3046\u3076\u3001\u307e\u305f\u3084\u3063\u3066\u307f\u3088\u3046\uff01",
        "notes": ["\u30c9", "\u30ec", "\u30df", "\u30d5\u30a1", "\u30bd", "\u30e9", "\u30b7"],
    },
    "vi": {
        "appName": "H\u1ed9p Nh\u1ea1c Cho B\u00e9", "start": "Ch\u1ea1m \u0111\u1ec3 ch\u01a1i", "continue": "Ch\u1ea1m \u0111\u1ec3 ti\u1ebfp t\u1ee5c",
        "free": "Ch\u01a1i t\u1ef1 do", "black": "Ph\u00edm \u0111en", "staff": "Khu\u00f4ng nh\u1ea1c", "now": "N\u1ed1t hi\u1ec7n t\u1ea1i",
        "language": "Ng\u00f4n ng\u1eef", "high": "Cao",
        "twinkle": "Ng\u00f4i sao l\u1ea5p l\u00e1nh", "mary": "Mary c\u00f3 m\u1ed9t ch\u00fa c\u1eebu non",
                "song": "B\u00e0i h\u00e1t", "piano": "Ch\u01a1i tr\u00ean \u0111\u00e0n c\u1ee7a b\u00e9", "stop": "D\u1eebng", "listening": "\u0110ang nghe\u2026 h\u00e3y ch\u01a1i \u0111\u00e0n nh\u00e9", "midi": "\u0110\u00e3 k\u1ebft n\u1ed1i \u0111\u00e0n MIDI", "micDenied": "Micr\u00f4 \u0111ang t\u1eaft \u2014 h\u00e3y cho ph\u00e9p trong tr\u00ecnh duy\u1ec7t", "great": "Gi\u1ecfi l\u1eafm!",
                "micTitle": "Cho ph\u00e9p micr\u00f4", "micBody": "\u0110\u1ec3 nghe \u0111\u00e0n c\u1ee7a b\u00e9, \u1ee9ng d\u1ee5ng c\u1ea7n micr\u00f4. \u00c2m thanh ch\u1ec9 \u0111\u01b0\u1ee3c ph\u00e2n t\u00edch tr\u00ean thi\u1ebft b\u1ecb n\u00e0y \u2014 kh\u00f4ng ghi \u00e2m, kh\u00f4ng t\u1ea3i l\u00ean.", "micAllow": "Cho ph\u00e9p micr\u00f4", "micBlocked": "Micr\u00f4 \u0111ang b\u1ecb ch\u1eb7n. Ch\u1ea1m bi\u1ec3u t\u01b0\u1ee3ng \u1ed5 kh\u00f3a (\U0001f512) c\u1ea1nh \u0111\u1ecba ch\u1ec9 web \u2192 Micr\u00f4 \u2192 Cho ph\u00e9p, r\u1ed3i ch\u1ea1m Th\u1eed l\u1ea1i.", "retry": "Th\u1eed l\u1ea1i", "close": "\u0110\u00f3ng",
                "treble": "Kh\u00f3a Sol", "bass": "Kh\u00f3a Fa", "clef": "Kh\u00f3a nh\u1ea1c",
                "quiz": "\u0110\u1ed1 vui", "quizEnd": "K\u1ebft th\u00fac \u0111\u1ed1 vui", "quizPraise": "\u0110\u00fang h\u1ebft r\u1ed3i, gi\u1ecfi qu\u00e1!", "quizTryLater": "Kh\u00f4ng sao, l\u1ea7n sau th\u1eed l\u1ea1i nh\u00e9!",
        "notes": ["\u0110\u00f4", "R\u00ea", "Mi", "Fa", "Son", "La", "Si"],
    },
    "fr": {
        "appName": "Bo\u00eete \u00e0 Musique B\u00e9b\u00e9", "start": "Touche pour jouer", "continue": "Touche pour continuer",
        "free": "Jeu libre", "black": "Touches noires", "staff": "Port\u00e9e", "now": "Note actuelle",
        "language": "Langue", "high": "Aigu",
        "twinkle": "Ah ! vous dirai-je, maman", "mary": "Marie avait un petit agneau",
                "song": "Chanson", "piano": "Jouer sur mon piano", "stop": "Arr\u00eater", "listening": "\u00c0 l'\u00e9coute\u2026 joue sur ton piano", "midi": "Piano MIDI connect\u00e9", "micDenied": "Micro d\u00e9sactiv\u00e9 \u2014 autorise-le dans le navigateur", "great": "Bravo !",
                "micTitle": "Autorise le micro", "micBody": "Pour entendre ton piano, l'appli a besoin du micro. Le son est analys\u00e9 uniquement sur cet appareil : rien n'est enregistr\u00e9 ni envoy\u00e9.", "micAllow": "Autoriser le micro", "micBlocked": "Le micro est bloqu\u00e9. Touche le cadenas (\U0001f512) \u00e0 c\u00f4t\u00e9 de l'adresse \u2192 Micro \u2192 Autoriser, puis touche R\u00e9essayer.", "retry": "R\u00e9essayer", "close": "Fermer",
                "treble": "Cl\u00e9 de sol", "bass": "Cl\u00e9 de fa", "clef": "Cl\u00e9",
                "quiz": "Quiz", "quizEnd": "Terminer le quiz", "quizPraise": "Tout juste, bravo !", "quizTryLater": "Ce n'est pas grave, on r\u00e9essaiera plus tard !",
        "notes": ["Do", "R\u00e9", "Mi", "Fa", "Sol", "La", "Si"],
    },
    "it": {
        "appName": "Carillon per Bimbi", "start": "Tocca per suonare", "continue": "Tocca per continuare",
        "free": "Suona libero", "black": "Tasti neri", "staff": "Pentagramma", "now": "Nota attuale",
        "language": "Lingua", "high": "Acuto",
        "twinkle": "Brilla brilla la stellina", "mary": "Maria aveva un agnellino",
                "song": "Canzone", "piano": "Suona sul mio pianoforte", "stop": "Ferma", "listening": "In ascolto\u2026 suona il tuo pianoforte", "midi": "Pianoforte MIDI collegato", "micDenied": "Microfono disattivato \u2014 consentilo nel browser", "great": "Bravissimo!",
                "micTitle": "Consenti il microfono", "micBody": "Per sentire il tuo pianoforte, l'app ha bisogno del microfono. Il suono viene analizzato solo su questo dispositivo: nulla viene registrato o caricato.", "micAllow": "Consenti microfono", "micBlocked": "Il microfono \u00e8 bloccato. Tocca il lucchetto (\U0001f512) accanto all'indirizzo \u2192 Microfono \u2192 Consenti, poi tocca Riprova.", "retry": "Riprova", "close": "Chiudi",
                "treble": "Chiave di violino", "bass": "Chiave di basso", "clef": "Chiave",
                "quiz": "Quiz", "quizEnd": "Termina il quiz", "quizPraise": "Tutto giusto, fantastico!", "quizTryLater": "Non fa niente, riproviamo pi\u00f9 tardi!",
        "notes": ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"],
    },
    "ru": {
        "appName": "\u041c\u0443\u0437\u044b\u043a\u0430\u043b\u044c\u043d\u0430\u044f \u0448\u043a\u0430\u0442\u0443\u043b\u043a\u0430", "start": "\u041d\u0430\u0436\u043c\u0438, \u0447\u0442\u043e\u0431\u044b \u0438\u0433\u0440\u0430\u0442\u044c", "continue": "\u041d\u0430\u0436\u043c\u0438, \u0447\u0442\u043e\u0431\u044b \u043f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u044c",
        "free": "\u0421\u0432\u043e\u0431\u043e\u0434\u043d\u0430\u044f \u0438\u0433\u0440\u0430", "black": "\u0427\u0451\u0440\u043d\u044b\u0435 \u043a\u043b\u0430\u0432\u0438\u0448\u0438", "staff": "\u041d\u043e\u0442\u043d\u044b\u0439 \u0441\u0442\u0430\u043d", "now": "\u0422\u0435\u043a\u0443\u0449\u0430\u044f \u043d\u043e\u0442\u0430",
        "language": "\u042f\u0437\u044b\u043a", "high": "\u0412\u044b\u0441\u043e\u043a\u0430\u044f",
        "twinkle": "\u0422\u044b \u0441\u0432\u0435\u0442\u0438, \u0437\u0432\u0435\u0437\u0434\u0430 \u043c\u043e\u044f", "mary": "\u0423 \u041c\u044d\u0440\u0438 \u0431\u044b\u043b \u0431\u0430\u0440\u0430\u0448\u0435\u043a",
                "song": "\u041f\u0435\u0441\u043d\u044f", "piano": "\u0418\u0433\u0440\u0430\u0442\u044c \u043d\u0430 \u043c\u043e\u0451\u043c \u043f\u0438\u0430\u043d\u0438\u043d\u043e", "stop": "\u0421\u0442\u043e\u043f", "listening": "\u0421\u043b\u0443\u0448\u0430\u044e\u2026 \u0438\u0433\u0440\u0430\u0439 \u043d\u0430 \u043f\u0438\u0430\u043d\u0438\u043d\u043e", "midi": "MIDI-\u043f\u0438\u0430\u043d\u0438\u043d\u043e \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u043e", "micDenied": "\u041c\u0438\u043a\u0440\u043e\u0444\u043e\u043d \u0432\u044b\u043a\u043b\u044e\u0447\u0435\u043d \u2014 \u0440\u0430\u0437\u0440\u0435\u0448\u0438\u0442\u0435 \u0435\u0433\u043e \u0432 \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u0435", "great": "\u041c\u043e\u043b\u043e\u0434\u0435\u0446!",
                "micTitle": "\u0420\u0430\u0437\u0440\u0435\u0448\u0438\u0442\u0435 \u043c\u0438\u043a\u0440\u043e\u0444\u043e\u043d", "micBody": "\u0427\u0442\u043e\u0431\u044b \u0441\u043b\u044b\u0448\u0430\u0442\u044c \u0432\u0430\u0448\u0435 \u043f\u0438\u0430\u043d\u0438\u043d\u043e, \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044e \u043d\u0443\u0436\u0435\u043d \u043c\u0438\u043a\u0440\u043e\u0444\u043e\u043d. \u0417\u0432\u0443\u043a \u0430\u043d\u0430\u043b\u0438\u0437\u0438\u0440\u0443\u0435\u0442\u0441\u044f \u0442\u043e\u043b\u044c\u043a\u043e \u043d\u0430 \u044d\u0442\u043e\u043c \u0443\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0435 \u2014 \u043d\u0438\u0447\u0435\u0433\u043e \u043d\u0435 \u0437\u0430\u043f\u0438\u0441\u044b\u0432\u0430\u0435\u0442\u0441\u044f \u0438 \u043d\u0435 \u043e\u0442\u043f\u0440\u0430\u0432\u043b\u044f\u0435\u0442\u0441\u044f.", "micAllow": "\u0420\u0430\u0437\u0440\u0435\u0448\u0438\u0442\u044c \u043c\u0438\u043a\u0440\u043e\u0444\u043e\u043d", "micBlocked": "\u041c\u0438\u043a\u0440\u043e\u0444\u043e\u043d \u0437\u0430\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u0430\u043d. \u041d\u0430\u0436\u043c\u0438\u0442\u0435 \u043d\u0430 \u0437\u0430\u043c\u043e\u043a (\U0001f512) \u0440\u044f\u0434\u043e\u043c \u0441 \u0430\u0434\u0440\u0435\u0441\u043e\u043c \u2192 \u041c\u0438\u043a\u0440\u043e\u0444\u043e\u043d \u2192 \u0420\u0430\u0437\u0440\u0435\u0448\u0438\u0442\u044c, \u0437\u0430\u0442\u0435\u043c \u043d\u0430\u0436\u043c\u0438\u0442\u0435 \u00ab\u0415\u0449\u0451 \u0440\u0430\u0437\u00bb.", "retry": "\u0415\u0449\u0451 \u0440\u0430\u0437", "close": "\u0417\u0430\u043a\u0440\u044b\u0442\u044c",
                "treble": "\u0421\u043a\u0440\u0438\u043f\u0438\u0447\u043d\u044b\u0439 \u043a\u043b\u044e\u0447", "bass": "\u0411\u0430\u0441\u043e\u0432\u044b\u0439 \u043a\u043b\u044e\u0447", "clef": "\u041a\u043b\u044e\u0447",
                "quiz": "\u0412\u0438\u043a\u0442\u043e\u0440\u0438\u043d\u0430", "quizEnd": "\u0417\u0430\u043a\u043e\u043d\u0447\u0438\u0442\u044c", "quizPraise": "\u0412\u0441\u0451 \u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e \u2014 \u0437\u0434\u043e\u0440\u043e\u0432\u043e!", "quizTryLater": "\u041d\u0438\u0447\u0435\u0433\u043e \u0441\u0442\u0440\u0430\u0448\u043d\u043e\u0433\u043e, \u043f\u043e\u043f\u0440\u043e\u0431\u0443\u0435\u043c \u043f\u043e\u0437\u0436\u0435!",
        "notes": ["\u0414\u043e", "\u0420\u0435", "\u041c\u0438", "\u0424\u0430", "\u0421\u043e\u043b\u044c", "\u041b\u044f", "\u0421\u0438"],
    },
    "de": {
        "appName": "Baby-Spieluhr", "start": "Tippen zum Spielen", "continue": "Tippen zum Weiterspielen",
        "free": "Freies Spiel", "black": "Schwarze Tasten", "staff": "Notenlinien", "now": "Aktueller Ton",
        "language": "Sprache", "high": "Hohes",
        "twinkle": "Funkel, funkel, kleiner Stern", "mary": "Maria hat ein kleines Lamm",
                "song": "Lied", "piano": "Auf meinem Klavier spielen", "stop": "Stopp", "listening": "Ich h\u00f6re zu\u2026 spiel auf deinem Klavier", "midi": "MIDI-Klavier verbunden", "micDenied": "Mikrofon ist aus \u2013 bitte im Browser erlauben", "great": "Super gemacht!",
                "micTitle": "Mikrofon erlauben", "micBody": "Um dein Klavier zu h\u00f6ren, braucht die App das Mikrofon. Der Ton wird nur auf diesem Ger\u00e4t ausgewertet \u2013 nichts wird aufgenommen oder hochgeladen.", "micAllow": "Mikrofon erlauben", "micBlocked": "Das Mikrofon ist blockiert. Tippe auf das Schloss (\U0001f512) neben der Adresse \u2192 Mikrofon \u2192 Erlauben und dann auf \u201eNochmal\u201c.", "retry": "Nochmal", "close": "Schlie\u00dfen",
                "treble": "Violinschl\u00fcssel", "bass": "Bassschl\u00fcssel", "clef": "Schl\u00fcssel",
                "quiz": "Quiz", "quizEnd": "Quiz beenden", "quizPraise": "Alles richtig \u2013 toll!", "quizTryLater": "Macht nichts \u2013 wir versuchen es sp\u00e4ter nochmal!",
        "notes": ["C", "D", "E", "F", "G", "A", "H"],   # German uses H for B
    },
    "hi": {
        "appName": "\u0936\u093f\u0936\u0941 \u0938\u0902\u0917\u0940\u0924 \u092c\u0949\u0915\u094d\u0938", "start": "\u0916\u0947\u0932\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u091b\u0941\u090f\u0901", "continue": "\u091c\u093e\u0930\u0940 \u0930\u0916\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u091b\u0941\u090f\u0901",
        "free": "\u092e\u0941\u0915\u094d\u0924 \u0935\u093e\u0926\u0928", "black": "\u0915\u093e\u0932\u0940 \u0915\u0941\u0902\u091c\u093f\u092f\u093e\u0901", "staff": "\u0938\u094d\u0935\u0930\u0932\u093f\u092a\u093f", "now": "\u0935\u0930\u094d\u0924\u092e\u093e\u0928 \u0938\u094d\u0935\u0930",
        "language": "\u092d\u093e\u0937\u093e", "high": "\u0924\u093e\u0930",
        "twinkle": "\u091a\u092e\u0915 \u091a\u092e\u0915 \u091b\u094b\u091f\u093e \u0924\u093e\u0930\u093e", "mary": "\u092e\u0948\u0930\u0940 \u0915\u093e \u091b\u094b\u091f\u093e \u092e\u0947\u092e\u0928\u093e",
                "song": "\u0917\u0940\u0924", "piano": "\u092e\u0947\u0930\u0947 \u092a\u093f\u092f\u093e\u0928\u094b \u092a\u0930 \u092c\u091c\u093e\u090f\u0901", "stop": "\u0930\u094b\u0915\u0947\u0902", "listening": "\u0938\u0941\u0928 \u0930\u0939\u0947 \u0939\u0948\u0902\u2026 \u0905\u092a\u0928\u093e \u092a\u093f\u092f\u093e\u0928\u094b \u092c\u091c\u093e\u090f\u0901", "midi": "MIDI \u092a\u093f\u092f\u093e\u0928\u094b \u091c\u0941\u0921\u093c\u093e \u0939\u0948", "micDenied": "\u092e\u093e\u0907\u0915\u094d\u0930\u094b\u092b\u093c\u094b\u0928 \u092c\u0902\u0926 \u0939\u0948 \u2014 \u092c\u094d\u0930\u093e\u0909\u091c\u093c\u0930 \u092e\u0947\u0902 \u0905\u0928\u0941\u092e\u0924\u093f \u0926\u0947\u0902", "great": "\u092c\u0939\u0941\u0924 \u092c\u0922\u093c\u093f\u092f\u093e!",
                "micTitle": "\u092e\u093e\u0907\u0915\u094d\u0930\u094b\u092b\u093c\u094b\u0928 \u0915\u0940 \u0905\u0928\u0941\u092e\u0924\u093f \u0926\u0947\u0902", "micBody": "\u0906\u092a\u0915\u093e \u092a\u093f\u092f\u093e\u0928\u094b \u0938\u0941\u0928\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0910\u092a \u0915\u094b \u092e\u093e\u0907\u0915\u094d\u0930\u094b\u092b\u093c\u094b\u0928 \u091a\u093e\u0939\u093f\u090f\u0964 \u0906\u0935\u093e\u091c\u093c \u0915\u0947\u0935\u0932 \u0907\u0938\u0940 \u0921\u093f\u0935\u093e\u0907\u0938 \u092a\u0930 \u091c\u093e\u0901\u091a\u0940 \u091c\u093e\u0924\u0940 \u0939\u0948 \u2014 \u0915\u0941\u091b \u092d\u0940 \u0930\u093f\u0915\u0949\u0930\u094d\u0921 \u092f\u093e \u0905\u092a\u0932\u094b\u0921 \u0928\u0939\u0940\u0902 \u0939\u094b\u0924\u093e\u0964", "micAllow": "\u092e\u093e\u0907\u0915\u094d\u0930\u094b\u092b\u093c\u094b\u0928 \u0915\u0940 \u0905\u0928\u0941\u092e\u0924\u093f \u0926\u0947\u0902", "micBlocked": "\u092e\u093e\u0907\u0915\u094d\u0930\u094b\u092b\u093c\u094b\u0928 \u092c\u094d\u0932\u0949\u0915 \u0939\u0948\u0964 \u0935\u0947\u092c \u092a\u0924\u0947 \u0915\u0947 \u092a\u093e\u0938 \u0924\u093e\u0932\u0947 (\U0001f512) \u092a\u0930 \u091f\u0948\u092a \u0915\u0930\u0947\u0902 \u2192 \u092e\u093e\u0907\u0915\u094d\u0930\u094b\u092b\u093c\u094b\u0928 \u2192 \u0905\u0928\u0941\u092e\u0924\u093f \u0926\u0947\u0902, \u092b\u093f\u0930 '\u092b\u093f\u0930 \u0938\u0947 \u0915\u094b\u0936\u093f\u0936 \u0915\u0930\u0947\u0902' \u0926\u092c\u093e\u090f\u0901\u0964", "retry": "\u092b\u093f\u0930 \u0938\u0947 \u0915\u094b\u0936\u093f\u0936 \u0915\u0930\u0947\u0902", "close": "\u092c\u0902\u0926 \u0915\u0930\u0947\u0902",
                "treble": "\u091f\u094d\u0930\u0947\u092c\u0932 \u0915\u094d\u0932\u0947\u092b\u093c", "bass": "\u092c\u0947\u0938 \u0915\u094d\u0932\u0947\u092b\u093c", "clef": "\u0915\u094d\u0932\u0947\u092b\u093c",
                "quiz": "\u092a\u094d\u0930\u0936\u094d\u0928\u094b\u0924\u094d\u0924\u0930\u0940", "quizEnd": "\u092a\u094d\u0930\u0936\u094d\u0928\u094b\u0924\u094d\u0924\u0930\u0940 \u0938\u092e\u093e\u092a\u094d\u0924 \u0915\u0930\u0947\u0902", "quizPraise": "\u0938\u092c \u0938\u0939\u0940 \u2014 \u0936\u093e\u0928\u0926\u093e\u0930!", "quizTryLater": "\u0915\u094b\u0908 \u092c\u093e\u0924 \u0928\u0939\u0940\u0902, \u092c\u093e\u0926 \u092e\u0947\u0902 \u092b\u093f\u0930 \u0915\u094b\u0936\u093f\u0936 \u0915\u0930\u0947\u0902\u0917\u0947!",
        "notes": ["\u0938\u093e", "\u0930\u0947", "\u0917", "\u092e", "\u092a", "\u0927", "\u0928\u093f"],   # Indian sargam syllables
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
