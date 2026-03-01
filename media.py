# media.py - Ultimate Open Source Media Bot 🎬
# Single File - God Level Telegram Bot
# Host on Render Web Service (Free Tier)

import os
import logging
import asyncio
import aiohttp
import html
import random
import string
import tempfile
from datetime import datetime
from urllib.parse import quote_plus, urlencode
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    InputMediaPhoto, BotCommand
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, ConversationHandler
)
from telegram.constants import ParseMode, ChatAction
from aiohttp import web

# ═══════════════════════════════════════════════════════════
# 📋 CONFIGURATION
# ═══════════════════════════════════════════════════════════

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")  # e.g. https://your-app.onrender.com

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════
# 🎨 STYLISH SYMBOLS & FONTS COLLECTION
# ═══════════════════════════════════════════════════════════

SYM = {
    # Status & Indicators
    "star": "✦", "star2": "✧", "diamond": "◆", "diamond2": "◇",
    "circle": "●", "circle2": "○", "dot": "•", "arrow": "➤",
    "arrow2": "➜", "arrow3": "➥", "arrow4": "⟫", "check": "✅",
    "cross": "❌", "fire": "🔥", "spark": "✨", "lightning": "⚡",
    "crown": "👑", "trophy": "🏆", "gem": "💎", "heart": "❤️",
    "rocket": "🚀", "globe": "🌍", "link": "🔗", "lock": "🔒",
    "unlock": "🔓", "key": "🔑", "magnify": "🔍", "bell": "🔔",
    "pin": "📌", "clip": "📎", "book": "📖", "scroll": "📜",
    "folder": "📁", "package": "📦", "cd": "💿", "film": "🎬",
    "camera": "📷", "tv": "📺", "radio": "📻", "headphone": "🎧",
    "mic": "🎤", "art": "🎨", "palette": "🎭", "music": "🎵",
    "note": "🎶", "game": "🎮", "dice": "🎲", "puzzle": "🧩",
    "robot": "🤖", "alien": "👽", "ghost": "👻", "skull": "💀",
    "eye": "👁️", "brain": "🧠", "dna": "🧬", "atom": "⚛️",
    "wave": "〰️", "infinity": "♾️", "yin": "☯️", "peace": "☮️",
    
    # Decorative Lines & Borders
    "line": "━━━━━━━━━━━━━━━━━━",
    "line2": "═══════════════════",
    "line3": "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
    "line4": "◈━━━━━━━━━━━━━━━◈",
    "line5": "╔══════════════════╗",
    "line6": "╚══════════════════╝",
    "line7": "┃",
    "dotline": "┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈",
    
    # Categories
    "movie": "🎬", "video": "📹", "image": "🖼️", "wallpaper": "🌄",
    "anime": "🌸", "music_cat": "🎵", "book_cat": "📚", "game_cat": "🎮",
    "science": "🔬", "space": "🚀", "news": "📰", "edu": "🎓",
    "code": "💻", "design": "🎨", "photo": "📸", "audio": "🔊",
    "doc": "📄", "data": "📊", "ai": "🤖", "three_d": "🧊",
}

def stylish_text(text, style="bold"):
    """Convert text to stylish Unicode fonts"""
    styles = {
        "bold": str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
            '𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵'
        ),
        "italic": str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            '𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻'
        ),
        "bold_italic": str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            '𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯'
        ),
        "mono": str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
            '𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿'
        ),
        "script": str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            '𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏'
        ),
        "double": str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
            '𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡'
        ),
        "circle": str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            'ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ'
        ),
        "square": str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            '🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉'
        ),
        "neg_square": str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            '🅰🅱🅲🅳🅴🅵🅶🅷🅸🅹🅺🅻🅼🅽🅾🅿🆀🆁🆂🆃🆄🆅🆆🆇🆈🆉'
        ),
    }
    if style in styles:
        return text.translate(styles[style])
    return text

# ═══════════════════════════════════════════════════════════
# 🌐 OPEN SOURCE DATABASE REGISTRY - WORLD'S LARGEST COLLECTION
# ═══════════════════════════════════════════════════════════

