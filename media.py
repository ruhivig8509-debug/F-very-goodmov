# media.py - Ultimate Open Source Media Bot
# EVERYTHING INSIDE TELEGRAM - NO EXTERNAL LINKS
# Stylish Unicode Fonts + God Level Design

import os
import logging
import asyncio
import aiohttp
import random
import re
import io
from datetime import datetime
from urllib.parse import quote_plus
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    BotCommand, InputMediaPhoto, InputMediaVideo, InputMediaAudio
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from telegram.constants import ParseMode, ChatAction
from aiohttp import web

# ══════════════════════════════════════════
#  CONFIGURATION
# ══════════════════════════════════════════

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ══════════════════════════════════════════
#  𝗦𝗧𝗬𝗟𝗜𝗦𝗛 𝗙𝗢𝗡𝗧𝗦 & 𝗦𝗬𝗠𝗕𝗢𝗟𝗦
# ══════════════════════════════════════════

def bold_sans(text):
    normal = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    styled = '𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵'
    return text.translate(str.maketrans(normal, styled))

def italic_sans(text):
    normal = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    styled = '𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻'
    return text.translate(str.maketrans(normal, styled))

def bold_italic(text):
    normal = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    styled = '𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯'
    return text.translate(str.maketrans(normal, styled))

def mono_font(text):
    normal = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    styled = '𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿'
    return text.translate(str.maketrans(normal, styled))

def script_font(text):
    normal = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    styled = '𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏'
    return text.translate(str.maketrans(normal, styled))

def double_font(text):
    normal = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    styled = '𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡'
    return text.translate(str.maketrans(normal, styled))

def fraktur_font(text):
    normal = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    styled = '𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷'
    return text.translate(str.maketrans(normal, styled))

def circled(text):
    normal = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    styled = 'ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ'
    return text.translate(str.maketrans(normal, styled))

def squared(text):
    normal = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    styled = '🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉'
    return text.upper().translate(str.maketrans(normal, styled))

def neg_squared(text):
    normal = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    styled = '🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉'
    return text.upper().translate(str.maketrans(normal, styled))

# ═══ Decorative Borders & Symbols ═══

TOP    = "╔══════════════════════════╗"
BOT    = "╚══════════════════════════╝"
SIDE   = "║"
LINE   = "━━━━━━━━━━━━━━━━━━━━━━━━━━"
LINE2  = "◈━━━━━━━━━━━━━━━━━━━━━━◈"
LINE3  = "▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
DOT_LN = "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄"
SPARK  = "╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍"

# Symbols
S = {
    "crown": "👑", "fire": "🔥", "star": "✦", "star2": "★",
    "diamond": "◆", "diamond2": "◇", "spark": "✨", "bolt": "⚡",
    "rocket": "🚀", "gem": "💎", "heart": "❤️", "check": "✅",
    "cross": "❌", "warn": "⚠️", "info": "ℹ️", "mag": "🔍",
    "globe": "🌍", "link": "🔗", "pin": "📌", "key": "🔑",
    "film": "🎬", "cam": "📷", "vid": "📹", "tv": "📺",
    "music": "🎵", "mic": "🎤", "head": "🎧", "note": "🎶",
    "book": "📖", "books": "📚", "scroll": "📜", "doc": "📄",
    "art": "🎨", "palette": "🖌️", "frame": "🖼️", "photo": "📸",
    "anime": "🌸", "cherry": "🌸", "sakura": "🎌", "cat": "🐱",
    "game": "🎮", "dice": "🎲", "puzzle": "🧩", "trophy": "🏆",
    "code": "💻", "robot": "🤖", "brain": "🧠", "atom": "⚛️",
    "cube": "🧊", "earth": "🌏", "map": "🗺️", "sun": "☀️",
    "moon": "🌙", "comet": "☄️", "wave": "🌊", "mount": "🏔️",
    "tree": "🌲", "flower": "🌺", "leaf": "🍃", "rain": "🌧️",
    "wall": "🌄", "city": "🏙️", "night": "🌃", "bridge": "🌉",
    "folder": "📁", "pack": "📦", "cd": "💿", "disk": "💾",
    "send": "📤", "recv": "📥", "clip": "📎", "bell": "🔔",
    "eye": "👁️", "point": "👉", "up": "👆", "clap": "👏",
    "flex": "💪", "pray": "🙏", "cool": "😎", "think": "🤔",
    "arrow": "➤", "arrow2": "➜", "arrow3": "⟫", "tri": "▸",
    "dot": "•", "ring": "◉", "sq": "■", "sq2": "▪️",
    "circle": "●", "circle2": "○", "inf": "♾️", "peace": "☮️",
    "tick": "✓", "plus": "✚", "x": "✗", "fleur": "⚜️",
}

# ══════════════════════════════════════════
#  𝗠𝗘𝗗𝗜𝗔 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗𝗘𝗥
# ══════════════════════════════════════════

class MediaDownloader:
    """Downloads media and sends DIRECTLY in Telegram"""

    def __init__(self):
        self.session = None

    async def get_session(self):
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            connector = aiohttp.TCPConnector(limit=10, force_close=True)
            self.session = aiohttp.ClientSession(
                timeout=timeout, connector=connector,
                headers={"User-Agent": "MediaBot/2.0"}
            )
        return self.session

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def download_bytes(self, url, max_size=45*1024*1024):
        """Download file as bytes (max 45MB for Telegram limit)"""
        try:
            session = await self.get_session()
            async with session.get(url) as resp:
                if resp.status != 200:
                    return None
                content_length = resp.headers.get('Content-Length')
                if content_length and int(content_length) > max_size:
                    return None
                data = await resp.read()
                if len(data) > max_size:
                    return None
                return data
        except Exception as e:
            logger.error(f"Download error: {e}")
            return None

    async def send_photo_telegram(self, bot, chat_id, image_url, caption=""):
        """Download image and send as Telegram photo"""
        try:
            data = await self.download_bytes(image_url, max_size=10*1024*1024)
            if data:
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=data,
                    caption=caption[:1024],
                    read_timeout=30,
                    write_timeout=30
                )
                return True
            else:
                # Try sending URL directly
                await bot.send_photo(
                    chat_id=chat_id,
                    photo=image_url,
                    caption=caption[:1024],
                    read_timeout=30,
                    write_timeout=30
                )
                return True
        except Exception as e:
            logger.error(f"Send photo error: {e}")
            return False

    async def send_video_telegram(self, bot, chat_id, video_url, caption="", thumb_url=None):
        """Download video and send as Telegram video"""
        try:
            data = await self.download_bytes(video_url, max_size=45*1024*1024)
            if data:
                thumb_data = None
                if thumb_url:
                    thumb_data = await self.download_bytes(thumb_url, max_size=1*1024*1024)
                await bot.send_video(
                    chat_id=chat_id,
                    video=data,
                    caption=caption[:1024],
                    thumbnail=thumb_data,
                    read_timeout=60,
                    write_timeout=60,
                    supports_streaming=True
                )
                return True
            return False
        except Exception as e:
            logger.error(f"Send video error: {e}")
            return False

    async def send_audio_telegram(self, bot, chat_id, audio_url, caption="", title=""):
        """Download audio and send as Telegram audio"""
        try:
            data = await self.download_bytes(audio_url, max_size=45*1024*1024)
            if data:
                await bot.send_audio(
                    chat_id=chat_id,
                    audio=data,
                    caption=caption[:1024],
                    title=title,
                    read_timeout=60,
                    write_timeout=60
                )
                return True
            return False
        except Exception as e:
            logger.error(f"Send audio error: {e}")
            return False

    async def send_document_telegram(self, bot, chat_id, doc_url, caption="", filename=""):
        """Download file and send as Telegram document"""
        try:
            data = await self.download_bytes(doc_url, max_size=45*1024*1024)
            if data:
                await bot.send_document(
                    chat_id=chat_id,
                    document=data,
                    caption=caption[:1024],
                    filename=filename or "file",
                    read_timeout=60,
                    write_timeout=60
                )
                return True
            return False
        except Exception as e:
            logger.error(f"Send document error: {e}")
            return False


