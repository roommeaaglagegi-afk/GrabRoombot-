import random
import asyncio
from highrise import *
from highrise import BaseBot, Item, Position
from highrise.models import SessionMetadata

moderators = ["SUNLIGHT._.1", "", "Sigma_boy__"]

casa = ["I Marry You 💍","Of course I do 💍❤️","I don't want to 💍💔","Of course I don't 💍💔","I Love You Of course I marry you 💍"]

curativo = ["🔴You Used the Bandage Your Life Is at: 100%🔴","🔴You Used the Bandage Your Life is at: 50%🔴","🔴You Used the Bandage Your Life is at: 60%🔴","🔴You Used Your Life Bandage is at: 75% Your Life is at: 90%🔴","🔴You Used the Bandage It is at: 91%🔴"]

bomba = ["💣🧟‍♂️ You Threw a Bomb on 1x Boss Zombie 🧟‍♀️💣","💣🧟 You Threw a Bomb on 3x Boss Zombie 🧟💣","💣🧟‍♂️ You Threw a Bomb on 2x Boss Zombie 💣🧟‍♀️","💣 🧟‍♂️ You Threw a Bomb on 7x Boss Zombie 💣🧟‍♂️","💣🧟 You Threw a Bomb on 4x Boss Zombie 🧟💣"]

facada = ["🧟🔪 You Stabbed 1x Zombie 🔪🧟","🧟🔪 You Stabbed 6x Zombie 🔪🧟","🧟🔪 You Stabbed 7x Zombie 🔪🧟","🧟‍♂️🔪🧟‍♂️ You Stabbed 8x Zombie 🔪🧟‍♂️","🧟 🔪 You Stabbed 10x Zombie 🔪🧟","🧟🔪 You Stabbed 9x Zombie 🔪🧟","🧟‍♀️🔪🧟‍♂️ You Stabbed 3x Zombie 🧟‍♂️🔪🧟‍♀️"]

atirar = ["🧟You Shot 5x Zombie🧟","🧟You Shot 1x Zombie🧟","🧟You Shot 8x Zombie🧟","🧟You Shot 3x Zombie🧟","🧟‍♂️You Shot 5x Zombie🧟‍♂️ ","🧟‍♀️You Shot 10x Zombie🧟‍♀️","🧟🧟‍♀️You Shot 9x Zombie 🧟🧟‍♀️"]

play = ["🔴Your Life is at 50% use : /bandage","🔴Your Life is at 20% use : /bandage","🔴Your Life is at 40% use : /bandage","🧟The Zombies Are Coming Use : /stab or /shoot","🧟🧟‍♂️ There Are Many Zombies 🧟‍♀️🧟 🛡 Use: /shield 🛡","🧟The Zombie Boss Is Coming Use: /bomb","🧟The Zombies Are Coming Use : /stab or /shoot","🧟🧟‍♂️ There are Lots of Zombies 🧟‍♀️🧟 🛡 Use: /shield 🛡","🔴Your Life is at 60% use: /bandage","🔴Your Life is at 10% use: /bandage","🧟The Zombies Are Coming Use : /stab or /shoot","🧟The Zombies They're Coming Use : /stab or /shoot"]

pescar = ["🥈YOU WON THE MEDAL: SILVER FISHERMAN🥈","🥉YOU WON THE MEDAL: BRONZE FISHERMAN🥉","🥉YOU WON THE MEDAL: BRONZE FISHERMAN🥉","🥉YOU WON THE MEDAL: BRONZE FISHERMAN🥉","🟡Event: /carp 🟡","⚫️You Fished 3x Night Moon⚫️(+150 POINTS)","⚫️You Fished 2x Night Moon⚫️(+100 POINTS)","⚫️You Fished 1x Night Moon⚫️(+50 POINTS)","🟡You Fished 1x Golden Shrimp 🟡 (MULTIPLE POINT)","🟡You Fished 1x Golden Flounder🟡 (MULTIPLE POINT)","🪼🌈You Fished 1x Octopus Rainbow🪼🌈 (EXTRA POINTS)","🐢You Caught 3x Turtle 🐢 (LOSS OF POINTS)","🦑You Caught 1x Giant Squid 🦑 (LEGENDARY)","🦀You Caught 6x Crab 🦀 (COMMON)","🦀You Caught 2x Crab 🦀 (COMMON)","🦀You Caught 8x Crab 🦀 (COMMON)","🪼You Caught 1x Sea Octopus🪼(EPIC)","🦈You Caught 2x Shark🦈 (EPIC)","🦈You Fished 5x Sharks🦈 (EPIC)","🐠You Fished 1x Sea Tuna🐠 (LEGENDARY)","🐠You Caught 3x Clown Fish🐠 (LEGENDARIOUS)","🐠You Caught 1x Clown Fish🐠 (LEGENDARIOUS)","🐟You Caught 1x Salmon🐟 (RARE)","🧜🏼‍♀️You Caught 5x Mermaid🧜🏼‍♀️(EPIC)","🐋You Caught 11x Sea Whale🐋(COMMON)","🐋🌈You Caught 1x Rainbow Whale🌈🐋 (EXTRA POINTS)","🥈YOU WON THE MEDAL: SILVER FISHERMAN🥈","🥇YOU WON THE MEDAL: GOLD FISHERMAN🥇","🏅YOU WON THE MEDAL: STAR FISHERMAN🏅","💎Event: /shrimp 💎"]

# Bot auto-loop emotes — confirmed 100% working, cycles every 8 seconds
LOOP_EMOTES = [
    "idle-floating",
    "sit-open",
    "idle-loop-sitfloor",
    "sit-relaxed",
    "idle-guitar",
    "sit-idle-sleep",
    "emote-looping",
    "emote-float",
    "dance-tiktok9",
    "dance-kawai",
    "idle-dance-casual",
    "idle-dance-tiktok4",
    "emote-stargazer",
    "emote-maniac",
    "emote-fashionista",
    "emote-hyped",
    "emote-punkguitar",
    "idle-nervous",
    "emote-howl",
    "emote-gravity",
    "emote-coolguy",
    "emote-frog",
    "emote-confused",
    "emote-heartshape",
    "dance-tiktok8",
    "dance-floss",
]