DATABASES = {
    # ──────────────────────────────────────────────────────
    # 🎬 MOVIES & FILMS
    # ──────────────────────────────────────────────────────
    "movies": {
        "icon": "🎬",
        "title": "𝗠𝗼𝘃𝗶𝗲𝘀 & 𝗙𝗶𝗹𝗺𝘀",
        "desc": "Free movies, films, documentaries from open databases",
        "sources": [
            {
                "name": "Internet Archive Movies",
                "icon": "🏛️",
                "url": "https://archive.org/details/movies",
                "search_url": "https://archive.org/search?query={query}&and[]=mediatype%3A%22movies%22",
                "api_url": "https://archive.org/advancedsearch.php?q={query}+mediatype:movies&output=json&rows={limit}&page={page}",
                "api_type": "archive_org",
                "desc": "World's largest free movie archive",
                "license": "Public Domain / Various",
                "count": "10M+ items"
            },
            {
                "name": "Archive Public Domain Movies",
                "icon": "🎞️",
                "url": "https://archive.org/details/publicmovies212",
                "search_url": "https://archive.org/search?query={query}+collection%3Apublicmovies212&and[]=mediatype%3A%22movies%22",
                "api_url": "https://archive.org/advancedsearch.php?q={query}+collection:publicmovies212&output=json&rows={limit}&page={page}",
                "api_type": "archive_org",
                "desc": "Curated public domain films",
                "license": "Public Domain",
                "count": "5000+ films"
            },
            {
                "name": "Archive Feature Films",
                "icon": "🎭",
                "url": "https://archive.org/details/feature_films",
                "search_url": "https://archive.org/search?query={query}+collection%3Afeature_films",
                "api_url": "https://archive.org/advancedsearch.php?q={query}+collection:feature_films&output=json&rows={limit}&page={page}",
                "api_type": "archive_org",
                "desc": "Feature-length free films",
                "license": "Public Domain",
                "count": "3000+ films"
            },
            {
                "name": "TMDB (TheMovieDB)",
                "icon": "🎥",
                "url": "https://www.themoviedb.org",
                "search_url": "https://www.themoviedb.org/search?query={query}",
                "api_url": "https://api.themoviedb.org/3/search/movie?api_key=demo&query={query}&page={page}",
                "api_type": "tmdb",
                "desc": "Movie info database (community built)",
                "license": "CC BY-NC 4.0",
                "count": "900K+ movies"
            },
            {
                "name": "OMDb API",
                "icon": "📀",
                "url": "https://www.omdbapi.com",
                "search_url": "https://www.omdbapi.com/?s={query}&type=movie",
                "api_type": "omdb",
                "desc": "Open movie database API",
                "license": "CC BY-NC 4.0",
                "count": "500K+ titles"
            },
            {
                "name": "Wikidata Movies",
                "icon": "📊",
                "url": "https://www.wikidata.org",
                "search_url": "https://www.wikidata.org/w/index.php?search={query}&ns0=1",
                "api_type": "wikidata",
                "desc": "Structured movie data from Wikidata",
                "license": "CC0",
                "count": "1M+ entries"
            },
            {
                "name": "Open Movie Database",
                "icon": "🎦",
                "url": "https://archive.org/details/open_source_movies",
                "search_url": "https://archive.org/search?query={query}+collection%3Aopen_source_movies",
                "api_url": "https://archive.org/advancedsearch.php?q={query}+collection:open_source_movies&output=json&rows={limit}&page={page}",
                "api_type": "archive_org",
                "desc": "Community contributed open source films",
                "license": "Various CC",
                "count": "50K+ videos"
            },
        ]
    },
    
    # ──────────────────────────────────────────────────────
    # 📹 VIDEOS
    # ──────────────────────────────────────────────────────
    "videos": {
        "icon": "📹",
        "title": "𝗩𝗶𝗱𝗲𝗼𝘀",
        "desc": "Free stock videos, clips, footage from open databases",
        "sources": [
            {
                "name": "Pexels Videos",
                "icon": "🎬",
                "url": "https://www.pexels.com/videos/",
                "search_url": "https://www.pexels.com/search/videos/{query}/",
                "api_url": "https://api.pexels.com/videos/search?query={query}&per_page={limit}&page={page}",
                "api_type": "pexels_video",
                "desc": "Free HD/4K stock video clips",
                "license": "Pexels License (Free)",
                "count": "50K+ videos"
            },
            {
                "name": "Pixabay Videos",
                "icon": "📽️",
                "url": "https://pixabay.com/videos/",
                "search_url": "https://pixabay.com/videos/search/{query}/",
                "api_url": "https://pixabay.com/api/videos/?key={api_key}&q={query}&per_page={limit}&page={page}",
                "api_type": "pixabay_video",
                "desc": "Free stock videos, motion graphics",
                "license": "Pixabay License (Free)",
                "count": "100K+ videos"
            },
            {
                "name": "Archive.org Community Video",
                "icon": "🏛️",
                "url": "https://archive.org/details/opensource_movies",
                "search_url": "https://archive.org/search?query={query}+mediatype%3Amovies+collection%3Aopensource_movies",
                "api_url": "https://archive.org/advancedsearch.php?q={query}+collection:opensource_movies&output=json&rows={limit}&page={page}",
                "api_type": "archive_org",
                "desc": "Community uploaded free videos",
                "license": "Various",
                "count": "500K+ videos"
            },
            {
                "name": "Coverr",
                "icon": "🎞️",
                "url": "https://coverr.co",
                "search_url": "https://coverr.co/s?q={query}",
                "api_type": "web_only",
                "desc": "Beautiful free stock video footage",
                "license": "Free (Coverr License)",
                "count": "5K+ videos"
            },
            {
                "name": "Videvo",
                "icon": "🎥",
                "url": "https://www.videvo.net",
                "search_url": "https://www.videvo.net/search/{query}/",
                "api_type": "web_only",
                "desc": "Free stock footage & motion graphics",
                "license": "Various (CC/Free)",
                "count": "20K+ clips"
            },
            {
                "name": "Pond5 Public Domain",
                "icon": "🌊",
                "url": "https://www.pond5.com/free",
                "search_url": "https://www.pond5.com/free?kw={query}",
                "api_type": "web_only",
                "desc": "Historic & public domain videos",
                "license": "Public Domain",
                "count": "80K+ clips"
            },
            {
                "name": "Mixkit",
                "icon": "🎭",
                "url": "https://mixkit.co/free-stock-video/",
                "search_url": "https://mixkit.co/free-stock-video/{query}/",
                "api_type": "web_only",
                "desc": "High quality free stock videos",
                "license": "Mixkit License (Free)",
                "count": "10K+ videos"
            },
            {
                "name": "NASA Video Gallery",
                "icon": "🚀",
                "url": "https://images.nasa.gov",
                "search_url": "https://images.nasa.gov/#/search-results?q={query}&media=video",
                "api_url": "https://images-api.nasa.gov/search?q={query}&media_type=video&page={page}",
                "api_type": "nasa",
                "desc": "Space videos, launches, ISS footage",
                "license": "Public Domain (NASA)",
                "count": "50K+ videos"
            },
        ]
    },
    
    # ──────────────────────────────────────────────────────
    # 🖼️ IMAGES
    # ──────────────────────────────────────────────────────
    "images": {
        "icon": "🖼️",
        "title": "𝗜𝗺𝗮𝗴𝗲𝘀",
        "desc": "Free images, photos, graphics from open databases",
        "sources": [
            {
                "name": "Unsplash",
                "icon": "📸",
                "url": "https://unsplash.com",
                "search_url": "https://unsplash.com/s/photos/{query}",
                "api_url": "https://api.unsplash.com/search/photos?query={query}&per_page={limit}&page={page}",
                "api_type": "unsplash",
                "desc": "High-quality free photos",
                "license": "Unsplash License",
                "count": "5M+ photos"
            },
            {
                "name": "Pexels Photos",
                "icon": "🖼️",
                "url": "https://www.pexels.com",
                "search_url": "https://www.pexels.com/search/{query}/",
                "api_url": "https://api.pexels.com/v1/search?query={query}&per_page={limit}&page={page}",
                "api_type": "pexels_photo",
                "desc": "Free stock photos",
                "license": "Pexels License",
                "count": "3M+ photos"
            },
            {
                "name": "Pixabay Images",
                "icon": "🎨",
                "url": "https://pixabay.com",
                "search_url": "https://pixabay.com/images/search/{query}/",
                "api_url": "https://pixabay.com/api/?key={api_key}&q={query}&per_page={limit}&page={page}",
                "api_type": "pixabay_image",
                "desc": "Free images, vectors, illustrations",
                "license": "Pixabay License",
                "count": "4M+ images"
            },
            {
                "name": "Openverse",
                "icon": "🌐",
                "url": "https://openverse.org",
                "search_url": "https://openverse.org/search/image?q={query}",
                "api_url": "https://api.openverse.org/v1/images/?q={query}&page={page}&page_size={limit}",
                "api_type": "openverse",
                "desc": "800M+ CC-licensed images search engine",
                "license": "Various CC",
                "count": "800M+ images"
            },
            {
                "name": "Wikimedia Commons",
                "icon": "🏛️",
                "url": "https://commons.wikimedia.org",
                "search_url": "https://commons.wikimedia.org/w/index.php?search={query}&title=Special:MediaSearch&type=image",
                "api_url": "https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={query}+filetype:image&srnamespace=6&format=json&srlimit={limit}",
                "api_type": "wikimedia",
                "desc": "Free media repository by Wikipedia",
                "license": "CC / Public Domain",
                "count": "100M+ files"
            },
            {
                "name": "StockSnap (CC0)",
                "icon": "📷",
                "url": "https://stocksnap.io",
                "search_url": "https://stocksnap.io/search/{query}",
                "api_type": "web_only",
                "desc": "CC0 public domain photos",
                "license": "CC0",
                "count": "50K+ photos"
            },
            {
                "name": "Public Domain Pictures",
                "icon": "🏞️",
                "url": "https://www.publicdomainpictures.net",
                "search_url": "https://www.publicdomainpictures.net/en/search.php?q={query}",
                "api_type": "web_only",
                "desc": "Public domain stock photos",
                "license": "Public Domain",
                "count": "200K+ images"
            },
            {
                "name": "NASA Images",
                "icon": "🚀",
                "url": "https://images.nasa.gov",
                "search_url": "https://images.nasa.gov/#/search-results?q={query}&media=image",
                "api_url": "https://images-api.nasa.gov/search?q={query}&media_type=image&page={page}",
                "api_type": "nasa",
                "desc": "Space, astronomy, NASA photos",
                "license": "Public Domain (NASA)",
                "count": "200K+ images"
            },
            {
                "name": "Library of Congress",
                "icon": "📚",
                "url": "https://www.loc.gov/pictures/",
                "search_url": "https://www.loc.gov/pictures/search/?q={query}",
                "api_url": "https://www.loc.gov/search/?q={query}&fa=online-format:image&fo=json&sp={page}&c={limit}",
                "api_type": "loc",
                "desc": "Historic photos & prints",
                "license": "Public Domain",
                "count": "1M+ images"
            },
            {
                "name": "Smithsonian Open Access",
                "icon": "🏛️",
                "url": "https://www.si.edu/openaccess",
                "search_url": "https://www.si.edu/search/images?edan_q={query}",
                "api_url": "https://api.si.edu/openaccess/api/v1.0/search?q={query}&rows={limit}&start={offset}&api_key=DEMO_KEY",
                "api_type": "smithsonian",
                "desc": "Smithsonian museum collections",
                "license": "CC0",
                "count": "4.5M+ images"
            },
            {
                "name": "Metropolitan Museum of Art",
                "icon": "🖼️",
                "url": "https://www.metmuseum.org/art/collection",
                "search_url": "https://www.metmuseum.org/art/collection/search?q={query}",
                "api_url": "https://collectionapi.metmuseum.org/public/collection/v1/search?q={query}&hasImages=true",
                "api_type": "met",
                "desc": "Art masterpieces collection",
                "license": "CC0 / Public Domain",
                "count": "500K+ artworks"
            },
            {
                "name": "Rijksmuseum",
                "icon": "🎨",
                "url": "https://www.rijksmuseum.nl/en/rijksstudio",
                "search_url": "https://www.rijksmuseum.nl/en/search?q={query}",
                "api_url": "https://www.rijksmuseum.nl/api/en/collection?q={query}&key=demo&format=json&ps={limit}&p={page}",
                "api_type": "rijks",
                "desc": "Dutch Masters art collection",
                "license": "CC0 / Public Domain",
                "count": "700K+ artworks"
            },
            {
                "name": "National Gallery of Art",
                "icon": "🖌️",
                "url": "https://www.nga.gov/artworks/free-images-and-open-access.html",
                "search_url": "https://www.nga.gov/collection-search-result.html?artobj_imagesonly=Images_online&keyword={query}",
                "api_type": "web_only",
                "desc": "60K+ fine art images",
                "license": "CC0",
                "count": "60K+ artworks"
            },
            {
                "name": "Google Open Images",
                "icon": "🔍",
                "url": "https://storage.googleapis.com/openimages/web/index.html",
                "search_url": "https://storage.googleapis.com/openimages/web/visualizer/index.html?type=detection&set=train&c={query}",
                "api_type": "web_only",
                "desc": "9M+ labeled images dataset",
                "license": "CC BY 4.0",
                "count": "9M+ images"
            },
        ]
    },
    
    # ──────────────────────────────────────────────────────
    # 🌄 WALLPAPERS
    # ──────────────────────────────────────────────────────
    "wallpapers": {
        "icon": "🌄",
        "title": "𝗪𝗮𝗹𝗹𝗽𝗮𝗽𝗲𝗿𝘀",
        "desc": "Free HD/4K wallpapers from open databases",
        "sources": [
            {
                "name": "Unsplash Wallpapers",
                "icon": "📱",
                "url": "https://unsplash.com/wallpapers",
                "search_url": "https://unsplash.com/s/photos/{query}-wallpaper",
                "api_type": "web_only",
                "desc": "Premium quality wallpapers",
                "license": "Unsplash License",
                "count": "500K+ wallpapers"
            },
            {
                "name": "Pexels Wallpapers",
                "icon": "🖥️",
                "url": "https://www.pexels.com/search/wallpaper/",
                "search_url": "https://www.pexels.com/search/{query}%20wallpaper/",
                "api_type": "web_only",
                "desc": "Free desktop & phone wallpapers",
                "license": "Pexels License",
                "count": "200K+ wallpapers"
            },
            {
                "name": "Wallhaven",
                "icon": "🎭",
                "url": "https://wallhaven.cc",
                "search_url": "https://wallhaven.cc/search?q={query}",
                "api_url": "https://wallhaven.cc/api/v1/search?q={query}&page={page}",
                "api_type": "wallhaven",
                "desc": "Largest wallpaper community",
                "license": "Various",
                "count": "1M+ wallpapers"
            },
            {
                "name": "Simple Desktops",
                "icon": "💻",
                "url": "https://simpledesktops.com",
                "search_url": "https://simpledesktops.com/browse/?q={query}",
                "api_type": "web_only",
                "desc": "Minimal, clean desktop wallpapers",
                "license": "Free",
                "count": "1K+ wallpapers"
            },
            {
                "name": "Pixabay Wallpapers",
                "icon": "🌅",
                "url": "https://pixabay.com/images/search/wallpaper/",
                "search_url": "https://pixabay.com/images/search/{query}+wallpaper/",
                "api_type": "web_only",
                "desc": "Free wallpaper images",
                "license": "Pixabay License",
                "count": "100K+ wallpapers"
            },
        ]
    },
    
    # ──────────────────────────────────────────────────────
    # 🌸 ANIME
    # ──────────────────────────────────────────────────────
    "anime": {
        "icon": "🌸",
        "title": "𝗔𝗻𝗶𝗺𝗲",
        "desc": "Anime databases, info, images",
        "sources": [
            {
                "name": "MyAnimeList (Jikan API)",
                "icon": "📋",
                "url": "https://myanimelist.net",
                "search_url": "https://myanimelist.net/search/all?q={query}",
                "api_url": "https://api.jikan.moe/v4/anime?q={query}&limit={limit}&page={page}",
                "api_type": "jikan",
                "desc": "World's largest anime database",
                "license": "Open API",
                "count": "60K+ anime"
            },
            {
                "name": "AniList",
                "icon": "📊",
                "url": "https://anilist.co",
                "search_url": "https://anilist.co/search/anime?search={query}",
                "api_url": "https://graphql.anilist.co",
                "api_type": "anilist",
                "desc": "Modern anime & manga tracking",
                "license": "Open API",
                "count": "50K+ anime"
            },
            {
                "name": "Kitsu",
                "icon": "🦊",
                "url": "https://kitsu.io",
                "search_url": "https://kitsu.io/anime?text={query}",
                "api_url": "https://kitsu.io/api/edge/anime?filter[text]={query}&page[limit]={limit}&page[offset]={offset}",
                "api_type": "kitsu",
                "desc": "Anime & manga discovery platform",
                "license": "Open API",
                "count": "45K+ anime"
            },
            {
                "name": "AniDB",
                "icon": "🗃️",
                "url": "https://anidb.net",
                "search_url": "https://anidb.net/anime/?adb.search={query}&do.search=1",
                "api_type": "web_only",
                "desc": "Detailed anime database",
                "license": "Open",
                "count": "15K+ anime"
            },
            {
                "name": "Anime-Planet",
                "icon": "🌍",
                "url": "https://www.anime-planet.com",
                "search_url": "https://www.anime-planet.com/anime/all?name={query}",
                "api_type": "web_only",
                "desc": "Anime recommendations & info",
                "license": "Open",
                "count": "50K+ anime"
            },
            {
                "name": "Waifu.pics (Anime Images)",
                "icon": "🎌",
                "url": "https://waifu.pics",
                "api_url": "https://api.waifu.pics/sfw/{query}",
                "api_type": "waifu",
                "desc": "Anime images API (SFW)",
                "license": "Open API",
                "count": "100K+ images"
            },
            {
                "name": "Nekos.life (Anime API)",
                "icon": "🐱",
                "url": "https://nekos.life",
                "api_url": "https://nekos.life/api/v2/img/{query}",
                "api_type": "nekos",
                "desc": "Anime images & fun API",
                "license": "Open API",
                "count": "50K+ images"
            },
            {
                "name": "Trace.moe (Anime Scene Search)",
                "icon": "🔍",
                "url": "https://trace.moe",
                "search_url": "https://trace.moe/?url={query}",
                "api_type": "web_only",
                "desc": "Search anime by screenshot",
                "license": "Open API",
                "count": "60K+ anime indexed"
            },
        ]
    },
    
    # ──────────────────────────────────────────────────────
    # 🎵 MUSIC & AUDIO
    # ──────────────────────────────────────────────────────
    "music": {
        "icon": "🎵",
        "title": "𝗠𝘂𝘀𝗶𝗰 & 𝗔𝘂𝗱𝗶𝗼",
        "desc": "Free music, sound effects, audio databases",
        "sources": [
            {
                "name": "Free Music Archive",
                "icon": "🎶",
                "url": "https://freemusicarchive.org",
                "search_url": "https://freemusicarchive.org/search?quicksearch={query}",
                "api_type": "web_only",
                "desc": "Free CC-licensed music",
                "license": "Various CC",
                "count": "200K+ tracks"
            },
            {
                "name": "Jamendo Music",
                "icon": "🎸",
                "url": "https://www.jamendo.com",
                "search_url": "https://www.jamendo.com/search?qs=fq={query}",
                "api_url": "https://api.jamendo.com/v3.0/tracks/?client_id=demo&search={query}&limit={limit}&offset={offset}",
                "api_type": "jamendo",
                "desc": "Free music for creators",
                "license": "CC / Free",
                "count": "700K+ tracks"
            },
            {
                "name": "Archive.org Audio",
                "icon": "🏛️",
                "url": "https://archive.org/details/audio",
                "search_url": "https://archive.org/search?query={query}&and[]=mediatype%3A%22audio%22",
                "api_url": "https://archive.org/advancedsearch.php?q={query}+mediatype:audio&output=json&rows={limit}&page={page}",
                "api_type": "archive_org",
                "desc": "Free audio archive",
                "license": "Various",
                "count": "5M+ audio items"
            },
            {
                "name": "Freesound",
                "icon": "🔊",
                "url": "https://freesound.org",
                "search_url": "https://freesound.org/search/?q={query}",
                "api_type": "web_only",
                "desc": "Sound effects & ambient sounds",
                "license": "CC",
                "count": "600K+ sounds"
            },
            {
                "name": "ccMixter",
                "icon": "🎛️",
                "url": "https://ccmixter.org",
                "search_url": "https://ccmixter.org/search?search_text={query}",
                "api_type": "web_only",
                "desc": "Community remix music",
                "license": "CC",
                "count": "50K+ tracks"
            },
            {
                "name": "Musopen",
                "icon": "🎻",
                "url": "https://musopen.org",
                "search_url": "https://musopen.org/search/?q={query}",
                "api_type": "web_only",
                "desc": "Free classical music recordings",
                "license": "Public Domain / CC",
                "count": "10K+ recordings"
            },
            {
                "name": "MusicBrainz",
                "icon": "📀",
                "url": "https://musicbrainz.org",
                "search_url": "https://musicbrainz.org/search?query={query}&type=recording",
                "api_url": "https://musicbrainz.org/ws/2/recording/?query={query}&fmt=json&limit={limit}&offset={offset}",
                "api_type": "musicbrainz",
                "desc": "Open music encyclopedia",
                "license": "CC0 / CC BY-NC-SA",
                "count": "30M+ recordings"
            },
            {
                "name": "BBC Sound Effects",
                "icon": "📻",
                "url": "https://sound-effects.bbcrewind.co.uk",
                "search_url": "https://sound-effects.bbcrewind.co.uk/search?q={query}",
                "api_type": "web_only",
                "desc": "BBC's sound effects library",
                "license": "Personal/Educational use",
                "count": "33K+ sounds"
            },
        ]
    },
    
    # ──────────────────────────────────────────────────────
    # 📚 BOOKS & DOCUMENTS
    # ──────────────────────────────────────────────────────
    "books": {
        "icon": "📚",
        "title": "𝗕𝗼𝗼𝗸𝘀 & 𝗗𝗼𝗰𝘂𝗺𝗲𝗻𝘁𝘀",
        "desc": "Free ebooks, textbooks, documents, papers",
        "sources": [
            {
                "name": "Project Gutenberg",
                "icon": "📖",
                "url": "https://www.gutenberg.org",
                "search_url": "https://www.gutenberg.org/ebooks/search/?query={query}",
                "api_url": "https://gutendex.com/books/?search={query}&page={page}",
                "api_type": "gutenberg",
                "desc": "70K+ free classic ebooks",
                "license": "Public Domain",
                "count": "70K+ books"
            },
            {
                "name": "Open Library",
                "icon": "🏛️",
                "url": "https://openlibrary.org",
                "search_url": "https://openlibrary.org/search?q={query}",
                "api_url": "https://openlibrary.org/search.json?q={query}&limit={limit}&page={page}",
                "api_type": "openlibrary",
                "desc": "Open catalog of every book",
                "license": "Open",
                "count": "20M+ books"
            },
            {
                "name": "Archive.org Texts",
                "icon": "📜",
                "url": "https://archive.org/details/texts",
                "search_url": "https://archive.org/search?query={query}&and[]=mediatype%3A%22texts%22",
                "api_url": "https://archive.org/advancedsearch.php?q={query}+mediatype:texts&output=json&rows={limit}&page={page}",
                "api_type": "archive_org",
                "desc": "Millions of free texts & books",
                "license": "Various",
                "count": "30M+ texts"
            },
            {
                "name": "Google Books (Preview)",
                "icon": "📗",
                "url": "https://books.google.com",
                "search_url": "https://www.google.com/search?tbm=bks&q={query}",
                "api_url": "https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={limit}&startIndex={offset}",
                "api_type": "google_books",
                "desc": "Book previews & info",
                "license": "Various",
                "count": "40M+ books indexed"
            },
            {
                "name": "Standard Ebooks",
                "icon": "📕",
                "url": "https://standardebooks.org",
                "search_url": "https://standardebooks.org/ebooks?query={query}",
                "api_type": "web_only",
                "desc": "Beautifully formatted free ebooks",
                "license": "Public Domain",
                "count": "800+ books"
            },
            {
                "name": "arXiv (Research Papers)",
                "icon": "📄",
                "url": "https://arxiv.org",
                "search_url": "https://arxiv.org/search/?query={query}&searchtype=all",
                "api_url": "http://export.arxiv.org/api/query?search_query=all:{query}&start={offset}&max_results={limit}",
                "api_type": "arxiv",
                "desc": "Open access research papers",
                "license": "Open Access",
                "count": "2M+ papers"
            },
            {
                "name": "CORE (Research Papers)",
                "icon": "🔬",
                "url": "https://core.ac.uk",
                "search_url": "https://core.ac.uk/search?q={query}",
                "api_type": "web_only",
                "desc": "Aggregator of open access papers",
                "license": "Open Access",
                "count": "300M+ papers"
            },
            {
                "name": "Semantic Scholar",
                "icon": "🧠",
                "url": "https://www.semanticscholar.org",
                "search_url": "https://www.semanticscholar.org/search?q={query}",
                "api_url": "https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={limit}&offset={offset}",
                "api_type": "semantic_scholar",
                "desc": "AI-powered research paper search",
                "license": "Open API",
                "count": "200M+ papers"
            },
        ]
    },
    
    # ──────────────────────────────────────────────────────
    # 🎮 GAMES & GAME ASSETS
    # ──────────────────────────────────────────────────────
    "games": {
        "icon": "🎮",
        "title": "𝗚𝗮𝗺𝗲𝘀 & 𝗔𝘀𝘀𝗲𝘁𝘀",
        "desc": "Free games, game assets, sprites, 3D models",
        "sources": [
            {
                "name": "itch.io (Free Games)",
                "icon": "🕹️",
                "url": "https://itch.io/games/free",
                "search_url": "https://itch.io/search?q={query}&type=games&price=free",
                "api_type": "web_only",
                "desc": "Indie games, many free",
                "license": "Various",
                "count": "500K+ games"
            },
            {
                "name": "OpenGameArt",
                "icon": "🎨",
                "url": "https://opengameart.org",
                "search_url": "https://opengameart.org/art-search-advanced?keys={query}",
                "api_type": "web_only",
                "desc": "Free game art, sprites, textures",
                "license": "CC / GPL / Public Domain",
                "count": "80K+ assets"
            },
            {
                "name": "Kenney Assets",
                "icon": "🧩",
                "url": "https://kenney.nl/assets",
                "search_url": "https://kenney.nl/assets?q={query}",
                "api_type": "web_only",
                "desc": "Public domain game assets",
                "license": "CC0",
                "count": "40K+ assets"
            },
            {
                "name": "RAWG Game Database",
                "icon": "📊",
                "url": "https://rawg.io",
                "search_url": "https://rawg.io/search?query={query}",
                "api_url": "https://api.rawg.io/api/games?search={query}&key=demo&page={page}&page_size={limit}",
                "api_type": "rawg",
                "desc": "Video game database & discovery",
                "license": "Open API",
                "count": "800K+ games"
            },
            {
                "name": "IGDB (Internet Game DB)",
                "icon": "🎯",
                "url": "https://www.igdb.com",
                "search_url": "https://www.igdb.com/search?utf8=✓&q={query}",
                "api_type": "web_only",
                "desc": "Comprehensive game information",
                "license": "Open",
                "count": "300K+ games"
            },
            {
                "name": "Free3D Models",
                "icon": "🧊",
                "url": "https://free3d.com",
                "search_url": "https://free3d.com/3d-models/{query}",
                "api_type": "web_only",
                "desc": "Free 3D models for games",
                "license": "Various Free",
                "count": "100K+ models"
            },
        ]
    },
    
    # ──────────────────────────────────────────────────────
    # 💻 CODE & SOFTWARE
    # ──────────────────────────────────────────────────────
    "code": {
        "icon": "💻",
        "title": "𝗖𝗼𝗱𝗲 & 𝗦𝗼𝗳𝘁𝘄𝗮𝗿𝗲",
        "desc": "Open source code, repos, software",
        "sources": [
            {
                "name": "GitHub",
                "icon": "🐙",
                "url": "https://github.com",
                "search_url": "https://github.com/search?q={query}&type=repositories",
                "api_url": "https://api.github.com/search/repositories?q={query}&per_page={limit}&page={page}",
                "api_type": "github",
                "desc": "World's largest code repository",
                "license": "Various Open Source",
                "count": "300M+ repos"
            },
            {
                "name": "GitLab",
                "icon": "🦊",
                "url": "https://gitlab.com",
                "search_url": "https://gitlab.com/search?search={query}",
                "api_url": "https://gitlab.com/api/v4/projects?search={query}&per_page={limit}&page={page}",
                "api_type": "gitlab",
                "desc": "Open source DevOps platform",
                "license": "Various",
                "count": "30M+ repos"
            },
            {
                "name": "SourceForge",
                "icon": "📦",
                "url": "https://sourceforge.net",
                "search_url": "https://sourceforge.net/directory/?q={query}",
                "api_type": "web_only",
                "desc": "Classic open source software hosting",
                "license": "Various Open Source",
                "count": "500K+ projects"
            },
            {
                "name": "Archive.org Software",
                "icon": "🏛️",
                "url": "https://archive.org/details/software",
                "search_url": "https://archive.org/search?query={query}&and[]=mediatype%3A%22software%22",
                "api_url": "https://archive.org/advancedsearch.php?q={query}+mediatype:software&output=json&rows={limit}&page={page}",
                "api_type": "archive_org",
                "desc": "Historical & free software archive",
                "license": "Various",
                "count": "500K+ items"
            },
            {
                "name": "F-Droid (Android FOSS)",
                "icon": "🤖",
                "url": "https://f-droid.org",
                "search_url": "https://search.f-droid.org/?q={query}",
                "api_type": "web_only",
                "desc": "Free & open source Android apps",
                "license": "Various FOSS",
                "count": "5K+ apps"
            },
        ]
    },
    
    # ──────────────────────────────────────────────────────
    # 🤖 AI & DATASETS
    # ──────────────────────────────────────────────────────
    "datasets": {
        "icon": "🤖",
        "title": "𝗔𝗜 & 𝗗𝗮𝘁𝗮𝘀𝗲𝘁𝘀",
        "desc": "Open datasets for ML, AI, research",
        "sources": [
            {
                "name": "Hugging Face Datasets",
                "icon": "🤗",
                "url": "https://huggingface.co/datasets",
                "search_url": "https://huggingface.co/datasets?search={query}",
                "api_url": "https://huggingface.co/api/datasets?search={query}&limit={limit}",
                "api_type": "huggingface",
                "desc": "ML datasets hub",
                "license": "Various",
                "count": "100K+ datasets"
            },
            {
                "name": "Kaggle Datasets",
                "icon": "📊",
                "url": "https://www.kaggle.com/datasets",
                "search_url": "https://www.kaggle.com/datasets?search={query}",
                "api_type": "web_only",
                "desc": "Data science competition datasets",
                "license": "Various",
                "count": "200K+ datasets"
            },
            {
                "name": "Papers With Code",
                "icon": "📝",
                "url": "https://paperswithcode.com",
                "search_url": "https://paperswithcode.com/search?q={query}",
                "api_type": "web_only",
                "desc": "ML papers with code & datasets",
                "license": "Open",
                "count": "100K+ papers"
            },
            {
                "name": "Google Dataset Search",
                "icon": "🔍",
                "url": "https://datasetsearch.research.google.com",
                "search_url": "https://datasetsearch.research.google.com/search?query={query}",
                "api_type": "web_only",
                "desc": "Google's dataset search engine",
                "license": "Various",
                "count": "25M+ datasets"
            },
            {
                "name": "UCI ML Repository",
                "icon": "📈",
                "url": "https://archive.ics.uci.edu",
                "search_url": "https://archive.ics.uci.edu/datasets?search={query}",
                "api_type": "web_only",
                "desc": "Classic ML benchmark datasets",
                "license": "CC BY 4.0",
                "count": "600+ datasets"
            },
            {
                "name": "Data.gov (US)",
                "icon": "🇺🇸",
                "url": "https://data.gov",
                "search_url": "https://catalog.data.gov/dataset?q={query}",
                "api_type": "web_only",
                "desc": "US Government open data",
                "license": "Public Domain",
                "count": "300K+ datasets"
            },
            {
                "name": "AWS Open Data",
                "icon": "☁️",
                "url": "https://registry.opendata.aws",
                "search_url": "https://registry.opendata.aws/?search=keywords:{query}",
                "api_type": "web_only",
                "desc": "Open data on AWS",
                "license": "Various Open",
                "count": "400+ datasets"
            },
        ]
    },
    
    # ──────────────────────────────────────────────────────
    # 🧊 3D MODELS & DESIGN
    # ──────────────────────────────────────────────────────
    "three_d": {
        "icon": "🧊",
        "title": "𝟯𝗗 𝗠𝗼𝗱𝗲𝗹𝘀 & 𝗗𝗲𝘀𝗶𝗴𝗻",
        "desc": "Free 3D models, CAD files, design resources",
        "sources": [
            {
                "name": "Sketchfab (Free)",
                "icon": "🎭",
                "url": "https://sketchfab.com/search?features=downloadable&q=&sort_by=-likeCount&type=models",
                "search_url": "https://sketchfab.com/search?features=downloadable&q={query}&sort_by=-likeCount&type=models",
                "api_type": "web_only",
                "desc": "Free downloadable 3D models",
                "license": "CC / Free",
                "count": "500K+ models"
            },
            {
                "name": "Thingiverse",
                "icon": "🖨️",
                "url": "https://www.thingiverse.com",
                "search_url": "https://www.thingiverse.com/search?q={query}&type=things",
                "api_type": "web_only",
                "desc": "3D printable models",
                "license": "Various CC",
                "count": "2M+ models"
            },
            {
                "name": "Smithsonian 3D",
                "icon": "🏛️",
                "url": "https://3d.si.edu",
                "search_url": "https://3d.si.edu/search/type:3d_package?edan_q={query}",
                "api_type": "web_only",
                "desc": "Smithsonian 3D-scanned artifacts",
                "license": "CC0",
                "count": "1K+ 3D scans"
            },
            {
                "name": "Poly Haven",
                "icon": "🌄",
                "url": "https://polyhaven.com",
                "search_url": "https://polyhaven.com/models?s={query}",
                "api_type": "web_only",
                "desc": "Free HDRIs, textures, 3D models",
                "license": "CC0",
                "count": "2K+ assets"
            },
            {
                "name": "TurboSquid (Free)",
                "icon": "🐙",
                "url": "https://www.turbosquid.com/Search/3D-Models/free",
                "search_url": "https://www.turbosquid.com/Search/3D-Models/free/{query}",
                "api_type": "web_only",
                "desc": "Free 3D models collection",
                "license": "Various",
                "count": "100K+ free models"
            },
            {
                "name": "NASA 3D Resources",
                "icon": "🚀",
                "url": "https://nasa3d.arc.nasa.gov",
                "search_url": "https://nasa3d.arc.nasa.gov/search/query/{query}",
                "api_type": "web_only",
                "desc": "NASA spacecraft & planet 3D models",
                "license": "Public Domain",
                "count": "500+ models"
            },
        ]
    },
    
    # ──────────────────────────────────────────────────────
    # 🗺️ MAPS & GEO DATA
    # ──────────────────────────────────────────────────────
    "maps": {
        "icon": "🗺️",
        "title": "𝗠𝗮𝗽𝘀 & 𝗚𝗲𝗼 𝗗𝗮𝘁𝗮",
        "desc": "Free maps, geographic data, satellite imagery",
        "sources": [
            {
                "name": "OpenStreetMap",
                "icon": "🗺️",
                "url": "https://www.openstreetmap.org",
                "search_url": "https://www.openstreetmap.org/search?query={query}",
                "api_type": "web_only",
                "desc": "Free, editable world map",
                "license": "ODbL",
                "count": "Entire world mapped"
            },
            {
                "name": "NASA Earthdata",
                "icon": "🌍",
                "url": "https://earthdata.nasa.gov",
                "search_url": "https://search.earthdata.nasa.gov/search?q={query}",
                "api_type": "web_only",
                "desc": "Earth science satellite data",
                "license": "Public Domain",
                "count": "50PB+ data"
            },
            {
                "name": "Natural Earth",
                "icon": "🌐",
                "url": "https://www.naturalearthdata.com",
                "search_url": "https://www.naturalearthdata.com/downloads/",
                "api_type": "web_only",
                "desc": "Free vector & raster map data",
                "license": "Public Domain",
                "count": "Global datasets"
            },
            {
                "name": "Mapillary (Street Images)",
                "icon": "📸",
                "url": "https://www.mapillary.com",
                "search_url": "https://www.mapillary.com/app/?lat=0&lng=0&z=2&focus=map",
                "api_type": "web_only",
                "desc": "Crowd-sourced street-level photos",
                "license": "CC BY-SA",
                "count": "2B+ images"
            },
        ]
    },
    
    # ──────────────────────────────────────────────────────
    # 🔬 SCIENCE & EDUCATION
    # ──────────────────────────────────────────────────────
    "science": {
        "icon": "🔬",
        "title": "𝗦𝗰𝗶𝗲𝗻𝗰𝗲 & 𝗘𝗱𝘂𝗰𝗮𝘁𝗶𝗼𝗻",
        "desc": "Scientific data, educational resources",
        "sources": [
            {
                "name": "Wikipedia",
                "icon": "📖",
                "url": "https://en.wikipedia.org",
                "search_url": "https://en.wikipedia.org/w/index.php?search={query}",
                "api_url": "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json&srlimit={limit}",
                "api_type": "wikipedia",
                "desc": "Free encyclopedia",
                "license": "CC BY-SA",
                "count": "60M+ articles"
            },
            {
                "name": "PubMed (Medical Papers)",
                "icon": "🏥",
                "url": "https://pubmed.ncbi.nlm.nih.gov",
                "search_url": "https://pubmed.ncbi.nlm.nih.gov/?term={query}",
                "api_type": "web_only",
                "desc": "Biomedical research papers",
                "license": "Open Access",
                "count": "36M+ papers"
            },
            {
                "name": "Khan Academy",
                "icon": "🎓",
                "url": "https://www.khanacademy.org",
                "search_url": "https://www.khanacademy.org/search?page_search_query={query}",
                "api_type": "web_only",
                "desc": "Free educational content",
                "license": "CC BY-NC-SA",
                "count": "10K+ lessons"
            },
            {
                "name": "MIT OpenCourseWare",
                "icon": "🏛️",
                "url": "https://ocw.mit.edu",
                "search_url": "https://ocw.mit.edu/search/?q={query}",
                "api_type": "web_only",
                "desc": "Free MIT course materials",
                "license": "CC BY-NC-SA",
                "count": "2500+ courses"
            },
            {
                "name": "Wolfram Alpha",
                "icon": "🧮",
                "url": "https://www.wolframalpha.com",
                "search_url": "https://www.wolframalpha.com/input?i={query}",
                "api_type": "web_only",
                "desc": "Computational knowledge engine",
                "license": "Various",
                "count": "Trillions of data"
            },
        ]
    },
    
    # ──────────────────────────────────────────────────────
    # 📰 NEWS & MEDIA
    # ──────────────────────────────────────────────────────
    "news": {
        "icon": "📰",
        "title": "𝗡𝗲𝘄𝘀 & 𝗠𝗲𝗱𝗶𝗮",
        "desc": "Open news archives & media databases",
        "sources": [
            {
                "name": "Wayback Machine",
                "icon": "⏰",
                "url": "https://web.archive.org",
                "search_url": "https://web.archive.org/web/*/{query}*",
                "api_type": "web_only",
                "desc": "Archived web pages & news",
                "license": "Archive",
                "count": "890B+ pages"
            },
            {
                "name": "GDELT Project",
                "icon": "🌍",
                "url": "https://www.gdeltproject.org",
                "search_url": "https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=artlist&format=html",
                "api_type": "web_only",
                "desc": "Global news database",
                "license": "Open",
                "count": "Billions of events"
            },
            {
                "name": "Common Crawl",
                "icon": "🕸️",
                "url": "https://commoncrawl.org",
                "search_url": "https://index.commoncrawl.org/CC-MAIN-2024-10-index?url={query}&output=json",
                "api_type": "web_only",
                "desc": "Open web crawl data",
                "license": "Open",
                "count": "250B+ pages"
            },
        ]
    },
    
    # ──────────────────────────────────────────────────────
    # 🎭 ICONS, FONTS & DESIGN RESOURCES
    # ──────────────────────────────────────────────────────
    "design": {
        "icon": "🎨",
        "title": "𝗗𝗲𝘀𝗶𝗴𝗻 𝗥𝗲𝘀𝗼𝘂𝗿𝗰𝗲𝘀",
        "desc": "Free icons, fonts, UI kits, design tools",
        "sources": [
            {
                "name": "Google Fonts",
                "icon": "🔤",
                "url": "https://fonts.google.com",
                "search_url": "https://fonts.google.com/?query={query}",
                "api_type": "web_only",
                "desc": "Free web fonts",
                "license": "Open Font License",
                "count": "1600+ fonts"
            },
            {
                "name": "Font Awesome",
                "icon": "⭐",
                "url": "https://fontawesome.com/icons",
                "search_url": "https://fontawesome.com/search?q={query}&o=r",
                "api_type": "web_only",
                "desc": "Popular icon library",
                "license": "CC BY 4.0 / MIT",
                "count": "2000+ free icons"
            },
            {
                "name": "Heroicons",
                "icon": "🦸",
                "url": "https://heroicons.com",
                "search_url": "https://heroicons.com/?search={query}",
                "api_type": "web_only",
                "desc": "Beautiful hand-crafted SVG icons",
                "license": "MIT",
                "count": "300+ icons"
            },
            {
                "name": "Feather Icons",
                "icon": "🪶",
                "url": "https://feathericons.com",
                "search_url": "https://feathericons.com/?query={query}",
                "api_type": "web_only",
                "desc": "Simple, beautiful open source icons",
                "license": "MIT",
                "count": "280+ icons"
            },
            {
                "name": "SVG Repo",
                "icon": "📐",
                "url": "https://www.svgrepo.com",
                "search_url": "https://www.svgrepo.com/vectors/{query}/",
                "api_type": "web_only",
                "desc": "Free SVG vectors & icons",
                "license": "Various CC / MIT",
                "count": "500K+ SVGs"
            },
            {
                "name": "Figma Community",
                "icon": "🎯",
                "url": "https://www.figma.com/community",
                "search_url": "https://www.figma.com/community/search?resource_type=mixed&sort_by=relevancy&query={query}",
                "api_type": "web_only",
                "desc": "Free design files, plugins, templates",
                "license": "CC / Free",
                "count": "100K+ resources"
            },
            {
                "name": "Dribbble (Freebies)",
                "icon": "🏀",
                "url": "https://dribbble.com/tags/freebie",
                "search_url": "https://dribbble.com/search/shots/popular/freebie?q={query}",
                "api_type": "web_only",
                "desc": "Free design resources from designers",
                "license": "Various Free",
                "count": "50K+ freebies"
            },
        ]
    },
}

