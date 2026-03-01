# media.py - Ultimate Indian Media Bot
# Indian Songs, Bollywood, Desi Content + World Open Databases
# EVERYTHING INSIDE TELEGRAM - NO LINKS!

import os
import logging
import asyncio
import aiohttp
import random
import re
import json
from datetime import datetime
from urllib.parse import quote_plus
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    BotCommand
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from telegram.constants import ChatAction
from aiohttp import web

# ══════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")

# Optional API Keys (free tier)
LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY", "")
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ══════════════════════════════════════════
#  𝗦𝗧𝗬𝗟𝗜𝗦𝗛 𝗙𝗢𝗡𝗧𝗦
# ══════════════════════════════════════════

def bold_s(t):
    n='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    s='𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵'
    return t.translate(str.maketrans(n,s))

def ital_s(t):
    n='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    s='𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻'
    return t.translate(str.maketrans(n,s))

def bital_s(t):
    n='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    s='𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯'
    return t.translate(str.maketrans(n,s))

def mono_s(t):
    n='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    s='𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿'
    return t.translate(str.maketrans(n,s))

def script_s(t):
    n='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    s='𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏'
    return t.translate(str.maketrans(n,s))

def double_s(t):
    n='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    s='𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡'
    return t.translate(str.maketrans(n,s))

def neg_sq(t):
    n='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    s='🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉'
    return t.upper().translate(str.maketrans(n,s))

# ═══ Design Elements ═══

T = "╔══════════════════════════════╗"
B = "╚══════════════════════════════╝"
V = "║"
L1 = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
L2 = "◈━━━━━━━━━━━━━━━━━━━━━━━━━◈"
L3 = "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
DL = "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄"
SP = "╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍"
FL = "❀━━━━━━━━━━━━━━━━━━━━━━━━❀"
ML = "♪━━━━━━━━━━━━━━━━━━━━━━━━♪"
IL = "🇮🇳━━━━━━━━━━━━━━━━━━━━━━🇮🇳"

# Symbols
E = {
    "crown":"👑","fire":"🔥","star":"✦","star2":"★","star3":"⭐",
    "diamond":"◆","diamond2":"◇","spark":"✨","bolt":"⚡",
    "rocket":"🚀","gem":"💎","heart":"❤️","heart2":"💖",
    "check":"✅","cross":"❌","warn":"⚠️","mag":"🔍",
    "globe":"🌍","india":"🇮🇳","om":"🕉️","namaste":"🙏",
    "diya":"🪔","sitar":"🪕","tabla":"🥁","veena":"🎸",
    "film":"🎬","cam":"📷","vid":"📹","tv":"📺",
    "music":"🎵","mic":"🎤","head":"🎧","note":"🎶",
    "notes":"🎵","sing":"🎤","disk":"💿","vinyl":"📀",
    "radio":"📻","speaker":"🔊","wave":"〰️","amp":"🔉",
    "book":"📖","books":"📚","scroll":"📜",
    "art":"🎨","frame":"🖼️","photo":"📸",
    "anime":"🌸","cherry":"🌸","sakura":"🎌",
    "game":"🎮","trophy":"🏆","code":"💻","robot":"🤖",
    "cube":"🧊","rocket2":"🚀","moon":"🌙",
    "wall":"🌄","city":"🏙️","night":"🌃",
    "folder":"📁","pack":"📦","recv":"📥","send":"📤",
    "key":"🔑","eye":"👁️","point":"👉","flex":"💪",
    "cool":"😎","love":"🥰","dance":"💃","party":"🎉",
    "arrow":"➤","arrow2":"➜","tri":"▸","dot":"•",
    "ring":"◉","circle":"●","inf":"♾️",
    "tick":"✓","plus":"✚","fleur":"⚜️",
    "rose":"🌹","lotus":"🪷","peacock":"🦚",
    "elephant":"🐘","tiger":"🐅","flag":"🏴",
    "temple":"🛕","prayer":"📿","rangoli":"🎭",
    "chai":"🍵","mango":"🥭","spice":"🌶️",
    "rupee":"₹","medal":"🏅","century":"💯",
}

# ══════════════════════════════════════════
#  𝗠𝗘𝗗𝗜𝗔 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗𝗘𝗥
# ══════════════════════════════════════════

class Downloader:
    def __init__(self):
        self.session = None
        self.spotify_token = None
        self.spotify_token_time = None

    async def get_session(self):
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            conn = aiohttp.TCPConnector(limit=15, force_close=True)
            self.session = aiohttp.ClientSession(
                timeout=timeout, connector=conn,
                headers={"User-Agent": "IndianMediaBot/2.0"}
            )
        return self.session

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def download(self, url, max_mb=45):
        try:
            s = await self.get_session()
            async with s.get(url) as r:
                if r.status != 200:
                    return None
                cl = r.headers.get('Content-Length')
                if cl and int(cl) > max_mb*1024*1024:
                    return None
                data = await r.read()
                if len(data) > max_mb*1024*1024:
                    return None
                return data
        except Exception as ex:
            logger.error(f"Download fail: {ex}")
            return None

    async def send_photo(self, bot, cid, url, cap=""):
        try:
            data = await self.download(url, 10)
            if data and len(data) > 1000:
                await bot.send_photo(chat_id=cid, photo=data, caption=cap[:1024])
                return True
            await bot.send_photo(chat_id=cid, photo=url, caption=cap[:1024])
            return True
        except Exception as ex:
            logger.error(f"Photo fail: {ex}")
            return False

    async def send_video(self, bot, cid, url, cap="", thumb_url=None):
        try:
            data = await self.download(url, 45)
            if not data:
                return False
            thumb = None
            if thumb_url:
                thumb = await self.download(thumb_url, 1)
            await bot.send_video(chat_id=cid, video=data, caption=cap[:1024],
                                thumbnail=thumb, supports_streaming=True,
                                read_timeout=120, write_timeout=120)
            return True
        except Exception as ex:
            logger.error(f"Video fail: {ex}")
            return False

    async def send_audio(self, bot, cid, url, cap="", title="", performer="", thumb_url=None):
        try:
            data = await self.download(url, 45)
            if not data:
                return False
            thumb = None
            if thumb_url:
                thumb = await self.download(thumb_url, 1)
            await bot.send_audio(chat_id=cid, audio=data, caption=cap[:1024],
                                title=title, performer=performer, thumbnail=thumb,
                                read_timeout=120, write_timeout=120)
            return True
        except Exception as ex:
            logger.error(f"Audio fail: {ex}")
            return False

    async def send_doc(self, bot, cid, url, cap="", fname=""):
        try:
            data = await self.download(url, 45)
            if not data:
                return False
            await bot.send_document(chat_id=cid, document=data,
                                   caption=cap[:1024], filename=fname)
            return True
        except Exception as ex:
            logger.error(f"Doc fail: {ex}")
            return False

    async def get_spotify_token(self):
        """Get Spotify API token"""
        if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
            return None
        if self.spotify_token and self.spotify_token_time:
            if (datetime.now() - self.spotify_token_time).seconds < 3500:
                return self.spotify_token
        try:
            s = await self.get_session()
            import base64
            creds = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()
            async with s.post("https://accounts.spotify.com/api/token",
                            headers={"Authorization": f"Basic {creds}"},
                            data={"grant_type": "client_credentials"}) as r:
                if r.status == 200:
                    data = await r.json()
                    self.spotify_token = data.get("access_token")
                    self.spotify_token_time = datetime.now()
                    return self.spotify_token
        except:
            pass
        return None

dl = Downloader()
UD = {}  # User data

# ══════════════════════════════════════════
#  🇮🇳 𝗜𝗡𝗗𝗜𝗔𝗡 𝗠𝗨𝗦𝗜𝗖 𝗦𝗘𝗔𝗥𝗖𝗛 𝗘𝗡𝗚𝗜𝗡𝗘𝗦
# ══════════════════════════════════════════

# ── 1. JioSaavn API (MAIN - Indian songs with actual audio!) ──

async def search_jiosaavn(query, limit=8):
    """Search JioSaavn - India's #1 music platform"""
    results = []
    try:
        s = await dl.get_session()
        # Using JioSaavn unofficial API
        url = f"https://saavn.dev/api/search/songs?query={quote_plus(query)}&limit={limit}"
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.json()
                songs = data.get("data", {}).get("results", [])
                for song in songs:
                    # Get best quality download URL
                    download_urls = song.get("downloadUrl", [])
                    audio_url = ""
                    for durl in reversed(download_urls):  # highest quality first
                        if durl.get("quality") in ["320kbps", "160kbps", "96kbps"]:
                            audio_url = durl.get("url", "")
                            break
                    if not audio_url and download_urls:
                        audio_url = download_urls[-1].get("url", "")

                    # Get image
                    images = song.get("image", [])
                    img_url = ""
                    for img in reversed(images):
                        if img.get("quality") in ["500x500", "150x150"]:
                            img_url = img.get("url", "")
                            break
                    if not img_url and images:
                        img_url = images[-1].get("url", "")

                    artists = song.get("artists", {}).get("primary", [])
                    artist_names = ", ".join([a.get("name", "") for a in artists]) if artists else song.get("primaryArtists", "Unknown")

                    results.append({
                        "type": "indian_song",
                        "title": song.get("name", "Unknown"),
                        "artist": artist_names,
                        "album": song.get("album", {}).get("name", ""),
                        "year": song.get("year", ""),
                        "duration": song.get("duration", 0),
                        "language": song.get("language", "Hindi"),
                        "play_count": song.get("playCount", ""),
                        "audio_url": audio_url,
                        "image_url": img_url,
                        "has_lyrics": song.get("hasLyrics", False),
                        "song_id": song.get("id", ""),
                        "source": "JioSaavn",
                        "label": song.get("label", ""),
                        "explicit": song.get("explicitContent", False),
                    })
    except Exception as ex:
        logger.error(f"JioSaavn error: {ex}")
    return results


