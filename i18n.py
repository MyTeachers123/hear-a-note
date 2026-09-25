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
        "appName": "Hear-a-Note for Toddlers",
        "iosTip": "iPad / iPhone: tap Share \u2192 \u201cAdd to Home Screen\u201d to open the app without the browser bar, and turn on Guided Access to lock it.",
        "free": "Pick A Song", "exit": "Exit full screen", "fullscreen": "Full screen", "black": "Black keys", "staff": "Staff", "now": "Current note",
        "language": "Language", "menu": "Menu \u2014 double-tap to open", "high": "High",
        "twinkle": "Twinkle Twinkle Little Star", "mary": "Mary Had a Little Lamb", "ode": "Ode to Joy", "jingle": "Jingle Bells", "play": "Listen", "stop": "Stop",
                "song": "Song", "mode": "Play mode", "modeScreen": "No piano", "modePiano": "Play a real piano", "listening": "Listening\u2026 play on your piano", "micDenied": "Microphone is off \u2014 allow it in browser settings",
                "micTitle": "Allow the microphone", "micBlocked": "The microphone is blocked. Tap the lock icon next to the web address \u2192 Microphone \u2192 Allow, then tap Try again.", "retry": "Try again", "close": "Close",
                "treble": "Treble clef", "bass": "Bass clef", "clef": "Clef",
                "quiz": "Challenge", "quizEnd": "End challenge",
        "notes": ["C", "D", "E", "F", "G", "A", "B"],
    },
    "es": {
        "appName": "Hear-a-Note for Toddlers",
        "iosTip": "iPad / iPhone: toca Compartir \u2192 \u00abA\u00f1adir a pantalla de inicio\u00bb para abrirla sin la barra del navegador, y activa Acceso guiado para bloquearla.",
        "free": "Elige una canci\u00f3n", "exit": "Salir de pantalla completa", "fullscreen": "Pantalla completa", "black": "Teclas negras", "staff": "Pentagrama", "now": "Nota actual",
        "language": "Idioma", "menu": "Men\u00fa: toca dos veces para abrir", "high": "Agudo",
        "twinkle": "Estrellita, \u00bfd\u00f3nde est\u00e1s?", "mary": "Mar\u00eda ten\u00eda un corderito", "ode": "Himno de la alegr\u00eda", "jingle": "Cascabel", "play": "Escuchar", "stop": "Parar",
                "song": "Canci\u00f3n", "mode": "Modo de juego", "modeScreen": "Sin piano", "modePiano": "Tocar un piano de verdad", "listening": "Escuchando\u2026 toca tu piano", "micDenied": "Micr\u00f3fono desactivado \u2014 act\u00edvalo en el navegador",
                "micTitle": "Permite el micr\u00f3fono", "micBlocked": "El micr\u00f3fono est\u00e1 bloqueado. Toca el candado junto a la direcci\u00f3n web \u2192 Micr\u00f3fono \u2192 Permitir, y luego toca Reintentar.", "retry": "Reintentar", "close": "Cerrar",
                "treble": "Clave de sol", "bass": "Clave de fa", "clef": "Clave",
                "quiz": "Desaf\u00edo", "quizEnd": "Terminar desaf\u00edo",
        "notes": ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"],
    },
    "zh-Hant": {
        "appName": "\u807d\u97f3\u5bf6",
        "iosTip": "iPad\uff0fiPhone\uff1a\u9ede\u300c\u5206\u4eab\u300d\u2192\u300c\u52a0\u5165\u4e3b\u756b\u9762\u300d\uff0c\u5f9e\u4e3b\u756b\u9762\u6253\u958b\u5c31\u6c92\u6709\u700f\u89bd\u5668\u5217\uff1b\u958b\u555f\u300c\u5f15\u5c0e\u4f7f\u7528\u6a21\u5f0f\u300d\u53ef\u9396\u5b9a App\u3002",
        "free": "\u9078\u4e00\u9996\u6b4c", "exit": "\u9000\u51fa\u5168\u5c4f", "fullscreen": "\u5168\u5c4f", "black": "\u9ed1\u9375", "staff": "\u4e94\u7dda\u8b5c", "now": "\u7576\u524d\u97f3",
        "language": "\u8a9e\u8a00", "menu": "\u9078\u55ae\uff08\u9ede\u5169\u4e0b\u6253\u958b\uff09", "high": "\u9ad8\u97f3",
        "twinkle": "\u5c0f\u661f\u661f", "mary": "\u746a\u8389\u6709\u96bb\u5c0f\u7dbf\u7f8a", "ode": "\u6b61\u6a02\u980c", "jingle": "\u9234\u5152\u97ff\u53ee\u5679", "play": "\u64ad\u653e", "stop": "\u505c\u6b62",
                "song": "\u6b4c\u66f2", "mode": "\u5f48\u594f\u65b9\u5f0f", "modeScreen": "\u4e0d\u4f7f\u7528\u92fc\u7434", "modePiano": "\u771f\u5be6\u92fc\u7434\u5f48\u594f", "listening": "\u8046\u807d\u4e2d\u2026\u8acb\u5f48\u4f60\u7684\u92fc\u7434", "micDenied": "\u9ea5\u514b\u98a8\u672a\u958b\u555f\uff0c\u8acb\u5728\u700f\u89bd\u5668\u8a2d\u5b9a\u4e2d\u5141\u8a31",
                "micTitle": "\u8acb\u5141\u8a31\u4f7f\u7528\u9ea5\u514b\u98a8", "micBlocked": "\u9ea5\u514b\u98a8\u88ab\u5c01\u9396\u4e86\u3002\u8acb\u9ede\u7db2\u5740\u65c1\u7684\u9396\u982d \u2192 \u9ea5\u514b\u98a8 \u2192 \u5141\u8a31\uff0c\u518d\u6309\u300c\u518d\u8a66\u4e00\u6b21\u300d\u3002", "retry": "\u518d\u8a66\u4e00\u6b21", "close": "\u95dc\u9589",
                "treble": "\u9ad8\u97f3\u8b5c\u865f", "bass": "\u4f4e\u97f3\u8b5c\u865f", "clef": "\u8b5c\u865f",
                "quiz": "\u6311\u6230", "quizEnd": "\u7d50\u675f\u6311\u6230",
        "notes": ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"],
    },
    "zh-Hans": {
        "appName": "\u542c\u97f3\u5b9d",
        "iosTip": "iPad\uff0fiPhone\uff1a\u70b9\u201c\u5206\u4eab\u201d\u2192\u201c\u6dfb\u52a0\u5230\u4e3b\u5c4f\u5e55\u201d\uff0c\u4ece\u4e3b\u5c4f\u5e55\u6253\u5f00\u5c31\u6ca1\u6709\u6d4f\u89c8\u5668\u680f\uff1b\u5f00\u542f\u201c\u5f15\u5bfc\u5f0f\u8bbf\u95ee\u201d\u53ef\u9501\u5b9a App\u3002",
        "free": "\u9009\u4e00\u9996\u6b4c", "exit": "\u9000\u51fa\u5168\u5c4f", "fullscreen": "\u5168\u5c4f", "black": "\u9ed1\u952e", "staff": "\u4e94\u7ebf\u8c31", "now": "\u5f53\u524d\u97f3",
        "language": "\u8bed\u8a00", "menu": "\u83dc\u5355\uff08\u70b9\u4e24\u4e0b\u6253\u5f00\uff09", "high": "\u9ad8\u97f3",
        "twinkle": "\u5c0f\u661f\u661f", "mary": "\u739b\u4e3d\u6709\u53ea\u5c0f\u7ef5\u7f8a", "ode": "\u6b22\u4e50\u9882", "jingle": "\u94c3\u513f\u54cd\u53ee\u5f53", "play": "\u64ad\u653e", "stop": "\u505c\u6b62",
                "song": "\u6b4c\u66f2", "mode": "\u5f39\u594f\u65b9\u5f0f", "modeScreen": "\u4e0d\u4f7f\u7528\u94a2\u7434", "modePiano": "\u771f\u5b9e\u94a2\u7434\u5f39\u594f", "listening": "\u8046\u542c\u4e2d\u2026\u8bf7\u5f39\u4f60\u7684\u94a2\u7434", "micDenied": "\u9ea6\u514b\u98ce\u672a\u5f00\u542f\uff0c\u8bf7\u5728\u6d4f\u89c8\u5668\u8bbe\u7f6e\u4e2d\u5141\u8bb8",
                "micTitle": "\u8bf7\u5141\u8bb8\u4f7f\u7528\u9ea6\u514b\u98ce", "micBlocked": "\u9ea6\u514b\u98ce\u88ab\u963b\u6b62\u4e86\u3002\u8bf7\u70b9\u7f51\u5740\u65c1\u7684\u9501\u5934 \u2192 \u9ea6\u514b\u98ce \u2192 \u5141\u8bb8\uff0c\u518d\u6309\u201c\u518d\u8bd5\u4e00\u6b21\u201d\u3002", "retry": "\u518d\u8bd5\u4e00\u6b21", "close": "\u5173\u95ed",
                "treble": "\u9ad8\u97f3\u8c31\u53f7", "bass": "\u4f4e\u97f3\u8c31\u53f7", "clef": "\u8c31\u53f7",
                "quiz": "\u6311\u6218", "quizEnd": "\u7ed3\u675f\u6311\u6218",
        "notes": ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"],
    },
    "ko": {
        "appName": "Hear-a-Note for Toddlers",
        "iosTip": "iPad / iPhone: \uacf5\uc720 \u2192 \u2018\ud648 \ud654\uba74\uc5d0 \ucd94\uac00\u2019\ub97c \ub204\ub974\uba74 \ube0c\ub77c\uc6b0\uc800 \ub9c9\ub300 \uc5c6\uc774 \uc5f4\ub824\uc694. \u2018\uc0ac\uc6a9\ubc95 \uc720\ub3c4 \uc811\uadfc\u2019\uc744 \ucf1c\uba74 \uc571\uc774 \uc7a0\uaca8\uc694.",
        "free": "\ub178\ub798 \uace0\ub974\uae30", "exit": "\uc804\uccb4 \ud654\uba74 \ub044\uae30", "fullscreen": "\uc804\uccb4 \ud654\uba74", "black": "\uac80\uc740 \uac74\ubc18", "staff": "\uc624\uc120\ubcf4", "now": "\uc9c0\uae08 \uc74c",
        "language": "\uc5b8\uc5b4", "menu": "\uba54\ub274 (\ub450 \ubc88 \ud0ed\ud558\uc5ec \uc5f4\uae30)", "high": "\ub192\uc740",
        "twinkle": "\ubc18\uc9dd\ubc18\uc9dd \uc791\uc740 \ubcc4", "mary": "\uba54\ub9ac\uc758 \uc5b4\ub9b0 \uc591", "ode": "\ud658\ud76c\uc758 \uc1a1\uac00", "jingle": "\uc9d5\uae00\ubca8", "play": "\ub4e3\uae30", "stop": "\uc815\uc9c0",
                "song": "\ub178\ub798", "mode": "\uc5f0\uc8fc \ubc29\ubc95", "modeScreen": "\ud53c\uc544\ub178 \uc5c6\uc774", "modePiano": "\uc9c4\uc9dc \ud53c\uc544\ub178\ub85c \uc5f0\uc8fc", "listening": "\ub4e3\ub294 \uc911\u2026 \ud53c\uc544\ub178\ub97c \uccd0 \ubcf4\uc138\uc694", "micDenied": "\ub9c8\uc774\ud06c\uac00 \uaebc\uc838 \uc788\uc5b4\uc694 \u2014 \ube0c\ub77c\uc6b0\uc800 \uc124\uc815\uc5d0\uc11c \ud5c8\uc6a9\ud558\uc138\uc694",
                "micTitle": "\ub9c8\uc774\ud06c\ub97c \ud5c8\uc6a9\ud574 \uc8fc\uc138\uc694", "micBlocked": "\ub9c8\uc774\ud06c\uac00 \ucc28\ub2e8\ub418\uc5b4 \uc788\uc5b4\uc694. \uc8fc\uc18c \uc606 \uc790\ubb3c\uc1e0 \u2192 \ub9c8\uc774\ud06c \u2192 \ud5c8\uc6a9\uc744 \ub204\ub978 \ub4a4 '\ub2e4\uc2dc \uc2dc\ub3c4'\ub97c \ub204\ub974\uc138\uc694.", "retry": "\ub2e4\uc2dc \uc2dc\ub3c4", "close": "\ub2eb\uae30",
                "treble": "\ub192\uc740\uc74c\uc790\ub9ac\ud45c", "bass": "\ub0ae\uc740\uc74c\uc790\ub9ac\ud45c", "clef": "\uc74c\uc790\ub9ac\ud45c",
                "quiz": "\ub3c4\uc804", "quizEnd": "\ub3c4\uc804 \ub05d\ub0b4\uae30",
        "notes": ["\ub3c4", "\ub808", "\ubbf8", "\ud30c", "\uc194", "\ub77c", "\uc2dc"],
    },
    "ja": {
        "appName": "Hear-a-Note for Toddlers",
        "iosTip": "iPad / iPhone\uff1a\u5171\u6709 \u2192\u300c\u30db\u30fc\u30e0\u753b\u9762\u306b\u8ffd\u52a0\u300d\u3067\u3001\u30d6\u30e9\u30a6\u30b6\u306e\u30d0\u30fc\u306a\u3057\u3067\u958b\u3051\u307e\u3059\u3002\u300c\u30a2\u30af\u30bb\u30b9\u30ac\u30a4\u30c9\u300d\u3092\u30aa\u30f3\u306b\u3059\u308b\u3068\u30a2\u30d7\u30ea\u3092\u56fa\u5b9a\u3067\u304d\u307e\u3059\u3002",
        "free": "\u3046\u305f\u3092\u3048\u3089\u3076", "exit": "\u305c\u3093\u304c\u3081\u3093\u3092\u3084\u3081\u308b", "fullscreen": "\u305c\u3093\u304c\u3081\u3093", "black": "\u304f\u308d\u3044\u3051\u3093\u3070\u3093", "staff": "\u3054\u305b\u3093\u3075", "now": "\u3044\u307e\u306e\u304a\u3068",
        "language": "\u3052\u3093\u3054", "menu": "\u30e1\u30cb\u30e5\u30fc\uff082\u304b\u3044\u30bf\u30c3\u30d7\u3067\u3072\u3089\u304f\uff09", "high": "\u305f\u304b\u3044",
        "twinkle": "\u304d\u3089\u304d\u3089\u307c\u3057", "mary": "\u30e1\u30ea\u30fc\u3055\u3093\u306e\u3072\u3064\u3058", "ode": "\u3088\u308d\u3053\u3073\u306e\u3046\u305f", "jingle": "\u30b8\u30f3\u30b0\u30eb\u30d9\u30eb", "play": "\u304d\u304f", "stop": "\u3068\u3081\u308b",
                "song": "\u3046\u305f", "mode": "\u3072\u304d\u304b\u305f", "modeScreen": "\u30d4\u30a2\u30ce\u3092\u3064\u304b\u308f\u306a\u3044", "modePiano": "\u307b\u3093\u3082\u306e\u306e\u30d4\u30a2\u30ce\u3067\u3072\u304f", "listening": "\u304d\u3044\u3066\u3044\u307e\u3059\u2026 \u30d4\u30a2\u30ce\u3092\u3072\u3044\u3066\u306d", "micDenied": "\u30de\u30a4\u30af\u304c\u30aa\u30d5\u3067\u3059\uff08\u30d6\u30e9\u30a6\u30b6\u306e\u305b\u3063\u3066\u3044\u3067\u304d\u3087\u304b\u3057\u3066\u304f\u3060\u3055\u3044\uff09",
                "micTitle": "\u30de\u30a4\u30af\u3092\u304d\u3087\u304b\u3057\u3066\u304f\u3060\u3055\u3044", "micBlocked": "\u30de\u30a4\u30af\u304c\u30d6\u30ed\u30c3\u30af\u3055\u308c\u3066\u3044\u307e\u3059\u3002\u30a2\u30c9\u30ec\u30b9\u306e\u6a2a\u306e\u304b\u304e \u2192 \u30de\u30a4\u30af \u2192 \u8a31\u53ef \u306b\u3057\u3066\u304b\u3089\u300c\u3082\u3046\u3044\u3061\u3069\u300d\u3092\u304a\u3057\u3066\u304f\u3060\u3055\u3044\u3002", "retry": "\u3082\u3046\u3044\u3061\u3069", "close": "\u3068\u3058\u308b",
                "treble": "\u30c8\u304a\u3093\u304d\u3054\u3046", "bass": "\u30d8\u304a\u3093\u304d\u3054\u3046", "clef": "\u304a\u3093\u304d\u3054\u3046",
                "quiz": "\u3061\u3087\u3046\u305b\u3093", "quizEnd": "\u3061\u3087\u3046\u305b\u3093\u3092\u304a\u308f\u308b",
        "notes": ["\u30c9", "\u30ec", "\u30df", "\u30d5\u30a1", "\u30bd", "\u30e9", "\u30b7"],
    },
    "vi": {
        "appName": "Hear-a-Note for Toddlers",
        "iosTip": "iPad / iPhone: ch\u1ea1m Chia s\u1ebb \u2192 \u201cTh\u00eam v\u00e0o MH ch\u00ednh\u201d \u0111\u1ec3 m\u1edf kh\u00f4ng c\u00f3 thanh tr\u00ecnh duy\u1ec7t; b\u1eadt Truy c\u1eadp \u0111\u01b0\u1ee3c h\u01b0\u1edbng d\u1eabn \u0111\u1ec3 kh\u00f3a \u1ee9ng d\u1ee5ng.",
        "free": "Ch\u1ecdn b\u00e0i h\u00e1t", "exit": "Tho\u00e1t to\u00e0n m\u00e0n h\u00ecnh", "fullscreen": "To\u00e0n m\u00e0n h\u00ecnh", "black": "Ph\u00edm \u0111en", "staff": "Khu\u00f4ng nh\u1ea1c", "now": "N\u1ed1t hi\u1ec7n t\u1ea1i",
        "language": "Ng\u00f4n ng\u1eef", "menu": "Menu \u2013 ch\u1ea1m hai l\u1ea7n \u0111\u1ec3 m\u1edf", "high": "Cao",
        "twinkle": "Ng\u00f4i sao l\u1ea5p l\u00e1nh", "mary": "Mary c\u00f3 m\u1ed9t ch\u00fa c\u1eebu non", "ode": "Kh\u00fac hoan ca", "jingle": "Jingle Bells", "play": "Nghe", "stop": "D\u1eebng",
                "song": "B\u00e0i h\u00e1t", "mode": "C\u00e1ch ch\u01a1i", "modeScreen": "Kh\u00f4ng d\u00f9ng \u0111\u00e0n piano", "modePiano": "Ch\u01a1i \u0111\u00e0n piano th\u1eadt", "listening": "\u0110ang nghe\u2026 h\u00e3y ch\u01a1i \u0111\u00e0n nh\u00e9", "micDenied": "Micr\u00f4 \u0111ang t\u1eaft \u2014 h\u00e3y cho ph\u00e9p trong tr\u00ecnh duy\u1ec7t",
                "micTitle": "Cho ph\u00e9p micr\u00f4", "micBlocked": "Micr\u00f4 \u0111ang b\u1ecb ch\u1eb7n. Ch\u1ea1m bi\u1ec3u t\u01b0\u1ee3ng \u1ed5 kh\u00f3a c\u1ea1nh \u0111\u1ecba ch\u1ec9 web \u2192 Micr\u00f4 \u2192 Cho ph\u00e9p, r\u1ed3i ch\u1ea1m Th\u1eed l\u1ea1i.", "retry": "Th\u1eed l\u1ea1i", "close": "\u0110\u00f3ng",
                "treble": "Kh\u00f3a Sol", "bass": "Kh\u00f3a Fa", "clef": "Kh\u00f3a nh\u1ea1c",
                "quiz": "Th\u1eed th\u00e1ch", "quizEnd": "K\u1ebft th\u00fac th\u1eed th\u00e1ch",
        "notes": ["\u0110\u00f4", "R\u00ea", "Mi", "Fa", "Son", "La", "Si"],
    },
    "fr": {
        "appName": "Hear-a-Note for Toddlers",
        "iosTip": "iPad / iPhone : touchez Partager \u2192 \u00ab Sur l\u2019\u00e9cran d\u2019accueil \u00bb pour l\u2019ouvrir sans la barre du navigateur, et activez l\u2019Acc\u00e8s guid\u00e9 pour la verrouiller.",
        "free": "Choisis une chanson", "exit": "Quitter le plein \u00e9cran", "fullscreen": "Plein \u00e9cran", "black": "Touches noires", "staff": "Port\u00e9e", "now": "Note actuelle",
        "language": "Langue", "menu": "Menu \u2013 touchez deux fois pour ouvrir", "high": "Aigu",
        "twinkle": "Ah ! vous dirai-je, maman", "mary": "Marie avait un petit agneau", "ode": "L'Hymne \u00e0 la joie", "jingle": "Vive le vent", "play": "\u00c9couter", "stop": "Arr\u00eater",
                "song": "Chanson", "mode": "Mode de jeu", "modeScreen": "Sans piano", "modePiano": "Jouer sur un vrai piano", "listening": "\u00c0 l'\u00e9coute\u2026 joue sur ton piano", "micDenied": "Micro d\u00e9sactiv\u00e9 \u2014 autorise-le dans le navigateur",
                "micTitle": "Autorise le micro", "micBlocked": "Le micro est bloqu\u00e9. Touche le cadenas \u00e0 c\u00f4t\u00e9 de l'adresse \u2192 Micro \u2192 Autoriser, puis touche R\u00e9essayer.", "retry": "R\u00e9essayer", "close": "Fermer",
                "treble": "Cl\u00e9 de sol", "bass": "Cl\u00e9 de fa", "clef": "Cl\u00e9",
                "quiz": "D\u00e9fi", "quizEnd": "Terminer le d\u00e9fi",
        "notes": ["Do", "R\u00e9", "Mi", "Fa", "Sol", "La", "Si"],
    },
    "it": {
        "appName": "Hear-a-Note for Toddlers",
        "iosTip": "iPad / iPhone: tocca Condividi \u2192 \u00abAggiungi alla schermata Home\u00bb per aprirla senza la barra del browser, e attiva Accesso guidato per bloccarla.",
        "free": "Scegli una canzone", "exit": "Esci da schermo intero", "fullscreen": "Schermo intero", "black": "Tasti neri", "staff": "Pentagramma", "now": "Nota attuale",
        "language": "Lingua", "menu": "Menu \u2013 tocca due volte per aprire", "high": "Acuto",
        "twinkle": "Brilla brilla la stellina", "mary": "Maria aveva un agnellino", "ode": "Inno alla gioia", "jingle": "Jingle Bells", "play": "Ascolta", "stop": "Ferma",
                "song": "Canzone", "mode": "Modalit\u00e0", "modeScreen": "Senza pianoforte", "modePiano": "Suona un pianoforte vero", "listening": "In ascolto\u2026 suona il tuo pianoforte", "micDenied": "Microfono disattivato \u2014 consentilo nel browser",
                "micTitle": "Consenti il microfono", "micBlocked": "Il microfono \u00e8 bloccato. Tocca il lucchetto accanto all'indirizzo \u2192 Microfono \u2192 Consenti, poi tocca Riprova.", "retry": "Riprova", "close": "Chiudi",
                "treble": "Chiave di violino", "bass": "Chiave di basso", "clef": "Chiave",
                "quiz": "Sfida", "quizEnd": "Termina la sfida",
        "notes": ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"],
    },
    "ru": {
        "appName": "Hear-a-Note for Toddlers",
        "iosTip": "iPad / iPhone: \u00ab\u041f\u043e\u0434\u0435\u043b\u0438\u0442\u044c\u0441\u044f\u00bb \u2192 \u00ab\u041d\u0430 \u044d\u043a\u0440\u0430\u043d \u201e\u0414\u043e\u043c\u043e\u0439\u201c\u00bb \u2014 \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435 \u043e\u0442\u043a\u0440\u043e\u0435\u0442\u0441\u044f \u0431\u0435\u0437 \u043f\u0430\u043d\u0435\u043b\u0438 \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u0430; \u00ab\u0413\u0438\u0434-\u0434\u043e\u0441\u0442\u0443\u043f\u00bb \u043d\u0435 \u0434\u0430\u0441\u0442 \u0438\u0437 \u043d\u0435\u0433\u043e \u0432\u044b\u0439\u0442\u0438.",
        "free": "\u0412\u044b\u0431\u0435\u0440\u0438 \u043f\u0435\u0441\u043d\u044e", "exit": "\u0412\u044b\u0439\u0442\u0438 \u0438\u0437 \u043f\u043e\u043b\u043d\u043e\u0433\u043e \u044d\u043a\u0440\u0430\u043d\u0430", "fullscreen": "\u0412\u043e \u0432\u0435\u0441\u044c \u044d\u043a\u0440\u0430\u043d", "black": "\u0427\u0451\u0440\u043d\u044b\u0435 \u043a\u043b\u0430\u0432\u0438\u0448\u0438", "staff": "\u041d\u043e\u0442\u043d\u044b\u0439 \u0441\u0442\u0430\u043d", "now": "\u0422\u0435\u043a\u0443\u0449\u0430\u044f \u043d\u043e\u0442\u0430",
        "language": "\u042f\u0437\u044b\u043a", "menu": "\u041c\u0435\u043d\u044e \u2014 \u043d\u0430\u0436\u043c\u0438\u0442\u0435 \u0434\u0432\u0430\u0436\u0434\u044b, \u0447\u0442\u043e\u0431\u044b \u043e\u0442\u043a\u0440\u044b\u0442\u044c", "high": "\u0412\u044b\u0441\u043e\u043a\u0430\u044f",
        "twinkle": "\u0422\u044b \u0441\u0432\u0435\u0442\u0438, \u0437\u0432\u0435\u0437\u0434\u0430 \u043c\u043e\u044f", "mary": "\u0423 \u041c\u044d\u0440\u0438 \u0431\u044b\u043b \u0431\u0430\u0440\u0430\u0448\u0435\u043a", "ode": "\u041e\u0434\u0430 \u043a \u0440\u0430\u0434\u043e\u0441\u0442\u0438", "jingle": "\u0411\u0443\u0431\u0435\u043d\u0447\u0438\u043a\u0438", "play": "\u0421\u043b\u0443\u0448\u0430\u0442\u044c", "stop": "\u0421\u0442\u043e\u043f",
                "song": "\u041f\u0435\u0441\u043d\u044f", "mode": "\u041a\u0430\u043a \u0438\u0433\u0440\u0430\u0442\u044c", "modeScreen": "\u0411\u0435\u0437 \u043f\u0438\u0430\u043d\u0438\u043d\u043e", "modePiano": "\u0418\u0433\u0440\u0430\u0442\u044c \u043d\u0430 \u043d\u0430\u0441\u0442\u043e\u044f\u0449\u0435\u043c \u043f\u0438\u0430\u043d\u0438\u043d\u043e", "listening": "\u0421\u043b\u0443\u0448\u0430\u044e\u2026 \u0438\u0433\u0440\u0430\u0439 \u043d\u0430 \u043f\u0438\u0430\u043d\u0438\u043d\u043e", "micDenied": "\u041c\u0438\u043a\u0440\u043e\u0444\u043e\u043d \u0432\u044b\u043a\u043b\u044e\u0447\u0435\u043d \u2014 \u0440\u0430\u0437\u0440\u0435\u0448\u0438\u0442\u0435 \u0435\u0433\u043e \u0432 \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u0435",
                "micTitle": "\u0420\u0430\u0437\u0440\u0435\u0448\u0438\u0442\u0435 \u043c\u0438\u043a\u0440\u043e\u0444\u043e\u043d", "micBlocked": "\u041c\u0438\u043a\u0440\u043e\u0444\u043e\u043d \u0437\u0430\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u0430\u043d. \u041d\u0430\u0436\u043c\u0438\u0442\u0435 \u043d\u0430 \u0437\u0430\u043c\u043e\u043a \u0440\u044f\u0434\u043e\u043c \u0441 \u0430\u0434\u0440\u0435\u0441\u043e\u043c \u2192 \u041c\u0438\u043a\u0440\u043e\u0444\u043e\u043d \u2192 \u0420\u0430\u0437\u0440\u0435\u0448\u0438\u0442\u044c, \u0437\u0430\u0442\u0435\u043c \u043d\u0430\u0436\u043c\u0438\u0442\u0435 \u00ab\u0415\u0449\u0451 \u0440\u0430\u0437\u00bb.", "retry": "\u0415\u0449\u0451 \u0440\u0430\u0437", "close": "\u0417\u0430\u043a\u0440\u044b\u0442\u044c",
                "treble": "\u0421\u043a\u0440\u0438\u043f\u0438\u0447\u043d\u044b\u0439 \u043a\u043b\u044e\u0447", "bass": "\u0411\u0430\u0441\u043e\u0432\u044b\u0439 \u043a\u043b\u044e\u0447", "clef": "\u041a\u043b\u044e\u0447",
                "quiz": "\u0418\u0441\u043f\u044b\u0442\u0430\u043d\u0438\u0435", "quizEnd": "\u0417\u0430\u043a\u043e\u043d\u0447\u0438\u0442\u044c \u0438\u0441\u043f\u044b\u0442\u0430\u043d\u0438\u0435",
        "notes": ["\u0414\u043e", "\u0420\u0435", "\u041c\u0438", "\u0424\u0430", "\u0421\u043e\u043b\u044c", "\u041b\u044f", "\u0421\u0438"],
    },
    "de": {
        "appName": "Hear-a-Note for Toddlers",
        "iosTip": "iPad / iPhone: Teilen \u2192 \u201eZum Home-Bildschirm\u201c \u00f6ffnet die App ohne Browserleiste; mit \u201eGef\u00fchrter Zugriff\u201c bleibt sie gesperrt.",
        "free": "W\u00e4hle ein Lied", "exit": "Vollbild beenden", "fullscreen": "Vollbild", "black": "Schwarze Tasten", "staff": "Notenlinien", "now": "Aktueller Ton",
        "language": "Sprache", "menu": "Men\u00fc \u2013 zweimal tippen zum \u00d6ffnen", "high": "Hohes",
        "twinkle": "Funkel, funkel, kleiner Stern", "mary": "Maria hat ein kleines Lamm", "ode": "Ode an die Freude", "jingle": "Jingle Bells", "play": "Anh\u00f6ren", "stop": "Stopp",
                "song": "Lied", "mode": "Spielmodus", "modeScreen": "Ohne Klavier", "modePiano": "Auf echtem Klavier spielen", "listening": "Ich h\u00f6re zu\u2026 spiel auf deinem Klavier", "micDenied": "Mikrofon ist aus \u2013 bitte im Browser erlauben",
                "micTitle": "Mikrofon erlauben", "micBlocked": "Das Mikrofon ist blockiert. Tippe auf das Schloss neben der Adresse \u2192 Mikrofon \u2192 Erlauben und dann auf \u201eNochmal\u201c.", "retry": "Nochmal", "close": "Schlie\u00dfen",
                "treble": "Violinschl\u00fcssel", "bass": "Bassschl\u00fcssel", "clef": "Schl\u00fcssel",
                "quiz": "Herausforderung", "quizEnd": "Herausforderung beenden",
        "notes": ["C", "D", "E", "F", "G", "A", "H"],   # German uses H for B
    },
    "hi": {
        "appName": "Hear-a-Note for Toddlers",
        "iosTip": "iPad / iPhone: \u0936\u0947\u092f\u0930 \u2192 \u201c\u0939\u094b\u092e \u0938\u094d\u0915\u094d\u0930\u0940\u0928 \u092e\u0947\u0902 \u091c\u094b\u0921\u093c\u0947\u0902\u201d \u0938\u0947 \u0910\u092a \u092c\u093f\u0928\u093e \u092c\u094d\u0930\u093e\u0909\u091c\u093c\u0930 \u092c\u093e\u0930 \u0915\u0947 \u0916\u0941\u0932\u0947\u0917\u093e; Guided Access \u091a\u093e\u0932\u0942 \u0915\u0930\u0915\u0947 \u0910\u092a \u0932\u0949\u0915 \u0915\u0930\u0947\u0902\u0964",
        "free": "\u0917\u0940\u0924 \u091a\u0941\u0928\u0947\u0902", "exit": "\u092a\u0942\u0930\u094d\u0923 \u0938\u094d\u0915\u094d\u0930\u0940\u0928 \u092c\u0902\u0926 \u0915\u0930\u0947\u0902", "fullscreen": "\u092a\u0942\u0930\u094d\u0923 \u0938\u094d\u0915\u094d\u0930\u0940\u0928", "black": "\u0915\u093e\u0932\u0940 \u0915\u0941\u0902\u091c\u093f\u092f\u093e\u0901", "staff": "\u0938\u094d\u0935\u0930\u0932\u093f\u092a\u093f", "now": "\u0935\u0930\u094d\u0924\u092e\u093e\u0928 \u0938\u094d\u0935\u0930",
        "language": "\u092d\u093e\u0937\u093e", "menu": "\u092e\u0947\u0928\u0942 \u2013 \u0916\u094b\u0932\u0928\u0947 \u0915\u0947 \u0932\u093f\u090f \u0926\u094b \u092c\u093e\u0930 \u091f\u0948\u092a \u0915\u0930\u0947\u0902", "high": "\u0924\u093e\u0930",
        "twinkle": "\u091a\u092e\u0915 \u091a\u092e\u0915 \u091b\u094b\u091f\u093e \u0924\u093e\u0930\u093e", "mary": "\u092e\u0948\u0930\u0940 \u0915\u093e \u091b\u094b\u091f\u093e \u092e\u0947\u092e\u0928\u093e", "ode": "\u0906\u0928\u0902\u0926 \u0915\u093e \u0917\u0940\u0924", "jingle": "\u091c\u093f\u0902\u0917\u0932 \u092c\u0947\u0932\u094d\u0938", "play": "\u0938\u0941\u0928\u0947\u0902", "stop": "\u0930\u094b\u0915\u0947\u0902",
                "song": "\u0917\u0940\u0924", "mode": "\u092c\u091c\u093e\u0928\u0947 \u0915\u093e \u0924\u0930\u0940\u0915\u093e", "modeScreen": "\u092a\u093f\u092f\u093e\u0928\u094b \u0915\u0947 \u092c\u093f\u0928\u093e", "modePiano": "\u0905\u0938\u0932\u0940 \u092a\u093f\u092f\u093e\u0928\u094b \u092a\u0930 \u092c\u091c\u093e\u090f\u0901", "listening": "\u0938\u0941\u0928 \u0930\u0939\u0947 \u0939\u0948\u0902\u2026 \u0905\u092a\u0928\u093e \u092a\u093f\u092f\u093e\u0928\u094b \u092c\u091c\u093e\u090f\u0901", "micDenied": "\u092e\u093e\u0907\u0915\u094d\u0930\u094b\u092b\u093c\u094b\u0928 \u092c\u0902\u0926 \u0939\u0948 \u2014 \u092c\u094d\u0930\u093e\u0909\u091c\u093c\u0930 \u092e\u0947\u0902 \u0905\u0928\u0941\u092e\u0924\u093f \u0926\u0947\u0902",
                "micTitle": "\u092e\u093e\u0907\u0915\u094d\u0930\u094b\u092b\u093c\u094b\u0928 \u0915\u0940 \u0905\u0928\u0941\u092e\u0924\u093f \u0926\u0947\u0902", "micBlocked": "\u092e\u093e\u0907\u0915\u094d\u0930\u094b\u092b\u093c\u094b\u0928 \u092c\u094d\u0932\u0949\u0915 \u0939\u0948\u0964 \u0935\u0947\u092c \u092a\u0924\u0947 \u0915\u0947 \u092a\u093e\u0938 \u0924\u093e\u0932\u0947 \u092a\u0930 \u091f\u0948\u092a \u0915\u0930\u0947\u0902 \u2192 \u092e\u093e\u0907\u0915\u094d\u0930\u094b\u092b\u093c\u094b\u0928 \u2192 \u0905\u0928\u0941\u092e\u0924\u093f \u0926\u0947\u0902, \u092b\u093f\u0930 '\u092b\u093f\u0930 \u0938\u0947 \u0915\u094b\u0936\u093f\u0936 \u0915\u0930\u0947\u0902' \u0926\u092c\u093e\u090f\u0901\u0964", "retry": "\u092b\u093f\u0930 \u0938\u0947 \u0915\u094b\u0936\u093f\u0936 \u0915\u0930\u0947\u0902", "close": "\u092c\u0902\u0926 \u0915\u0930\u0947\u0902",
                "treble": "\u091f\u094d\u0930\u0947\u092c\u0932 \u0915\u094d\u0932\u0947\u092b\u093c", "bass": "\u092c\u0947\u0938 \u0915\u094d\u0932\u0947\u092b\u093c", "clef": "\u0915\u094d\u0932\u0947\u092b\u093c",
                "quiz": "\u091a\u0941\u0928\u094c\u0924\u0940", "quizEnd": "\u091a\u0941\u0928\u094c\u0924\u0940 \u0938\u092e\u093e\u092a\u094d\u0924 \u0915\u0930\u0947\u0902",
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