# ═══════════════════════════════════════════════════════════
# 🔍 ADVANCED SEARCH ENGINE
# ═══════════════════════════════════════════════════════════

class MediaSearchEngine:
    """Advanced search engine that queries multiple open databases"""
    
    def __init__(self):
        self.session = None
        self.cache = {}
        self.search_history = {}
    
    async def get_session(self):
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=15)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def search_archive_org(self, query, limit=10, page=1):
        """Search Internet Archive"""
        results = []
        try:
            session = await self.get_session()
            url = f"https://archive.org/advancedsearch.php?q={quote_plus(query)}&output=json&rows={limit}&page={page}&fl[]=identifier,title,description,mediatype,downloads,date,creator"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json(content_type=None)
                    docs = data.get("response", {}).get("docs", [])
                    for doc in docs:
                        identifier = doc.get("identifier", "")
                        results.append({
                            "title": doc.get("title", "Unknown"),
                            "desc": (doc.get("description", "") or "")[:200],
                            "url": f"https://archive.org/details/{identifier}",
                            "download": f"https://archive.org/download/{identifier}",
                            "type": doc.get("mediatype", "unknown"),
                            "date": doc.get("date", "N/A"),
                            "creator": doc.get("creator", "Unknown"),
                            "downloads": doc.get("downloads", 0),
                            "source": "Internet Archive"
                        })
        except Exception as e:
            logger.error(f"Archive.org search error: {e}")
        return results
    
    async def search_openverse(self, query, limit=10, page=1):
        """Search Openverse (800M+ CC images)"""
        results = []
        try:
            session = await self.get_session()
            url = f"https://api.openverse.org/v1/images/?q={quote_plus(query)}&page={page}&page_size={limit}"
            headers = {"User-Agent": "MediaBot/1.0"}
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("results", []):
                        results.append({
                            "title": item.get("title", "Untitled"),
                            "desc": f"By: {item.get('creator', 'Unknown')} | License: {item.get('license', 'CC')}",
                            "url": item.get("foreign_landing_url", item.get("url", "")),
                            "thumbnail": item.get("thumbnail", ""),
                            "download": item.get("url", ""),
                            "type": "image",
                            "source": "Openverse",
                            "license": item.get("license", "CC"),
                            "creator": item.get("creator", "Unknown"),
                        })
        except Exception as e:
            logger.error(f"Openverse search error: {e}")
        return results
    
    async def search_jikan(self, query, limit=10, page=1):
        """Search MyAnimeList via Jikan API"""
        results = []
        try:
            session = await self.get_session()
            url = f"https://api.jikan.moe/v4/anime?q={quote_plus(query)}&limit={limit}&page={page}"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("data", []):
                        score = item.get("score", "N/A")
                        episodes = item.get("episodes", "?")
                        status = item.get("status", "Unknown")
                        results.append({
                            "title": item.get("title", "Unknown"),
                            "desc": f"⭐ {score} | 📺 {episodes} eps | {status}\n{(item.get('synopsis', '') or '')[:150]}",
                            "url": item.get("url", ""),
                            "thumbnail": item.get("images", {}).get("jpg", {}).get("image_url", ""),
                            "type": "anime",
                            "source": "MyAnimeList",
                            "score": score,
                            "episodes": episodes,
                        })
        except Exception as e:
            logger.error(f"Jikan search error: {e}")
        return results
    
    async def search_kitsu(self, query, limit=10, page=1):
        """Search Kitsu anime database"""
        results = []
        try:
            session = await self.get_session()
            offset = (page - 1) * limit
            url = f"https://kitsu.io/api/edge/anime?filter[text]={quote_plus(query)}&page[limit]={limit}&page[offset]={offset}"
            headers = {"Accept": "application/vnd.api+json"}
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("data", []):
                        attrs = item.get("attributes", {})
                        results.append({
                            "title": attrs.get("canonicalTitle", "Unknown"),
                            "desc": (attrs.get("synopsis", "") or "")[:200],
                            "url": f"https://kitsu.io/anime/{item.get('id', '')}",
                            "thumbnail": (attrs.get("posterImage", {}) or {}).get("small", ""),
                            "type": "anime",
                            "source": "Kitsu",
                            "score": attrs.get("averageRating", "N/A"),
                        })
        except Exception as e:
            logger.error(f"Kitsu search error: {e}")
        return results
    
    async def search_gutenberg(self, query, limit=10, page=1):
        """Search Project Gutenberg books"""
        results = []
        try:
            session = await self.get_session()
            url = f"https://gutendex.com/books/?search={quote_plus(query)}&page={page}"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("results", [])[:limit]:
                        authors = ", ".join([a.get("name", "") for a in item.get("authors", [])])
                        formats = item.get("formats", {})
                        download_url = formats.get("text/plain; charset=utf-8", 
                                      formats.get("text/plain", 
                                      formats.get("application/epub+zip", "")))
                        results.append({
                            "title": item.get("title", "Unknown"),
                            "desc": f"✍️ {authors}\n📥 Downloads: {item.get('download_count', 0)}",
                            "url": f"https://www.gutenberg.org/ebooks/{item.get('id', '')}",
                            "download": download_url,
                            "type": "book",
                            "source": "Project Gutenberg",
                            "author": authors,
                        })
        except Exception as e:
            logger.error(f"Gutenberg search error: {e}")
        return results
    
    async def search_openlibrary(self, query, limit=10, page=1):
        """Search Open Library"""
        results = []
        try:
            session = await self.get_session()
            url = f"https://openlibrary.org/search.json?q={quote_plus(query)}&limit={limit}&page={page}"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("docs", []):
                        cover_id = item.get("cover_i", "")
                        cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else ""
                        authors = ", ".join(item.get("author_name", ["Unknown"]))
                        key = item.get("key", "")
                        results.append({
                            "title": item.get("title", "Unknown"),
                            "desc": f"✍️ {authors}\n📅 {item.get('first_publish_year', 'N/A')}",
                            "url": f"https://openlibrary.org{key}",
                            "thumbnail": cover_url,
                            "type": "book",
                            "source": "Open Library",
                            "author": authors,
                        })
        except Exception as e:
            logger.error(f"Open Library search error: {e}")
        return results
    
    async def search_github(self, query, limit=10, page=1):
        """Search GitHub repositories"""
        results = []
        try:
            session = await self.get_session()
            url = f"https://api.github.com/search/repositories?q={quote_plus(query)}&per_page={limit}&page={page}&sort=stars"
            headers = {"Accept": "application/vnd.github.v3+json"}
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("items", []):
                        results.append({
                            "title": item.get("full_name", "Unknown"),
                            "desc": f"⭐ {item.get('stargazers_count', 0)} | 🍴 {item.get('forks_count', 0)} | {item.get('language', 'N/A')}\n{(item.get('description', '') or '')[:150]}",
                            "url": item.get("html_url", ""),
                            "type": "code",
                            "source": "GitHub",
                            "stars": item.get("stargazers_count", 0),
                        })
        except Exception as e:
            logger.error(f"GitHub search error: {e}")
        return results
    
    async def search_nasa(self, query, media_type="image", limit=10, page=1):
        """Search NASA Image and Video Library"""
        results = []
        try:
            session = await self.get_session()
            url = f"https://images-api.nasa.gov/search?q={quote_plus(query)}&media_type={media_type}&page={page}"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    items = data.get("collection", {}).get("items", [])[:limit]
                    for item in items:
                        item_data = item.get("data", [{}])[0]
                        links = item.get("links", [{}])
                        thumb = links[0].get("href", "") if links else ""
                        results.append({
                            "title": item_data.get("title", "Unknown"),
                            "desc": (item_data.get("description", "") or "")[:200],
                            "url": item.get("href", ""),
                            "thumbnail": thumb,
                            "type": media_type,
                            "source": "NASA",
                            "date": item_data.get("date_created", "N/A"),
                        })
        except Exception as e:
            logger.error(f"NASA search error: {e}")
        return results
    
    async def search_wikipedia(self, query, limit=10):
        """Search Wikipedia"""
        results = []
        try:
            session = await self.get_session()
            url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote_plus(query)}&format=json&srlimit={limit}"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("query", {}).get("search", []):
                        title = item.get("title", "")
                        snippet = item.get("snippet", "")
                        # Remove HTML tags from snippet
                        import re
                        snippet = re.sub(r'<[^>]+>', '', snippet)
                        results.append({
                            "title": title,
                            "desc": snippet[:200],
                            "url": f"https://en.wikipedia.org/wiki/{quote_plus(title.replace(' ', '_'))}",
                            "type": "article",
                            "source": "Wikipedia",
                        })
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
        return results
    
    async def search_wallhaven(self, query, limit=10, page=1):
        """Search Wallhaven wallpapers"""
        results = []
        try:
            session = await self.get_session()
            url = f"https://wallhaven.cc/api/v1/search?q={quote_plus(query)}&page={page}"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("data", [])[:limit]:
                        results.append({
                            "title": f"Wallhaven #{item.get('id', '')}",
                            "desc": f"📐 {item.get('resolution', 'N/A')} | 👁️ {item.get('views', 0)} views | ❤️ {item.get('favorites', 0)} favs",
                            "url": item.get("url", ""),
                            "thumbnail": item.get("thumbs", {}).get("small", ""),
                            "download": item.get("path", ""),
                            "type": "wallpaper",
                            "source": "Wallhaven",
                            "resolution": item.get("resolution", ""),
                        })
        except Exception as e:
            logger.error(f"Wallhaven search error: {e}")
        return results
    
    async def search_met_museum(self, query, limit=10):
        """Search Metropolitan Museum of Art"""
        results = []
        try:
            session = await self.get_session()
            search_url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={quote_plus(query)}&hasImages=true"
            async with session.get(search_url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    object_ids = data.get("objectIDs", [])[:limit]
                    for obj_id in object_ids:
                        try:
                            detail_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}"
                            async with session.get(detail_url) as detail_resp:
                                if detail_resp.status == 200:
                                    obj = await detail_resp.json()
                                    results.append({
                                        "title": obj.get("title", "Unknown"),
                                        "desc": f"🎨 {obj.get('artistDisplayName', 'Unknown Artist')} | 📅 {obj.get('objectDate', 'N/A')}\n{obj.get('medium', '')}",
                                        "url": obj.get("objectURL", ""),
                                        "thumbnail": obj.get("primaryImageSmall", ""),
                                        "download": obj.get("primaryImage", ""),
                                        "type": "artwork",
                                        "source": "Met Museum",
                                    })
                        except:
                            continue
        except Exception as e:
            logger.error(f"Met Museum search error: {e}")
        return results
    
    async def search_huggingface(self, query, limit=10):
        """Search Hugging Face datasets"""
        results = []
        try:
            session = await self.get_session()
            url = f"https://huggingface.co/api/datasets?search={quote_plus(query)}&limit={limit}"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data:
                        results.append({
                            "title": item.get("id", "Unknown"),
                            "desc": f"📥 {item.get('downloads', 0)} downloads | ❤️ {item.get('likes', 0)} likes",
                            "url": f"https://huggingface.co/datasets/{item.get('id', '')}",
                            "type": "dataset",
                            "source": "Hugging Face",
                        })
        except Exception as e:
            logger.error(f"Hugging Face search error: {e}")
        return results
    
    async def search_google_books(self, query, limit=10, page=1):
        """Search Google Books"""
        results = []
        try:
            session = await self.get_session()
            offset = (page - 1) * limit
            url = f"https://www.googleapis.com/books/v1/volumes?q={quote_plus(query)}&maxResults={limit}&startIndex={offset}"
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("items", []):
                        vol = item.get("volumeInfo", {})
                        authors = ", ".join(vol.get("authors", ["Unknown"]))
                        thumb = vol.get("imageLinks", {}).get("thumbnail", "")
                        results.append({
                            "title": vol.get("title", "Unknown"),
                            "desc": f"✍️ {authors} | 📅 {vol.get('publishedDate', 'N/A')}\n{(vol.get('description', '') or '')[:150]}",
                            "url": vol.get("infoLink", vol.get("previewLink", "")),
                            "thumbnail": thumb,
                            "type": "book",
                            "source": "Google Books",
                        })
        except Exception as e:
            logger.error(f"Google Books search error: {e}")
        return results
    
    async def universal_search(self, query, category="all", limit=5, page=1):
        """Search across multiple databases simultaneously"""
        all_results = []
        tasks = []
        
        search_map = {
            "movies": [
                ("archive_movies", self.search_archive_org, {"query": f"{query} collection:feature_films", "limit": limit, "page": page}),
            ],
            "videos": [
                ("archive_videos", self.search_archive_org, {"query": f"{query} mediatype:movies", "limit": limit, "page": page}),
                ("nasa_videos", self.search_nasa, {"query": query, "media_type": "video", "limit": limit, "page": page}),
            ],
            "images": [
                ("openverse", self.search_openverse, {"query": query, "limit": limit, "page": page}),
                ("nasa_images", self.search_nasa, {"query": query, "media_type": "image", "limit": limit, "page": page}),
            ],
            "wallpapers": [
                ("wallhaven", self.search_wallhaven, {"query": query, "limit": limit, "page": page}),
            ],
            "anime": [
                ("jikan", self.search_jikan, {"query": query, "limit": limit, "page": page}),
                ("kitsu", self.search_kitsu, {"query": query, "limit": limit, "page": page}),
            ],
            "music": [
                ("archive_audio", self.search_archive_org, {"query": f"{query} mediatype:audio", "limit": limit, "page": page}),
            ],
            "books": [
                ("gutenberg", self.search_gutenberg, {"query": query, "limit": limit, "page": page}),
                ("openlibrary", self.search_openlibrary, {"query": query, "limit": limit, "page": page}),
                ("google_books", self.search_google_books, {"query": query, "limit": limit, "page": page}),
            ],
            "code": [
                ("github", self.search_github, {"query": query, "limit": limit, "page": page}),
            ],
            "datasets": [
                ("huggingface", self.search_huggingface, {"query": query, "limit": limit}),
            ],
            "science": [
                ("wikipedia", self.search_wikipedia, {"query": query, "limit": limit}),
            ],
        }
        
        if category == "all":
            for cat_searches in search_map.values():
                for name, func, kwargs in cat_searches:
                    tasks.append((name, func(**kwargs)))
        elif category in search_map:
            for name, func, kwargs in search_map[category]:
                tasks.append((name, func(**kwargs)))
        
        if tasks:
            gathered = await asyncio.gather(*[t[1] for t in tasks], return_exceptions=True)
            for i, result in enumerate(gathered):
                if isinstance(result, list):
                    all_results.extend(result)
                elif isinstance(result, Exception):
                    logger.error(f"Search error in {tasks[i][0]}: {result}")
        
        return all_results

