import asyncio
import os
import logging
from concurrent.futures import ThreadPoolExecutor
from aiohttp import web

from highrise import BaseBot
from highrise.models import SessionMetadata, User, Position, AnchorPosition

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STREAM_PORT  = 5000
STREAM_MOUNT = "/stream"
SONG_DIR     = "/tmp/beatbot"

REPLIT_DOMAIN = os.getenv("REPLIT_DEV_DOMAIN", "")
CUSTOM_URL    = os.getenv("STREAM_URL", "")
if CUSTOM_URL:
    PUBLIC_URL = CUSTOM_URL
elif REPLIT_DOMAIN:
    PUBLIC_URL = f"https://{REPLIT_DOMAIN}{STREAM_MOUNT}"
else:
    PUBLIC_URL = f"http://localhost:{STREAM_PORT}{STREAM_MOUNT}"

os.makedirs(SONG_DIR, exist_ok=True)

_EXECUTOR = ThreadPoolExecutor(max_workers=2)

# ─────────────────────────────────────────────────────────────────
#  Emote lists
# ─────────────────────────────────────────────────────────────────

BOT_EMOTES = [
    "emote-float",
    "dance-floss",
    "emote-cozy",
    "emote-relax",
    "emote-ponder",
    "emote-smooch",
    "emote-laidback",
    "emote-posh",
]

USER_EMOTES = {
    "!smooch":      "emote-smooch",
    "!laidback":    "emote-laidback",
    "!ghostfloat":  "emote-float",
    "!cozynap":     "emote-cozy",
    "!posh":        "emote-posh",
    "!ponder":      "emote-ponder",
    "!floss":       "dance-floss",
    "!relax":       "emote-relax",
}


# ─────────────────────────────────────────────────────────────────
#  Download helper — pytubefix (sync, runs in thread)
# ─────────────────────────────────────────────────────────────────

def _download_sync(query: str, out_path: str) -> str | None:
    """Download audio from YouTube using pytubefix. Returns title or None."""
    try:
        from pytubefix import Search
        results = Search(query)
        if not results.videos:
            return None
        yt = results.videos[0]
        title = yt.title

        stream = (
            yt.streams.filter(only_audio=True, file_extension="mp4").first()
            or yt.streams.filter(only_audio=True).first()
        )
        if not stream:
            return None

        tmp = stream.download(output_path=SONG_DIR, filename="audio_tmp")
        return (title, tmp)
    except Exception as e:
        logger.error(f"pytubefix error: {e}")
        return None