async def get_jiosaavn_lyrics(song_id):
    """Get lyrics from JioSaavn"""
    try:
        s = await dl.get_session()
        url = f"https://saavn.dev/api/songs/{song_id}/lyrics"
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.json()
                lyrics = data.get("data", {}).get("lyrics", "")
                # Clean HTML tags
                lyrics = re.sub(r'<[^>]+>', '\n', lyrics)
                lyrics = re.sub(r'\n{3,}', '\n\n', lyrics)
                return lyrics.strip()
    except:
        pass
    return ""


async def get_jiosaavn_album(query, limit=5):
    """Search JioSaavn albums"""
    results = []
    try:
        s = await dl.get_session()
        url = f"https://saavn.dev/api/search/albums?query={quote_plus(query)}&limit={limit}"
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.json()
                albums = data.get("data", {}).get("results", [])
                for album in albums:
                    images = album.get("image", [])
                    img_url = images[-1].get("url", "") if images else ""
                    results.append({
                        "type": "album",
                        "title": album.get("name", "Unknown"),
                        "artist": album.get("artist", "Unknown"),
                        "year": album.get("year", ""),
                        "language": album.get("language", ""),
                        "song_count": album.get("songCount", 0),
                        "album_id": album.get("id", ""),
                        "image_url": img_url,
                        "source": "JioSaavn",
                    })
    except Exception as ex:
        logger.error(f"JioSaavn album error: {ex}")
    return results


async def get_jiosaavn_album_songs(album_id):
    """Get all songs from a JioSaavn album"""
    results = []
    try:
        s = await dl.get_session()
        url = f"https://saavn.dev/api/albums?id={album_id}"
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.json()
                songs = data.get("data", {}).get("songs", [])
                for song in songs:
                    download_urls = song.get("downloadUrl", [])
                    audio_url = ""
                    for durl in reversed(download_urls):
                        if durl.get("quality") in ["320kbps", "160kbps", "96kbps"]:
                            audio_url = durl.get("url", "")
                            break
                    if not audio_url and download_urls:
                        audio_url = download_urls[-1].get("url", "")
                    images = song.get("image", [])
                    img_url = images[-1].get("url", "") if images else ""
                    artists = song.get("artists", {}).get("primary", [])
                    artist_names = ", ".join([a.get("name", "") for a in artists]) if artists else "Unknown"
                    results.append({
                        "type": "indian_song",
                        "title": song.get("name", "Unknown"),
                        "artist": artist_names,
                        "album": song.get("album", {}).get("name", ""),
                        "duration": song.get("duration", 0),
                        "audio_url": audio_url,
                        "image_url": img_url,
                        "song_id": song.get("id", ""),
                        "source": "JioSaavn",
                        "language": song.get("language", "Hindi"),
                    })
    except Exception as ex:
        logger.error(f"JioSaavn album songs error: {ex}")
    return results


async def search_jiosaavn_playlists(query, limit=5):
    """Search JioSaavn playlists"""
    results = []
    try:
        s = await dl.get_session()
        url = f"https://saavn.dev/api/search/playlists?query={quote_plus(query)}&limit={limit}"
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.json()
                playlists = data.get("data", {}).get("results", [])
                for pl in playlists:
                    images = pl.get("image", [])
                    img_url = images[-1].get("url", "") if images else ""
                    results.append({
                        "type": "playlist",
                        "title": pl.get("name", "Unknown"),
                        "song_count": pl.get("songCount", 0),
                        "playlist_id": pl.get("id", ""),
                        "image_url": img_url,
                        "source": "JioSaavn",
                        "language": pl.get("language", ""),
                    })
    except:
        pass
    return results


async def search_jiosaavn_artists(query, limit=5):
    """Search JioSaavn artists"""
    results = []
    try:
        s = await dl.get_session()
        url = f"https://saavn.dev/api/search/artists?query={quote_plus(query)}&limit={limit}"
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.json()
                artists = data.get("data", {}).get("results", [])
                for art in artists:
                    images = art.get("image", [])
                    img_url = images[-1].get("url", "") if images else ""
                    results.append({
                        "type": "artist_info",
                        "title": art.get("name", "Unknown"),
                        "artist_id": art.get("id", ""),
                        "image_url": img_url,
                        "role": art.get("role", ""),
                        "source": "JioSaavn",
                    })
    except:
        pass
    return results


# ── 2. Spotify Search (for info + 30s preview) ──

async def search_spotify(query, limit=5):
    results = []
    token = await dl.get_spotify_token()
    if not token:
        return results
    try:
        s = await dl.get_session()
        url = f"https://api.spotify.com/v1/search?q={quote_plus(query)}&type=track&market=IN&limit={limit}"
        headers = {"Authorization": f"Bearer {token}"}
        async with s.get(url, headers=headers) as r:
            if r.status == 200:
                data = await r.json()
                for track in data.get("tracks", {}).get("items", []):
                    artists = ", ".join([a["name"] for a in track.get("artists", [])])
                    album = track.get("album", {})
                    images = album.get("images", [])
                    img = images[0]["url"] if images else ""
                    results.append({
                        "type": "spotify_track",
                        "title": track.get("name", "Unknown"),
                        "artist": artists,
                        "album": album.get("name", ""),
                        "duration": track.get("duration_ms", 0) // 1000,
                        "preview_url": track.get("preview_url", ""),
                        "image_url": img,
                        "popularity": track.get("popularity", 0),
                        "release_date": album.get("release_date", ""),
                        "source": "Spotify",
                        "explicit": track.get("explicit", False),
                    })
    except Exception as ex:
        logger.error(f"Spotify error: {ex}")
    return results


# ── 3. Last.fm (song info, similar, tags) ──

async def search_lastfm(query, limit=5):
    results = []
    if not LASTFM_API_KEY:
        return results
    try:
        s = await dl.get_session()
        url = (f"https://ws.audioscrobbler.com/2.0/?method=track.search"
               f"&track={quote_plus(query)}&api_key={LASTFM_API_KEY}"
               f"&format=json&limit={limit}")
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.json()
                tracks = data.get("results", {}).get("trackmatches", {}).get("track", [])
                for t in tracks:
                    images = t.get("image", [])
                    img = ""
                    for i in reversed(images):
                        if i.get("#text"):
                            img = i["#text"]
                            break
                    results.append({
                        "type": "lastfm_track",
                        "title": t.get("name", "Unknown"),
                        "artist": t.get("artist", "Unknown"),
                        "listeners": t.get("listeners", "0"),
                        "image_url": img,
                        "source": "Last.fm",
                    })
    except:
        pass
    return results


# ── 4. Internet Archive Indian Audio ──

async def search_archive_indian_audio(query, limit=5, page=1):
    results = []
    try:
        s = await dl.get_session()
        q = f"{query} (hindi OR bollywood OR indian OR punjabi OR tamil OR telugu)"
        url = (f"https://archive.org/advancedsearch.php?"
               f"q={quote_plus(q)}+mediatype:audio&output=json&rows={limit}&page={page}"
               f"&fl[]=identifier,title,creator,description,date,downloads")
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.json()
                for doc in data.get("response", {}).get("docs", []):
                    ident = doc.get("identifier", "")
                    audio_url = ""
                    try:
                        furl = f"https://archive.org/metadata/{ident}/files"
                        async with s.get(furl) as fr:
                            if fr.status == 200:
                                fd = await fr.json()
                                for f in fd.get("result", []):
                                    nm = f.get("name", "")
                                    sz = int(f.get("size", 0) or 0)
                                    if any(nm.lower().endswith(x) for x in ['.mp3','.ogg','.flac','.wav']):
                                        if sz < 45*1024*1024:
                                            audio_url = f"https://archive.org/download/{ident}/{quote_plus(nm)}"
                                            break
                    except:
                        pass
                    title = doc.get("title", "Unknown")
                    if isinstance(title, list): title = title[0]
                    creator = doc.get("creator", "Unknown")
                    if isinstance(creator, list): creator = creator[0]
                    results.append({
                        "type": "audio",
                        "title": str(title),
                        "artist": str(creator),
                        "desc": str(doc.get("description", ""))[:200],
                        "audio_url": audio_url,
                        "downloads": doc.get("downloads", 0),
                        "source": "Internet Archive",
                        "thumbnail": f"https://archive.org/services/img/{ident}",
                    })
    except Exception as ex:
        logger.error(f"Archive Indian audio error: {ex}")
    return results