# Global search engine instance
search_engine = MediaSearchEngine()

# ═══════════════════════════════════════════════════════════
# 📱 BOT HANDLERS
# ═══════════════════════════════════════════════════════════

# User states for conversation
USER_STATES = {}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with stylish welcome"""
    user = update.effective_user
    name = user.first_name or "User"
    
    welcome = f"""
╔══════════════════════════════════╗
┃  {SYM['crown']} 𝓤𝓛𝓣𝓘𝓜𝓐𝓣𝓔  𝓜𝓔𝓓𝓘𝓐  𝓑𝓞𝓣 {SYM['crown']}  ┃
╚══════════════════════════════════╝

{SYM['spark']} 𝓦𝓮𝓵𝓬𝓸𝓶𝓮, {stylish_text(name, 'bold')}! {SYM['spark']}

◈━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◈

{SYM['robot']} {stylish_text('FEATURES', 'double')}:

{SYM['fire']} 🔍 𝗨𝗻𝗶𝘃𝗲𝗿𝘀𝗮𝗹 𝗦𝗲𝗮𝗿𝗰𝗵
   ↳ {stylish_text('100+ open databases', 'italic')} at once

{SYM['fire']} 🎬 𝗠𝗼𝘃𝗶𝗲𝘀 & 𝗙𝗶𝗹𝗺𝘀
   ↳ Archive · TMDB · Public Domain

