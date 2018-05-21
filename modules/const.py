"""Un module qui contient toutes les constantes utilisées par multi-pour-tous."""
# Defaults
stream_addr = "127.0.0.1"
stream_port = "9999"
stream_fps = 60

# Networking
KEYPRESS = 'P'
KEYUP = 'U'
KEYMSG = 'K'
TEXTMSG = 'M'
MSGKEYSEP = '|'
MSGSEP = "@"


# Aide à utiliser win32
win32_LEFT = 0
win32_TOP = 1
win32_RIGHT = 2
win32_BOTTOM = 3

# ScanCodes DirectInput pour le clavier
DIK_ESCAPE = 0x01
DIK_AMPERSAND = 0x02
DIK_EACUTE = 0x03
DIK_QUOTES = 0x04
DIK_QUOTE = 0x05
DIK_LBRACKET = 0x06
DIK_MINUS = 0x07
DIK_EGRAVE = 0x08
DIK_UNDERLINE = 0x09
DIK_CCEDILLA = 0x0A
DIK_AGRAVE = 0x0B
DIK_RBRACKET = 0x0C
DIK_EQUALS = 0x0D
DIK_BACK = 0x0E
DIK_TAB = 0x0F
DIK_A = 0x10
DIK_Z = 0x11
DIK_E = 0x12
DIK_R = 0x13
DIK_T = 0x14
DIK_Y = 0x15
DIK_U = 0x16
DIK_I = 0x17
DIK_O = 0x18
DIK_P = 0x19
DIK_CIRCUMFLEX = 0x1A
DIK_DOLLAR = 0x1B
DIK_RETURN = 0x1C
DIK_LCONTROL = 0x1D
DIK_Q = 0x1E
DIK_S = 0x1F
DIK_D = 0x20
DIK_F = 0x21
DIK_G = 0x22
DIK_H = 0x23
DIK_J = 0x24
DIK_K = 0x25
DIK_L = 0x26
DIK_M = 0x27
DIK_UGRAVE = 0x28
DIK_MULTIPLY = 0x29
DIK_LSHIFT = 0x2A
DIK_LESSTHAN = 0x2B
DIK_W = 0x2C
DIK_X = 0x2D
DIK_C = 0x2E
DIK_V = 0x2F
DIK_B = 0x30
DIK_N = 0x31
DIK_COMMA = 0x32
DIK_SEMICOLON = 0x33
DIK_COLON = 0x34
DIK_EXCLAMATION = 0x35
DIK_RSHIFT = 0x36
DIK_NUMMULTIPLY = 0x37
DIK_LMENU = 0x38  # TODO : Je sais pas ce que c'est
DIK_SPACE = 0x39
DIK_CAPITAL = 0x3A
DIK_F1 = 0x3B
DIK_F2 = 0x3C
DIK_F3 = 0x3D
DIK_F4 = 0x3E
DIK_F5 = 0x3F
DIK_F6 = 0x40
DIK_F7 = 0x41
DIK_F8 = 0x42
DIK_F9 = 0x43
DIK_F10 = 0x44
DIK_NUMLOCK = 0x45
DIK_SCROLL = 0x46
DIK_NUMPAD7 = 0x47
DIK_NUMPAD8 = 0x48
DIK_NUMPAD9 = 0x49
DIK_SUBTRACT = 0x4A
DIK_NUMPAD4 = 0x4B
DIK_NUMPAD5 = 0x4C
DIK_NUMPAD6 = 0x4D
DIK_ADD = 0x4E
DIK_NUMPAD1 = 0x4F
DIK_NUMPAD2 = 0x50
DIK_NUMPAD3 = 0x51
DIK_NUMPAD0 = 0x52
DIK_DECIMAL = 0x53
DIK_F11 = 0x57
DIK_F12 = 0x58
DIK_F13 = 0x64
DIK_F14 = 0x65
DIK_F15 = 0x66
DIK_KANA = 0x70
DIK_CONVERT = 0x79
DIK_NOCONVERT = 0x7B
DIK_YEN = 0x7D
DIK_NUMPADEQUALS = 0x8D
# DIK_CIRCUMFLEX = 0x90
DIK_AT = 0x91
# DIK_E = 0x92
DIK_UNDERLINE = 0x93
DIK_KANJI = 0x94
DIK_STOP = 0x95
DIK_AX = 0x96
DIK_UNLABELED = 0x97
DIK_NUMPADENTER = 0x9C
DIK_RCONTROL = 0x9D
DIK_NUMPADCOMMA = 0xB3
DIK_DIVIDE = 0xB5
DIK_SYSRQ = 0xB7
DIK_RMENU = 0xB8
DIK_HOME = 0xC7
DIK_UP = 72
DIK_NUMUP = 0xC8
DIK_PRIOR = 0xC9
DIK_LEFT = 0xCB
DIK_RIGHT = 0xCD
DIK_END = 0xCF
DIK_DOWN = 0xD0
DIK_NEXT = 0xD1
DIK_INSERT = 0xD2
DIK_DELETE = 0xD3
DIK_LWIN = 0xDB
DIK_RWIN = 0xDC
DIK_APPS = 0xDD