# Global instances
downloader = MediaDownloader()
USER_DATA = {}

# ══════════════════════════════════════════
#  𝗔𝗣𝗜 𝗦𝗘𝗔𝗥𝗖𝗛 𝗘𝗡𝗚𝗜𝗡𝗘𝗦
# ══════════════════════════════════════════

async def get_session():
    return await downloader.get_session()

# ── IMAGES: Openverse (800M+ CC images) ──

async def search_openverse_images(query, page=1, limit=8):
    results = []
    try:
        session = await get_session()
        url = f"https://api.openverse.org/v1/images/?q={quote_plus(query)}&page={page}&page_size={limit}"
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                for item in data.get("results", []):
                    results.append({
                        "type": "image",
                        "title": item.get("title", "Untitled") or "Untitled",
                        "creator": item.get("creator", "Unknown") or "Unknown",
                        "license": item.get("license", "CC") or "CC",
                        "image_url": item.get("url", ""),
                        "thumbnail": item.get("thumbnail", "") or item.get("url", ""),
                        "source": item.get("source", "Openverse"),
                        "width": item.get("width", 0),
                        "height": item.get("height", 0),
                    })
    except Exception as e:
        logger.error(f"Openverse error: {e}")
    return results

# ── IMAGES: Wikimedia Commons ──

async def search_wikimedia_images(query, limit=5):
    results = []
    try:
        session = await get_session()
        url = (f"https://commons.wikimedia.org/w/api.php?"
               f"action=query&generator=search&gsrnamespace=6&gsrsearch={quote_plus(query)}"
               f"&gsrlimit={limit}&prop=imageinfo&iiprop=url|size|mime|extmetadata"
               f"&format=json&iiurlwidth=800")
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                pages = data.get("query", {}).get("pages", {})
                for pid, page_data in pages.items():
                    ii = page_data.get("imageinfo", [{}])[0]
                    mime = ii.get("mime", "")
                    if "image" not in mime:
                        continue
                    thumb = ii.get("thumburl", ii.get("url", ""))
                    full_url = ii.get("url", "")
                    title = page_data.get("title", "").replace("File:", "")
                    meta = ii.get("extmetadata", {})
                    artist = meta.get("Artist", {}).get("value", "Unknown")
                    artist = re.sub(r'<[^>]+>', '', str(artist))[:50]
                    results.append({
                        "type": "image",
                        "title": title,
                        "creator": artist,
                        "license": meta.get("LicenseShortName", {}).get("value", "CC"),
                        "image_url": full_url,
                        "thumbnail": thumb,
                        "source": "Wikimedia Commons",
                        "width": ii.get("width", 0),
                        "height": ii.get("height", 0),
                    })
    except Exception as e:
        logger.error(f"Wikimedia error: {e}")
    return results

# ── IMAGES/VIDEOS: NASA ──

async def search_nasa(query, media_type="image", limit=5):
    results = []
    try:
        session = await get_session()
        url = f"https://images-api.nasa.gov/search?q={quote_plus(query)}&media_type={media_type}&page_size={limit}"
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                items = data.get("collection", {}).get("items", [])[:limit]
                for item in items:
                    item_data = item.get("data", [{}])[0]
                    links = item.get("links", [])
                    thumb = links[0].get("href", "") if links else ""
                    nasa_id = item_data.get("nasa_id", "")

                    # Get actual media file
                    media_url = ""
                    if nasa_id:
                        asset_url = f"https://images-api.nasa.gov/asset/{nasa_id}"
                        try:
                            async with session.get(asset_url) as aresp:
                                if aresp.status == 200:
                                    adata = await aresp.json()
                                    collection_items = adata.get("collection", {}).get("items", [])
                                    for ci in collection_items:
                                        href = ci.get("href", "")
                                        if media_type == "image" and any(href.lower().endswith(x) for x in ['.jpg', '.jpeg', '.png', '.webp']):
                                            if "orig" in href or "large" in href:
                                                media_url = href
                                                break
                                        elif media_type == "video" and any(href.lower().endswith(x) for x in ['.mp4', '.webm']):
                                            if "orig" in href or "large" in href or "medium" in href:
                                                media_url = href
                                                break
                                    if not media_url and collection_items:
                                        for ci in collection_items:
                                            href = ci.get("href", "")
                                            if media_type == "image" and any(href.lower().endswith(x) for x in ['.jpg', '.jpeg', '.png']):
                                                media_url = href
                                                break
                                            elif media_type == "video" and href.lower().endswith('.mp4'):
                                                media_url = href
                                                break
                        except:
                            pass

                    if not media_url:
                        media_url = thumb

                    results.append({
                        "type": media_type,
                        "title": item_data.get("title", "NASA Media"),
                        "desc": (item_data.get("description", "") or "")[:200],
                        "media_url": media_url,
                        "thumbnail": thumb,
                        "source": "NASA",
                        "date": item_data.get("date_created", "")[:10],
                        "creator": item_data.get("photographer", "NASA"),
                    })
    except Exception as e:
        logger.error(f"NASA error: {e}")
    return results

# ── WALLPAPERS: Wallhaven ──

async def search_wallhaven(query, page=1, limit=8):
    results = []
    try:
        session = await get_session()
        url = f"https://wallhaven.cc/api/v1/search?q={quote_plus(query)}&page={page}&sorting=relevance&categories=111&purity=100"
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                for item in data.get("data", [])[:limit]:
                    results.append({
                        "type": "image",
                        "title": f"Wallpaper {item.get('id', '')}",
                        "image_url": item.get("path", ""),
                        "thumbnail": item.get("thumbs", {}).get("small", ""),
                        "source": "Wallhaven",
                        "resolution": item.get("resolution", ""),
                        "views": item.get("views", 0),
                        "favorites": item.get("favorites", 0),
                        "creator": "Wallhaven Community",
                        "license": "Wallhaven",
                    })
    except Exception as e:
        logger.error(f"Wallhaven error: {e}")
    return results

# ── ANIME: Jikan (MyAnimeList) ──

async def search_anime_jikan(query, page=1, limit=8):
    results = []
    try:
        session = await get_session()
        url = f"https://api.jikan.moe/v4/anime?q={quote_plus(query)}&limit={limit}&page={page}&sfw=true"
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                for item in data.get("data", []):
                    img = item.get("images", {}).get("jpg", {})
                    trailer = item.get("trailer", {})
                    results.append({
                        "type": "anime",
                        "title": item.get("title", "Unknown"),
                        "title_jp": item.get("title_japanese", ""),
                        "score": item.get("score", "N/A"),
                        "episodes": item.get("episodes", "?"),
                        "status": item.get("status", ""),
                        "rating": item.get("rating", ""),
                        "synopsis": (item.get("synopsis", "") or "")[:300],
                        "image_url": img.get("large_image_url", img.get("image_url", "")),
                        "thumbnail": img.get("small_image_url", img.get("image_url", "")),
                        "trailer_url": trailer.get("url", ""),
                        "trailer_embed": trailer.get("embed_url", ""),
                        "genres": ", ".join([g.get("name", "") for g in item.get("genres", [])]),
                        "year": item.get("year", ""),
                        "source": "MyAnimeList",
                        "mal_url": item.get("url", ""),
                    })
    except Exception as e:
        logger.error(f"Jikan error: {e}")
    return results

# ── ANIME: Kitsu ──