{SYM['fire']} 🖼️ 𝗜𝗺𝗮𝗴𝗲𝘀 & 𝗣𝗵𝗼𝘁𝗼𝘀
   ↳ Openverse · NASA · Museums (800M+)

{SYM['fire']} 🌸 𝗔𝗻𝗶𝗺𝗲 𝗗𝗮𝘁𝗮𝗯𝗮𝘀𝗲
   ↳ MAL · AniList · Kitsu

{SYM['fire']} 🎵 𝗠𝘂𝘀𝗶𝗰 & 𝗔𝘂𝗱𝗶𝗼
   ↳ FMA · Jamendo · Freesound

{SYM['fire']} 📚 𝗕𝗼𝗼𝗸𝘀 & 𝗣𝗮𝗽𝗲𝗿𝘀
   ↳ Gutenberg · Open Library · arXiv

{SYM['fire']} 💻 𝗖𝗼𝗱𝗲 & 𝗗𝗮𝘁𝗮𝘀𝗲𝘁𝘀
   ↳ GitHub · HuggingFace · Kaggle

{SYM['fire']} 🧊 𝟯𝗗 𝗠𝗼𝗱𝗲𝗹𝘀
   ↳ Sketchfab · Thingiverse · NASA 3D

◈━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◈

{SYM['arrow']} {stylish_text('Quick Start', 'bold')}:
   {SYM['dot']} 𝗝𝘂𝘀𝘁 𝘁𝘆𝗽𝗲 𝗮𝗻𝘆𝘁𝗵𝗶𝗻𝗴 𝘁𝗼 𝘀𝗲𝗮𝗿𝗰𝗵!
   {SYM['dot']} /search [query] — quick search
   {SYM['dot']} /categories — browse by type
   {SYM['dot']} /help — all commands