# Emote number map — user can type 1, 2, 3... to use an emote
EMOTE_NUMBERS = {
    # Reactions / Expressions (1-20)
    "1":  "emote-ghostfloat",
    "2":  "emote-laughing",
    "3":  "emote-hello",
    "4":  "emote-bow",
    "5":  "emote-shy",
    "6":  "emote-shy2",
    "7":  "emote-pose1",
    "8":  "emoji-thumbsup",
    "9":  "emote-celebrate",
    "10": "emote-confused",
    "11": "emote-exasperatedb",
    "12": "emote-hearteyes",
    "13": "emote-embarrassed",
    "14": "emote-frustrated",
    "15": "emote-shocked",
    "16": "emoji-angry",
    "17": "emoji-gagging",
    "18": "emoji-celebrate",
    "19": "emote-tired",
    "20": "emote-oops",
    # Poses / Fashion (21-40)
    "21": "emote-fashionista",
    "22": "emote-model",
    "23": "emote-pose7",
    "24": "emote-pose5",
    "25": "emote-pose4",
    "26": "emote-pose3",
    "27": "emote-pose10",
    "28": "emote-pose9",
    "29": "emote-pose6",
    "30": "emote-cutey",
    "31": "emote-flirt",
    "32": "emote-curtsy",
    "33": "emote-salute",
    "34": "emote-cutesalute",
    "35": "emote-pose13",
    "36": "emote-dramatic",
    "37": "emote-coolguy",
    "38": "emote-puppet",
    "39": "emote-heartshape",
    "40": "emote-opera",
    # Fun / Action (41-60)
    "41": "emote-kissing-bound",
    "42": "emote-kissing-passionate",
    "43": "emote-hug",
    "44": "emote-slap",
    "45": "emote-gift",
    "46": "emote-snowball",
    "47": "emote-snowangel",
    "48": "emote-trampoline",
    "49": "emote-swordfight",
    "50": "emote-energyball",
    "51": "emote-boxer",
    "52": "emote-charging",
    "53": "emote-timejump",
    "54": "emote-teleporting",
    "55": "emote-launch",
    "56": "emote-telekinesis",
    "57": "emote-gravity",
    "58": "emote-fireworks",
    "59": "emote-juggling",
    "60": "emote-thief",
    # Chill / Vibes (61-75)
    "61": "sit-open",
    "62": "sit-relaxed",
    "63": "sit-idle-sleep",
    "64": "emote-float",
    "65": "emote-looping",
    "66": "idle-floating",
    "67": "emote-stargazer",
    "68": "emote-howl",
    "69": "emote-frog",
    "70": "emote-astronaut",
    "71": "emote-zombierun",
    "72": "emote-maniac",
    "73": "emote-hyped",
    "74": "emote-headblowup",
    "75": "emote-creepycute",
    # Trending / New (76-90)
    "76": "emote-wavey",
    "77": "emote-surf",
    "78": "emote-handwalk",
    "79": "emote-cartwheel",
    "80": "emote-iceskating",
    "81": "emote-snake",
    "82": "emote-fading",
    "83": "emote-celebrationstep",
    "84": "emote-greedy",
    "85": "emote-punkguitar",
    "86": "idle-guitar",
    "87": "dance-pennywise",
    "88": "dance-shoppingcart",
    "89": "emote-sheephop",
    "90": "dance-kid",
    # Dances (101-130)
    "101": "dance-tiktok9",
    "102": "dance-tiktok11",
    "103": "dance-tiktok1",
    "104": "dance-tiktok2",
    "105": "dance-tiktok3",
    "106": "dance-tiktok5",
    "107": "dance-tiktok6",
    "108": "dance-tiktok7",
    "109": "dance-tiktok8",
    "110": "dance-tiktok12",
    "111": "dance-tiktok15",
    "112": "dance-tiktok16",
    "113": "dance-kawai",
    "114": "dance-touch",
    "115": "dance-employee",
    "116": "dance-russian",
    "117": "dance-macarena",
    "118": "dance-blackpink",
    "119": "dance-hiphop",
    "120": "dance-creepypuppet",
    "121": "dance-anime",
    "122": "dance-anime3",
    "123": "dance-wrong",
    "124": "dance-weird",
    "125": "dance-icecream",
    "126": "dance-tiktok8",
    "127": "dance-tiktok2",
    "128": "dance-pinguin",
    "129": "dance-jinglebell",
    "130": "emote-sleigh",
    # Idles (131-143)
    "131": "idle-loop-sitfloor",
    "132": "idle-floating",
    "133": "idle-nervous",
    "134": "idle-wild",
    "135": "idle-fighter",
    "136": "idle-guitar",
    "137": "idle_singing",
    "138": "idle-toilet",
    "139": "idle-dance-tiktok4",
    "140": "idle-dance-casual",
    "141": "idle-enthusiastic",
    "142": "idle-cold",
    "143": "idle-wild",
}