async def search_anime_kitsu(query, limit=5):
    results = []
    try:
        session = await get_session()
        url = f"https://kitsu.io/api/edge/anime?filter[text]={quote_plus(query)}&page[limit]={limit}"
        headers = {"Accept": "application/vnd.api+json"}
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                for item in data.get("data", []):
                    a = item.get("attributes", {})
                    poster = a.get("posterImage", {}) or {}
                    cover = a.get("coverImage", {}) or {}
                    results.append({
                        "type": "anime",
                        "title": a.get("canonicalTitle", "Unknown"),
                        "title_jp": a.get("titles", {}).get("ja_jp", ""),
                        "score": a.get("averageRating", "N/A"),
                        "episodes": a.get("episodeCount", "?"),
                        "status": a.get("status", ""),
                        "synopsis": (a.get("synopsis", "") or "")[:300],
                        "image_url": poster.get("large", poster.get("medium", poster.get("original", ""))),
                        "thumbnail": poster.get("small", poster.get("tiny", "")),
                        "cover_url": cover.get("large", cover.get("original", "")),
                        "source": "Kitsu",
                    })
    except Exception as e:
        logger.error(f"Kitsu error: {e}")
    return results

# ── ANIME IMAGES: Waifu.pics ──

async def get_waifu_image(category="waifu"):
    try:
        session = await get_session()
        categories = ["waifu", "neko", "shinobu", "megumin", "bully", "cuddle",
                      "cry", "hug", "awoo", "kiss", "lick", "pat", "smug",
                      "bonk", "yeet", "blush", "smile", "wave", "highfive",
                      "handhold", "nom", "bite", "glomp", "slap", "kill",
                      "kick", "happy", "wink", "poke", "dance", "cringe"]
        if category.lower() not in categories:
            category = "waifu"
        url = f"https://api.waifu.pics/sfw/{category.lower()}"
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("url", "")
    except:
        pass
    return ""

async def get_waifu_many(category="waifu", count=5):
    try:
        session = await get_session()
        url = f"https://api.waifu.pics/many/sfw/{category.lower()}"
        async with session.post(url, json={}) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("files", [])[:count]
    except:
        pass
    return []

# ── MUSIC: Internet Archive Audio ──

async def search_archive_audio(query, limit=5, page=1):
    results = []
    try:
        session = await get_session()
        url = (f"https://archive.org/advancedsearch.php?"
               f"q={quote_plus(query)}+mediatype:audio&output=json&rows={limit}&page={page}"
               f"&fl[]=identifier,title,creator,description,date,downloads")
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                for doc in data.get("response", {}).get("docs", []):
                    identifier = doc.get("identifier", "")
                    # Get actual audio file
                    audio_url = ""
                    try:
                        files_url = f"https://archive.org/metadata/{identifier}/files"
                        async with session.get(files_url) as fresp:
                            if fresp.status == 200:
                                fdata = await fresp.json()
                                for f in fdata.get("result", []):
                                    name = f.get("name", "")
                                    if any(name.lower().endswith(x) for x in ['.mp3', '.ogg', '.flac', '.wav']):
                                        audio_url = f"https://archive.org/download/{identifier}/{quote_plus(name)}"
                                        break
                    except:
                        pass
                    results.append({
                        "type": "audio",
                        "title": doc.get("title", "Unknown") if isinstance(doc.get("title"), str) else str(doc.get("title", "Unknown")),
                        "creator": doc.get("creator", "Unknown") if isinstance(doc.get("creator"), str) else str(doc.get("creator", "Unknown")),
                        "desc": (str(doc.get("description", "")) or "")[:200],
                        "audio_url": audio_url,
                        "page_url": f"https://archive.org/details/{identifier}",
                        "downloads": doc.get("downloads", 0),
                        "source": "Internet Archive",
                    })
    except Exception as e:
        logger.error(f"Archive audio error: {e}")
    return results

# ── MOVIES/VIDEOS: Internet Archive ──

async def search_archive_video(query, limit=5, page=1):
    results = []
    try:
        session = await get_session()
        url = (f"https://archive.org/advancedsearch.php?"
               f"q={quote_plus(query)}+mediatype:movies&output=json&rows={limit}&page={page}"
               f"&fl[]=identifier,title,creator,description,date,downloads")
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                for doc in data.get("response", {}).get("docs", []):
                    identifier = doc.get("identifier", "")
                    video_url = ""
                    thumb_url = f"https://archive.org/services/img/{identifier}"
                    try:
                        files_url = f"https://archive.org/metadata/{identifier}/files"
                        async with session.get(files_url) as fresp:
                            if fresp.status == 200:
                                fdata = await fresp.json()
                                best_size = 0
                                for f in fdata.get("result", []):
                                    name = f.get("name", "")
                                    size = int(f.get("size", 0) or 0)
                                    if any(name.lower().endswith(x) for x in ['.mp4', '.ogv', '.webm']):
                                        # prefer mp4, under 45MB
                                        if name.lower().endswith('.mp4') and size < 45*1024*1024:
                                            if size > best_size:
                                                video_url = f"https://archive.org/download/{identifier}/{quote_plus(name)}"
                                                best_size = size
                                if not video_url:
                                    for f in fdata.get("result", []):
                                        name = f.get("name", "")
                                        size = int(f.get("size", 0) or 0)
                                        if name.lower().endswith('.mp4') and size < 45*1024*1024:
                                            video_url = f"https://archive.org/download/{identifier}/{quote_plus(name)}"
                                            break
                    except:
                        pass
                    results.append({
                        "type": "video",
                        "title": doc.get("title", "Unknown") if isinstance(doc.get("title"), str) else str(doc.get("title", "Unknown")),
                        "creator": doc.get("creator", "Unknown") if isinstance(doc.get("creator"), str) else str(doc.get("creator", "Unknown")),
                        "desc": (str(doc.get("description", ""))[:200]) if doc.get("description") else "",
                        "video_url": video_url,
                        "thumbnail": thumb_url,
                        "page_url": f"https://archive.org/details/{identifier}",
                        "downloads": doc.get("downloads", 0),
                        "source": "Internet Archive",
                    })
    except Exception as e:
        logger.error(f"Archive video error: {e}")
    return results

# ── BOOKS: Gutenberg ──

async def search_gutenberg(query, limit=5, page=1):
    results = []
    try:
        session = await get_session()
        url = f"https://gutendex.com/books/?search={quote_plus(query)}&page={page}"
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                for item in data.get("results", [])[:limit]:
                    authors = ", ".join([a.get("name", "") for a in item.get("authors", [])])
                    formats = item.get("formats", {})
                    cover = formats.get("image/jpeg", "")
                    txt_url = (formats.get("text/plain; charset=utf-8") or
                              formats.get("text/plain; charset=us-ascii") or
                              formats.get("text/plain", ""))
                    epub_url = formats.get("application/epub+zip", "")
                    results.append({
                        "type": "book",
                        "title": item.get("title", "Unknown"),
                        "creator": authors or "Unknown",
                        "cover_url": cover,
                        "txt_url": txt_url,
                        "epub_url": epub_url,
                        "downloads": item.get("download_count", 0),
                        "book_id": item.get("id", ""),
                        "source": "Project Gutenberg",
                        "subjects": ", ".join(item.get("subjects", [])[:3]),
                    })
    except Exception as e:
        logger.error(f"Gutenberg error: {e}")
    return results

# ── CODE: GitHub ──

async def search_github_repos(query, limit=5, page=1):
    results = []
    try:
        session = await get_session()
        url = f"https://api.github.com/search/repositories?q={quote_plus(query)}&per_page={limit}&page={page}&sort=stars"
        headers = {"Accept": "application/vnd.github.v3+json"}
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                for item in data.get("items", []):
                    owner = item.get("owner", {})
                    results.append({
                        "type": "code",
                        "title": item.get("full_name", "Unknown"),
                        "desc": (item.get("description", "") or "")[:200],
                        "stars": item.get("stargazers_count", 0),
                        "forks": item.get("forks_count", 0),
                        "language": item.get("language", "N/A"),
                        "avatar_url": owner.get("avatar_url", ""),
                        "repo_url": item.get("html_url", ""),
                        "source": "GitHub",
                    })
    except Exception as e:
        logger.error(f"GitHub error: {e}")
    return results

# ── WIKIPEDIA ──