# ── 5. Archive.org Indian Movies/Videos ──

async def search_archive_indian_video(query, limit=5, page=1):
    results = []
    try:
        s = await dl.get_session()
        q = f"{query} (hindi OR bollywood OR indian OR desi)"
        url = (f"https://archive.org/advancedsearch.php?"
               f"q={quote_plus(q)}+mediatype:movies&output=json&rows={limit}&page={page}"
               f"&fl[]=identifier,title,creator,description,date,downloads")
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.json()
                for doc in data.get("response", {}).get("docs", []):
                    ident = doc.get("identifier", "")
                    video_url = ""
                    thumb = f"https://archive.org/services/img/{ident}"
                    try:
                        furl = f"https://archive.org/metadata/{ident}/files"
                        async with s.get(furl) as fr:
                            if fr.status == 200:
                                fd = await fr.json()
                                for f in fd.get("result", []):
                                    nm = f.get("name", "")
                                    sz = int(f.get("size", 0) or 0)
                                    if nm.lower().endswith('.mp4') and sz < 45*1024*1024:
                                        video_url = f"https://archive.org/download/{ident}/{quote_plus(nm)}"
                                        break
                    except:
                        pass
                    title = doc.get("title", "Unknown")
                    if isinstance(title, list): title = title[0]
                    creator = doc.get("creator", "Unknown")
                    if isinstance(creator, list): creator = creator[0]
                    results.append({
                        "type": "video",
                        "title": str(title),
                        "creator": str(creator),
                        "desc": str(doc.get("description", ""))[:200],
                        "video_url": video_url,
                        "thumbnail": thumb,
                        "downloads": doc.get("downloads", 0),
                        "source": "Internet Archive",
                    })
    except Exception as ex:
        logger.error(f"Archive Indian video error: {ex}")
    return results


# ── 6. Other APIs (Images, Anime, Books etc) ──

async def search_openverse(query, page=1, limit=5):
    results = []
    try:
        s = await dl.get_session()
        url = f"https://api.openverse.org/v1/images/?q={quote_plus(query)}&page={page}&page_size={limit}"
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.json()
                for item in data.get("results", []):
                    results.append({
                        "type":"image","title":item.get("title","Untitled") or "Untitled",
                        "creator":item.get("creator","Unknown") or "Unknown",
                        "image_url":item.get("url",""),"thumbnail":item.get("thumbnail",""),
                        "source":"Openverse","license":item.get("license","CC"),
                    })
    except:pass
    return results

async def search_wallhaven(query, page=1, limit=5):
    results = []
    try:
        s = await dl.get_session()
        url = f"https://wallhaven.cc/api/v1/search?q={quote_plus(query)}&page={page}&sorting=relevance&purity=100"
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.json()
                for item in data.get("data",[])[:limit]:
                    results.append({
                        "type":"image","title":f"Wall #{item.get('id','')}",
                        "image_url":item.get("path",""),"thumbnail":item.get("thumbs",{}).get("small",""),
                        "source":"Wallhaven","resolution":item.get("resolution",""),
                        "creator":"Community","license":"Wallhaven",
                    })
    except:pass
    return results

async def search_anime(query, limit=5):
    results = []
    try:
        s = await dl.get_session()
        url = f"https://api.jikan.moe/v4/anime?q={quote_plus(query)}&limit={limit}&sfw=true"
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.json()
                for item in data.get("data",[]):
                    img = item.get("images",{}).get("jpg",{})
                    results.append({
                        "type":"anime","title":item.get("title","Unknown"),
                        "title_jp":item.get("title_japanese",""),
                        "score":item.get("score","N/A"),"episodes":item.get("episodes","?"),
                        "status":item.get("status",""),"synopsis":(item.get("synopsis","") or "")[:300],
                        "image_url":img.get("large_image_url",img.get("image_url","")),
                        "genres":", ".join([g.get("name","") for g in item.get("genres",[])]),
                        "year":item.get("year",""),"source":"MyAnimeList",
                    })
    except:pass
    return results

async def search_gutenberg(query, limit=5, page=1):
    results = []
    try:
        s = await dl.get_session()
        url = f"https://gutendex.com/books/?search={quote_plus(query)}&page={page}"
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.json()
                for item in data.get("results",[])[:limit]:
                    authors = ", ".join([a.get("name","") for a in item.get("authors",[])])
                    fmt = item.get("formats",{})
                    cover = fmt.get("image/jpeg","")
                    epub = fmt.get("application/epub+zip","")
                    txt = fmt.get("text/plain; charset=utf-8") or fmt.get("text/plain","")
                    results.append({
                        "type":"book","title":item.get("title","Unknown"),"creator":authors,
                        "cover_url":cover,"epub_url":epub,"txt_url":txt,
                        "downloads":item.get("download_count",0),"source":"Gutenberg",
                    })
    except:pass
    return results

async def search_github(query, limit=5):
    results = []
    try:
        s = await dl.get_session()
        url = f"https://api.github.com/search/repositories?q={quote_plus(query)}&per_page={limit}&sort=stars"
        async with s.get(url, headers={"Accept":"application/vnd.github.v3+json"}) as r:
            if r.status == 200:
                data = await r.json()
                for item in data.get("items",[]):
                    results.append({
                        "type":"code","title":item.get("full_name",""),
                        "desc":(item.get("description","") or "")[:200],
                        "stars":item.get("stargazers_count",0),"forks":item.get("forks_count",0),
                        "language":item.get("language","N/A"),
                        "avatar_url":item.get("owner",{}).get("avatar_url",""),
                        "source":"GitHub",
                    })
    except:pass
    return results

async def search_nasa(query, limit=5):
    results = []
    try:
        s = await dl.get_session()
        url = f"https://images-api.nasa.gov/search?q={quote_plus(query)}&media_type=image&page_size={limit}"
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.json()
                for item in data.get("collection",{}).get("items",[])[:limit]:
                    d = item.get("data",[{}])[0]
                    links = item.get("links",[])
                    thumb = links[0].get("href","") if links else ""
                    results.append({
                        "type":"image","title":d.get("title","NASA"),
                        "desc":(d.get("description","") or "")[:200],
                        "image_url":thumb,"thumbnail":thumb,
                        "source":"NASA","creator":"NASA",
                    })
    except:pass
    return results

async def get_waifu_many(cat="waifu", count=5):
    try:
        s = await dl.get_session()
        url = f"https://api.waifu.pics/many/sfw/{cat.lower()}"
        async with s.post(url, json={}) as r:
            if r.status == 200:
                data = await r.json()
                return data.get("files",[])[:count]
    except:pass
    return []

async def search_wikipedia(query, limit=3):
    results = []
    try:
        s = await dl.get_session()
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(query)}"
        async with s.get(url) as r:
            if r.status == 200:
                data = await r.json()
                results.append({
                    "type":"wiki","title":data.get("title",""),
                    "extract":data.get("extract",""),
                    "image_url":data.get("originalimage",{}).get("source","") or data.get("thumbnail",{}).get("source",""),
                    "source":"Wikipedia",
                })
    except:pass
    return results


# ══════════════════════════════════════════
#  🎵 𝗦𝗘𝗡𝗗 𝗥𝗘𝗦𝗨𝗟𝗧𝗦 𝗧𝗢 𝗧𝗘𝗟𝗘𝗚𝗥𝗔𝗠
# ══════════════════════════════════════════

def format_duration(secs):
    try:
        secs = int(secs)
        m, s = divmod(secs, 60)
        return f"{m}:{s:02d}"
    except:
        return "0:00"

def make_progress_bar(val, max_val=10, length=10):
    try:
        v = float(val)
        filled = int(v / max_val * length)
        return "█" * filled + "░" * (length - filled)
    except:
        return "░" * length