# All emote name → emote ID (user types the name in chat to use)
EMOTE_MAP = {
    # Reactions / Expressions
    "ghostfloat":      "emote-ghostfloat",
    "laugh":           "emote-laughing",
    "laughing":        "emote-laughing",
    "wave":            "emote-hello",
    "hello":           "emote-hello",
    "bow":             "emote-bow",
    "shy":             "emote-shy",
    "bashful":         "emote-shy2",
    "wink":            "emote-pose1",
    "thumbsup":        "emoji-thumbsup",
    "celebrate":       "emote-celebrate",
    "party":           "emote-celebrate",
    "confused":        "emote-confused",
    "ponder":          "emote-confused",
    "facepalm":        "emote-exasperatedb",
    "hearteyes":       "emote-hearteyes",
    "embarrassed":     "emote-embarrassed",
    "frustrated":      "emote-frustrated",
    "shocked":         "emote-shocked",
    "angry":           "emoji-angry",
    "gagging":         "emoji-gagging",
    "raise":           "emoji-celebrate",
    "tired":           "emote-tired",
    "oops":            "emote-oops",
    # Poses / Fashion
    "fashion":         "emote-fashionista",
    "model":           "emote-model",
    "beautiful":       "emote-pose7",
    "icon":            "emote-pose5",
    "posh":            "emote-pose5",
    "musclepose":      "emote-pose4",
    "fightme":         "emote-pose3",
    "arabesque":       "emote-pose10",
    "ditzy":           "emote-pose9",
    "surprise":        "emote-pose6",
    "flirtywave":      "emote-cutey",
    "cutey":           "emote-cutey",
    "flirt":           "emote-flirt",
    "curtsy":          "emote-curtsy",
    "salute":          "emote-salute",
    "attention":       "emote-salute",
    "cutesalute":      "emote-cutesalute",
    "winkpose":        "emote-pose13",
    "dramatic":        "emote-dramatic",
    "coolguy":         "emote-coolguy",
    "puppet":          "emote-puppet",
    "hearteyes2":      "emote-heartshape",
    "opera":           "emote-opera",
    # Fun / Action
    "smooch":          "emote-kissing-bound",
    "smooch2":         "emote-kissing-passionate",
    "kiss":            "emote-kissing-bound",
    "hug":             "emote-hug",
    "slap":            "emote-slap",
    "foryou":          "emote-gift",
    "gift":            "emote-gift",
    "snowball":        "emote-snowball",
    "snowangel":       "emote-snowangel",
    "trampoline":      "emote-trampoline",
    "swordfight":      "emote-swordfight",
    "fight":           "emote-swordfight",
    "energyball":      "emote-energyball",
    "boxer":           "emote-boxer",
    "charging":        "emote-charging",
    "timejump":        "emote-timejump",
    "time":            "emote-timejump",
    "teleport":        "emote-teleporting",
    "launch":          "emote-launch",
    "telekinesis":     "emote-telekinesis",
    "zerogravity":     "emote-gravity",
    "gravity":         "emote-gravity",
    "fireworks":       "emote-fireworks",
    "juggling":        "emote-juggling",
    "thief":           "emote-thief",
    # Chill / Vibes
    "laidback":        "sit-open",
    "relaxing":        "sit-relaxed",
    "relaxed":         "sit-relaxed",
    "repose":          "sit-relaxed",
    "cozynap":         "sit-idle-sleep",
    "nap":             "sit-idle-sleep",
    "float":           "emote-float",
    "fairy":           "emote-looping",
    "fairytwirl":      "emote-looping",
    "floating":        "idle-floating",
    "fairyfloat":      "idle-floating",
    "ghost":           "idle-floating",
    "stargaze":        "emote-stargazer",
    "star":            "emote-stargazer",
    "stargazer":       "emote-stargazer",
    "howl":            "emote-howl",
    "frog":            "emote-frog",
    "astronaut":       "emote-astronaut",
    "zombie":          "emote-zombierun",
    "maniac":          "emote-maniac",
    "hyped":           "emote-hyped",
    "revelations":     "emote-headblowup",
    "watchyourback":   "emote-creepycute",
    "watch":           "emote-creepycute",
    # Trending / New
    "wavey":           "emote-wavey",
    "surf":            "emote-surf",
    "handwalk":        "emote-handwalk",
    "cartwheel":       "emote-cartwheel",
    "iceskating":      "emote-iceskating",
    "skating":         "emote-iceskating",
    "worm":            "emote-snake",
    "snake":           "emote-snake",
    "fading":          "emote-fading",
    "celebration":     "emote-celebrationstep",
    "greedy":          "emote-greedy",
    "punk":            "emote-punkguitar",
    "airguitar":       "idle-guitar",
    "pennywise":       "dance-pennywise",
    "shopping":        "dance-shoppingcart",
    "shop":            "dance-shoppingcart",
    "sheephop":        "emote-sheephop",
    "kid":             "dance-kid",
    # Dances
    "dance":           "dance-tiktok9",
    "tiktok":          "dance-tiktok11",
    "tiktok1":         "dance-tiktok1",
    "tiktok2":         "dance-tiktok2",
    "tiktok3":         "dance-tiktok3",
    "tiktok5":         "dance-tiktok5",
    "tiktok6":         "dance-tiktok6",
    "tiktok7":         "dance-tiktok7",
    "tiktok8":         "dance-tiktok8",
    "tiktok9":         "dance-tiktok9",
    "tiktok10":        "dance-tiktok10",
    "tiktok11":        "dance-tiktok11",
    "tiktok12":        "dance-tiktok12",
    "tiktok15":        "dance-tiktok15",
    "tiktok16":        "dance-tiktok16",
    "savage":          "dance-tiktok8",
    "dontstartnow":    "dance-tiktok2",
    "kawaii":          "dance-kawai",
    "touch":           "dance-touch",
    "pushit":          "dance-employee",
    "russian":         "dance-russian",
    "macarena":        "dance-macarena",
    "blackpink":       "dance-blackpink",
    "hiphop":          "dance-hiphop",
    "creepypuppet":    "dance-creepypuppet",
    "creepy":          "dance-creepypuppet",
    "saunter":         "dance-anime",
    "anime":           "dance-anime",
    "animedance":      "dance-anime3",
    "uwu":             "dance-wrong",
    "wrong":           "dance-wrong",
    "weird":           "dance-weird",
    "icecream":        "dance-icecream",
    "penguin":         "dance-pinguin",
    "pinguin":         "dance-pinguin",
    "jingle":          "dance-jinglebell",
    "sleigh":          "emote-sleigh",
    # Idles
    "sit":             "idle-loop-sitfloor",
    "nervous":         "idle-nervous",
    "bitnervous":      "idle-nervous",
    "wild":            "idle-wild",
    "scritchy":        "idle-wild",
    "scratch":         "idle-wild",
    "fighter":         "idle-fighter",
    "guitar":          "idle-guitar",
    "singing":         "idle_singing",
    "sing":            "idle_singing",
    "gottago":         "idle-toilet",
    "sayso":           "idle-dance-tiktok4",
    "tik4":            "idle-dance-tiktok4",
    "casual":          "idle-dance-casual",
    "enthused":        "idle-enthusiastic",
    "cold":            "idle-cold",
}