async def search_wikipedia(query, limit=3):
    results = []
    try:
        session = await get_session()
        url = (f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(query)}")
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                thumb = data.get("thumbnail", {}).get("source", "")
                orig = data.get("originalimage", {}).get("source", "")
                results.append({
                    "type": "wiki",
                    "title": data.get("title", ""),
                    "extract": data.get("extract", ""),
                    "image_url": orig or thumb,
                    "thumbnail": thumb,
                    "source": "Wikipedia",
                })
    except:
        pass
    # Also search
    try:
        session = await get_session()
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote_plus(query)}&format=json&srlimit={limit}"
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                for item in data.get("query", {}).get("search", []):
                    title = item.get("title", "")
                    snippet = re.sub(r'<[^>]+>', '', item.get("snippet", ""))
                    results.append({
                        "type": "wiki",
                        "title": title,
                        "extract": snippet,
                        "source": "Wikipedia",
                    })
    except:
        pass
    return results

# ── HUGGING FACE DATASETS ──

async def search_huggingface(query, limit=5):
    results = []
    try:
        session = await get_session()
        url = f"https://huggingface.co/api/datasets?search={quote_plus(query)}&limit={limit}&sort=downloads&direction=-1"
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                for item in data[:limit]:
                    results.append({
                        "type": "dataset",
                        "title": item.get("id", "Unknown"),
                        "downloads": item.get("downloads", 0),
                        "likes": item.get("likes", 0),
                        "tags": ", ".join(item.get("tags", [])[:5]),
                        "source": "Hugging Face",
                    })
    except Exception as e:
        logger.error(f"HuggingFace error: {e}")
    return results


# ══════════════════════════════════════════
#  𝗥𝗘𝗦𝗨𝗟𝗧 𝗙𝗢𝗥𝗠𝗔𝗧𝗧𝗘𝗥 & 𝗦𝗘𝗡𝗗𝗘𝗥
# ══════════════════════════════════════════