# &
# dic_DIK = [
#     DIK_ESCAPE,
#     DIK_AMPERSAND,
#     DIK_EACUTE,
#     DIK_QUOTES,
#     DIK_QUOTE,
#     DIK_LBRACKET,
#     DIK_MINUS,
#     DIK_EGRAVE,
#     DIK_UNDERLINE,
#     DIK_CCEDILLA,
#     DIK_AGRAVE,
#     DIK_RBRACKET,
#     DIK_EQUALS,
#     DIK_BACK,
#     DIK_TAB,
#     DIK_A,
#     DIK_Z,
#     DIK_E,
#     DIK_R,
#     DIK_T,
#     DIK_Y,
#     DIK_U,
#     DIK_I,
#     DIK_O,
#     DIK_P,
#     DIK_CIRCUMFLEX,
#     DIK_DOLLAR,
#     DIK_RETURN,
#     DIK_LCONTROL,
#     DIK_Q,
#     DIK_S,
#     DIK_D,
#     DIK_F,
#     DIK_G,
#     DIK_H,
#     DIK_J,
#     DIK_K,
#     DIK_L,
#     DIK_M,
#     DIK_UGRAVE,
#     DIK_MULTIPLY,
#     DIK_LSHIFT,
#     DIK_LESSTHAN,
#     DIK_W,
#     DIK_X,
#     DIK_C,
#     DIK_V,
#     DIK_B,
#     DIK_N,
#     DIK_COMMA,
#     DIK_SEMICOLON,
#     DIK_COLON,
#     DIK_EXCLAMATION,
#     DIK_RSHIFT,
#     DIK_NUMMULTIPLY,
#     DIK_LMENU,
#     DIK_SPACE,
#     DIK_CAPITAL,
#     DIK_F1,
#     DIK_F2,
#     DIK_F3,
#     DIK_F4,
#     DIK_F5,
#     DIK_F6,
#     DIK_F7,
#     DIK_F8,
#     DIK_F9,
#     DIK_F10,
#     DIK_NUMLOCK,
#     DIK_SCROLL,
#     DIK_NUMPAD7,
#     DIK_NUMPAD8,
#     DIK_NUMPAD9,
#     DIK_SUBTRACT,
#     DIK_NUMPAD4,
#     DIK_NUMPAD5,
#     DIK_NUMPAD6,
#     DIK_ADD,
#     DIK_NUMPAD1,
#     DIK_NUMPAD2,
#     DIK_NUMPAD3,
#     DIK_NUMPAD0,
#     DIK_DECIMAL,
#     DIK_F11,
#     DIK_F12,
#     DIK_F13,
#     DIK_F14,
#     DIK_F15,
#     DIK_KANA,
#     DIK_CONVERT,
#     DIK_NOCONVERT,
#     DIK_YEN,
#     DIK_NUMPADEQUALS,
#     DIK_AT,
#     DIK_UNDERLINE,
#     DIK_KANJI,
#     DIK_STOP,
#     DIK_AX,
#     DIK_UNLABELED,
#     DIK_NUMPADENTER,
#     DIK_RCONTROL,
#     DIK_NUMPADCOMMA,
#     DIK_DIVIDE,
#     DIK_SYSRQ,
#     DIK_RMENU,
#     DIK_HOME,
#     DIK_UP,
#     DIK_PRIOR,
#     DIK_LEFT,
#     DIK_RIGHT,
#     DIK_END,
#     DIK_DOWN,
#     DIK_NEXT,
#     DIK_INSERT,
#     DIK_DELETE,
#     DIK_LWIN,
#     DIK_RWIN,
#     DIK_APPS,
# ]