# Emote-all map (moderator only)
EMOTE_ALL_MAP = {
    "Fashion All":      "emote-fashionista",
    "Wrong All":        "dance-wrong",
    "Cutey All":        "emote-cutey",
    "Superpose All":    "emote-superpose",
    "Punk All":         "emote-punkguitar",
    "Tiktok2 All":      "dance-tiktok2",
    "Dontstartnow All": "dance-tiktok2",
    "Tiktok8 All":      "dance-tiktok8",
    "Savage All":       "dance-tiktok8",
    "Tiktok9 All":      "dance-tiktok9",
    "Viral All":        "dance-tiktok9",
    "Viralgroove All":  "dance-tiktok9",
    "Tiktok10 All":     "dance-tiktok10",
    "Gagging All":      "emoji-gagging",
    "Blackpink All":    "dance-blackpink",
    "Creepy All":       "dance-creepypuppet",
    "Revelations All":  "emote-headblowup",
    "Bashful All":      "emote-shy2",
    "Arabesque All":    "emote-pose10",
    "Party All":        "emote-celebrate",
    "Pose3 All":        "emote-pose3",
    "Pose7 All":        "emote-pose7",
    "Pose5 All":        "emote-pose5",
    "Pose1 All":        "emote-pose1",
    "Pose8 All":        "emote-pose8",
    "Pose9 All":        "emote-pose9",
    "Enthused All":     "idle-enthusiastic",
    "Sing All":         "idle_singing",
    "Singing All":      "idle_singing",
    "Teleport All":     "emote-teleporting",
    "Telekinesis All":  "emote-telekinesis",
    "Casual All":       "idle-dance-casual",
    "Icecream All":     "dance-icecream",
    "Watch All":        "emote-creepycute",
    "Zombie All":       "emote-zombierun",
    "Celebrate All":    "emoji-celebrate",
    "Kiss All":         "emote-kiss",
    "Bow All":          "emote-bow",
    "Snowangel All":    "emote-snowangel",
    "Confused All":     "emote-confused",
    "Charging All":     "emote-charging",
    "Wei All":          "dance-weird",
    "Weird All":        "dance-weird",
    "Cursing All":      "emoji-cursing",
    "Greedy All":       "emote-greedy",
    "Russian All":      "dance-russian",
    "Shop All":         "dance-shoppingcart",
    "Shopping All":     "dance-shoppingcart",
    "Model All":        "emote-model",
    "Ren All":          "dance-macarena",
    "Macarena All":     "dance-macarena",
    "Snake All":        "emote-snake",
    "Uwu All":          "idle-uwu",
    "Skating All":      "emote-iceskating",
    "Ice All":          "emote-iceskating",
    "Time All":         "emote-timejump",
    "Gottago All":      "idle-toilet",
    "Scritchy All":     "idle-wild",
    "Bitnervous All":   "idle-nervous",
    "Nervous All":      "idle-nervous",
    "Jingle All":       "dance-jinglebell",
    "Curtsy All":       "emote-curtsy",
    "Hot All":          "emote-hot",
    "Hyped All":        "emote-hyped",
    "Sleigh All":       "emote-sleigh",
    "Surprise All":     "emote-pose6",
    "Repose All":       "sit-relaxed",
    "Kawaii All":       "dance-kawai",
    "Touch All":        "dance-touch",
    "Gift All":         "emote-gift",
    "Pushit All":       "dance-employee",
    "Salute All":       "emote-cutesalute",
    "Attention All":    "emote-salute",
    "Tiktok All":       "dance-tiktok11",
    "Smooch All":       "emote-Smooch",
    "Launch All":       "emote-launch",
    "Fairyfloat All":   "idle-floating",
    "Fairytwirl All":   "emote-looping",
    "Airguitar All":    "idle-guitar",
    "Guitar All":       "idle-guitar",
    "Penguin All":      "dance-pinguin",
    "Pinguin All":      "dance-pinguin",
    "Astronaut All":    "emote-astronaut",
    "Anime All":        "dance-anime",
    "Saunter All":      "dance-anime",
    "Flirt All":        "emote-lust",
    "Flirtywave All":   "emote-lust",
    "Relaxed All":      "sit-relaxed",
    "Ghostfloat All":   "idle-floating",
    "Ghost All":        "idle-floating",
    "Posh All":         "emote-pose5",
    "Cozynap All":      "idle-loop-sitfloor",
    "Nap All":          "idle-loop-sitfloor",
    "Ponder All":       "emote-confused",
    "Laidback All":     "sit-relaxed",
}


def _s(msg, *variants):
    ml = msg.lower()
    return any(ml == v.lower() or ml.startswith(v.lower() + " ") for v in variants)