async def send_results_to_telegram(bot, chat_id, results, query, category, page=1):
    """Send each result as NATIVE Telegram media - NO LINKS!"""

    if not results:
        no_result = (
            f"\n{TOP}\n"
            f"{SIDE}  {S['cross']} {bold_sans('NO RESULTS FOUND')} {S['cross']}\n"
            f"{BOT}\n\n"
            f"{S['mag']} {bold_sans('Query')}: {italic_sans(query)}\n"
            f"{S['folder']} {bold_sans('Category')}: {italic_sans(category)}\n\n"
            f"{LINE2}\n\n"
            f"{S['arrow']} {bold_italic('Tips')}:\n"
            f"  {S['dot']} {italic_sans('Try different keywords')}\n"
            f"  {S['dot']} {italic_sans('Use English for better results')}\n"
            f"  {S['dot']} {italic_sans('Try specific category')}\n\n"
            f"{LINE3}"
        )
        await bot.send_message(chat_id=chat_id, text=no_result)
        return

    # Header message
    cat_icons = {
        "images": S['frame'], "wallpapers": S['wall'], "anime": S['anime'],
        "movies": S['film'], "videos": S['vid'], "music": S['music'],
        "books": S['books'], "code": S['code'], "datasets": S['robot'],
        "nasa_img": S['rocket'], "nasa_vid": S['rocket'], "wiki": S['book'],
        "all": S['globe'], "waifu": S['sakura'],
    }
    c_icon = cat_icons.get(category, S['mag'])

    header = (
        f"\n{TOP}\n"
        f"{SIDE}  {c_icon} {bold_sans(category.upper().replace('_',' '))} {bold_sans('RESULTS')} {c_icon}\n"
        f"{BOT}\n\n"
        f"{S['mag']} {bold_sans('Query')}: {script_font(query)}\n"
        f"{S['pack']} {bold_sans('Found')}: {bold_sans(str(len(results)))} {italic_sans('results')} {S['dot']} {italic_sans('Page')} {bold_sans(str(page))}\n\n"
        f"{SPARK}\n"
    )
    await bot.send_message(chat_id=chat_id, text=header)

    sent_count = 0
    for i, r in enumerate(results):
        try:
            rtype = r.get("type", "")

            # ═══ IMAGE ═══
            if rtype == "image":
                img_url = r.get("image_url", "") or r.get("thumbnail", "")
                if not img_url:
                    continue

                caption = (
                    f"{S['frame']} {bold_sans(r.get('title', 'Image')[:60])}\n"
                    f"{DOT_LN}\n"
                    f"{S['palette']} {italic_sans('By')}: {bold_sans(r.get('creator', 'Unknown')[:30])}\n"
                )
                if r.get("resolution"):
                    caption += f"{S['tv']} {italic_sans('Resolution')}: {bold_sans(r.get('resolution', ''))}\n"
                if r.get("views"):
                    caption += f"{S['eye']} {italic_sans('Views')}: {bold_sans(str(r.get('views', 0)))}\n"
                if r.get("license"):
                    caption += f"{S['key']} {italic_sans('License')}: {mono_font(r.get('license', 'CC'))}\n"
                caption += (
                    f"{S['globe']} {italic_sans('Source')}: {bold_sans(r.get('source', ''))}\n"
                    f"{LINE2}"
                )

                success = await downloader.send_photo_telegram(bot, chat_id, img_url, caption)
                if success:
                    sent_count += 1

            # ═══ VIDEO ═══
            elif rtype == "video":
                vid_url = r.get("video_url", "") or r.get("media_url", "")
                if not vid_url:
                    # Send thumbnail as photo with info
                    thumb = r.get("thumbnail", "")
                    if thumb:
                        caption = (
                            f"{S['vid']} {bold_sans(r.get('title', 'Video')[:60])}\n"
                            f"{DOT_LN}\n"
                            f"{S['palette']} {italic_sans('By')}: {bold_sans(r.get('creator', 'Unknown')[:30])}\n"
                            f"{S['globe']} {italic_sans('Source')}: {bold_sans(r.get('source', ''))}\n"
                            f"{S['warn']} {italic_sans('Video too large for Telegram')}\n"
                            f"{LINE2}"
                        )
                        await downloader.send_photo_telegram(bot, chat_id, thumb, caption)
                        sent_count += 1
                    continue

                caption = (
                    f"{S['film']} {bold_sans(r.get('title', 'Video')[:60])}\n"
                    f"{DOT_LN}\n"
                    f"{S['palette']} {italic_sans('By')}: {bold_sans(r.get('creator', 'Unknown')[:30])}\n"
                    f"{S['globe']} {italic_sans('Source')}: {bold_sans(r.get('source', ''))}\n"
                    f"{S['recv']} {italic_sans('Downloads')}: {bold_sans(str(r.get('downloads', 0)))}\n"
                    f"{LINE2}"
                )

                thumb = r.get("thumbnail", "")
                success = await downloader.send_video_telegram(bot, chat_id, vid_url, caption, thumb)
                if success:
                    sent_count += 1
                else:
                    # Fallback: send thumbnail with info
                    if thumb:
                        caption += f"\n{S['warn']} {italic_sans('Video too large, showing preview')}"
                        await downloader.send_photo_telegram(bot, chat_id, thumb, caption)
                        sent_count += 1

            # ═══ AUDIO ═══
            elif rtype == "audio":
                audio_url = r.get("audio_url", "")
                if not audio_url:
                    continue

                caption = (
                    f"{S['music']} {bold_sans(r.get('title', 'Audio')[:60])}\n"
                    f"{DOT_LN}\n"
                    f"{S['mic']} {italic_sans('Artist')}: {bold_sans(r.get('creator', 'Unknown')[:30])}\n"
                    f"{S['globe']} {italic_sans('Source')}: {bold_sans(r.get('source', ''))}\n"
                    f"{S['recv']} {italic_sans('Downloads')}: {bold_sans(str(r.get('downloads', 0)))}\n"
                    f"{LINE2}"
                )

                title = r.get("title", "Audio")
                success = await downloader.send_audio_telegram(bot, chat_id, audio_url, caption, title)
                if success:
                    sent_count += 1

            # ═══ ANIME ═══
            elif rtype == "anime":
                img_url = r.get("image_url", "") or r.get("thumbnail", "")
                if not img_url:
                    continue

                score = r.get("score", "N/A")
                score_bar = ""
                if score and score != "N/A":
                    try:
                        s = float(score)
                        filled = int(s / 10 * 10)
                        score_bar = "█" * filled + "░" * (10 - filled)
                    except:
                        score_bar = ""

                caption = (
                    f"{S['anime']} {bold_sans(r.get('title', 'Anime')[:50])}\n"
                )
                if r.get("title_jp"):
                    caption += f"   {italic_sans(r.get('title_jp', '')[:40])}\n"
                caption += f"{DOT_LN}\n"

                if score_bar:
                    caption += f"{S['star2']} {italic_sans('Score')}: {bold_sans(str(score))} [{score_bar}]\n"
                else:
                    caption += f"{S['star2']} {italic_sans('Score')}: {bold_sans(str(score))}\n"

                caption += (
                    f"{S['tv']} {italic_sans('Episodes')}: {bold_sans(str(r.get('episodes', '?')))}\n"
                    f"{S['bolt']} {italic_sans('Status')}: {bold_sans(r.get('status', 'N/A'))}\n"
                )
                if r.get("genres"):
                    caption += f"{S['puzzle']} {italic_sans('Genres')}: {mono_font(r.get('genres', ''))}\n"
                if r.get("year"):
                    caption += f"{S['globe']} {italic_sans('Year')}: {bold_sans(str(r.get('year', '')))}\n"
                caption += f"{DOT_LN}\n"

                synopsis = r.get("synopsis", "")
                if synopsis:
                    caption += f"{italic_sans(synopsis[:200])}\n"
                caption += f"\n{S['globe']} {italic_sans('Source')}: {bold_sans(r.get('source', ''))}\n"
                caption += f"{LINE2}"

                # Truncate caption
                if len(caption) > 1024:
                    caption = caption[:1020] + "..."

                await downloader.send_photo_telegram(bot, chat_id, img_url, caption)
                sent_count += 1

            # ═══ BOOK ═══
            elif rtype == "book":
                caption = (
                    f"{S['books']} {bold_sans(r.get('title', 'Book')[:60])}\n"
                    f"{DOT_LN}\n"
                    f"{S['palette']} {italic_sans('Author')}: {bold_sans(r.get('creator', 'Unknown')[:40])}\n"
                    f"{S['recv']} {italic_sans('Downloads')}: {bold_sans(str(r.get('downloads', 0)))}\n"
                )
                if r.get("subjects"):
                    caption += f"{S['puzzle']} {italic_sans('Subjects')}: {mono_font(r.get('subjects', '')[:60])}\n"
                caption += (
                    f"{S['globe']} {italic_sans('Source')}: {bold_sans(r.get('source', ''))}\n"
                    f"{LINE2}"
                )

                # Send cover image
                cover = r.get("cover_url", "")
                if cover:
                    await downloader.send_photo_telegram(bot, chat_id, cover, caption)
                    sent_count += 1

                # Send ebook file
                epub_url = r.get("epub_url", "")
                txt_url = r.get("txt_url", "")
                if epub_url:
                    title = r.get("title", "book")
                    file_caption = f"{S['books']} {bold_sans(title[:50])}\n{S['pack']} {italic_sans('EPUB Format')}"
                    safe_title = re.sub(r'[^\w\s-]', '', title)[:50]
                    await downloader.send_document_telegram(bot, chat_id, epub_url, file_caption, f"{safe_title}.epub")
                    sent_count += 1
                elif txt_url:
                    title = r.get("title", "book")
                    file_caption = f"{S['books']} {bold_sans(title[:50])}\n{S['doc']} {italic_sans('Text Format')}"
                    safe_title = re.sub(r'[^\w\s-]', '', title)[:50]
                    await downloader.send_document_telegram(bot, chat_id, txt_url, file_caption, f"{safe_title}.txt")
                    sent_count += 1

            # ═══ CODE (GitHub) ═══
            elif rtype == "code":
                avatar = r.get("avatar_url", "")
                caption = (
                    f"{S['code']} {bold_sans(r.get('title', 'Repo')[:50])}\n"
                    f"{DOT_LN}\n"
                    f"{S['star2']} {italic_sans('Stars')}: {bold_sans(str(r.get('stars', 0)))} "
                    f"{S['dot']} {italic_sans('Forks')}: {bold_sans(str(r.get('forks', 0)))}\n"
                    f"{S['bolt']} {italic_sans('Language')}: {bold_sans(str(r.get('language', 'N/A')))}\n"
                    f"{DOT_LN}\n"
                    f"{italic_sans(r.get('desc', '')[:150])}\n"
                    f"\n{S['globe']} {italic_sans('Source')}: {bold_sans('GitHub')}\n"
                    f"{LINE2}"
                )
                if avatar:
                    await downloader.send_photo_telegram(bot, chat_id, avatar, caption)
                else:
                    await bot.send_message(chat_id=chat_id, text=caption)
                sent_count += 1

            # ═══ WIKI ═══
            elif rtype == "wiki":
                img = r.get("image_url", "") or r.get("thumbnail", "")
                caption = (
                    f"{S['book']} {bold_sans(r.get('title', 'Article')[:50])}\n"
                    f"{DOT_LN}\n"
                    f"{italic_sans(r.get('extract', '')[:400])}\n"
                    f"\n{S['globe']} {italic_sans('Source')}: {bold_sans('Wikipedia')}\n"
                    f"{LINE2}"
                )
                if len(caption) > 1024:
                    caption = caption[:1020] + "..."
                if img:
                    await downloader.send_photo_telegram(bot, chat_id, img, caption)
                else:
                    await bot.send_message(chat_id=chat_id, text=caption)
                sent_count += 1

            # ═══ DATASET ═══
            elif rtype == "dataset":
                text = (
                    f"{S['robot']} {bold_sans(r.get('title', 'Dataset')[:50])}\n"
                    f"{DOT_LN}\n"
                    f"{S['recv']} {italic_sans('Downloads')}: {bold_sans(str(r.get('downloads', 0)))}\n"
                    f"{S['heart']} {italic_sans('Likes')}: {bold_sans(str(r.get('likes', 0)))}\n"
                    f"{S['puzzle']} {italic_sans('Tags')}: {mono_font(r.get('tags', '')[:60])}\n"
                    f"\n{S['globe']} {italic_sans('Source')}: {bold_sans('Hugging Face')}\n"
                    f"{LINE2}"
                )
                await bot.send_message(chat_id=chat_id, text=text)
                sent_count += 1

            await asyncio.sleep(0.5)  # Rate limiting

        except Exception as e:
            logger.error(f"Error sending result {i}: {e}")
            continue

    # Footer with navigation
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(
            f"⬅️ {bold_sans('Page')} {page-1}",
            callback_data=f"p|{category}|{query[:40]}|{page-1}"
        ))
    nav_buttons.append(InlineKeyboardButton(
        f"➡️ {bold_sans('Page')} {page+1}",
        callback_data=f"p|{category}|{query[:40]}|{page+1}"
    ))

    footer_text = (
        f"\n{LINE2}\n"
        f"{S['check']} {bold_sans('Sent')}: {bold_sans(str(sent_count))} / {len(results)} {italic_sans('results')}\n"
        f"{S['spark']} {italic_sans('Page')} {bold_sans(str(page))} {S['dot']} {italic_sans('Category')}: {bold_sans(category)}\n"
        f"{LINE3}\n"
    )

    keyboard = [
        nav_buttons,
        [
            InlineKeyboardButton(f"{S['folder']} Categories", callback_data="menu_cat"),
            InlineKeyboardButton(f"{S['globe']} Home", callback_data="menu_home"),
        ]
    ]

    await bot.send_message(
        chat_id=chat_id,
        text=footer_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ══════════════════════════════════════════
#  𝗕𝗢𝗧 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦
# ══════════════════════════════════════════

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "User"

    text = (
        f"\n{TOP}\n"
        f"{SIDE}  {S['crown']} {neg_squared('ULTIMATE MEDIA BOT')} {S['crown']}\n"
        f"{BOT}\n\n"
        f"{S['spark']} {script_font('Welcome')}, {bold_sans(name)}! {S['spark']}\n\n"
        f"{LINE2}\n\n"
        f"{S['robot']} {fraktur_font('What I Can Do')}:\n\n"
        f"  {S['frame']} {bold_sans('Images')} {S['dot']} {italic_sans('Openverse 800M+, NASA, Wikimedia')}\n"
        f"  {S['wall']} {bold_sans('Wallpapers')} {S['dot']} {italic_sans('Wallhaven HD/4K')}\n"
        f"  {S['anime']} {bold_sans('Anime')} {S['dot']} {italic_sans('MAL, Kitsu, Waifu pics')}\n"
        f"  {S['film']} {bold_sans('Movies')} {S['dot']} {italic_sans('Internet Archive Free')}\n"
        f"  {S['vid']} {bold_sans('Videos')} {S['dot']} {italic_sans('Archive.org, NASA')}\n"
        f"  {S['music']} {bold_sans('Music')} {S['dot']} {italic_sans('Archive Audio, Free Music')}\n"
        f"  {S['books']} {bold_sans('Books')} {S['dot']} {italic_sans('Gutenberg 70K+ ebooks')}\n"
        f"  {S['code']} {bold_sans('Code')} {S['dot']} {italic_sans('GitHub Repos')}\n"
        f"  {S['robot']} {bold_sans('Datasets')} {S['dot']} {italic_sans('Hugging Face AI')}\n"
        f"  {S['rocket']} {bold_sans('NASA')} {S['dot']} {italic_sans('Space photos & videos')}\n"
        f"  {S['book']} {bold_sans('Wikipedia')} {S['dot']} {italic_sans('Knowledge articles')}\n"
        f"  {S['sakura']} {bold_sans('Waifu')} {S['dot']} {italic_sans('Anime character images')}\n\n"
        f"{LINE2}\n\n"
        f"{S['bolt']} {bold_italic('Everything shows INSIDE Telegram!')}\n"
        f"{S['bolt']} {bold_italic('Photos, Videos, Audio - All Native!')}\n"
        f"{S['bolt']} {bold_italic('NO external links needed!')}\n\n"
        f"{S['arrow']} {bold_sans('Just type anything to search!')}\n\n"
        f"{LINE3}\n"
    )

    kb = [
        [
            InlineKeyboardButton(f"{S['mag']}  {bold_sans('Search All')}", callback_data="cat|all"),
        ],
        [
            InlineKeyboardButton(f"{S['frame']} Images", callback_data="cat|images"),
            InlineKeyboardButton(f"{S['wall']} Walls", callback_data="cat|wallpapers"),
            InlineKeyboardButton(f"{S['anime']} Anime", callback_data="cat|anime"),
        ],
        [
            InlineKeyboardButton(f"{S['film']} Movies", callback_data="cat|movies"),
            InlineKeyboardButton(f"{S['vid']} Videos", callback_data="cat|videos"),
            InlineKeyboardButton(f"{S['music']} Music", callback_data="cat|music"),
        ],
        [
            InlineKeyboardButton(f"{S['books']} Books", callback_data="cat|books"),
            InlineKeyboardButton(f"{S['code']} Code", callback_data="cat|code"),
            InlineKeyboardButton(f"{S['robot']} AI Data", callback_data="cat|datasets"),
        ],
        [
            InlineKeyboardButton(f"{S['rocket']} NASA", callback_data="cat|nasa_img"),
            InlineKeyboardButton(f"{S['book']} Wiki", callback_data="cat|wiki"),
            InlineKeyboardButton(f"{S['sakura']} Waifu", callback_data="cat|waifu"),
        ],
        [
            InlineKeyboardButton(f"{S['dice']}  {bold_sans('Random')}", callback_data="random"),
            InlineKeyboardButton(f"❓ {bold_sans('Help')}", callback_data="help"),
        ],
    ]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = (
        f"\n{TOP}\n"
        f"{SIDE}  {S['book']} {bold_sans('COMMANDS & HELP')} {S['book']}\n"
        f"{BOT}\n\n"
        f"{S['arrow']} {bold_sans('Search Commands')}:\n\n"
        f"  {S['tri']} /search {italic_sans('query')} {S['dot']} All databases\n"
        f"  {S['tri']} /image {italic_sans('query')} {S['dot']} Photos & images\n"
        f"  {S['tri']} /wallpaper {italic_sans('query')} {S['dot']} HD wallpapers\n"
        f"  {S['tri']} /anime {italic_sans('query')} {S['dot']} Anime search\n"
        f"  {S['tri']} /waifu {italic_sans('category')} {S['dot']} Anime images\n"
        f"  {S['tri']} /movie {italic_sans('query')} {S['dot']} Free movies\n"
        f"  {S['tri']} /video {italic_sans('query')} {S['dot']} Free videos\n"
        f"  {S['tri']} /music {italic_sans('query')} {S['dot']} Free music\n"
        f"  {S['tri']} /book {italic_sans('query')} {S['dot']} Free ebooks\n"
        f"  {S['tri']} /code {italic_sans('query')} {S['dot']} GitHub repos\n"
        f"  {S['tri']} /dataset {italic_sans('query')} {S['dot']} AI datasets\n"
        f"  {S['tri']} /nasa {italic_sans('query')} {S['dot']} NASA media\n"
        f"  {S['tri']} /wiki {italic_sans('query')} {S['dot']} Wikipedia\n"
        f"  {S['tri']} /random {S['dot']} Random discovery\n\n"
        f"{LINE2}\n\n"
        f"{S['spark']} {bold_italic('PRO TIP')}: Just type anything!\n"
        f"   {italic_sans('Bot auto-searches in your last category')}\n\n"
        f"{S['check']} {bold_sans('Waifu Categories')}:\n"
        f"   {mono_font('waifu neko shinobu megumin')}\n"
        f"   {mono_font('hug pat smile wave dance')}\n"
        f"   {mono_font('kiss blush happy wink cry')}\n\n"
        f"{LINE3}\n"
    )

    kb = [[InlineKeyboardButton(f"{S['arrow2']} Back", callback_data="menu_home")]]

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))