async def send_results(bot, cid, results, query, category, page=1):
    """Send results as native Telegram media"""

    if not results:
        txt = (
            f"\n{T}\n{V}  {E['cross']} {bold_s('NO RESULTS FOUND')} {E['cross']}\n{B}\n\n"
            f"{E['mag']} {bold_s('Query')}: {ital_s(query)}\n"
            f"{E['folder']} {bold_s('Category')}: {ital_s(category)}\n\n"
            f"{L2}\n\n"
            f"{E['arrow']} {bital_s('Tips')}:\n"
            f"  {E['dot']} {ital_s('Try different keywords')}\n"
            f"  {E['dot']} {ital_s('Hindi: Arijit Singh, Tere Bina')}\n"
            f"  {E['dot']} {ital_s('Movie: Dilwale, Sholay')}\n"
            f"\n{L3}"
        )
        await bot.send_message(chat_id=cid, text=txt)
        return

    # Category icons
    ci = {
        "song":E['music'], "album":E['disk'], "bollywood":E['film'],
        "indian_music":E['sitar'], "images":E['frame'], "wallpapers":E['wall'],
        "anime":E['anime'], "books":E['books'], "code":E['code'],
        "nasa":E['rocket'], "wiki":E['book'], "waifu":E['cherry'],
        "all":E['globe'], "indian_video":E['film'], "playlist":E['note'],
        "artist":E['mic'],
    }
    icon = ci.get(category, E['mag'])

    # Header
    header = (
        f"\n{T}\n"
        f"{V}  {icon} {bold_s(category.upper().replace('_',' '))} {bold_s('RESULTS')} {icon}\n"
        f"{B}\n\n"
        f"{E['mag']} {bold_s('Query')}: {script_s(query)}\n"
        f"{E['pack']} {bold_s('Found')}: {bold_s(str(len(results)))} {ital_s('results')}\n\n"
        f"{SP}\n"
    )
    await bot.send_message(chat_id=cid, text=header)

    sent = 0
    for i, r in enumerate(results):
        try:
            rt = r.get("type", "")

            # ═══════════════════════════════════
            # 🎵 INDIAN SONG (JioSaavn with audio!)
            # ═══════════════════════════════════
            if rt == "indian_song":
                audio_url = r.get("audio_url", "")
                img_url = r.get("image_url", "")
                title = r.get("title", "Unknown")
                artist = r.get("artist", "Unknown")
                album = r.get("album", "")
                dur = format_duration(r.get("duration", 0))
                lang = r.get("language", "Hindi")
                plays = r.get("play_count", "")
                label = r.get("label", "")
                year = r.get("year", "")
                explicit = r.get("explicit", False)

                cap = (
                    f"{E['india']} {E['music']} {bold_s(title)}\n"
                    f"{FL}\n"
                    f"{E['mic']} {ital_s('Artist')}: {bold_s(artist)}\n"
                )
                if album:
                    cap += f"{E['disk']} {ital_s('Album')}: {bold_s(album)}\n"
                cap += (
                    f"{E['bolt']} {ital_s('Duration')}: {mono_s(dur)}\n"
                    f"{E['om']} {ital_s('Language')}: {bold_s(lang)}\n"
                )
                if year:
                    cap += f"{E['star3']} {ital_s('Year')}: {bold_s(str(year))}\n"
                if plays:
                    cap += f"{E['fire']} {ital_s('Plays')}: {bold_s(str(plays))}\n"
                if label:
                    cap += f"{E['vinyl']} {ital_s('Label')}: {mono_s(label)}\n"
                if explicit:
                    cap += f"{E['warn']} {mono_s('EXPLICIT')}\n"
                cap += (
                    f"{E['globe']} {ital_s('Source')}: {bold_s('JioSaavn')} {E['india']}\n"
                    f"{ML}"
                )

                if audio_url:
                    # Send as AUDIO in Telegram!
                    success = await dl.send_audio(bot, cid, audio_url, cap, title, artist, img_url)
                    if success:
                        sent += 1
                    elif img_url:
                        await dl.send_photo(bot, cid, img_url, cap)
                        sent += 1
                elif img_url:
                    cap += f"\n{E['warn']} {ital_s('Audio not available for this track')}"
                    await dl.send_photo(bot, cid, img_url, cap)
                    sent += 1

            # ═══════════════════════════════════
            # 💿 ALBUM
            # ═══════════════════════════════════
            elif rt == "album":
                img_url = r.get("image_url", "")
                cap = (
                    f"{E['india']} {E['disk']} {bold_s(r.get('title','Unknown'))}\n"
                    f"{FL}\n"
                    f"{E['mic']} {ital_s('Artist')}: {bold_s(r.get('artist','Unknown'))}\n"
                    f"{E['star3']} {ital_s('Year')}: {bold_s(str(r.get('year','')))}\n"
                    f"{E['music']} {ital_s('Songs')}: {bold_s(str(r.get('song_count',0)))}\n"
                    f"{E['om']} {ital_s('Language')}: {bold_s(r.get('language',''))}\n"
                    f"{E['globe']} {ital_s('Source')}: {bold_s('JioSaavn')} {E['india']}\n"
                    f"{ML}"
                )
                if img_url:
                    await dl.send_photo(bot, cid, img_url, cap)
                else:
                    await bot.send_message(chat_id=cid, text=cap)
                sent += 1

                # Show button to get album songs
                kb = [[InlineKeyboardButton(
                    f"{E['music']} {bold_s('Get All Songs')}",
                    callback_data=f"album|{r.get('album_id','')}"
                )]]
                await bot.send_message(
                    chat_id=cid,
                    text=f"{E['point']} {ital_s('Click to download all songs from this album')}",
                    reply_markup=InlineKeyboardMarkup(kb)
                )

            # ═══════════════════════════════════
            # 🎤 ARTIST INFO
            # ═══════════════════════════════════
            elif rt == "artist_info":
                img_url = r.get("image_url", "")
                cap = (
                    f"{E['india']} {E['mic']} {bold_s(r.get('title','Unknown'))}\n"
                    f"{FL}\n"
                    f"{E['star3']} {ital_s('Role')}: {bold_s(r.get('role','Artist'))}\n"
                    f"{E['globe']} {ital_s('Source')}: {bold_s('JioSaavn')} {E['india']}\n"
                    f"{ML}"
                )
                if img_url:
                    await dl.send_photo(bot, cid, img_url, cap)
                else:
                    await bot.send_message(chat_id=cid, text=cap)
                sent += 1

            # ═══════════════════════════════════
            # 🎵 SPOTIFY TRACK (30s preview)
            # ═══════════════════════════════════
            elif rt == "spotify_track":
                preview = r.get("preview_url", "")
                img_url = r.get("image_url", "")
                title = r.get("title", "Unknown")
                artist = r.get("artist", "Unknown")
                pop = r.get("popularity", 0)
                pop_bar = make_progress_bar(pop, 100, 10)

                cap = (
                    f"{E['head']} {bold_s(title)}\n"
                    f"{DL}\n"
                    f"{E['mic']} {ital_s('Artist')}: {bold_s(artist)}\n"
                    f"{E['disk']} {ital_s('Album')}: {bold_s(r.get('album',''))}\n"
                    f"{E['bolt']} {ital_s('Duration')}: {mono_s(format_duration(r.get('duration',0)))}\n"
                    f"{E['fire']} {ital_s('Popularity')}: [{pop_bar}] {bold_s(str(pop))}%\n"
                    f"{E['star3']} {ital_s('Released')}: {bold_s(r.get('release_date',''))}\n"
                    f"{E['globe']} {ital_s('Source')}: {bold_s('Spotify')}\n"
                    f"{ML}"
                )
                if r.get("explicit"):
                    cap += f"\n{E['warn']} {mono_s('EXPLICIT')}"

                if preview:
                    cap_audio = cap + f"\n{E['head']} {ital_s('30 second preview')}"
                    success = await dl.send_audio(bot, cid, preview, cap_audio, title, artist, img_url)
                    if success:
                        sent += 1
                        continue
                if img_url:
                    await dl.send_photo(bot, cid, img_url, cap)
                    sent += 1

            # ═══════════════════════════════════
            # 🎵 ARCHIVE AUDIO
            # ═══════════════════════════════════
            elif rt == "audio":
                audio_url = r.get("audio_url", "")
                cap = (
                    f"{E['music']} {bold_s(r.get('title','Audio')[:60])}\n"
                    f"{DL}\n"
                    f"{E['mic']} {ital_s('Artist')}: {bold_s(r.get('artist','Unknown')[:30])}\n"
                    f"{E['recv']} {ital_s('Downloads')}: {bold_s(str(r.get('downloads',0)))}\n"
                    f"{E['globe']} {ital_s('Source')}: {bold_s(r.get('source',''))}\n"
                    f"{ML}"
                )
                if audio_url:
                    success = await dl.send_audio(bot, cid, audio_url, cap, r.get("title",""), r.get("artist",""))
                    if success:
                        sent += 1
                    else:
                        thumb = r.get("thumbnail", "")
                        if thumb:
                            cap += f"\n{E['warn']} {ital_s('File too large for Telegram')}"
                            await dl.send_photo(bot, cid, thumb, cap)
                            sent += 1

            # ═══════════════════════════════════
            # 🎬 VIDEO
            # ═══════════════════════════════════
            elif rt == "video":
                vid_url = r.get("video_url", "")
                thumb = r.get("thumbnail", "")
                cap = (
                    f"{E['film']} {bold_s(r.get('title','Video')[:60])}\n"
                    f"{DL}\n"
                    f"{E['art']} {ital_s('By')}: {bold_s(r.get('creator','Unknown')[:30])}\n"
                    f"{E['recv']} {ital_s('Downloads')}: {bold_s(str(r.get('downloads',0)))}\n"
                    f"{E['globe']} {ital_s('Source')}: {bold_s(r.get('source',''))}\n"
                    f"{L2}"
                )
                if vid_url:
                    success = await dl.send_video(bot, cid, vid_url, cap, thumb)
                    if success:
                        sent += 1
                    elif thumb:
                        cap += f"\n{E['warn']} {ital_s('Video too large, showing preview')}"
                        await dl.send_photo(bot, cid, thumb, cap)
                        sent += 1
                elif thumb:
                    await dl.send_photo(bot, cid, thumb, cap)
                    sent += 1

            # ═══════════════════════════════════
            # 🖼️ IMAGE
            # ═══════════════════════════════════
            elif rt == "image":
                img_url = r.get("image_url","") or r.get("thumbnail","")
                if not img_url: continue
                cap = (
                    f"{E['frame']} {bold_s(r.get('title','Image')[:60])}\n"
                    f"{DL}\n"
                    f"{E['art']} {ital_s('By')}: {bold_s(r.get('creator','Unknown')[:30])}\n"
                )
                if r.get("resolution"):
                    cap += f"{E['tv']} {ital_s('Resolution')}: {bold_s(r.get('resolution',''))}\n"
                cap += (
                    f"{E['globe']} {ital_s('Source')}: {bold_s(r.get('source',''))}\n"
                    f"{L2}"
                )
                await dl.send_photo(bot, cid, img_url, cap)
                sent += 1

            # ═══════════════════════════════════
            # 🌸 ANIME
            # ═══════════════════════════════════
            elif rt == "anime":
                img_url = r.get("image_url","")
                if not img_url: continue
                score = r.get("score","N/A")
                bar = make_progress_bar(score if score != "N/A" else 0)
                cap = (
                    f"{E['anime']} {bold_s(r.get('title','')[:50])}\n"
                )
                if r.get("title_jp"):
                    cap += f"   {ital_s(r.get('title_jp','')[:40])}\n"
                cap += (
                    f"{DL}\n"
                    f"{E['star2']} {ital_s('Score')}: {bold_s(str(score))} [{bar}]\n"
                    f"{E['tv']} {ital_s('Episodes')}: {bold_s(str(r.get('episodes','?')))}\n"
                    f"{E['bolt']} {ital_s('Status')}: {bold_s(r.get('status',''))}\n"
                )
                if r.get("genres"):
                    cap += f"{E['puzzle']} {ital_s('Genres')}: {mono_s(r.get('genres',''))}\n"
                if r.get("synopsis"):
                    cap += f"{DL}\n{ital_s(r.get('synopsis','')[:200])}\n"
                cap += f"\n{E['globe']} {ital_s('Source')}: {bold_s(r.get('source',''))}\n{L2}"
                if len(cap) > 1024: cap = cap[:1020] + "..."
                await dl.send_photo(bot, cid, img_url, cap)
                sent += 1

            # ═══════════════════════════════════
            # 📚 BOOK
            # ═══════════════════════════════════
            elif rt == "book":
                cap = (
                    f"{E['books']} {bold_s(r.get('title','')[:60])}\n"
                    f"{DL}\n"
                    f"{E['art']} {ital_s('Author')}: {bold_s(r.get('creator','')[:40])}\n"
                    f"{E['recv']} {ital_s('Downloads')}: {bold_s(str(r.get('downloads',0)))}\n"
                    f"{E['globe']} {ital_s('Source')}: {bold_s(r.get('source',''))}\n{L2}"
                )
                cover = r.get("cover_url","")
                if cover:
                    await dl.send_photo(bot, cid, cover, cap)
                    sent += 1
                epub = r.get("epub_url","")
                if epub:
                    fcap = f"{E['books']} {bold_s(r.get('title','')[:50])}\n{E['pack']} {ital_s('EPUB')}"
                    safe = re.sub(r'[^\w\s-]','',r.get('title','book'))[:50]
                    await dl.send_doc(bot, cid, epub, fcap, f"{safe}.epub")
                    sent += 1

            # ═══════════════════════════════════
            # 💻 CODE
            # ═══════════════════════════════════
            elif rt == "code":
                cap = (
                    f"{E['code']} {bold_s(r.get('title','')[:50])}\n"
                    f"{DL}\n"
                    f"{E['star2']} {ital_s('Stars')}: {bold_s(str(r.get('stars',0)))} "
                    f"{E['dot']} {ital_s('Forks')}: {bold_s(str(r.get('forks',0)))}\n"
                    f"{E['bolt']} {ital_s('Language')}: {bold_s(str(r.get('language','N/A')))}\n"
                    f"{DL}\n{ital_s(r.get('desc','')[:150])}\n"
                    f"\n{E['globe']} {bold_s('GitHub')}\n{L2}"
                )
                avatar = r.get("avatar_url","")
                if avatar:
                    await dl.send_photo(bot, cid, avatar, cap)
                else:
                    await bot.send_message(chat_id=cid, text=cap)
                sent += 1

            # ═══════════════════════════════════
            # 📖 WIKI
            # ═══════════════════════════════════
            elif rt == "wiki":
                img = r.get("image_url","")
                cap = (
                    f"{E['book']} {bold_s(r.get('title','')[:50])}\n"
                    f"{DL}\n{ital_s(r.get('extract','')[:400])}\n"
                    f"\n{E['globe']} {bold_s('Wikipedia')}\n{L2}"
                )
                if len(cap) > 1024: cap = cap[:1020] + "..."
                if img:
                    await dl.send_photo(bot, cid, img, cap)
                else:
                    await bot.send_message(chat_id=cid, text=cap)
                sent += 1

            # ═══════════════════════════════════
            # LAST.FM TRACK
            # ═══════════════════════════════════
            elif rt == "lastfm_track":
                img = r.get("image_url", "")
                cap = (
                    f"{E['head']} {bold_s(r.get('title','')[:50])}\n"
                    f"{DL}\n"
                    f"{E['mic']} {ital_s('Artist')}: {bold_s(r.get('artist',''))}\n"
                    f"{E['eye']} {ital_s('Listeners')}: {bold_s(r.get('listeners','0'))}\n"
                    f"{E['globe']} {bold_s('Last.fm')}\n{ML}"
                )
                if img:
                    await dl.send_photo(bot, cid, img, cap)
                else:
                    await bot.send_message(chat_id=cid, text=cap)
                sent += 1

            await asyncio.sleep(0.5)

        except Exception as ex:
            logger.error(f"Send result {i} error: {ex}")
            continue

    # Footer
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton(f"⬅️ Page {page-1}", callback_data=f"p|{category}|{query[:30]}|{page-1}"))
    nav.append(InlineKeyboardButton(f"➡️ Page {page+1}", callback_data=f"p|{category}|{query[:30]}|{page+1}"))

    footer = (
        f"\n{L2}\n"
        f"{E['check']} {bold_s('Sent')}: {bold_s(str(sent))}/{len(results)}\n"
        f"{E['spark']} {ital_s('Page')} {bold_s(str(page))}\n"
        f"{L3}\n"
    )
    kb = [
        nav,
        [
            InlineKeyboardButton(f"{E['folder']} Menu", callback_data="menu_cat"),
            InlineKeyboardButton(f"{E['india']} Home", callback_data="menu_home"),
        ]
    ]
    await bot.send_message(chat_id=cid, text=footer, reply_markup=InlineKeyboardMarkup(kb))