◈━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◈

{SYM['globe']} {stylish_text('100+ Open Databases', 'bold')} {SYM['dot']} {stylish_text('Billions of Files', 'italic')}
{SYM['infinity']} {stylish_text('Free Forever', 'bold_italic')} {SYM['diamond']} {stylish_text('Zero Limits', 'bold_italic')}

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
"""
    
    keyboard = [
        [
            InlineKeyboardButton(f"{SYM['magnify']} Universal Search", callback_data="cat_all"),
            InlineKeyboardButton(f"{SYM['folder']} Categories", callback_data="categories"),
        ],
        [
            InlineKeyboardButton(f"{SYM['film']} Movies", callback_data="cat_movies"),
            InlineKeyboardButton(f"{SYM['camera']} Images", callback_data="cat_images"),
            InlineKeyboardButton(f"{SYM['anime']} Anime", callback_data="cat_anime"),
        ],
        [
            InlineKeyboardButton(f"{SYM['music']} Music", callback_data="cat_music"),
            InlineKeyboardButton(f"{SYM['book']} Books", callback_data="cat_books"),
            InlineKeyboardButton(f"{SYM['game']} Games", callback_data="cat_games"),
        ],
        [
            InlineKeyboardButton(f"{SYM['wallpaper']} Wallpapers", callback_data="cat_wallpapers"),
            InlineKeyboardButton(f"{SYM['code']} Code", callback_data="cat_code"),
            InlineKeyboardButton(f"{SYM['ai']} Datasets", callback_data="cat_datasets"),
        ],
        [
            InlineKeyboardButton(f"{SYM['three_d']} 3D Models", callback_data="cat_three_d"),
            InlineKeyboardButton(f"{SYM['globe']} Maps", callback_data="cat_maps"),
            InlineKeyboardButton(f"{SYM['science']} Science", callback_data="cat_science"),
        ],
        [
            InlineKeyboardButton(f"{SYM['art']} Design", callback_data="cat_design"),
            InlineKeyboardButton(f"{SYM['tv']} Videos", callback_data="cat_videos"),
            InlineKeyboardButton(f"{SYM['news']} News", callback_data="cat_news"),
        ],
        [
            InlineKeyboardButton(f"{SYM['scroll']} All Databases ({sum(len(v['sources']) for v in DATABASES.values())}+)", callback_data="all_databases"),
        ],
        [
            InlineKeyboardButton(f"❓ Help", callback_data="help"),
            InlineKeyboardButton(f"📊 Stats", callback_data="stats"),
        ],
    ]
    
    await update.message.reply_text(
        welcome,
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = f"""
{SYM['line5']}
{SYM['line7']}  {SYM['book']} {stylish_text('HELP & COMMANDS', 'bold')} {SYM['book']}
{SYM['line6']}

{SYM['arrow']} {stylish_text('Search Commands', 'bold')}:

  {SYM['dot']} /search <query> — Universal search
  {SYM['dot']} /movie <name> — Search movies
  {SYM['dot']} /image <query> — Search images
  {SYM['dot']} /anime <name> — Search anime
  {SYM['dot']} /music <query> — Search music
  {SYM['dot']} /book <title> — Search books
  {SYM['dot']} /video <query> — Search videos
  {SYM['dot']} /wallpaper <query> — Search wallpapers
  {SYM['dot']} /code <query> — Search GitHub repos
  {SYM['dot']} /dataset <query> — Search AI datasets
  {SYM['dot']} /three_d <query> — Search 3D models
  {SYM['dot']} /wiki <query> — Search Wikipedia
  {SYM['dot']} /nasa <query> — Search NASA media

{SYM['line4']}

{SYM['arrow']} {stylish_text('Browse Commands', 'bold')}:

  {SYM['dot']} /categories — All media categories
  {SYM['dot']} /databases — List all 100+ databases
  {SYM['dot']} /sources <category> — Sources for category
  {SYM['dot']} /stats — Bot statistics
  {SYM['dot']} /random — Random media discovery

{SYM['line4']}

{SYM['arrow']} {stylish_text('Advanced Search', 'bold')}:

  {SYM['dot']} /advsearch — Advanced search with filters
  {SYM['dot']} Type query directly → auto-search
  {SYM['dot']} Reply with page number → next page

{SYM['line4']}

{SYM['arrow']} {stylish_text('Tips', 'bold_italic')}:
  {SYM['star']} Just type anything to search!
  {SYM['star']} Use category buttons for focused search
  {SYM['star']} Click {SYM['link']} buttons to open in browser
  {SYM['star']} Use ➡️ Next buttons for more results

{SYM['line3']}
"""
    
    keyboard = [
        [InlineKeyboardButton(f"{SYM['arrow2']} Back to Menu", callback_data="back_to_start")]
    ]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            help_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text(
            help_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True
        )


async def categories_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all categories with stylish design"""
    text = f"""
{SYM['line5']}
{SYM['line7']}  {SYM['folder']} {stylish_text('MEDIA CATEGORIES', 'bold')} {SYM['folder']}
{SYM['line6']}

{SYM['spark']} {stylish_text('Choose a category to explore', 'italic')}:

"""
    
    total_sources = 0
    for key, cat in DATABASES.items():
        count = len(cat["sources"])
        total_sources += count
        text += f"  {cat['icon']} {cat['title']} — {count} sources\n"
    
    text += f"""
{SYM['line4']}

{SYM['globe']} {stylish_text('Total', 'bold')}: {total_sources}+ Open Databases
{SYM['infinity']} {stylish_text('Billions of free media files', 'italic')}

{SYM['line3']}
"""
    
    keyboard = []
    cats = list(DATABASES.items())
    for i in range(0, len(cats), 3):
        row = []
        for j in range(i, min(i+3, len(cats))):
            key, cat = cats[j]
            row.append(InlineKeyboardButton(
                f"{cat['icon']} {key.replace('_',' ').title()}", 
                callback_data=f"cat_{key}"
            ))
        keyboard.append(row)
    
    keyboard.append([
        InlineKeyboardButton(f"{SYM['magnify']} Search All", callback_data="cat_all"),
        InlineKeyboardButton(f"{SYM['arrow2']} Back", callback_data="back_to_start"),
    ])
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True
        )
    else:
        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True
        )


async def show_category_sources(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
    """Show all sources for a specific category"""
    if category not in DATABASES:
        return
    
    cat = DATABASES[category]
    text = f"""
{SYM['line5']}
{SYM['line7']}  {cat['icon']} {cat['title']} {cat['icon']}
{SYM['line6']}

{SYM['spark']} {stylish_text(cat['desc'], 'italic')}

{SYM['line4']}
"""
    
    for i, src in enumerate(cat["sources"], 1):
        text += f"""
{SYM['diamond']} {src['icon']} {stylish_text(src['name'], 'bold')}
   {SYM['dot']} {src['desc']}
   {SYM['dot']} {SYM['unlock']} {src['license']} | {SYM['package']} {src['count']}
   {SYM['dot']} {SYM['link']} {src['url']}
"""
    
    text += f"""
{SYM['line4']}

{SYM['magnify']} {stylish_text('Send me a search query for this category!', 'bold_italic')}
{SYM['arrow']} Or type: /{'movie' if category == 'movies' else category} <your query>

{SYM['line3']}
"""
    
    keyboard = [
        [InlineKeyboardButton(
            f"{SYM['magnify']} Search in {cat['title']}", 
            callback_data=f"search_in_{category}"
        )],
    ]
    
    # Add source links as buttons (max 8)
    for i in range(0, min(len(cat["sources"]), 8), 2):
        row = []
        for j in range(i, min(i+2, len(cat["sources"]), 8)):
            src = cat["sources"][j]
            row.append(InlineKeyboardButton(
                f"{src['icon']} {src['name'][:20]}", 
                url=src["url"]
            ))
        keyboard.append(row)
    
    keyboard.append([
        InlineKeyboardButton(f"{SYM['folder']} Categories", callback_data="categories"),
        InlineKeyboardButton(f"{SYM['arrow2']} Back", callback_data="back_to_start"),
    ])
    
    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                disable_web_page_preview=True
            )
        except Exception:
            await update.callback_query.message.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                disable_web_page_preview=True
            )
    else:
        await update.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            disable_web_page_preview=True
        )


async def all_databases_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show ALL databases from ALL categories"""
    text = f"""
{SYM['line5']}
{SYM['line7']}  {SYM['globe']} {stylish_text('ALL OPEN DATABASES', 'bold')} {SYM['globe']}
{SYM['line6']}