# ─── Category-specific commands ───

async def _do_search(update, ctx, query, category):
    if not query:
        USER_DATA[update.effective_user.id] = {"cat": category}
        text = (
            f"\n{LINE2}\n"
            f"{S['mag']} {bold_sans(category.upper())} {bold_sans('SEARCH')}\n\n"
            f"{S['arrow']} {italic_sans('Type your search query:')}\n"
            f"{S['dot']} {italic_sans('I will search and show results')}\n"
            f"{S['dot']} {bold_italic('directly in Telegram!')}\n"
            f"{LINE2}\n"
        )
        await update.message.reply_text(text)
        return
    
    await update.message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
    
    loading = (
        f"\n{S['bolt']} {bold_sans('Searching')}...\n"
        f"{S['mag']} {italic_sans(query)}\n"
        f"{S['folder']} {italic_sans(category)}\n"
        f"{SPARK}\n"
    )
    msg = await update.message.reply_text(loading)
    
    results = await _fetch_results(query, category)
    await msg.delete()
    await send_results_to_telegram(ctx.bot, update.effective_chat.id, results, query, category)


async def _fetch_results(query, category, page=1):
    """Fetch results from APIs based on category"""
    if category == "images":
        r1 = await search_openverse_images(query, page, 5)
        r2 = await search_wikimedia_images(query, 3)
        return r1 + r2
    elif category == "wallpapers":
        return await search_wallhaven(query, page, 8)
    elif category == "anime":
        r1 = await search_anime_jikan(query, page, 5)
        r2 = await search_anime_kitsu(query, 3)
        return r1 + r2
    elif category == "movies" or category == "videos":
        return await search_archive_video(query, 5, page)
    elif category == "music":
        return await search_archive_audio(query, 5, page)
    elif category == "books":
        return await search_gutenberg(query, 5, page)
    elif category == "code":
        return await search_github_repos(query, 5, page)
    elif category == "datasets":
        return await search_huggingface(query, 5)
    elif category == "nasa_img":
        return await search_nasa(query, "image", 5)
    elif category == "nasa_vid":
        return await search_nasa(query, "video", 5)
    elif category == "wiki":
        return await search_wikipedia(query, 3)
    elif category == "waifu":
        urls = await get_waifu_many(query or "waifu", 5)
        return [{"type": "image", "title": f"Waifu {query}", "image_url": u,
                 "creator": "Waifu.pics", "source": "Waifu.pics", "license": "API"} for u in urls]
    elif category == "all":
        all_r = []
        tasks = [
            search_openverse_images(query, 1, 3),
            search_wallhaven(query, 1, 2),
            search_anime_jikan(query, 1, 2),
            search_archive_video(query, 2, 1),
            search_archive_audio(query, 2, 1),
            search_gutenberg(query, 2, 1),
            search_nasa(query, "image", 2),
        ]
        gathered = await asyncio.gather(*tasks, return_exceptions=True)
        for r in gathered:
            if isinstance(r, list):
                all_r.extend(r)
        return all_r
    return []