# ══════════════════════════════════════════
#  𝗙𝗘𝗧𝗖𝗛 𝗥𝗘𝗦𝗨𝗟𝗧𝗦
# ══════════════════════════════════════════

async def fetch(query, cat, page=1):
    if cat == "song":
        return await search_jiosaavn(query, 8)
    elif cat == "album":
        return await get_jiosaavn_album(query, 5)
    elif cat == "playlist":
        return await search_jiosaavn_playlists(query, 5)
    elif cat == "artist":
        return await search_jiosaavn_artists(query, 5)
    elif cat == "bollywood":
        r1 = await search_jiosaavn(f"{query} bollywood", 5)
        r2 = await search_archive_indian_video(query, 3, page)
        return r1 + r2
    elif cat == "indian_music":
        r1 = await search_jiosaavn(query, 5)
        r2 = await search_archive_indian_audio(query, 3, page)
        r3 = await search_spotify(query, 2) if SPOTIFY_CLIENT_ID else []
        r4 = await search_lastfm(query, 2) if LASTFM_API_KEY else []
        return r1 + r2 + r3 + r4
    elif cat == "indian_video":
        return await search_archive_indian_video(query, 5, page)
    elif cat == "images":
        r1 = await search_openverse(query, page, 4)
        r2 = await search_nasa(query, 2)
        return r1 + r2
    elif cat == "wallpapers":
        return await search_wallhaven(query, page, 6)
    elif cat == "anime":
        return await search_anime(query, 5)
    elif cat == "books":
        return await search_gutenberg(query, 5, page)
    elif cat == "code":
        return await search_github(query, 5)
    elif cat == "waifu":
        urls = await get_waifu_many(query or "waifu", 5)
        return [{"type":"image","title":f"Waifu {query}","image_url":u,
                "creator":"waifu.pics","source":"waifu.pics"} for u in urls]
    elif cat == "wiki":
        return await search_wikipedia(query, 3)
    elif cat == "nasa":
        return await search_nasa(query, 5)
    elif cat == "all":
        tasks = [
            search_jiosaavn(query, 3),
            search_openverse(query, 1, 2),
            search_anime(query, 2),
            search_gutenberg(query, 2),
        ]
        gathered = await asyncio.gather(*tasks, return_exceptions=True)
        all_r = []
        for r in gathered:
            if isinstance(r, list): all_r.extend(r)
        return all_r
    return []