"""
    
    total = 0
    for key, cat in DATABASES.items():
        text += f"\n{cat['icon']} {stylish_text(cat['title'], 'bold')} ({len(cat['sources'])} sources)\n"
        text += f"{SYM['dotline']}\n"
        for src in cat["sources"]:
            total += 1
            text += f"  {src['icon']} {src['name']} — {src['count']}\n"
    
    text += f"""
{SYM['line4']}
{SYM['crown']} {stylish_text(f'Total: {total}+ Open Databases', 'bold')}
{SYM['line3']}
"""
    
    # Split if too long
    if len(text) > 4096:
        parts = []
        current = ""
        for line in text.split('\n'):
            if len(current) + len(line) + 1 > 4000:
                parts.append(current)
                current = line
            else:
                current += '\n' + line
        if current:
            parts.append(current)
        
        for i, part in enumerate(parts):
            keyboard = []
            if i == len(parts) - 1:
                keyboard = [[
                    InlineKeyboardButton(f"{SYM['arrow2']} Back", callback_data="back_to_start")
                ]]
            
            if update.callback_query and i == 0:
                await update.callback_query.edit_message_text(
                    part, 
                    reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None,
                    disable_web_page_preview=True
                )
            else:
                msg = update.callback_query.message if update.callback_query else update.message
                await msg.reply_text(
                    part,
                    reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None,
                    disable_web_page_preview=True
                )
    else:
        keyboard = [[
            InlineKeyboardButton(f"{SYM['arrow2']} Back", callback_data="back_to_start")
        ]]
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, reply_markup=InlineKeyboardMarkup(keyboard),
                disable_web_page_preview=True
            )
        else:
            await update.message.reply_text(
                text, reply_markup=InlineKeyboardMarkup(keyboard),
                disable_web_page_preview=True
            )



# ═══════════════════════════════════════════════════════════
# 📨 SEND FILE TO CHAT — Memory-Safe Logic for Render
# ═══════════════════════════════════════════════════════════

TELEGRAM_MAX_BYTES = 50 * 1024 * 1024  # 50 MB hard limit

async def send_file_to_chat(context, chat_id, result: dict):
    """
    Send a media file to a Telegram chat.
    Strategy:
      1. Try direct URL send via Telegram API (no disk usage).
      2. On failure → temp download → upload → IMMEDIATE os.remove().
    """
    url      = result.get("download") or result.get("url", "")
    title    = (result.get("title") or "media")[:60]
    r_type   = result.get("type", "media")
    caption  = (
        f"{SYM['film']} {stylish_text(title, 'bold')}\n"
        f"{SYM['dot']} {stylish_text('Source', 'italic')}: {result.get('source', 'Unknown')}\n"
        f"{SYM['link']} {url}"
    )

    if not url:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"{SYM['cross']} {stylish_text('No downloadable link found for this item.', 'bold')}"
        )
        return

    # ── Helpers ────────────────────────────────────────────
    async def _try_direct():
        """Attempt to send using direct URL (zero disk usage)."""
        try:
            if r_type in ("image", "wallpaper", "artwork"):
                await context.bot.send_photo(chat_id=chat_id, photo=url, caption=caption)
            elif r_type in ("audio", "music"):
                await context.bot.send_audio(chat_id=chat_id, audio=url, caption=caption)
            elif r_type in ("video", "movies", "anime"):
                await context.bot.send_video(chat_id=chat_id, video=url, caption=caption)
            else:
                await context.bot.send_document(chat_id=chat_id, document=url, caption=caption)
            return True
        except Exception as e:
            logger.warning(f"Direct URL send failed ({e}), switching to temp download...")
            return False

    async def _try_temp_download():
        """Download to /tmp, upload to Telegram, delete immediately."""
        tmp_path = None
        try:
            async with aiohttp.ClientSession() as sess:
                async with sess.get(url, timeout=aiohttp.ClientTimeout(total=120)) as resp:
                    if resp.status != 200:
                        raise Exception(f"HTTP {resp.status}")
                    # Check Content-Length before downloading
                    content_length = int(resp.headers.get("Content-Length", 0))
                    if content_length and content_length > TELEGRAM_MAX_BYTES:
                        size_mb = content_length / (1024 * 1024)
                        await context.bot.send_message(
                            chat_id=chat_id,
                            text=(
                                f"{SYM['cross']} {stylish_text('File Too Large!', 'bold')}\n\n"
                                f"{SYM['dot']} Size: {size_mb:.1f} MB\n"
                                f"{SYM['dot']} Telegram bot limit: 50 MB\n\n"
                                f"{SYM['link']} {stylish_text('Direct download link:', 'italic')}\n{url}"
                            )
                        )
                        return

                    # Write to a temp file
                    suffix = os.path.splitext(url.split("?")[0])[-1] or ".bin"
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tf:
                        tmp_path = tf.name
                        downloaded = 0
                        async for chunk in resp.content.iter_chunked(1024 * 256):
                            downloaded += len(chunk)
                            if downloaded > TELEGRAM_MAX_BYTES:
                                raise Exception("File exceeds 50 MB during download")
                            tf.write(chunk)

            # Upload from temp file
            with open(tmp_path, "rb") as f:
                if r_type in ("image", "wallpaper", "artwork"):
                    await context.bot.send_photo(chat_id=chat_id, photo=f, caption=caption)
                elif r_type in ("audio", "music"):
                    await context.bot.send_audio(chat_id=chat_id, audio=f, caption=caption)
                elif r_type in ("video", "movies", "anime"):
                    await context.bot.send_video(chat_id=chat_id, video=f, caption=caption)
                else:
                    await context.bot.send_document(chat_id=chat_id, document=f, caption=caption)

        except Exception as e:
            logger.error(f"Temp download/upload failed: {e}")
            size_info = ""
            if "50 MB" in str(e):
                size_info = (
                    f"\n\n{SYM['cross']} {stylish_text('File exceeds Telegram 50 MB limit.', 'bold')}\n"
                    f"{SYM['link']} Use the link to download directly:\n{url}"
                )
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f"{SYM['cross']} {stylish_text('Failed to send file.', 'bold')}\n"
                    f"{SYM['dot']} {str(e)[:200]}{size_info}\n\n"
                    f"{SYM['link']} {stylish_text('Direct link:', 'italic')} {url}"
                ),
                disable_web_page_preview=True
            )
        finally:
            # ✅ ALWAYS delete temp file immediately — zero permanent storage
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                    logger.info(f"Temp file deleted: {tmp_path}")
                except Exception as del_err:
                    logger.error(f"Failed to delete temp file {tmp_path}: {del_err}")

    # ── Main flow ──────────────────────────────────────────
    success = await _try_direct()
    if not success:
        await _try_temp_download()


def format_search_results(results, query, category, page=1):
    """Format search results into stylish message"""
    if not results:
        text = f"""
{SYM['line5']}
{SYM['line7']}  {SYM['magnify']} {stylish_text('SEARCH RESULTS', 'bold')} {SYM['magnify']}
{SYM['line6']}

{SYM['cross']} {stylish_text('No results found', 'bold')} for:
   "{stylish_text(query, 'italic')}"

{SYM['arrow']} {stylish_text('Tips', 'bold')}:
   {SYM['dot']} Try different keywords
   {SYM['dot']} Use English keywords for better results
   {SYM['dot']} Try a specific category search

{SYM['line3']}
"""
        return text, []
    
    cat_icon = DATABASES.get(category, {}).get("icon", SYM['magnify']) if category != "all" else SYM['globe']
    cat_name = DATABASES.get(category, {}).get("title", "All Databases") if category != "all" else "𝗨𝗻𝗶𝘃𝗲𝗿𝘀𝗮𝗹 𝗦𝗲𝗮𝗿𝗰𝗵"
    
    text = f"""
{SYM['line5']}
{SYM['line7']}  {cat_icon} {cat_name} {cat_icon}
{SYM['line6']}

{SYM['magnify']} {stylish_text('Query', 'bold')}: "{stylish_text(query, 'italic')}"
{SYM['package']} {stylish_text('Results', 'bold')}: {len(results)} found | Page {page}

{SYM['line4']}
"""
    
    buttons = []
    
    for i, r in enumerate(results[:8], 1):
        title = (r.get("title", "Unknown") or "Unknown")[:50]
        desc = (r.get("desc", "") or "")[:120]
        source = r.get("source", "Unknown")
        url = r.get("url", "")
        r_type = r.get("type", "media")
        
        type_icons = {
            "movies": "🎬", "video": "📹", "image": "🖼️", "wallpaper": "🌄",
            "anime": "🌸", "audio": "🎵", "book": "📚", "code": "💻",
            "dataset": "🤖", "artwork": "🎨", "article": "📖", "3d": "🧊",
        }
        icon = type_icons.get(r_type, "📄")
        
        text += f"""
{SYM['diamond']} {icon} {stylish_text(title, 'bold')}
   {SYM['dot']} {desc}
   {SYM['dot']} {SYM['globe']} {source}
"""
        
        result_idx = i - 1   # 0-based index into results list
        row = []
        if url:
            btn_label = f"{icon} {title[:22]}…"
            row.append(InlineKeyboardButton(btn_label, url=url))
        
        # "Send to Chat" button — uses download URL if available, else page URL
        send_url = r.get("download") or url
        if send_url:
            row.append(InlineKeyboardButton(
                f"📨 Send",
                callback_data=f"send_{result_idx}"
            ))
        
        if row:
            buttons.append(row)
        
        if r.get("download") and r.get("download") != url:
            buttons.append([InlineKeyboardButton(f"📥 Download: {title[:20]}…", url=r["download"])])
    
    text += f"""
{SYM['line4']}

{SYM['star']} {stylish_text('Click buttons below to open links', 'italic')}

{SYM['line3']}
"""
    
    # Navigation buttons
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(
            f"⬅️ Page {page-1}", 
            callback_data=f"page_{category}_{quote_plus(query)}_{page-1}"
        ))
    nav_row.append(InlineKeyboardButton(
        f"➡️ Page {page+1}", 
        callback_data=f"page_{category}_{quote_plus(query)}_{page+1}"
    ))
    buttons.append(nav_row)
    
    buttons.append([
        InlineKeyboardButton(f"{SYM['folder']} Categories", callback_data="categories"),
        InlineKeyboardButton(f"{SYM['arrow2']} Home", callback_data="back_to_start"),
    ])
    
    return text, buttons


async def perform_search(update: Update, context: ContextTypes.DEFAULT_TYPE, query: str, category: str = "all", page: int = 1):
    """Perform search and show results"""
    user_id = update.effective_user.id
    
    # Send "searching" message
    if update.callback_query:
        msg = update.callback_query.message
    else:
        msg = update.message
    
    searching_text = f"""
{SYM['line4']}
{SYM['magnify']} {stylish_text('Searching...', 'bold')}
{SYM['dot']} Query: "{stylish_text(query, 'italic')}"
{SYM['dot']} Category: {category.replace('_', ' ').title()}
{SYM['dot']} Scanning 100+ databases...
{SYM['lightning']} Please wait...
{SYM['line4']}
"""
    
    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(searching_text)
        except:
            search_msg = await msg.reply_text(searching_text)
    else:
        search_msg = await msg.reply_text(searching_text)
    
    # Perform the search
    results = await search_engine.universal_search(query, category, limit=8, page=page)
    
    # Format results
    text, buttons = format_search_results(results, query, category, page)
    
    # Store search state
    USER_STATES[user_id] = {
        "last_query": query,
        "last_category": category,
        "last_page": page,
        "last_results": results,   # ← cached for "Send to Chat" callbacks
    }
    
    keyboard = InlineKeyboardMarkup(buttons) if buttons else None
    
    # Truncate if too long
    if len(text) > 4096:
        text = text[:4090] + "\n..."
    
    try:
        if update.callback_query:
            await update.callback_query.edit_message_text(
                text, reply_markup=keyboard, disable_web_page_preview=True
            )
        else:
            await search_msg.edit_text(
                text, reply_markup=keyboard, disable_web_page_preview=True
            )
    except Exception as e:
        logger.error(f"Error sending results: {e}")
        await msg.reply_text(
            text, reply_markup=keyboard, disable_web_page_preview=True
        )


# ─── Category-specific search commands ───

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /search command"""
    query = " ".join(context.args) if context.args else ""
    if not query:
        await update.message.reply_text(
            f"{SYM['magnify']} {stylish_text('Universal Search', 'bold')}\n\n"
            f"{SYM['arrow']} Usage: /search <your query>\n"
            f"{SYM['dot']} Example: /search nature 4K\n\n"
            f"Or just type your query directly!"
        )
        return
    await perform_search(update, context, query, "all")

async def movie_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await show_category_sources(update, context, "movies")
        return
    await perform_search(update, context, query, "movies")

async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await show_category_sources(update, context, "images")
        return
    await perform_search(update, context, query, "images")

async def anime_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await show_category_sources(update, context, "anime")
        return
    await perform_search(update, context, query, "anime")

async def music_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await show_category_sources(update, context, "music")
        return
    await perform_search(update, context, query, "music")

async def book_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await show_category_sources(update, context, "books")
        return
    await perform_search(update, context, query, "books")

async def video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await show_category_sources(update, context, "videos")
        return
    await perform_search(update, context, query, "videos")

async def wallpaper_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await show_category_sources(update, context, "wallpapers")
        return
    await perform_search(update, context, query, "wallpapers")

async def code_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await show_category_sources(update, context, "code")
        return
    await perform_search(update, context, query, "code")

async def dataset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await show_category_sources(update, context, "datasets")
        return
    await perform_search(update, context, query, "datasets")

async def three_d_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await show_category_sources(update, context, "three_d")
        return
    await perform_search(update, context, query, "three_d")

async def wiki_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await update.message.reply_text(f"{SYM['arrow']} Usage: /wiki <query>")
        return
    await perform_search(update, context, query, "science")

async def nasa_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args) if context.args else ""
    if not query:
        await update.message.reply_text(f"{SYM['arrow']} Usage: /nasa <query>")
        return
    
    results = await search_engine.search_nasa(query, "image", 5)
    results += await search_engine.search_nasa(query, "video", 5)
    text, buttons = format_search_results(results, query, "images")
    keyboard = InlineKeyboardMarkup(buttons) if buttons else None
    if len(text) > 4096:
        text = text[:4090] + "\n..."
    await update.message.reply_text(text, reply_markup=keyboard, disable_web_page_preview=True)