async def cmd_search(update, ctx):
    q = " ".join(ctx.args) if ctx.args else ""
    await _do_search(update, ctx, q, "all")

async def cmd_image(update, ctx):
    q = " ".join(ctx.args) if ctx.args else ""
    await _do_search(update, ctx, q, "images")

async def cmd_wallpaper(update, ctx):
    q = " ".join(ctx.args) if ctx.args else ""
    await _do_search(update, ctx, q, "wallpapers")

async def cmd_anime(update, ctx):
    q = " ".join(ctx.args) if ctx.args else ""
    await _do_search(update, ctx, q, "anime")

async def cmd_movie(update, ctx):
    q = " ".join(ctx.args) if ctx.args else ""
    await _do_search(update, ctx, q, "movies")

async def cmd_video(update, ctx):
    q = " ".join(ctx.args) if ctx.args else ""
    await _do_search(update, ctx, q, "videos")

async def cmd_music(update, ctx):
    q = " ".join(ctx.args) if ctx.args else ""
    await _do_search(update, ctx, q, "music")

async def cmd_book(update, ctx):
    q = " ".join(ctx.args) if ctx.args else ""
    await _do_search(update, ctx, q, "books")

async def cmd_code(update, ctx):
    q = " ".join(ctx.args) if ctx.args else ""
    await _do_search(update, ctx, q, "code")

async def cmd_dataset(update, ctx):
    q = " ".join(ctx.args) if ctx.args else ""
    await _do_search(update, ctx, q, "datasets")

async def cmd_nasa(update, ctx):
    q = " ".join(ctx.args) if ctx.args else ""
    await _do_search(update, ctx, q, "nasa_img")

async def cmd_wiki(update, ctx):
    q = " ".join(ctx.args) if ctx.args else ""
    await _do_search(update, ctx, q, "wiki")

async def cmd_waifu(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    cat = ctx.args[0] if ctx.args else "waifu"
    
    valid = ["waifu", "neko", "shinobu", "megumin", "bully", "cuddle",
             "cry", "hug", "awoo", "kiss", "lick", "pat", "smug",
             "bonk", "yeet", "blush", "smile", "wave", "highfive",
             "handhold", "nom", "bite", "glomp", "slap", "kill",
             "kick", "happy", "wink", "poke", "dance", "cringe"]

    if cat.lower() not in valid:
        text = (
            f"\n{S['sakura']} {bold_sans('WAIFU CATEGORIES')}\n"
            f"{DOT_LN}\n\n"
        )
        for i in range(0, len(valid), 5):
            row = valid[i:i+5]
            text += "  " + "  ".join([f"{S['cherry']} {mono_font(c)}" for c in row]) + "\n"
        text += f"\n{S['arrow']} {italic_sans('Usage')}: /waifu {mono_font('category')}\n{LINE2}"
        await update.message.reply_text(text)
        return

    await update.message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
    urls = await get_waifu_many(cat.lower(), 5)

    if not urls:
        await update.message.reply_text(f"{S['cross']} {bold_sans('No images found')}")
        return

    header = (
        f"\n{S['sakura']} {bold_sans('WAIFU')} {S['dot']} {circled(cat.upper())}\n"
        f"{SPARK}\n"
    )
    await update.message.reply_text(header)

    for i, url in enumerate(urls):
        caption = (
            f"{S['cherry']} {bold_sans(f'Waifu {cat.title()}')} #{i+1}\n"
            f"{S['key']} {italic_sans('Category')}: {mono_font(cat)}\n"
            f"{S['globe']} {italic_sans('Source')}: {bold_sans('waifu.pics')}\n"
            f"{LINE2}"
        )
        await downloader.send_photo_telegram(ctx.bot, update.effective_chat.id, url, caption)
        await asyncio.sleep(0.3)

    # More button
    kb = [[InlineKeyboardButton(f"{S['sakura']} More {cat.title()}", callback_data=f"waifu|{cat}")]]
    await ctx.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{S['check']} {bold_sans('5 images sent!')} {S['point']} {italic_sans('Want more?')}",
        reply_markup=InlineKeyboardMarkup(kb)
    )