sdl_to_dik = {27: DIK_ESCAPE,
              49: DIK_AMPERSAND,
              50: DIK_EACUTE,
              51: DIK_QUOTES,
              52: DIK_QUOTE,
              53: DIK_LBRACKET,
              54: DIK_MINUS,
              55: DIK_EGRAVE,
              56: DIK_UNDERLINE,
              57: DIK_CCEDILLA,
              48: DIK_AGRAVE,
              41: DIK_RBRACKET,
              61: DIK_EQUALS,
              8: DIK_BACK,
              9: DIK_TAB,
              97: DIK_A,
              122: DIK_Z,
              101: DIK_E,
              114: DIK_R,
              116: DIK_T,
              121: DIK_Y,
              117: DIK_U,
              105: DIK_I,
              111: DIK_O,
              112: DIK_P,
              94: DIK_CIRCUMFLEX,
              36: DIK_DOLLAR,
              13: DIK_RETURN,
              1073742048: DIK_PRIOR,
              113: DIK_Q,
              115: DIK_S,
              100: DIK_D,
              102: DIK_F,
              103: DIK_G,
              104: DIK_H,
              106: DIK_J,
              107: DIK_K,
              108: DIK_L,
              109: DIK_M,
              249: DIK_UGRAVE,
              42: DIK_MULTIPLY,
              1073742049: DIK_LSHIFT,
              60: DIK_LESSTHAN,
              119: DIK_W,
              120: DIK_X,
              99: DIK_C,
              118: DIK_V,
              98: DIK_B,
              110: DIK_N,
              44: DIK_COMMA,
              59: DIK_SEMICOLON,
              58: DIK_COLON,
              33: DIK_EXCLAMATION,
              1073742053: DIK_RSHIFT,
              1073741909: DIK_NUMMULTIPLY,
              1073741925: DIK_RMENU,
              32: DIK_SPACE,
              1073741881: DIK_CAPITAL,
              1073741882: DIK_F1,
              1073741883: DIK_F2,
              1073741884: DIK_F3,
              1073741885: DIK_F4,
              1073741886: DIK_F5,
              1073741887: DIK_F6,
              1073741888: DIK_F7,
              1073741889: DIK_F8,
              1073741890: DIK_F9,
              1073741891: DIK_F10,
              1073741892: DIK_F11,
              1073741907: DIK_SCROLL,
              1073741895: DIK_NUMLOCK,
              1073741919: DIK_NUMPAD7,
              1073741920: DIK_NUMPAD8,
              1073741921: DIK_NUMPAD9,
              1073741910: DIK_SUBTRACT,
              1073741916: DIK_NUMPAD4,
              1073741917: DIK_NUMPAD5,
              1073741918: DIK_NUMPAD6,
              1073741911: DIK_ADD,
              1073741913: DIK_NUMPAD1,
              1073741914: DIK_NUMPAD2,
              1073741915: DIK_NUMPAD3,
              1073741922: DIK_NUMPAD0,
              1073741923: DIK_DECIMAL,
              1073741893: DIK_APPS,
              1073742093: DIK_AT,
              1073742052: DIK_RCONTROL,
              1073741908: DIK_DIVIDE,
              1073741906: DIK_UP,
              1073742054: DIK_LEFT,
              1073741903: DIK_RIGHT,
              1073741901: DIK_END,
              1073741905: DIK_DOWN,
              1073741897: DIK_INSERT,
              127: DIK_DELETE,
              1073742051: DIK_RWIN
              }