# ══════════════════════════════════════════
#  𝗕𝗢𝗧 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦
# ══════════════════════════════════════════

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name or "User"
    txt = (
        f"\n{T}\n"
        f"{V}  {E['crown']} {neg_sq('INDIAN MEDIA BOT')} {E['crown']}\n"
        f"{B}\n\n"
        f"{E['spark']} {script_s('Namaste')}, {bold_s(name)}! {E['namaste']}\n\n"
        f"{IL}\n\n"
        f"{E['india']} {bold_s('INDIAN MUSIC')} {E['sitar']}\n"
        f"  {E['music']} {bold_s('Songs')} — {ital_s('JioSaavn, Spotify, Last.fm')}\n"
        f"  {E['disk']} {bold_s('Albums')} — {ital_s('Full album songs download')}\n"
        f"  {E['note']} {bold_s('Playlists')} — {ital_s('Curated playlists')}\n"
        f"  {E['mic']} {bold_s('Artists')} — {ital_s('Artist info & songs')}\n"
        f"  {E['film']} {bold_s('Bollywood')} — {ital_s('Movie songs + videos')}\n"
        f"  {E['head']} {bold_s('Lyrics')} — {ital_s('Song lyrics')}\n\n"
        f"{IL}\n\n"
        f"{E['globe']} {bold_s('WORLD MEDIA')} {E['spark']}\n"
        f"  {E['frame']} {bold_s('Images')} — {ital_s('800M+ Openverse, NASA')}\n"
        f"  {E['wall']} {bold_s('Wallpapers')} — {ital_s('Wallhaven HD/4K')}\n"
        f"  {E['anime']} {bold_s('Anime')} — {ital_s('MAL + Waifu')}\n"
        f"  {E['books']} {bold_s('Books')} — {ital_s('70K+ free ebooks')}\n"
        f"  {E['code']} {bold_s('Code')} — {ital_s('GitHub repos')}\n"
        f"  {E['rocket']} {bold_s('NASA')} — {ital_s('Space media')}\n"
        f"  {E['book']} {bold_s('Wikipedia')} — {ital_s('Articles')}\n\n"
        f"{L2}\n\n"
        f"{E['bolt']} {bital_s('SAB KUCH TELEGRAM MEIN!')}\n"
        f"{E['bolt']} {bital_s('SONGS AUDIO MEIN AYENGE!')}\n"
        f"{E['bolt']} {bital_s('NO LINKS - DIRECT PLAY!')}\n\n"
        f"{E['arrow']} {bold_s('Just type song name!')}\n"
        f"   {ital_s('Example: Tum Hi Ho')}\n\n"
        f"{L3}\n"
    )

    kb = [
        [InlineKeyboardButton(f"{E['mag']} {bold_s('Search All')}", callback_data="cat|all")],
        [
            InlineKeyboardButton(f"{E['music']} Song", callback_data="cat|song"),
            InlineKeyboardButton(f"{E['disk']} Album", callback_data="cat|album"),
            InlineKeyboardButton(f"{E['mic']} Artist", callback_data="cat|artist"),
        ],
        [
            InlineKeyboardButton(f"{E['film']} Bollywood", callback_data="cat|bollywood"),
            InlineKeyboardButton(f"{E['sitar']} Indian", callback_data="cat|indian_music"),
            InlineKeyboardButton(f"{E['note']} Playlist", callback_data="cat|playlist"),
        ],
        [
            InlineKeyboardButton(f"{E['frame']} Images", callback_data="cat|images"),
            InlineKeyboardButton(f"{E['wall']} Walls", callback_data="cat|wallpapers"),
            InlineKeyboardButton(f"{E['anime']} Anime", callback_data="cat|anime"),
        ],
        [
            InlineKeyboardButton(f"{E['books']} Books", callback_data="cat|books"),
            InlineKeyboardButton(f"{E['code']} Code", callback_data="cat|code"),
            InlineKeyboardButton(f"{E['cherry']} Waifu", callback_data="cat|waifu"),
        ],
        [
            InlineKeyboardButton(f"{E['rocket']} NASA", callback_data="cat|nasa"),
            InlineKeyboardButton(f"{E['book']} Wiki", callback_data="cat|wiki"),
            InlineKeyboardButton(f"{E['dice']} Random", callback_data="random"),
        ],
        [InlineKeyboardButton(f"❓ {bold_s('Help')}", callback_data="help")],
    ]
    await update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = (
        f"\n{T}\n{V}  {E['book']} {bold_s('HELP')} {E['book']}\n{B}\n\n"
        f"{E['india']} {bold_s('INDIAN MUSIC COMMANDS')}:\n\n"
        f"  {E['tri']} /song {ital_s('name')} — {ital_s('Indian songs')}\n"
        f"  {E['tri']} /album {ital_s('name')} — {ital_s('Full album')}\n"
        f"  {E['tri']} /artist {ital_s('name')} — {ital_s('Artist search')}\n"
        f"  {E['tri']} /bollywood {ital_s('query')} — {ital_s('Bollywood')}\n"
        f"  {E['tri']} /lyrics {ital_s('song')} — {ital_s('Song lyrics')}\n"
        f"  {E['tri']} /playlist {ital_s('name')} — {ital_s('Playlists')}\n"
        f"  {E['tri']} /hindi {ital_s('query')} — {ital_s('Hindi songs')}\n"
        f"  {E['tri']} /punjabi {ital_s('query')} — {ital_s('Punjabi songs')}\n"
        f"  {E['tri']} /tamil {ital_s('query')} — {ital_s('Tamil songs')}\n"
        f"  {E['tri']} /telugu {ital_s('query')} — {ital_s('Telugu songs')}\n\n"
        f"{L2}\n\n"
        f"{E['globe']} {bold_s('OTHER COMMANDS')}:\n\n"
        f"  {E['tri']} /search {ital_s('query')} — {ital_s('All databases')}\n"
        f"  {E['tri']} /image {ital_s('query')} — {ital_s('Photos')}\n"
        f"  {E['tri']} /wallpaper {ital_s('query')} — {ital_s('Wallpapers')}\n"
        f"  {E['tri']} /anime {ital_s('query')} — {ital_s('Anime')}\n"
        f"  {E['tri']} /waifu {ital_s('cat')} — {ital_s('Anime images')}\n"
        f"  {E['tri']} /book {ital_s('query')} — {ital_s('Free ebooks')}\n"
        f"  {E['tri']} /code {ital_s('query')} — {ital_s('GitHub')}\n"
        f"  {E['tri']} /nasa {ital_s('query')} — {ital_s('Space')}\n"
        f"  {E['tri']} /wiki {ital_s('query')} — {ital_s('Wikipedia')}\n"
        f"  {E['tri']} /random — {ital_s('Random discovery')}\n\n"
        f"{L2}\n\n"
        f"{E['spark']} {bital_s('PRO TIPS')}:\n"
        f"  {E['dot']} {ital_s('Sirf gaane ka naam likho, audio aayega!')}\n"
        f"  {E['dot']} {ital_s('Album search karo, saare gaane milenge!')}\n"
        f"  {E['dot']} {ital_s('Hindi, Punjabi, Tamil, Telugu sab hai!')}\n\n"
        f"{L3}\n"
    )
    kb = [[InlineKeyboardButton(f"{E['arrow2']} Back", callback_data="menu_home")]]
    if update.callback_query:
        await update.callback_query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))


async def do_search(update, ctx, query, cat):
    if not query:
        UD[update.effective_user.id] = {"cat": cat}
        cat_names = {
            "song":"🎵 Indian Song","album":"💿 Album","artist":"🎤 Artist",
            "bollywood":"🎬 Bollywood","indian_music":"🇮🇳 Indian Music",
            "playlist":"🎶 Playlist","images":"🖼️ Images","wallpapers":"🌄 Wallpapers",
            "anime":"🌸 Anime","books":"📚 Books","code":"💻 Code",
            "waifu":"🌸 Waifu","nasa":"🚀 NASA","wiki":"📖 Wiki","all":"🌍 All",
        }
        txt = (
            f"\n{L2}\n"
            f"{E['mag']} {bold_s(cat_names.get(cat, cat.upper()))}\n\n"
            f"{E['arrow']} {ital_s('Apna search query type karo!')}\n"
            f"{E['dot']} {bital_s('Telegram mein hi result aayega!')}\n"
            f"{L2}\n"
        )
        await update.message.reply_text(txt)
        return

    await update.message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
    loading = (
        f"\n{E['bolt']} {bold_s('Searching')}...\n"
        f"{E['mag']} {script_s(query)}\n"
        f"{SP}\n"
    )
    msg = await update.message.reply_text(loading)
    results = await fetch(query, cat)
    try: await msg.delete()
    except: pass
    await send_results(ctx.bot, update.effective_chat.id, results, query, cat)