class Bot(BaseBot):

    def __init__(self):
        self._emote_index = 0

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        print("working")
        try:
            await self.highrise.walk_to(Position(18.5, 0.0, 12.5, "BackLeft"))
        except Exception as e:
            print(f"walk_to error: {e}")
        asyncio.ensure_future(self._emote_loop())

    async def _emote_loop(self):
        while True:
            try:
                emote = LOOP_EMOTES[self._emote_index % len(LOOP_EMOTES)]
                self._emote_index += 1
                await self.highrise.send_emote(emote)
            except Exception as e:
                print(f"loop emote '{emote}' error: {e}")
            await asyncio.sleep(8)

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        try:
            print(f"{user.username} joined the room")
            await self.highrise.chat(f"✨ WELCOME TO OUR GRAB ROOM! CHECK ALL GRABS & SPIN 🌻🥀 {user.username} 🌹 BEST OF LUCK!")
            await self.highrise.chat("Use: /help | Floors: f1 f2 f3 | Teleport: -t @user | Emotes: type name or number 1-98")
            await self.highrise.chat("Buying via PM: @Sigma_boy__ Thanks.")
            await self.highrise.send_emote("hcc-jetpack")
            await self.highrise.send_emote("hcc-jetpack", user.id)
        except Exception as e:
            print(f"on_user_join error: {e}")

    async def on_user_leave(self, user: User) -> None:
        try:
            print(f"{user.username} left the room")
        except Exception as e:
            print(f"on_user_leave error: {e}")

    async def on_chat(self, user: User, message: str) -> None:
        try:
            print(f"{user.username}: {message}")
            await self._handle_chat(user, message)
        except Exception as e:
            print(f"on_chat error [{user.username}]: {e}")

    async def _handle_chat(self, user: User, message: str):
        msg = message.strip()

        # ── HELP ──────────────────────────────────────────────────────────
        if _s(msg, "/help", "!help", "help", "Help"):
            await self.highrise.chat("COMMANDS: /emote list | /peoples | /fish | /play | /stab | /shoot | /bomb | /shield | /curative | /marry me?")
            await self.highrise.chat("FLOORS: f1 f2 f3 | TELEPORT: -t @user | SUMMON: /summon @user")
            await self.highrise.chat("MOD: !kick @user | !tipall [amt] | !tipme [amt] | !wallet | !fit 1-11 | [Emote] All")
            await self.highrise.chat("EMOTES: Type name (e.g. uwu, fashion, kawaii) OR number 1-98 | /emote list for full list")
            await self.highrise.send_emote("dance-floss")
            return

        # ── EMOTE LIST ─────────────────────────────────────────────────────
        if _s(msg, "-emotelist", "/emotelist", "!emotelist", "/emote list", "!emote list", "/emotes", "!emotes", "/lista", "!lista"):
            await self.highrise.send_whisper(user.id, "😄 REACTIONS (1-20): 1.ghostfloat 2.laugh 3.wave 4.bow 5.shy 6.bashful 7.wink 8.thumbsup 9.celebrate 10.confused 11.facepalm 12.hearteyes 13.embarrassed 14.frustrated 15.shocked 16.angry 17.gagging 18.raise 19.tired 20.oops")
            await self.highrise.send_whisper(user.id, "💃 POSES (21-40): 21.fashion 22.model 23.beautiful 24.icon 25.musclepose 26.fightme 27.arabesque 28.ditzy 29.surprise 30.flirtywave 31.flirt 32.curtsy 33.salute 34.cutesalute 35.winkpose 36.dramatic 37.coolguy 38.puppet 39.hearteyes2 40.opera")
            await self.highrise.send_whisper(user.id, "🎭 FUN/ACTION (41-60): 41.smooch 42.smooch2 43.hug 44.slap 45.foryou 46.snowball 47.snowangel 48.trampoline 49.swordfight 50.energyball 51.boxer 52.charging 53.timejump 54.teleport 55.launch 56.telekinesis 57.zerogravity 58.fireworks 59.juggling 60.thief")
            await self.highrise.send_whisper(user.id, "😴 CHILL (61-75): 61.laidback 62.relaxing 63.cozynap 64.float 65.fairy 66.ghostfloat 67.stargaze 68.howl 69.frog 70.astronaut 71.zombie 72.maniac 73.hyped 74.revelations 75.watchyourback")
            await self.highrise.send_whisper(user.id, "🔥 TRENDING (76-90): 76.wavey 77.surf 78.handwalk 79.cartwheel 80.iceskating 81.worm 82.fading 83.celebration 84.greedy 85.punk 86.airguitar 87.pennywise 88.shopping 89.sheephop 90.kid")
            await self.highrise.send_whisper(user.id, "🕺 DANCES (101-130): 101.dance 102.tiktok 103.tiktok1 104.tiktok2 105.tiktok3 106.tiktok5 107.tiktok6 108.tiktok7 109.tiktok8 110.tiktok12 111.tiktok15 112.tiktok16 113.kawaii 114.touch 115.pushit 116.russian 117.macarena 118.blackpink 119.hiphop 120.creepypuppet 121.saunter 122.animedance 123.uwu 124.weird 125.icecream 126.savage 127.dontstartnow 128.penguin 129.jingle 130.sleigh")
            await self.highrise.send_whisper(user.id, "🧘 IDLES (131-143): 131.sit 132.floating 133.nervous 134.wild 135.fighter 136.guitar 137.singing 138.gottago 139.sayso 140.casual 141.enthused 142.cold 143.scratch | Type name OR number to use!")
            await self.highrise.send_emote("dance-floss")
            return

        # ── EMOTE ALL LIST ─────────────────────────────────────────────────
        if _s(msg, "!emoteall"):
            await self.highrise.send_whisper(user.id, "EMOTE ALL: Fashion All | Wrong All | Cutey All | Superpose All | Punk All | Tiktok2 All | Tiktok8 All | Tiktok9 All | Tiktok10 All | Gagging All | Blackpink All | Creepy All | Revelations All | Bashful All | Arabesque All | Party All")
            await self.highrise.send_whisper(user.id, "Pose3 All | Pose7 All | Pose5 All | Pose1 All | Enthused All | Pose8 All | Sing All | Teleport All | Telekinesis All | Casual All | Icecream All | Watch All | Zombie All | Celebrate All | Kiss All | Bow All | Snowangel All | Confused All")
            await self.highrise.send_whisper(user.id, "Skating All | Time All | Gottago All | Scritchy All | Nervous All | Jingle All | Curtsy All | Hot All | Hyped All | Sleigh All | Surprise All | Repose All | Kawaii All | Touch All | Gift All | Pushit All | Tiktok All | Smooch All | Launch All | Relaxed All | Ponder All | Ghostfloat All | Posh All | Cozynap All")
            return

        # ── PEOPLES ───────────────────────────────────────────────────────
        if _s(msg, "/peoples", "!peoples"):
            room_users = (await self.highrise.get_room_users()).content
            await self.highrise.chat(f"There are {len(room_users)} people in the room 🏠")
            await self.highrise.send_emote("dance-floss")
            return

        # ── FLOOR NAVIGATION ──────────────────────────────────────────────
        if _s(msg, "f1", "/f1", "!f1", "-f1", "/floor1", "!floor1", "-floor1", "floor1", "floor 1", "!floor 1", "-1", "Floor1", "Floor 1"):
            await self.highrise.teleport(user.id, Position(20.0, 0.0, 8.0))
            return

        if _s(msg, "f2", "/f2", "!f2", "-f2", "/floor2", "!floor2", "-floor2", "floor2", "floor 2", "!floor 2", "-2", "Floor2", "Floor 2"):
            await self.highrise.teleport(user.id, Position(8.0, 10.0, 1.0))
            return

        if _s(msg, "f3", "/f3", "!f3", "-f3", "/floor3", "!floor3", "-floor3", "floor3", "floor 3", "!floor 3", "-3", "Floor3", "Floor 3"):
            await self.highrise.teleport(user.id, Position(20.0, 14.8, 4.0))
            return

        # ── TELEPORT TO USER: -t @user ─────────────────────────────────────
        if msg.lower().startswith("-t "):
            target = msg[3:].strip().lstrip("@")
            await self.teleport_to_user(user, target)
            return

        # ── TELEPORT (moderator legacy) ────────────────────────────────────
        if _s(msg, "/tele", "!tele", "/tp", "!tp") and user.username in moderators:
            await self.teleporter(msg)
            return

        # ── SUMMON ─────────────────────────────────────────────────────────
        if _s(msg, "/summon", "!summon", "/summom", "!summom", "Summon", "Summom"):
            if user.username in moderators:
                target = msg.split("@")[-1].strip() if "@" in msg else msg.split()[-1]
                await self.teleport_user_next_to(target, user)
            return

        # ── GAME COMMANDS ──────────────────────────────────────────────────
        if msg.lower() in ("/fish", "fish"):
            await self.highrise.send_whisper(user.id, "You Are Fishing 🎣...")
            await self.highrise.send_whisper(user.id, random.choice(pescar))
            return

        if msg.lower() in ("/bomb", "bomb"):
            await self.highrise.send_whisper(user.id, random.choice(bomba))
            return

        if msg.lower() in ("/stab", "stab"):
            await self.highrise.send_whisper(user.id, random.choice(facada))
            return

        if msg.lower() in ("/curative", "curative", "/bandage", "bandage"):
            await self.highrise.react("heart", user.id)
            await self.highrise.send_whisper(user.id, random.choice(curativo))
            return

        if msg.lower() in ("/play", "play"):
            await self.highrise.send_whisper(user.id, random.choice(play))
            return

        if msg.lower() in ("/shoot", "shoot"):
            await self.highrise.send_whisper(user.id, random.choice(atirar))
            return

        if msg.lower() == "/marry me?":
            await self.highrise.chat(random.choice(casa))
            return

        if _s(msg, "/carp", "carp"):
            await self.highrise.react("clap", user.id)
            await self.highrise.send_whisper(user.id, "🟡You Caught 1x Golden Carp🟡 YOU WON THE MEDAL: (MEGA FISHERMAN)")
            return

        if _s(msg, "/shrimp", "shrimp"):
            await self.highrise.react("clap", user.id)
            await self.highrise.send_whisper(user.id, "💎You Caught 1x Diamond Shrimp💎 YOU WON THE MEDAL: (DIAMANTE MASTER FISHERMAN)")
            return

        if _s(msg, "/shield", "shield"):
            await self.highrise.react("heart", user.id)
            await self.highrise.send_whisper(user.id, f"@{user.username} 🛡 You Used The Shield 🛡")
            return

        # ── WALLET (moderator) ─────────────────────────────────────────────
        if _s(msg, "!wallet", "Wallet", "wallet", "Carteira", "carteira") and user.username in moderators:
            wallet = (await self.highrise.get_wallet()).content
            await self.highrise.send_whisper(user.id, f"BALANCE: {wallet[0].amount} {wallet[0].type}")
            await self.highrise.send_emote("dance-tiktok14")
            return

        # ── TIP ALL (moderator) ────────────────────────────────────────────
        if msg.lower().startswith("!tipall ") and user.username in moderators:
            parts = msg.split()
            if len(parts) != 2:
                await self.highrise.chat("Usage: !tipall [amount]")
                return
            try:
                amount = int(parts[1])
            except ValueError:
                await self.highrise.chat("Invalid amount")
                return
            bars = {10000:"gold_bar_10k",5000:"gold_bar_5000",1000:"gold_bar_1k",500:"gold_bar_500",100:"gold_bar_100",50:"gold_bar_50",10:"gold_bar_10",5:"gold_bar_5",1:"gold_bar_1"}
            bot_wallet = await self.highrise.get_wallet()
            bot_amount = bot_wallet.content[0].amount
            room_users = (await self.highrise.get_room_users()).content
            if bot_amount < amount * len(room_users):
                await self.highrise.chat("Not enough funds to tip everyone")
                return
            for room_user, _ in room_users:
                rem = amount
                for bar_val in sorted(bars.keys(), reverse=True):
                    if rem >= bar_val:
                        cnt = rem // bar_val
                        rem %= bar_val
                        for _ in range(cnt):
                            try:
                                await self.highrise.tip_user(room_user.id, bars[bar_val])
                            except Exception as e:
                                print(f"tip error: {e}")
            return

        # ── TIP ME (moderator) ─────────────────────────────────────────────
        if msg.lower().startswith("!tipme ") and user.username in moderators:
            try:
                amount = int(msg.split()[1])
                bars = {10000:"gold_bar_10k",5000:"gold_bar_5000",1000:"gold_bar_1k",500:"gold_bar_500",100:"gold_bar_100",50:"gold_bar_50",10:"gold_bar_10",5:"gold_bar_5",1:"gold_bar_1"}
                bot_wallet = await self.highrise.get_wallet()
                if bot_wallet.content[0].amount < amount:
                    await self.highrise.chat("Not enough funds.")
                    return
                for bar_val in sorted(bars.keys(), reverse=True):
                    if amount >= bar_val:
                        cnt = amount // bar_val
                        amount %= bar_val
                        for _ in range(cnt):
                            try:
                                await self.highrise.tip_user(user.id, bars[bar_val])
                            except Exception as e:
                                print(f"tipme error: {e}")
            except (IndexError, ValueError):
                await self.highrise.chat("Usage: !tipme [amount]")
            return

        # ── KICK (moderator) ───────────────────────────────────────────────
        if _s(msg, "!kick"):
            if user.username not in moderators:
                await self.highrise.chat("You don't have permission for this command.")
                return
            parts = msg.split()
            if len(parts) != 2:
                await self.highrise.chat("Usage: !kick @username")
                return
            username = parts[1].lstrip("@")
            room_users = (await self.highrise.get_room_users()).content
            user_id = None
            for room_user, _ in room_users:
                if room_user.username.lower() == username.lower():
                    user_id = room_user.id
                    break
            if not user_id:
                await self.highrise.chat("User not found in room.")
                return
            try:
                await self.highrise.moderate_room(user_id, "kick")
                await self.highrise.chat(f"{username} has been kicked!")
            except Exception as e:
                await self.highrise.chat(f"Kick failed: {e}")
            return

        # ── FIT (moderator) ────────────────────────────────────────────────
        if msg.lower().startswith("!fit") and user.username in moderators:
            await self._handle_fit(user, msg)
            return

        # ── EMOTE ALL (moderator) ──────────────────────────────────────────
        emote_all_done = await self._handle_emote_all(user, msg)
        if emote_all_done:
            return

        # ── EMOJI REACTIONS ────────────────────────────────────────────────
        await self._handle_emoji(user, message)

        # ── EMOTE BY NUMBER ────────────────────────────────────────────────
        if msg.strip() in EMOTE_NUMBERS:
            emote_id = EMOTE_NUMBERS[msg.strip()]
            try:
                await self.highrise.send_emote(emote_id, user.id)
            except Exception as e:
                print(f"number emote error: {e}")
            return

        # ── EMOTE BY NAME ──────────────────────────────────────────────────
        await self._handle_emote(user, msg)

    async def _handle_emoji(self, user: User, message: str):
        emoji_map = [
            (["😡","🤬","😤","🤨","😒","🙄"], "emote-boxer"),
            (["🤔","🧐","🥸","🫤","😕"],       "emote-confused"),
            (["😗","😘","😙","💋","😚"],        "emote-kiss"),
            (["😊","🥰","😳","🤗"],             "idle-uwu"),
            (["🤢","🤮","🤧","🤒"],             "emoji-gagging"),
            (["😱","😬","😰","😫","😨"],        "idle-nervous"),
            (["🤯"],                             "emote-headblowup"),
            (["☺️","🫣","😍","🥺","🥹"],        "emote-shy2"),
            (["😏","🙃","🤤","😋","😈"],        "emote-lust"),
            (["🥵","🫠"],                        "emote-hot"),
        ]
        for emojis, emote_id in emoji_map:
            if any(message.startswith(e) for e in emojis):
                try:
                    await self.highrise.send_emote(emote_id, user.id)
                    if emote_id in ("emote-kiss", "idle-uwu"):
                        await self.highrise.send_emote("emote-blowkisses")
                except Exception as e:
                    print(f"emoji emote error: {e}")
                return

    async def _handle_emote(self, user: User, msg: str):
        ml = msg.lower().strip().lstrip("/").lstrip("!")
        if ml in EMOTE_MAP:
            try:
                await self.highrise.send_emote(EMOTE_MAP[ml], user.id)
            except Exception as e:
                print(f"emote '{ml}' error: {e}")
            return
        # Also check with prefix stripped already handled above, check raw
        raw = msg.lower().strip()
        for keyword, emote_id in EMOTE_MAP.items():
            if raw == keyword or raw == f"/{keyword}" or raw == f"!{keyword}":
                try:
                    await self.highrise.send_emote(emote_id, user.id)
                except Exception as e:
                    print(f"emote '{keyword}' error: {e}")
                return

    async def _handle_emote_all(self, user: User, msg: str) -> bool:
        if user.username not in moderators:
            return False
        for trigger, emote_id in EMOTE_ALL_MAP.items():
            if msg == trigger or msg.lower() == trigger.lower():
                try:
                    room_users = (await self.highrise.get_room_users()).content
                    for room_user, _ in room_users:
                        try:
                            await self.highrise.send_emote(emote_id, room_user.id)
                        except Exception:
                            pass
                except Exception as e:
                    print(f"emote all error: {e}")
                return True
        return False

    async def _handle_fit(self, user: User, msg: str):
        fits = {
            "!fit 1": ([
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=1),
                Item(type='clothing', amount=1, id='shirt-n_room32019jerseywhite', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='pants-n_room22019longcutoffsdenim', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='hair_back-n_malenew16', account_bound=False, active_palette=39),
                Item(type='clothing', amount=1, id='nose-n_03_b', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='hair_front-n_malenew16', account_bound=False, active_palette=1),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle22', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='face_hair-n_newbasicfacehairupper06', account_bound=False, active_palette=1),
                Item(type='clothing', amount=1, id='face_hair-n_newbasicfacehairlower16', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='sock-n_starteritems2020whitesocks', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='shoes-n_room12019sneakersblack', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='mouth-basic2018openfullround', account_bound=False, active_palette=1),
                Item(type='clothing', amount=1, id='eye-n_basic2018malediamondsleepy', account_bound=False, active_palette=7),
                Item(type='clothing', amount=1, id='eyebrow-n_basic2018newbrows14', account_bound=False, active_palette=-1),
            ], "👕 FIT[1] applied!"),
            "!fit 2": ([
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=23),
                Item(type='clothing', amount=1, id='shirt-n_room12019cropsweaterwhite', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='pants-n_room12019rippedpantsblue', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='hair_back-n_basic2018mediumcurlymarilyn', account_bound=False, active_palette=39),
                Item(type='clothing', amount=1, id='nose-n_01', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='hair_front-n_basic2018marilyncurls', account_bound=False, active_palette=39),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle22', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='blush-f_blush01', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='sock-n_starteritems2020whitesocks', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='shoes-n_room12019hightopsblack', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='mouth-n_basic2018toothyfullpeaked', account_bound=False, active_palette=24),
                Item(type='clothing', amount=1, id='eye-n_basic2018pinkshadow2', account_bound=False, active_palette=7),
                Item(type='clothing', amount=1, id='eyebrow-n_08', account_bound=False, active_palette=-1),
            ], "👕 FIT[2] applied!"),
            "!fit 3": ([
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=1),
                Item(type='clothing', amount=1, id='shirt-f_punklace', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='pants-n_room22019shortcutoffsdenim', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=4, id='nose-n_01', account_bound=False, active_palette=4),
                Item(type='clothing', amount=1, id='mouth-basic2018openfullpeaked', account_bound=False, active_palette=8),
                Item(type='clothing', amount=1, id='hair_front-n_basic2018straightbluntbangs', account_bound=False, active_palette=28),
                Item(type='clothing', amount=1, id='hair_back-n_basic2018straighthighpony', account_bound=False, active_palette=28),
                Item(type='clothing', amount=1, id='eyebrow-n_basic2018newbrows14', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='eye-n_basic2018dolleyes', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='shoes-n_starteritems2019flatsblack', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='necklace-n_room32019locknecklace', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='earrings-n_room12019goldhoops', account_bound=False, active_palette=-1),
            ], "👕 FIT[3] applied!"),
            "!fit 4": ([
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=3),
                Item(type='clothing', amount=1, id='shirt-n_room22019bratoppink', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='pants-n_room22019undiespink', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='hair_back-n_basic2020overshoulderwavy', account_bound=False, active_palette=77),
                Item(type='clothing', amount=1, id='nose-n_01_b', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='hair_front-n_basic2020overshoulderwavy', account_bound=False, active_palette=77),
                Item(type='clothing', amount=1, id='earrings-n_room12019goldhoops', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle22', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='glasses-n_room32019smallshades', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='shoes-n_registrationavatars2023gothgirlshoes', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='mouth-n_basic2018pillowfullpeaked', account_bound=False, active_palette=9),
                Item(type='clothing', amount=1, id='eye-n_basic2018falselashes', account_bound=False, active_palette=10),
                Item(type='clothing', amount=1, id='eyebrow-n_26', account_bound=False, active_palette=-1),
            ], "👕 FIT[4] applied!"),
            "!fit 5": ([
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=1),
                Item(type='clothing', amount=1, id='shirt-n_room12019cropsweaterblack', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='skirt-n_room12019pleatedskirtgrey', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=4, id='nose-n_basic2018newnose15', account_bound=False, active_palette=4),
                Item(type='clothing', amount=1, id='mouth-n_room22019sillymouth', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='hair_front-n_basic2020overshoulderwavy', account_bound=False, active_palette=1),
                Item(type='clothing', amount=1, id='hair_back-n_basic2020overshoulderwavy', account_bound=False, active_palette=1),
                Item(type='clothing', amount=1, id='eyebrow-n_basic2018newbrows16', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='eye-n_basic2018teardrop', account_bound=False, active_palette=7),
                Item(type='clothing', amount=1, id='shoes-n_registrationavatars2023gothgirlshoes', account_bound=False, active_palette=0),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle35', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle22', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle32', account_bound=False, active_palette=-1),
            ], "👕 FIT[5] applied!"),
            "!fit 6": ([
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=4),
                Item(type='clothing', amount=1, id='shirt-n_room32019longlineteesweatshirtgrey', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='pants-n_starteritems2019cuffedjeansblue', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=4, id='hair_back-n_malenew19', account_bound=False, active_palette=80),
                Item(type='clothing', amount=1, id='nose-n_basic2018newnose04', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=4, id='hair_front-n_malenew19', account_bound=False, active_palette=80),
                Item(type='clothing', amount=1, id='watch-n_room32019blackwatch', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle22', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='shoes-n_room12019sneakersblack', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='mouth-basic2018whistlemouth', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='eye-n_basic2018malealmondsquint', account_bound=False, active_palette=7),
                Item(type='clothing', amount=1, id='eyebrow-n_04', account_bound=False, active_palette=-1),
            ], "👕 FIT[6] applied!"),
            "!fit 7": ([
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=3),
                Item(type='clothing', amount=1, id='shirt-n_starteritems2019pulloverblack', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='pants-n_starteritems2019mensshortsblack', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=4, id='hair_back-n_malenew23', account_bound=False, active_palette=82),
                Item(type='clothing', amount=1, id='nose-n_01', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=4, id='hair_front-n_malenew23', account_bound=False, active_palette=82),
                Item(type='clothing', amount=1, id='watch-n_room32019blackwatch', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle22', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='shoes-n_room12019sneakersblack', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='mouth-vip_f_01', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='eye-n_basic2018malealmondsquint', account_bound=False, active_palette=7),
                Item(type='clothing', amount=1, id='eyebrow-n_26', account_bound=False, active_palette=-1),
            ], "👕 FIT[7] applied!"),
            "!fit 8": ([
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=23),
                Item(type='clothing', amount=1, id='shirt-n_registrationavatars2023arianadress', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='pants-n_room22019undiesblack', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=4, id='hair_back-n_basic2019poofbob', account_bound=False, active_palette=82),
                Item(type='clothing', amount=1, id='nose-n_01', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=4, id='hair_front-n_basic2018straightbangslowpart', account_bound=False, active_palette=82),
                Item(type='clothing', amount=1, id='earrings-n_room12019goldhoops', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle22', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='shoes-n_registrationavatars2023arianaboots', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='mouth-n_registrationavatars2023pinkmouth', account_bound=False, active_palette=3),
                Item(type='clothing', amount=1, id='eye-n_registrationavatars2023gymgirleyes', account_bound=False, active_palette=7),
                Item(type='clothing', amount=1, id='eyebrow-n_08', account_bound=False, active_palette=-1),
            ], "👕 FIT[8] applied!"),
            "!fit 9": ([
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=1),
                Item(type='clothing', amount=1, id='shirt-n_room12019sweaterwithbuttondowngrey', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='pants-n_room12019formalslackskhaki', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='hair_back-n_malenew16', account_bound=False, active_palette=1),
                Item(type='clothing', amount=1, id='nose-n_03_b', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='hair_front-n_malenew16', account_bound=False, active_palette=1),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle22', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='sock-n_starteritems2020whitesocks', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='shoes-n_room12019sneakersblack', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='mouth-basic2018openfullround', account_bound=False, active_palette=1),
                Item(type='clothing', amount=1, id='eye-n_basic2018malediamondsleepy', account_bound=False, active_palette=7),
                Item(type='clothing', amount=1, id='eyebrow-n_basic2018newbrows14', account_bound=False, active_palette=-1),
            ], "👕 FIT[9] applied!"),
            "!fit 10": ([
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=3),
                Item(type='clothing', amount=1, id='shirt-n_winxudcrwrdsone2024winxblueshirt', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='skirt-n_winxudcrwrdsone2024pinkskirtstrawberrys', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=4, id='hair_back-n_basic2018wavypulledback', account_bound=False, active_palette=1),
                Item(type='clothing', amount=1, id='nose-n_01', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=4, id='hair_front-n_basic2018sidebangspulledback', account_bound=False, active_palette=1),
                Item(type='clothing', amount=1, id='earrings-n_room12019goldhoops', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle22', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='shoes-n_room12019sneakerspink', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='mouth-n_registrationavatars2023pinkmouth', account_bound=False, active_palette=3),
                Item(type='clothing', amount=1, id='eye-n_basic2018liftedeyes', account_bound=False, active_palette=7),
                Item(type='clothing', amount=1, id='eyebrow-n_08', account_bound=False, active_palette=-1),
            ], "👕 FIT[10] applied!"),
            "!fit 11": ([
                Item(type='clothing', amount=1, id='body-flesh', account_bound=False, active_palette=6),
                Item(type='clothing', amount=1, id='shirt-n_registrationavatars2023gothguyhoodie', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='pants-n_starteritems2019cuffedjeansblack', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=4, id='hair_back-m_23', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='nose-n_01_b', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=4, id='hair_front-m_23', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='sock-n_starteritems2020blacksocks', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='freckle-n_basic2018freckle22', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='shoes-n_registrationavatars2023furrysneakers', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='mouth-vip_f_01', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='eye-n_basic2018malealmondsquint', account_bound=False, active_palette=7),
                Item(type='clothing', amount=1, id='eyebrow-n_26', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='bag-n_registrationavatars2023furrytail', account_bound=False, active_palette=-1),
                Item(type='clothing', amount=1, id='hat-n_registrationavatars2023wolfears', account_bound=False, active_palette=-1),
            ], "👕 FIT[11] applied!"),
        }

        key = msg.lower().strip()
        if key in fits:
            outfit_items, response = fits[key]
            try:
                await self.highrise.set_outfit(outfit=outfit_items)
                await self.highrise.chat(response)
            except Exception as e:
                print(f"set_outfit error: {e}")
                await self.highrise.chat(f"Fit change failed: {e}")
        else:
            await self.highrise.chat("Usage: !fit 1 to !fit 11")

    async def teleporter(self, message: str):
        try:
            parts = message.split()
            if len(parts) >= 2 and "@" in parts[1]:
                username = parts[1].lstrip("@")
                room_users = (await self.highrise.get_room_users()).content
                for room_user, pos in room_users:
                    if room_user.username.lower() == username.lower():
                        if isinstance(pos, Position):
                            await self.highrise.teleport(room_user.id, pos)
                        return
        except Exception as e:
            print(f"teleporter error: {e}")

    async def teleport_to_user(self, user: User, target_username: str):
        try:
            room_users = (await self.highrise.get_room_users()).content
            for room_user, pos in room_users:
                if room_user.username.lower() == target_username.lower():
                    if isinstance(pos, Position):
                        await self.highrise.teleport(user.id, Position(pos.x, pos.y, pos.z))
                        return
            await self.highrise.send_whisper(user.id, f"User @{target_username} not found in room.")
        except Exception as e:
            print(f"teleport_to_user error: {e}")

    async def teleport_user_next_to(self, target_username: str, requester: User):
        try:
            room_users = (await self.highrise.get_room_users()).content
            req_pos = None
            target_id = None
            for room_user, pos in room_users:
                if room_user.username.lower() == requester.username.lower():
                    req_pos = pos
                if room_user.username.lower() == target_username.lower():
                    target_id = room_user.id
            if target_id and req_pos and isinstance(req_pos, Position):
                await self.highrise.teleport(target_id, Position(req_pos.x, req_pos.y, req_pos.z))
        except Exception as e:
            print(f"teleport_user_next_to error: {e}")