async def download_song(query: str, out_path: str) -> str | None:
    """Async wrapper: download via pytubefix then convert to MP3."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(_EXECUTOR, _download_sync, query, out_path)
    if not result:
        return None
    title, tmp = result

    proc = await asyncio.create_subprocess_exec(
        "ffmpeg", "-i", tmp,
        "-vn", "-c:a", "libmp3lame", "-b:a", "128k",
        out_path, "-y",
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    await proc.wait()

    try:
        os.remove(tmp)
    except Exception:
        pass

    return title if proc.returncode == 0 else None


# ─────────────────────────────────────────────────────────────────
#  Streaming server
# ─────────────────────────────────────────────────────────────────

class StreamServer:
    def __init__(self):
        self.listeners: dict[int, asyncio.Queue] = {}
        self.ffmpeg_proc = None
        self.is_streaming = False

    async def start(self) -> None:
        app = web.Application()
        app.router.add_get(STREAM_MOUNT, self._handle_listener)
        app.router.add_get("/", self._handle_index)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", STREAM_PORT)
        await site.start()
        logger.info(f"Stream server started on port {STREAM_PORT}")

    async def _handle_index(self, request: web.Request) -> web.Response:
        return web.Response(
            text=(
                "<html><body style='background:#111;color:#eee;font-family:sans-serif'>"
                "<h2>🎧 BeatBot DJ Radio</h2>"
                f"<audio controls autoplay src='{STREAM_MOUNT}'></audio>"
                "</body></html>"
            ),
            content_type="text/html",
        )

    async def _handle_listener(self, request: web.Request) -> web.StreamResponse:
        response = web.StreamResponse(
            headers={
                "Content-Type": "audio/mpeg",
                "icy-name": "BeatBot DJ",
                "icy-br": "128",
                "icy-pub": "0",
                "Cache-Control": "no-cache, no-store",
                "Access-Control-Allow-Origin": "*",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )
        await response.prepare(request)

        for _ in range(10):
            await response.write(self._silence_frame())

        queue: asyncio.Queue = asyncio.Queue(maxsize=200)
        lid = id(response)
        self.listeners[lid] = queue
        logger.info(f"Listener connected (total: {len(self.listeners)})")

        try:
            while True:
                try:
                    chunk = await asyncio.wait_for(queue.get(), timeout=1)
                    if chunk is None:
                        break
                    await response.write(chunk)
                except asyncio.TimeoutError:
                    await response.write(self._silence_frame())
        except (ConnectionResetError, Exception):
            pass
        finally:
            self.listeners.pop(lid, None)
            logger.info(f"Listener disconnected (total: {len(self.listeners)})")
        return response

    @staticmethod
    def _silence_frame() -> bytes:
        return bytes([
            0xFF, 0xFB, 0x90, 0x00,
            *([0x00] * 124),
        ])

    async def broadcast(self, chunk: bytes) -> None:
        slow = []
        for lid, q in list(self.listeners.items()):
            try:
                q.put_nowait(chunk)
            except asyncio.QueueFull:
                slow.append(lid)
        for lid in slow:
            self.listeners.pop(lid, None)

    async def stream_file(self, filepath: str) -> None:
        if self.ffmpeg_proc and self.ffmpeg_proc.returncode is None:
            self.ffmpeg_proc.terminate()
            try:
                await asyncio.wait_for(self.ffmpeg_proc.wait(), timeout=5)
            except asyncio.TimeoutError:
                self.ffmpeg_proc.kill()

        self.is_streaming = True
        self.ffmpeg_proc = await asyncio.create_subprocess_exec(
            "ffmpeg", "-re",
            "-i", filepath,
            "-vn", "-c:a", "libmp3lame", "-b:a", "128k",
            "-f", "mp3", "pipe:1",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )

        try:
            while True:
                chunk = await self.ffmpeg_proc.stdout.read(8192)
                if not chunk:
                    break
                await self.broadcast(chunk)
        finally:
            self.is_streaming = False

    def stop(self) -> None:
        self.is_streaming = False
        if self.ffmpeg_proc and self.ffmpeg_proc.returncode is None:
            self.ffmpeg_proc.terminate()


# ─────────────────────────────────────────────────────────────────
#  Highrise Bot
# ─────────────────────────────────────────────────────────────────

class BeatBotDJ(BaseBot):
    def __init__(self):
        super().__init__()
        self.server       = StreamServer()
        self.music_queue  = []
        self.now_playing  = None
        self.is_busy      = False
        self.skip_votes   = set()
        self.emote_task   = None
        self.emote_index  = 0

    # ── Lifecycle ────────────────────────────────────────────────

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        logger.info("BeatBot DJ starting...")
        await self.server.start()
        await asyncio.sleep(1)
        logger.info(f"Public stream URL: {PUBLIC_URL}")
        await self.highrise.chat(
            "🎧 BeatBot DJ Online! RAM BOT 🎶\n"
            "!play [song] — Request karo\n"
            "!np !queue !skip !stop !help"
        )

    # ── User Join ────────────────────────────────────────────────

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        for emote_id in ("dance-floss", "emote-float", "idle_dancing"):
            try:
                await self.highrise.send_emote(emote_id)
                break
            except Exception:
                continue
        await self.highrise.chat(
            f"WELCOME TO THE ROOM ENJOY MUSIC RAM BOT 🎶🎵\n"
            f"👋 {user.username} aa gaye!\n"
            "!play [song] likh ke request karo 🎧"
        )

    # ── Chat ─────────────────────────────────────────────────────

    async def on_chat(self, user: User, message: str) -> None:
        msg = message.strip()
        low = msg.lower()

        if low.startswith("!play ") or low.startswith("!request "):
            song = msg[6:].strip() if low.startswith("!play ") else msg[9:].strip()
            if song:
                await self.cmd_play(user, song)
            else:
                await self.highrise.chat("❌ Song naam likho. Example: !play Tum Hi Ho")

        elif low in ("!queue", "!q"):
            await self.cmd_queue()
        elif low in ("!np", "!nowplaying"):
            await self.cmd_nowplaying()
        elif low == "!skip":
            await self.cmd_skip(user)
        elif low == "!stop":
            await self.cmd_stop()
        elif low == "!radio":
            await self.highrise.chat(f"📻 Radio URL:\n{PUBLIC_URL}")
        elif low == "!help":
            await self.cmd_help()
        elif low in USER_EMOTES:
            await self.cmd_user_emote(user, USER_EMOTES[low])

    # ── Commands ─────────────────────────────────────────────────

    async def cmd_play(self, user: User, song: str) -> None:
        self.music_queue.append({"song": song, "requested_by": user.username})
        if self.is_busy:
            await self.highrise.chat(
                f"✅ Queue #{len(self.music_queue)}: {song}\n"
                f"👤 {user.username}"
            )
        else:
            await self.highrise.chat(f"🔍 Searching: {song}...")
            asyncio.ensure_future(self.play_next())

    async def cmd_queue(self) -> None:
        if not self.now_playing and not self.music_queue:
            await self.highrise.chat("📭 Queue khali! !play [song] likho")
            return
        lines = []
        if self.now_playing:
            lines.append(f"▶️ {self.now_playing.get('title', self.now_playing['song'])}")
            lines.append(f"   👤 {self.now_playing['requested_by']}")
        for i, e in enumerate(self.music_queue[:5], 1):
            lines.append(f"{i}. {e['song']} — {e['requested_by']}")
        if len(self.music_queue) > 5:
            lines.append(f"...+{len(self.music_queue) - 5} more")
        await self.highrise.chat("\n".join(lines))

    async def cmd_nowplaying(self) -> None:
        if self.now_playing:
            title = self.now_playing.get("title", self.now_playing["song"])
            await self.highrise.chat(
                f"🎵 Now Playing:\n🎶 {title}\n"
                f"👤 {self.now_playing['requested_by']}"
            )
        else:
            await self.highrise.chat("⏸️ Koi song nahi chal raha! !play likho")

    async def cmd_skip(self, user: User) -> None:
        if not self.now_playing:
            await self.highrise.chat("⏸️ Koi song nahi chal raha!")
            return
        self.skip_votes.add(user.username)
        if len(self.skip_votes) >= 2:
            await self.highrise.chat("⏭️ Skip! Agla song...")
            self.server.stop()
            asyncio.ensure_future(self.play_next())
        else:
            await self.highrise.chat(
                f"🗳️ {user.username} ne skip vote diya ({len(self.skip_votes)}/2)"
            )

    async def cmd_stop(self) -> None:
        self.music_queue.clear()
        self.server.stop()
        self.now_playing = None
        self.is_busy = False
        if self.emote_task and not self.emote_task.done():
            self.emote_task.cancel()
        await self.highrise.chat("⏹️ Music band kar diya. Queue clear!")

    async def cmd_help(self) -> None:
        await self.highrise.chat(
            "🎧 RAM BOT Commands:\n"
            "!play [song] — Song request\n"
            "!np — Kya chal raha hai\n"
            "!queue — Queue dekho\n"
            "!skip — Skip vote (2 chahiye)\n"
            "!stop — Band karo\n"
            "!radio — Stream URL\n"
            "Emotes: !smooch !laidback !ghostfloat\n"
            "!cozynap !posh !ponder !floss !relax"
        )

    async def cmd_user_emote(self, user: User, emote_id: str) -> None:
        try:
            await self.highrise.send_emote(emote_id, user.id)
        except Exception:
            try:
                await self.highrise.send_emote(emote_id)
            except Exception:
                pass

    # ── Queue Engine ─────────────────────────────────────────────

    async def play_next(self) -> None:
        if not self.music_queue:
            self.now_playing = None
            self.is_busy = False
            if self.emote_task and not self.emote_task.done():
                self.emote_task.cancel()
            await self.highrise.chat("📭 Queue khatam! !play [song] se request karo 🎵")
            return

        entry = self.music_queue.pop(0)
        self.now_playing = entry
        self.skip_votes.clear()
        asyncio.ensure_future(self.download_and_stream(entry))

    async def download_and_stream(self, entry: dict) -> None:
        song      = entry["song"]
        requester = entry["requested_by"]
        out_path  = os.path.join(SONG_DIR, "now.mp3")

        try:
            self.is_busy = True

            if os.path.exists(out_path):
                os.remove(out_path)

            logger.info(f"Downloading: {song}")
            title = await download_song(song, out_path)

            if not title or not os.path.exists(out_path):
                logger.error(f"Download failed for: {song}")
                await self.highrise.chat(
                    f"❌ '{song}' nahi mila. Agla try karunga..."
                )
                self.is_busy = False
                await self.play_next()
                return

            self.now_playing["title"] = title
            logger.info(f"Downloaded: {title}")

            await self.highrise.chat(
                f"🎵 Now Playing:\n"
                f"🎶 {title}\n"
                f"👤 Requested by: {requester}"
            )

            if self.emote_task is None or self.emote_task.done():
                self.emote_task = asyncio.ensure_future(self.bot_emote_loop())

            await self.server.stream_file(out_path)

            if self.is_busy:
                await self.play_next()

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Stream error: {e}")
            await self.highrise.chat(f"❌ Error hua. Agla song try karunga...")
            self.is_busy = False
            await asyncio.sleep(2)
            await self.play_next()

    # ── Bot Emote Loop (10 sec) ───────────────────────────────────

    async def bot_emote_loop(self) -> None:
        try:
            while self.is_busy:
                emote_id = BOT_EMOTES[self.emote_index % len(BOT_EMOTES)]
                try:
                    await self.highrise.send_emote(emote_id)
                except Exception:
                    pass
                self.emote_index += 1
                await asyncio.sleep(10)
        except asyncio.CancelledError:
            pass