async def random_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Random media discovery"""
    random_queries = [
        "nature", "space", "ocean", "mountain", "sunset", "city",
        "abstract", "minimal", "vintage", "cyberpunk", "fantasy",
        "naruto", "one piece", "dragon", "music", "piano",
        "python", "machine learning", "robot", "galaxy", "flowers",
        "architecture", "wildlife", "aurora", "waterfall", "desert"
    ]
    random_cats = list(DATABASES.keys())
    
    query = random.choice(random_queries)
    category = random.choice(random_cats)
    
    await update.message.reply_text(
        f"{SYM['dice']} {stylish_text('Random Discovery!', 'bold')}\n"
        f"{SYM['dot']} Query: {query}\n"
        f"{SYM['dot']} Category: {DATABASES[category]['icon']} {category}\n"
        f"{SYM['lightning']} Searching..."
    )
    
    await perform_search(update, context, query, category)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot statistics"""
    total_sources = sum(len(cat["sources"]) for cat in DATABASES.values())
    total_categories = len(DATABASES)
    
    # Estimate total items
    estimates = {
        "movies": "10M+", "videos": "1M+", "images": "900M+",
        "wallpapers": "2M+", "anime": "200K+", "music": "40M+",
        "books": "100M+", "games": "2M+", "code": "300M+",
        "datasets": "25M+", "three_d": "3M+", "maps": "Entire Planet",
        "science": "500M+", "news": "1T+", "design": "1M+"
    }
    
    text = f"""
{SYM['line5']}
{SYM['line7']}  {SYM['trophy']} {stylish_text('BOT STATISTICS', 'bold')} {SYM['trophy']}
{SYM['line6']}

{SYM['diamond']} {stylish_text('Database Coverage', 'bold')}:

   {SYM['globe']} Categories: {total_categories}
   {SYM['link']} Sources: {total_sources}+ databases
   {SYM['package']} Total Media: Billions of files

{SYM['line4']}

{SYM['diamond']} {stylish_text('Per Category Estimates', 'bold')}:

"""
    for key, cat in DATABASES.items():
        est = estimates.get(key, "N/A")
        text += f"   {cat['icon']} {cat['title']}: {est}\n"
    
    text += f"""
{SYM['line4']}

{SYM['diamond']} {stylish_text('Supported APIs', 'bold')}:

   {SYM['check']} Internet Archive API
   {SYM['check']} Openverse API (800M+ images)
   {SYM['check']} Jikan/MAL API (anime)
   {SYM['check']} Kitsu API (anime)
   {SYM['check']} Gutenberg API (books)
   {SYM['check']} Open Library API
   {SYM['check']} Google Books API
   {SYM['check']} GitHub API
   {SYM['check']} NASA API
   {SYM['check']} Wikipedia API
   {SYM['check']} Wallhaven API
   {SYM['check']} Met Museum API
   {SYM['check']} Hugging Face API
   {SYM['check']} And many more...

{SYM['line4']}

{SYM['crown']} {stylish_text('All Free & Open Source!', 'bold_italic')}
{SYM['infinity']} {stylish_text('No limits, no payments', 'italic')}

{SYM['line3']}
"""
    
    keyboard = [[InlineKeyboardButton(f"{SYM['arrow2']} Back", callback_data="back_to_start")]]
    
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True
        )
    else:
        await update.message.reply_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True
        )


# ─── Callback Query Handler ───

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all callback queries from inline buttons"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = update.effective_user.id
    
    if data == "back_to_start":
        # Recreate start message
        user = update.effective_user
        name = user.first_name or "User"
        welcome = f"""
{SYM['line5']}
{SYM['line7']}  {SYM['crown']} {stylish_text('ULTIMATE MEDIA BOT', 'bold')} {SYM['crown']}
{SYM['line6']}

{SYM['spark']} Welcome back, {stylish_text(name, 'bold')}! {SYM['spark']}

{SYM['arrow']} Choose a category or search anything!
{SYM['dot']} Just type your query to search

{SYM['line3']}
"""
        keyboard = [
            [
                InlineKeyboardButton(f"{SYM['magnify']} Search All", callback_data="cat_all"),
                InlineKeyboardButton(f"{SYM['folder']} Categories", callback_data="categories"),
            ],
            [
                InlineKeyboardButton(f"🎬 Movies", callback_data="cat_movies"),
                InlineKeyboardButton(f"🖼️ Images", callback_data="cat_images"),
                InlineKeyboardButton(f"🌸 Anime", callback_data="cat_anime"),
            ],
            [
                InlineKeyboardButton(f"🎵 Music", callback_data="cat_music"),
                InlineKeyboardButton(f"📚 Books", callback_data="cat_books"),
                InlineKeyboardButton(f"🎮 Games", callback_data="cat_games"),
            ],
            [
                InlineKeyboardButton(f"🌄 Wallpapers", callback_data="cat_wallpapers"),
                InlineKeyboardButton(f"💻 Code", callback_data="cat_code"),
                InlineKeyboardButton(f"🤖 Datasets", callback_data="cat_datasets"),
            ],
            [
                InlineKeyboardButton(f"🧊 3D", callback_data="cat_three_d"),
                InlineKeyboardButton(f"📹 Videos", callback_data="cat_videos"),
                InlineKeyboardButton(f"🎨 Design", callback_data="cat_design"),
            ],
        ]
        await query.edit_message_text(
            welcome, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True
        )
    
    elif data == "categories":
        await categories_command(update, context)
    
    elif data == "all_databases":
        await all_databases_command(update, context)
    
    elif data == "help":
        await help_command(update, context)
    
    elif data == "stats":
        await stats_command(update, context)
    
    elif data.startswith("cat_"):
        category = data[4:]  # Remove "cat_"
        if category == "all":
            # Prompt for search query
            USER_STATES[user_id] = {"awaiting_search": True, "search_category": "all"}
            text = f"""
{SYM['line4']}
{SYM['magnify']} {stylish_text('Universal Search', 'bold')}

{SYM['arrow']} {stylish_text('Type your search query:', 'italic')}
{SYM['dot']} I'll search across ALL 100+ databases

{SYM['star']} Examples:
   {SYM['dot']} "space galaxy 4K"
   {SYM['dot']} "naruto"
   {SYM['dot']} "python machine learning"
   {SYM['dot']} "beethoven symphony"
{SYM['line4']}
"""
            keyboard = [[InlineKeyboardButton(f"{SYM['arrow2']} Back", callback_data="back_to_start")]]
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        elif category in DATABASES:
            await show_category_sources(update, context, category)
    
    elif data.startswith("search_in_"):
        category = data[10:]
        USER_STATES[user_id] = {"awaiting_search": True, "search_category": category}
        cat = DATABASES.get(category, {})
        text = f"""
{SYM['line4']}
{cat.get('icon', SYM['magnify'])} {stylish_text(f"Search in {cat.get('title', category)}", 'bold')}

{SYM['arrow']} {stylish_text('Type your search query:', 'italic')}

{SYM['star']} I'll search across {len(cat.get('sources', []))} databases
{SYM['line4']}
"""
        keyboard = [[InlineKeyboardButton(f"{SYM['arrow2']} Back", callback_data=f"cat_{category}")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data.startswith("page_"):
        # Handle pagination: page_category_query_pagenum
        parts = data.split("_", 3)
        if len(parts) >= 4:
            category = parts[1]
            from urllib.parse import unquote_plus
            search_query = unquote_plus(parts[2])
            page_num = int(parts[3])
            await perform_search(update, context, search_query, category, page_num)

    elif data.startswith("send_"):
        # ── Send media file directly to this chat ──────────
        await query.answer("⏳ Sending file…", show_alert=False)
        try:
            idx = int(data[5:])
        except ValueError:
            await query.message.reply_text(f"{SYM['cross']} Invalid send request.")
            return

        state   = USER_STATES.get(user_id, {})
        results = state.get("last_results", [])

        if not results or idx >= len(results):
            await query.message.reply_text(
                f"{SYM['cross']} {stylish_text('Result expired!', 'bold')}\n"
                f"{SYM['dot']} Please search again and retry."
            )
            return

        result  = results[idx]
        chat_id = query.message.chat_id

        # Notify user we're working on it
        status_msg = await query.message.reply_text(
            f"{SYM['lightning']} {stylish_text('Fetching & sending file…', 'bold')}\n"
            f"{SYM['dot']} {stylish_text('Please wait', 'italic')} — this may take a moment."
        )

        try:
            await send_file_to_chat(context, chat_id, result)
        except Exception as e:
            logger.error(f"send_file_to_chat error: {e}")
            await query.message.reply_text(
                f"{SYM['cross']} {stylish_text('Error sending file.', 'bold')}\n"
                f"{SYM['dot']} {str(e)[:300]}"
            )
        finally:
            # Clean up status message
            try:
                await status_msg.delete()
            except Exception:
                pass


# ─── Text Message Handler (auto-search) ───

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages as search queries"""
    if not update.message or not update.message.text:
        return
    
    text = update.message.text.strip()
    if text.startswith("/"):
        return
    
    user_id = update.effective_user.id
    state = USER_STATES.get(user_id, {})
    
    category = state.get("search_category", "all")
    
    # Clear awaiting state
    if "awaiting_search" in state:
        del state["awaiting_search"]
    
    await perform_search(update, context, text, category)


# ═══════════════════════════════════════════════════════════
# 🌐 WEB SERVER FOR RENDER
# ═══════════════════════════════════════════════════════════

async def health_handler(request):
    """Health check endpoint for Render"""
    total_sources = sum(len(cat["sources"]) for cat in DATABASES.values())
    return web.json_response({
        "status": "alive",
        "bot": "Ultimate Media Bot",
        "databases": total_sources,
        "categories": len(DATABASES),
        "timestamp": datetime.now().isoformat()
    })

async def webhook_handler(request):
    """Handle incoming webhook updates"""
    try:
        data = await request.json()
        update = Update.de_json(data, request.app["bot_app"].bot)
        await request.app["bot_app"].process_update(update)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    return web.Response(status=200)


# ═══════════════════════════════════════════════════════════
# 🚀 MAIN APPLICATION
# ═══════════════════════════════════════════════════════════

async def post_init(application):
    """Set bot commands after initialization"""
    commands = [
        BotCommand("start", "🏠 Start the bot"),
        BotCommand("search", "🔍 Universal search"),
        BotCommand("categories", "📁 Browse categories"),
        BotCommand("movie", "🎬 Search movies"),
        BotCommand("image", "🖼️ Search images"),
        BotCommand("anime", "🌸 Search anime"),
        BotCommand("music", "🎵 Search music"),
        BotCommand("book", "📚 Search books"),
        BotCommand("video", "📹 Search videos"),
        BotCommand("wallpaper", "🌄 Search wallpapers"),
        BotCommand("code", "💻 Search code repos"),
        BotCommand("dataset", "🤖 Search AI datasets"),
        BotCommand("three_d", "🧊 Search 3D models"),
        BotCommand("wiki", "📖 Search Wikipedia"),
        BotCommand("nasa", "🚀 Search NASA media"),
        BotCommand("random", "🎲 Random discovery"),
        BotCommand("databases", "📊 List all databases"),
        BotCommand("stats", "📈 Bot statistics"),
        BotCommand("help", "❓ Help & commands"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info("Bot commands set successfully!")


def main():
    """Main function to run the bot"""
    
    # Build application
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    
    # Register handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CommandHandler("categories", categories_command))
    app.add_handler(CommandHandler("databases", all_databases_command))
    app.add_handler(CommandHandler("movie", movie_command))
    app.add_handler(CommandHandler("image", image_command))
    app.add_handler(CommandHandler("anime", anime_command))
    app.add_handler(CommandHandler("music", music_command))
    app.add_handler(CommandHandler("book", book_command))
    app.add_handler(CommandHandler("video", video_command))
    app.add_handler(CommandHandler("wallpaper", wallpaper_command))
    app.add_handler(CommandHandler("code", code_command))
    app.add_handler(CommandHandler("dataset", dataset_command))
    app.add_handler(CommandHandler("three_d", three_d_command))
    app.add_handler(CommandHandler("wiki", wiki_command))
    app.add_handler(CommandHandler("nasa", nasa_command))
    app.add_handler(CommandHandler("random", random_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    if WEBHOOK_URL:
        # ─── WEBHOOK MODE (for Render) ───
        logger.info(f"Starting in WEBHOOK mode on port {PORT}")
        
        # Create aiohttp web app
        web_app = web.Application()
        web_app["bot_app"] = app
        
        web_app.router.add_get("/", health_handler)
        web_app.router.add_get("/health", health_handler)
        web_app.router.add_post(f"/webhook/{BOT_TOKEN}", webhook_handler)
        
        async def on_startup(web_application):
            await app.initialize()
            await app.bot.set_webhook(
                url=f"{WEBHOOK_URL}/webhook/{BOT_TOKEN}",
                allowed_updates=["message", "callback_query"]
            )
            await app.start()
            logger.info(f"Webhook set: {WEBHOOK_URL}/webhook/{BOT_TOKEN}")
        
        async def on_shutdown(web_application):
            await search_engine.close()
            await app.stop()
            await app.shutdown()
        
        web_app.on_startup.append(on_startup)
        web_app.on_shutdown.append(on_shutdown)
        
        web.run_app(web_app, host="0.0.0.0", port=PORT)
    
    else:
        # ─── POLLING MODE (for local testing) ───
        logger.info("Starting in POLLING mode")
        app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
    