# Individual commands
async def cmd_search(u, c):
    await do_search(u, c, " ".join(c.args) if c.args else "", "all")

async def cmd_song(u, c):
    await do_search(u, c, " ".join(c.args) if c.args else "", "song")

async def cmd_album(u, c):
    await do_search(u, c, " ".join(c.args) if c.args else "", "album")

async def cmd_artist(u, c):
    await do_search(u, c, " ".join(c.args) if c.args else "", "artist")

async def cmd_bollywood(u, c):
    await do_search(u, c, " ".join(c.args) if c.args else "", "bollywood")

async def cmd_playlist(u, c):
    await do_search(u, c, " ".join(c.args) if c.args else "", "playlist")

async def cmd_hindi(u, c):
    q = " ".join(c.args) if c.args else ""
    await do_search(u, c, f"{q} hindi" if q else "", "song")

async def cmd_punjabi(u, c):
    q = " ".join(c.args) if c.args else ""
    await do_search(u, c, f"{q} punjabi" if q else "", "song")

async def cmd_tamil(u, c):
    q = " ".join(c.args) if c.args else ""
    await do_search(u, c, f"{q} tamil" if q else "", "song")

async def cmd_telugu(u, c):
    q = " ".join(c.args) if c.args else ""
    await do_search(u, c, f"{q} telugu" if q else "", "song")

async def cmd_image(u, c):
    await do_search(u, c, " ".join(c.args) if c.args else "", "images")

async def cmd_wallpaper(u, c):
    await do_search(u, c, " ".join(c.args) if c.args else "", "wallpapers")

async def cmd_anime(u, c):
    await do_search(u, c, " ".join(c.args) if c.args else "", "anime")

async def cmd_book(u, c):
    await do_search(u, c, " ".join(c.args) if c.args else "", "books")

async def cmd_code(u, c):
    await do_search(u, c, " ".join(c.args) if c.args else "", "code")

async def cmd_nasa(u, c):
    await do_search(u, c, " ".join(c.args) if c.args else "", "nasa")

async def cmd_wiki(u, c):
    await do_search(u, c, " ".join(c.args) if c.args else "", "wiki")

async def cmd_waifu(u: Update, c: ContextTypes.DEFAULT_TYPE):
    cat = c.args[0] if c.args else "waifu"
    valid = ["waifu","neko","shinobu","megumin","hug","pat","smile",
             "wave","dance","kiss","blush","happy","wink","cry","cuddle","awoo"]
    if cat.lower() not in valid:
        txt = f"\n{E['cherry']} {bold_s('WAIFU CATEGORIES')}\n{DL}\n\n"
        for i in range(0, len(valid), 4):
            txt += "  " + "  ".join([f"{E['cherry']} {mono_s(v)}" for v in valid[i:i+4]]) + "\n"
        txt += f"\n{E['arrow']} /waifu {mono_s('category')}\n{L2}"
        await u.message.reply_text(txt)
        return
    await u.message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
    urls = await get_waifu_many(cat.lower(), 5)
    if not urls:
        await u.message.reply_text(f"{E['cross']} {bold_s('No images found')}")
        return
    for i, url in enumerate(urls):
        cap = f"{E['cherry']} {bold_s(f'Waifu {cat.title()}')} #{i+1}\n{E['globe']} {bold_s('waifu.pics')}\n{L2}"
        await dl.send_photo(c.bot, u.effective_chat.id, url, cap)
        await asyncio.sleep(0.3)
    kb = [[InlineKeyboardButton(f"{E['cherry']} More", callback_data=f"waifu|{cat}")]]
    await c.bot.send_message(chat_id=u.effective_chat.id,
        text=f"{E['check']} {bold_s('5 sent!')} {ital_s('More?')}",
        reply_markup=InlineKeyboardMarkup(kb))


async def cmd_lyrics(u: Update, c: ContextTypes.DEFAULT_TYPE):
    """Get lyrics for a song"""
    q = " ".join(c.args) if c.args else ""
    if not q:
        await u.message.reply_text(f"{E['arrow']} /lyrics {ital_s('song name')}")
        return

    await u.message.reply_chat_action(ChatAction.TYPING)
    msg = await u.message.reply_text(f"{E['bolt']} {bold_s('Finding lyrics')}...")

    songs = await search_jiosaavn(q, 1)
    if not songs:
        await msg.edit_text(f"{E['cross']} {bold_s('Song not found')}")
        return

    song = songs[0]
    sid = song.get("song_id", "")
    title = song.get("title", "Unknown")
    artist = song.get("artist", "Unknown")

    lyrics = ""
    if sid:
        lyrics = await get_jiosaavn_lyrics(sid)

    if not lyrics:
        await msg.edit_text(f"{E['cross']} {bold_s('Lyrics not available for')} {ital_s(title)}")
        return

    txt = (
        f"\n{T}\n"
        f"{V}  {E['scroll']} {bold_s('LYRICS')} {E['scroll']}\n"
        f"{B}\n\n"
        f"{E['music']} {bold_s(title)}\n"
        f"{E['mic']} {ital_s(artist)}\n\n"
        f"{FL}\n\n"
        f"{lyrics}\n\n"
        f"{FL}\n"
        f"{E['globe']} {bold_s('JioSaavn')} {E['india']}\n"
        f"{L3}\n"
    )

    # Split if too long
    if len(txt) > 4096:
        parts = [txt[i:i+4000] for i in range(0, len(txt), 4000)]
        await msg.delete()
        for part in parts:
            await c.bot.send_message(chat_id=u.effective_chat.id, text=part)
    else:
        await msg.edit_text(txt)

    # Also send the song
    if song.get("audio_url") and song.get("image_url"):
        cap = f"{E['music']} {bold_s(title)}\n{E['mic']} {ital_s(artist)}\n{ML}"
        await dl.send_audio(c.bot, u.effective_chat.id, song["audio_url"], cap, title, artist, song["image_url"])


async def cmd_random(u: Update, c: ContextTypes.DEFAULT_TYPE):
    indian_q = ["Arijit Singh","Tum Hi Ho","Kal Ho Na Ho","Chaiyya Chaiyya",
                "Dil Se","Kabira","Channa Mereya","Tere Bina","Kun Faya",
                "Kesariya","Raataan Lambiyan","Pasoori","Excuses","Brown Munde",
                "Laung Laachi","Naatu Naatu","Pushpa","Srivalli","Jai Ho"]
    world_q = ["nature","space","galaxy","sunset","ocean","cyberpunk"]
    cats = ["song","song","song","wallpapers","anime","images"]

    q = random.choice(indian_q + world_q)
    cat = "song" if q in indian_q else random.choice(cats)

    txt = f"\n{E['dice']} {bold_s('RANDOM')}\n{E['mag']} {ital_s(q)}\n{SP}\n"
    await u.message.reply_text(txt)
    await u.message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
    results = await fetch(q, cat)
    await send_results(c.bot, u.effective_chat.id, results, q, cat)


# ── Callback Handler ──