async def cmd_random(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    queries = ["nature", "space", "ocean", "sunset", "city", "mountain",
               "abstract", "cyberpunk", "naruto", "galaxy", "flowers",
               "aurora", "waterfall", "forest", "lightning", "robot"]
    cats = ["images", "wallpapers", "anime", "nasa_img", "waifu"]

    q = random.choice(queries)
    c = random.choice(cats)

    text = (
        f"\n{S['dice']} {bold_sans('RANDOM DISCOVERY')}\n"
        f"{S['mag']} {italic_sans(q)} {S['dot']} {italic_sans(c)}\n"
        f"{SPARK}\n"
    )
    await update.message.reply_text(text)
    await update.message.reply_chat_action(ChatAction.UPLOAD_PHOTO)

    if c == "waifu":
        urls = await get_waifu_many("waifu", 3)
        results = [{"type": "image", "title": "Random Waifu", "image_url": u,
                    "creator": "Waifu.pics", "source": "Waifu.pics", "license": "API"} for u in urls]
    else:
        results = await _fetch_results(q, c)

    await send_results_to_telegram(ctx.bot, update.effective_chat.id, results, q, c)


# ── Callback Handler ──

async def callback_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    uid = update.effective_user.id
    chat_id = update.effective_chat.id

    if data == "menu_home":
        await query.message.delete()
        # Fake update for start
        update.message = query.message
        await cmd_start(update, ctx)

    elif data == "menu_cat":
        text = (
            f"\n{TOP}\n"
            f"{SIDE}  {S['folder']} {bold_sans('CATEGORIES')} {S['folder']}\n"
            f"{BOT}\n\n"
            f"{S['arrow']} {italic_sans('Choose a category:')}\n\n"
            f"{LINE2}\n"
        )
        kb = [
            [
                InlineKeyboardButton(f"{S['frame']} Images", callback_data="cat|images"),
                InlineKeyboardButton(f"{S['wall']} Walls", callback_data="cat|wallpapers"),
                InlineKeyboardButton(f"{S['anime']} Anime", callback_data="cat|anime"),
            ],
            [
                InlineKeyboardButton(f"{S['film']} Movies", callback_data="cat|movies"),
                InlineKeyboardButton(f"{S['vid']} Videos", callback_data="cat|videos"),
                InlineKeyboardButton(f"{S['music']} Music", callback_data="cat|music"),
            ],
            [
                InlineKeyboardButton(f"{S['books']} Books", callback_data="cat|books"),
                InlineKeyboardButton(f"{S['code']} Code", callback_data="cat|code"),
                InlineKeyboardButton(f"{S['robot']} Datasets", callback_data="cat|datasets"),
            ],
            [
                InlineKeyboardButton(f"{S['rocket']} NASA", callback_data="cat|nasa_img"),
                InlineKeyboardButton(f"{S['book']} Wiki", callback_data="cat|wiki"),
                InlineKeyboardButton(f"{S['sakura']} Waifu", callback_data="cat|waifu"),
            ],
            [InlineKeyboardButton(f"{S['arrow2']} Home", callback_data="menu_home")],
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))

    elif data == "help":
        await cmd_help(update, ctx)

    elif data == "random":
        await query.message.delete()
        update.message = query.message
        await cmd_random(update, ctx)

    elif data.startswith("cat|"):
        cat = data.split("|")[1]
        USER_DATA[uid] = {"cat": cat}

        if cat == "waifu":
            text = (
                f"\n{S['sakura']} {bold_sans('WAIFU IMAGES')}\n"
                f"{DOT_LN}\n"
                f"{S['arrow']} {italic_sans('Choose a category:')}\n\n"
            )
            valid = ["waifu", "neko", "shinobu", "megumin", "hug", "pat",
                     "smile", "wave", "dance", "kiss", "blush", "happy",
                     "wink", "cry", "cuddle", "awoo"]
            kb = []
            for i in range(0, len(valid), 3):
                row = [InlineKeyboardButton(f"{S['cherry']} {v.title()}", callback_data=f"waifu|{v}")
                       for v in valid[i:i+3]]
                kb.append(row)
            kb.append([InlineKeyboardButton(f"{S['arrow2']} Back", callback_data="menu_cat")])
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))
        else:
            text = (
                f"\n{LINE2}\n"
                f"{S['mag']} {bold_sans(cat.upper())} {bold_sans('SEARCH')}\n\n"
                f"{S['arrow']} {italic_sans('Type your search query now!')}\n"
                f"{S['dot']} {bold_italic('Results will appear as native Telegram media')}\n"
                f"{LINE2}\n"
            )
            kb = [[InlineKeyboardButton(f"{S['arrow2']} Back", callback_data="menu_cat")]]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("waifu|"):
        wcat = data.split("|")[1]
        await query.message.delete()
        await ctx.bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_PHOTO)

        urls = await get_waifu_many(wcat, 5)
        for i, url in enumerate(urls):
            caption = (
                f"{S['cherry']} {bold_sans(f'Waifu {wcat.title()}')} #{i+1}\n"
                f"{S['key']} {mono_font(wcat)} {S['dot']} {italic_sans('waifu.pics')}\n"
                f"{LINE2}"
            )
            await downloader.send_photo_telegram(ctx.bot, chat_id, url, caption)
            await asyncio.sleep(0.3)

        kb = [
            [InlineKeyboardButton(f"{S['sakura']} More {wcat.title()}", callback_data=f"waifu|{wcat}")],
            [InlineKeyboardButton(f"{S['arrow2']} Categories", callback_data="cat|waifu")],
        ]
        await ctx.bot.send_message(
            chat_id=chat_id,
            text=f"{S['check']} {bold_sans('5 sent!')} {italic_sans('More?')}",
            reply_markup=InlineKeyboardMarkup(kb)
        )

    elif data.startswith("p|"):
        # Pagination: p|category|query|page
        parts = data.split("|")
        if len(parts) >= 4:
            cat = parts[1]
            q = parts[2]
            pg = int(parts[3])
            await query.message.delete()
            await ctx.bot.send_chat_action(chat_id=chat_id, action=ChatAction.UPLOAD_PHOTO)

            loading = f"{S['bolt']} {bold_sans('Loading page')} {pg}..."
            await ctx.bot.send_message(chat_id=chat_id, text=loading)

            results = await _fetch_results(q, cat, pg)
            await send_results_to_telegram(ctx.bot, chat_id, results, q, cat, pg)


# ── Text message handler (auto search) ──

async def text_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text.strip()
    if text.startswith("/"):
        return

    uid = update.effective_user.id
    cat = USER_DATA.get(uid, {}).get("cat", "all")

    await update.message.reply_chat_action(ChatAction.UPLOAD_PHOTO)

    loading = (
        f"\n{S['bolt']} {bold_sans('Searching')}...\n"
        f"{S['mag']} {script_font(text)}\n"
        f"{S['folder']} {italic_sans(cat)}\n"
        f"{SPARK}\n"
    )
    msg = await update.message.reply_text(loading)

    results = await _fetch_results(text, cat)
    await msg.delete()
    await send_results_to_telegram(ctx.bot, update.effective_chat.id, results, text, cat)


# ══════════════════════════════════════════
#  🌐 WEB SERVER (Render)
# ══════════════════════════════════════════

async def health(request):
    return web.json_response({
        "status": "alive",
        "bot": "Ultimate Media Bot v2",
        "features": "Images, Videos, Audio, Anime - ALL inside Telegram",
        "time": datetime.now().isoformat()
    })

async def webhook(request):
    try:
        data = await request.json()
        update = Update.de_json(data, request.app["bot"].bot)
        await request.app["bot"].process_update(update)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    return web.Response(status=200)


# ══════════════════════════════════════════
#  🚀 MAIN
# ══════════════════════════════════════════

async def post_init(app):
    cmds = [
        BotCommand("start", "🏠 Home"),
        BotCommand("search", "🔍 Search all"),
        BotCommand("image", "🖼️ Images"),
        BotCommand("wallpaper", "🌄 Wallpapers"),
        BotCommand("anime", "🌸 Anime"),
        BotCommand("waifu", "🌸 Waifu images"),
        BotCommand("movie", "🎬 Movies"),
        BotCommand("video", "📹 Videos"),
        BotCommand("music", "🎵 Music"),
        BotCommand("book", "📚 Books"),
        BotCommand("code", "💻 GitHub"),
        BotCommand("dataset", "🤖 AI Datasets"),
        BotCommand("nasa", "🚀 NASA"),
        BotCommand("wiki", "📖 Wikipedia"),
        BotCommand("random", "🎲 Random"),
        BotCommand("help", "❓ Help"),
    ]
    await app.bot.set_my_commands(cmds)
    logger.info(f"{S['check']} Bot commands set!")


def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # Commands
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("search", cmd_search))
    app.add_handler(CommandHandler("image", cmd_image))
    app.add_handler(CommandHandler("wallpaper", cmd_wallpaper))
    app.add_handler(CommandHandler("anime", cmd_anime))
    app.add_handler(CommandHandler("waifu", cmd_waifu))
    app.add_handler(CommandHandler("movie", cmd_movie))
    app.add_handler(CommandHandler("video", cmd_video))
    app.add_handler(CommandHandler("music", cmd_music))
    app.add_handler(CommandHandler("book", cmd_book))
    app.add_handler(CommandHandler("code", cmd_code))
    app.add_handler(CommandHandler("dataset", cmd_dataset))
    app.add_handler(CommandHandler("nasa", cmd_nasa))
    app.add_handler(CommandHandler("wiki", cmd_wiki))
    app.add_handler(CommandHandler("random", cmd_random))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    if WEBHOOK_URL:
        logger.info(f"🌐 WEBHOOK mode on port {PORT}")
        web_app = web.Application()
        web_app["bot"] = app

        web_app.router.add_get("/", health)
        web_app.router.add_get("/health", health)
        web_app.router.add_post(f"/webhook/{BOT_TOKEN}", webhook)

        async def on_startup(wa):
            await app.initialize()
            await app.bot.set_webhook(f"{WEBHOOK_URL}/webhook/{BOT_TOKEN}",
                                      allowed_updates=["message", "callback_query"])
            await app.start()
            logger.info(f"{S['check']} Webhook: {WEBHOOK_URL}/webhook/***")

        async def on_shutdown(wa):
            await downloader.close()
            await app.stop()
            await app.shutdown()

        web_app.on_startup.append(on_startup)
        web_app.on_shutdown.append(on_shutdown)
        web.run_app(web_app, host="0.0.0.0", port=PORT)
    else:
        logger.info("🖥️ POLLING mode")
        app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()