async def cb_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    uid = update.effective_user.id
    cid = update.effective_chat.id

    if data == "menu_home":
        try: await q.message.delete()
        except: pass
        update.message = q.message
        await cmd_start(update, ctx)

    elif data == "menu_cat":
        txt = (
            f"\n{T}\n{V}  {E['folder']} {bold_s('CATEGORIES')} {E['folder']}\n{B}\n\n"
            f"{E['arrow']} {ital_s('Choose:')}\n{L2}\n"
        )
        kb = [
            [
                InlineKeyboardButton(f"{E['music']} Song", callback_data="cat|song"),
                InlineKeyboardButton(f"{E['disk']} Album", callback_data="cat|album"),
                InlineKeyboardButton(f"{E['mic']} Artist", callback_data="cat|artist"),
            ],
            [
                InlineKeyboardButton(f"{E['film']} Bollywood", callback_data="cat|bollywood"),
                InlineKeyboardButton(f"{E['sitar']} Indian", callback_data="cat|indian_music"),
                InlineKeyboardButton(f"{E['note']} Playlist", callback_data="cat|playlist"),
            ],
            [
                InlineKeyboardButton(f"{E['frame']} Images", callback_data="cat|images"),
                InlineKeyboardButton(f"{E['wall']} Walls", callback_data="cat|wallpapers"),
                InlineKeyboardButton(f"{E['anime']} Anime", callback_data="cat|anime"),
            ],
            [
                InlineKeyboardButton(f"{E['books']} Books", callback_data="cat|books"),
                InlineKeyboardButton(f"{E['code']} Code", callback_data="cat|code"),
                InlineKeyboardButton(f"{E['cherry']} Waifu", callback_data="cat|waifu"),
            ],
            [
                InlineKeyboardButton(f"{E['rocket']} NASA", callback_data="cat|nasa"),
                InlineKeyboardButton(f"{E['book']} Wiki", callback_data="cat|wiki"),
            ],
            [InlineKeyboardButton(f"{E['arrow2']} Home", callback_data="menu_home")],
        ]
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb))

    elif data == "help":
        await cmd_help(update, ctx)

    elif data == "random":
        try: await q.message.delete()
        except: pass
        update.message = q.message
        await cmd_random(update, ctx)

    elif data.startswith("cat|"):
        cat = data.split("|")[1]
        UD[uid] = {"cat": cat}

        if cat == "waifu":
            valid = ["waifu","neko","shinobu","megumin","hug","pat",
                     "smile","wave","dance","kiss","blush","happy","wink","cry"]
            txt = f"\n{E['cherry']} {bold_s('WAIFU')}\n{DL}\n"
            kb = []
            for i in range(0, len(valid), 3):
                kb.append([InlineKeyboardButton(f"{E['cherry']} {v.title()}", callback_data=f"waifu|{v}") for v in valid[i:i+3]])
            kb.append([InlineKeyboardButton(f"{E['arrow2']} Back", callback_data="menu_cat")])
            await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb))
        else:
            hints = {
                "song":"Arijit Singh, Tum Hi Ho, Kesariya",
                "album":"Kabir Singh, Rockstar, Aashiqui 2",
                "artist":"Arijit Singh, Shreya Ghoshal, AP Dhillon",
                "bollywood":"Dilwale, Jawan, Pathaan",
                "indian_music":"ghazal, qawwali, classical",
                "playlist":"romantic, party, sad",
            }
            hint = hints.get(cat, "anything you want")
            txt = (
                f"\n{L2}\n"
                f"{E['mag']} {bold_s(cat.upper().replace('_',' '))}\n\n"
                f"{E['arrow']} {ital_s('Type your query:')}\n"
                f"{E['dot']} {ital_s('Example')}: {mono_s(hint)}\n"
                f"{E['bolt']} {bital_s('Audio directly Telegram mein!')}\n"
                f"{L2}\n"
            )
            kb = [[InlineKeyboardButton(f"{E['arrow2']} Back", callback_data="menu_cat")]]
            await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("waifu|"):
        wcat = data.split("|")[1]
        try: await q.message.delete()
        except: pass
        await ctx.bot.send_chat_action(chat_id=cid, action=ChatAction.UPLOAD_PHOTO)
        urls = await get_waifu_many(wcat, 5)
        for i, url in enumerate(urls):
            cap = f"{E['cherry']} {bold_s(f'Waifu {wcat.title()}')} #{i+1}\n{E['globe']} {bold_s('waifu.pics')}\n{L2}"
            await dl.send_photo(ctx.bot, cid, url, cap)
            await asyncio.sleep(0.3)
        kb = [
            [InlineKeyboardButton(f"{E['cherry']} More", callback_data=f"waifu|{wcat}")],
            [InlineKeyboardButton(f"{E['arrow2']} Back", callback_data="cat|waifu")],
        ]
        await ctx.bot.send_message(chat_id=cid,
            text=f"{E['check']} {bold_s('5 sent!')}",
            reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("album|"):
        album_id = data.split("|")[1]
        try: await q.message.delete()
        except: pass
        await ctx.bot.send_chat_action(chat_id=cid, action=ChatAction.UPLOAD_PHOTO)

        txt = f"{E['bolt']} {bold_s('Loading album songs')}..."
        await ctx.bot.send_message(chat_id=cid, text=txt)

        songs = await get_jiosaavn_album_songs(album_id)
        if songs:
            await send_results(ctx.bot, cid, songs, "album", "song")
        else:
            await ctx.bot.send_message(chat_id=cid, text=f"{E['cross']} {bold_s('Album songs not found')}")

    elif data.startswith("p|"):
        parts = data.split("|")
        if len(parts) >= 4:
            cat = parts[1]
            query = parts[2]
            pg = int(parts[3])
            try: await q.message.delete()
            except: pass
            await ctx.bot.send_chat_action(chat_id=cid, action=ChatAction.UPLOAD_PHOTO)
            results = await fetch(query, cat, pg)
            await send_results(ctx.bot, cid, results, query, cat, pg)


# ── Text Handler ──

async def text_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    txt = update.message.text.strip()
    if txt.startswith("/"):
        return

    uid = update.effective_user.id
    cat = UD.get(uid, {}).get("cat", "song")  # Default = Indian song!

    await update.message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
    loading = f"\n{E['bolt']} {bold_s('Searching')}...\n{E['mag']} {script_s(txt)}\n{SP}\n"
    msg = await update.message.reply_text(loading)
    results = await fetch(txt, cat)
    try: await msg.delete()
    except: pass
    await send_results(ctx.bot, update.effective_chat.id, results, txt, cat)


# ══════════════════════════════════════════
#  🌐 RENDER WEB SERVER
# ══════════════════════════════════════════

async def health(req):
    return web.json_response({
        "status": "alive", "bot": "Indian Media Bot v3",
        "features": "JioSaavn Songs, Bollywood, Anime, Books - ALL in Telegram",
        "time": datetime.now().isoformat()
    })

async def webhook(req):
    try:
        data = await req.json()
        update = Update.de_json(data, req.app["bot"].bot)
        await req.app["bot"].process_update(update)
    except Exception as ex:
        logger.error(f"Webhook: {ex}")
    return web.Response(status=200)


# ══════════════════════════════════════════
#  🚀 MAIN
# ══════════════════════════════════════════

async def post_init(app):
    cmds = [
        BotCommand("start", "🏠 Home"),
        BotCommand("song", "🎵 Indian Songs (JioSaavn)"),
        BotCommand("album", "💿 Album Search"),
        BotCommand("artist", "🎤 Artist Search"),
        BotCommand("lyrics", "📜 Song Lyrics"),
        BotCommand("bollywood", "🎬 Bollywood"),
        BotCommand("hindi", "🇮🇳 Hindi Songs"),
        BotCommand("punjabi", "🇮🇳 Punjabi Songs"),
        BotCommand("tamil", "🇮🇳 Tamil Songs"),
        BotCommand("telugu", "🇮🇳 Telugu Songs"),
        BotCommand("playlist", "🎶 Playlists"),
        BotCommand("search", "🔍 Search All"),
        BotCommand("image", "🖼️ Images"),
        BotCommand("wallpaper", "🌄 Wallpapers"),
        BotCommand("anime", "🌸 Anime"),
        BotCommand("waifu", "🌸 Waifu Images"),
        BotCommand("book", "📚 Free Books"),
        BotCommand("code", "💻 GitHub"),
        BotCommand("nasa", "🚀 NASA"),
        BotCommand("wiki", "📖 Wikipedia"),
        BotCommand("random", "🎲 Random"),
        BotCommand("help", "❓ Help"),
    ]
    await app.bot.set_my_commands(cmds)
    logger.info(f"{E['check']} Bot ready!")


def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # Indian Music Commands
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("song", cmd_song))
    app.add_handler(CommandHandler("album", cmd_album))
    app.add_handler(CommandHandler("artist", cmd_artist))
    app.add_handler(CommandHandler("bollywood", cmd_bollywood))
    app.add_handler(CommandHandler("playlist", cmd_playlist))
    app.add_handler(CommandHandler("lyrics", cmd_lyrics))
    app.add_handler(CommandHandler("hindi", cmd_hindi))
    app.add_handler(CommandHandler("punjabi", cmd_punjabi))
    app.add_handler(CommandHandler("tamil", cmd_tamil))
    app.add_handler(CommandHandler("telugu", cmd_telugu))

    # World Media Commands
    app.add_handler(CommandHandler("search", cmd_search))
    app.add_handler(CommandHandler("image", cmd_image))
    app.add_handler(CommandHandler("wallpaper", cmd_wallpaper))
    app.add_handler(CommandHandler("anime", cmd_anime))
    app.add_handler(CommandHandler("waifu", cmd_waifu))
    app.add_handler(CommandHandler("book", cmd_book))
    app.add_handler(CommandHandler("code", cmd_code))
    app.add_handler(CommandHandler("nasa", cmd_nasa))
    app.add_handler(CommandHandler("wiki", cmd_wiki))
    app.add_handler(CommandHandler("random", cmd_random))

    app.add_handler(CallbackQueryHandler(cb_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    if WEBHOOK_URL:
        logger.info(f"🌐 WEBHOOK on port {PORT}")
        wa = web.Application()
        wa["bot"] = app
        wa.router.add_get("/", health)
        wa.router.add_get("/health", health)
        wa.router.add_post(f"/webhook/{BOT_TOKEN}", webhook)

        async def on_start(w):
            await app.initialize()
            await app.bot.set_webhook(f"{WEBHOOK_URL}/webhook/{BOT_TOKEN}",
                                      allowed_updates=["message","callback_query"])
            await app.start()
            logger.info(f"{E['check']} Webhook set!")

        async def on_stop(w):
            await dl.close()
            await app.stop()
            await app.shutdown()

        wa.on_startup.append(on_start)
        wa.on_shutdown.append(on_stop)
        web.run_app(wa, host="0.0.0.0", port=PORT)
    else:
        logger.info("🖥️ POLLING mode")
        app.run_polling(allowed_updates=["message","callback_query"])

if __name__ == "__main__":
    main()