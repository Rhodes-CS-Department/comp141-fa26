"""
Word Monsters, animated version: the parts of the game that aren't about lists.

You don't need to open this file.  The game keeps the monsters in two lists,
monsters and distances, and calls the functions you write to change them.
This file does everything else: the drawing, the animation, and the rules.
"""

import math
import os
import random
import time
import traceback
import __main__

from IPython.display import display
from ipycanvas import MultiCanvas, hold_canvas

# What your notebook gets when it runs "from word_monsters import *".
__all__ = ["blast", "play"]

# ---------- Game settings ----------

FAR = 8                  # the farthest spot on the board
NEAREST_START = 4        # the closest a monster can start
WAVE_SIZE = 6            # how many monsters a game starts with
MAX_LETTERS = 38         # the most letters a starting wave can have in all
SPELL_USES = 1           # how many times each one-use spell works
POINTS_PER_DEFEAT = 10   # until spell_points is written
CHAIN_BONUS = 5          # points for each new word-chain link
ARRIVAL_EVERY = 4        # a new monster arrives every this many turns
NOVA_REACH = 2           # nova hits monsters this close or closer
SPECIALS = ["zap", "nova", "gust", "fire"]
BACKUP_NAMES = ["zombie", "ghost", "goblin", "mummy", "witch", "troll"]

WIDTH = 770
HEIGHT = 362
TOP = 28
FPS = 30
WAIT = True              # False skips the pauses between frames (for testing)
FUNCTIONS = None         # a dict of functions to use instead of the notebook's (for testing)

stats = {"frames": 0, "seconds": 0.0}
fx = random.Random()     # random numbers for effects only
HERE = os.path.dirname(os.path.abspath(__file__))
THIS_FILE = os.path.abspath(__file__)


# ---------- Rules that aren't about lists ----------

# Returns what's left of one monster after a spell hits it.
def blast(monster, spell):
    answer = ""
    for idx in range(0, len(monster)):
        if monster[idx] not in spell:
            answer = answer + monster[idx]
    return answer


# How many monsters (or ghosts) have reached the base.
def count_arrived(distances):
    count = 0
    for idx in range(0, len(distances)):
        if distances[idx] <= 0:
            count += 1
    return count


def find_file(filename):
    if os.path.exists(filename):
        return filename
    return os.path.join(HERE, filename)


def load_names():
    names = []
    try:
        with open(find_file("monsters.txt"), "r") as file:
            for line in file:
                name = line.strip().lower()
                if name.isalpha() and len(name) <= 10 and name not in names:
                    names.append(name)
    except OSError:
        pass
    return names if names else list(BACKUP_NAMES)


def load_words():
    words = set()
    with open(find_file("words.txt"), "r") as file:
        for line in file:
            word = line.strip().lower()
            if word.isalpha():
                words.add(word)
    return words


def make_wave(rng, names):
    """A random starting wave: different names, and no two monsters in the same lane and spot."""
    count = min(WAVE_SIZE, len(names))
    chosen = rng.sample(names, count)
    for tries in range(100):
        if sum(len(name) for name in chosen) <= MAX_LETTERS:
            break
        chosen = rng.sample(names, count)
    spots = [(lane, d) for lane in range(3) for d in range(NEAREST_START, FAR + 1)]
    picked = rng.sample(spots, count)
    return chosen, [d for lane, d in picked], [lane for lane, d in picked]


# ---------- Calling the functions you write ----------

class Stop(Exception):
    """Ends the game with a clear message instead of a long error."""


def do_nothing():
    pass


def written(name):
    """Your version of a function, or None if your notebook doesn't have one yet.
    A starter function that's still just pass counts as not written yet."""
    if FUNCTIONS is not None:
        function = FUNCTIONS.get(name)
    else:
        function = getattr(__main__, name, None)
    if not callable(function):
        return None
    code = getattr(function, "__code__", None)
    if code is not None and code.co_code == do_nothing.__code__.co_code:
        return None
    return function


def call(name, *args):
    try:
        return written(name)(*args)
    except Stop:
        raise
    except Exception as error:
        raise Stop(crash_message(name, error)) from None


def crash_message(name, error):
    lines = ["Your " + name + " function stopped with an error"]
    frames = [f for f in traceback.extract_tb(error.__traceback__)
              if os.path.abspath(f.filename) != THIS_FILE]
    if frames and frames[-1].line:
        lines[0] = lines[0] + " on this line:"
        lines.append("    " + frames[-1].line.strip())
    else:
        lines[0] = lines[0] + ":"
    lines.append(type(error).__name__ + ": " + str(error))
    if isinstance(error, IndexError):
        lines.append(name + " tried to look past the end of a list.")
    return "\n".join(lines)


def check_names(name, monsters):
    if not isinstance(monsters, list):
        raise Stop(name + " should give back a list, but it gave back " + repr(monsters)
                   + ".  Did you forget to return it?")
    for item in monsters:
        if not isinstance(item, str):
            raise Stop("After " + name + ", monsters has " + repr(item)
                       + " in it, but every item in monsters should be a string.")


def check_numbers(name, distances):
    if not isinstance(distances, list):
        raise Stop(name + " should give back a list, but it gave back " + repr(distances)
                   + ".  Did you forget to return it?")
    for item in distances:
        if isinstance(item, bool) or not isinstance(item, int):
            raise Stop("After " + name + ", distances has " + repr(item)
                       + " in it, but every item in distances should be a whole number.")


def check_lined_up(name, monsters, distances):
    if len(monsters) != len(distances):
        raise Stop("After " + name + ", monsters has " + str(len(monsters)) + " items but distances has "
                   + str(len(distances)) + ".  The two lists have to stay lined up, because the same "
                   + "index is the same monster.")


def check_same_size(name, list_name, before, now):
    if len(now) != len(before):
        raise Stop(name + " changed how many items " + list_name + " has.  It should only change "
                   + "the items that are already there.")


def check_made_new_list(name, list_name, before, now, returned):
    if now == before and isinstance(returned, list) and returned != before:
        raise Stop(name + " made a new list, but " + list_name + " didn't change.  "
                   + "Change the items of " + list_name + " itself instead.")


def check_count(name, value):
    if isinstance(value, bool) or not isinstance(value, int):
        raise Stop(name + " should return a whole number, but it returned " + repr(value) + ".")
    return value


def check_true_false(name, value):
    if not isinstance(value, bool):
        raise Stop(name + " should return True or False, but it returned " + repr(value) + ".")
    return value


# ---------- The game ----------

class Game:
    def __init__(self, setup, board_type=None):
        self.setup = setup
        self.rng = random.Random(setup)
        self.names = load_names()
        self.dictionary = load_words()
        self.monsters, self.distances, self.lanes = make_wave(self.rng, self.names)
        self.ids = list(range(len(self.monsters)))
        self.looks = {i: color_for(self.monsters[i]) for i in self.ids}
        self.next_id = len(self.ids)
        self.spell_history = []
        self.uses = {}
        self.score = 0
        self.links = 0
        self.turn = 1
        self.said = set()
        self.cleanup_skipped = False
        self.result = None
        self.board = (board_type or NullBoard)(self)

    # ----- small helpers -----

    def say_once(self, key, text):
        if key not in self.said:
            self.said.add(key)
            print(text)

    def alive(self):
        return [m for m in self.monsters if m != ""]

    def score_shown(self):
        return any(written(n) for n in ("count_defeated", "spell_points", "count_links"))

    def cleanup_ready(self):
        return bool(written("remaining_monsters") and written("remaining_distances")
                    and not self.cleanup_skipped)

    def snapshot(self):
        return [{"id": self.ids[k], "name": self.monsters[k], "d": self.distances[k],
                 "lane": self.lanes[k], "look": self.looks[self.ids[k]]}
                for k in range(len(self.monsters))]

    def hud(self):
        return {"turn": self.turn, "left": len(self.alive()), "setup": self.setup,
                "score": self.score if self.score_shown() else None}

    def special_for(self, spell):
        if spell not in SPECIALS or not written(spell) or self.uses.get(spell, 0) >= SPELL_USES:
            return None
        if spell == "zap" and not self.cleanup_ready():
            return None
        return spell

    def ready_specials(self):
        return [s for s in SPECIALS if self.special_for(s)]

    # A monster's name, or the name with s or es on the end, would wipe that monster out.
    def is_monster_name(self, spell):
        for name in self.names:
            if spell == name or spell == name + "s" or spell == name + "es":
                return True
        return False

    def opening_notes(self):
        notes = []
        if not written("cast_spell"):
            notes.append("(cast_spell isn't written yet, so spells won't do anything.)")
        if not written("march"):
            notes.append("(march isn't written yet, so the monsters will stand still.)")
        if written("remaining_monsters") and not written("remaining_distances"):
            notes.append("(The game will use remaining_monsters once remaining_distances is written "
                         "too, so the two lists stay lined up.)")
        if written("remaining_distances") and not written("remaining_monsters"):
            notes.append("(The game will use remaining_distances once remaining_monsters is written "
                         "too, so the two lists stay lined up.)")
        if written("zap") and not self.cleanup_ready():
            notes.append("(zap will work once remaining_monsters and remaining_distances are written.)")
        return notes

    # ----- one turn -----

    def take_turn(self, spell):
        """Returns "again" if the spell didn't count, or "on", "win", or "lose"."""
        board = self.board
        if not (3 <= len(spell) <= 6 and spell.isalpha() and spell in self.dictionary):
            print("That's not a spell I know.  Try another word.")
            board.reject(spell + "?")
            return "again"
        if self.is_monster_name(spell):
            print("Monster names can't be spells.  Try another word.")
            board.reject("no monster names")
            return "again"
        if written("already_cast"):
            if check_true_false("already_cast", call("already_cast", list(self.spell_history), spell)):
                print("You already cast " + spell + ".  Try a new word.")
                board.reject("already cast")
                return "again"
        special = self.special_for(spell)
        if special == "nova" and written("count_close"):
            if check_count("count_close", call("count_close", list(self.distances), NOVA_REACH)) == 0:
                print("No monsters are close enough.  Nova fizzles, but you keep it.")
                board.reject("nova fizzles", "#aab0d0")
                return "again"

        self.spell_history.append(spell)
        defeated_before = self.count_defeated_now()
        points_before = self.spell_points_now()
        before = self.snapshot()
        if special:
            self.uses[special] = self.uses.get(special, 0) + 1
            self.run_special(special)
        else:
            self.run_cast_spell(spell)
        board.change(before, self.snapshot(), special or "blast", spell)

        self.add_score(defeated_before, points_before)
        self.add_chain_bonus()
        self.clean_up()
        board.set_hud(self.hud())

        if len(self.alive()) == 0:
            board.win()
            self.result = "win"
            return "win"

        self.run_march()
        if written("add_monster") and self.turn % ARRIVAL_EVERY == 0:
            self.run_add_monster()

        arrived = [k for k in range(len(self.distances)) if self.distances[k] <= 0]
        if count_arrived(list(self.distances)) > 0:
            board.lose()
            if all(self.monsters[k] == "" for k in arrived):
                print("A defeated monster's ghost reached your base.  Game over!")
                print("(Ghosts are defeated monsters still in the lists.  remaining_monsters "
                      "and remaining_distances clear them out.)")
            else:
                print("A monster reached your base.  Game over!")
            self.result = "lose"
            return "lose"

        self.turn += 1
        board.set_hud(self.hud())
        board.finish_turn()
        return "on"

    def run_cast_spell(self, spell):
        if not written("cast_spell"):
            return
        before = list(self.monsters)
        returned = call("cast_spell", self.monsters, spell)
        check_names("cast_spell", self.monsters)
        check_same_size("cast_spell", "monsters", before, self.monsters)
        check_made_new_list("cast_spell", "monsters", before, self.monsters, returned)
        if self.monsters == before and [blast(m, spell) for m in before] != before:
            self.say_once("cast_spell", "(cast_spell ran, but no names changed.)")

    def run_special(self, special):
        before_names = list(self.monsters)
        before_distances = list(self.distances)
        if special == "zap":
            returned = call("zap", self.monsters, self.distances)
        elif special == "nova":
            returned = call("nova", self.monsters, self.distances)
        elif special == "fire":
            returned = call("fire", self.monsters)
        else:
            returned = call("gust", self.distances, FAR)
        check_names(special, self.monsters)
        check_numbers(special, self.distances)
        check_same_size(special, "monsters", before_names, self.monsters)
        check_same_size(special, "distances", before_distances, self.distances)
        if special == "gust":
            check_made_new_list("gust", "distances", before_distances, self.distances, returned)
            if self.distances == before_distances:
                self.say_once("gust", "(gust ran, but no distances changed.)")
        else:
            check_made_new_list(special, "monsters", before_names, self.monsters, returned)
            new_defeats = [k for k in range(len(self.monsters))
                           if self.monsters[k] == "" and before_names[k] != ""]
            if not new_defeats:
                self.say_once(special, "(" + special + " ran, but no monster was defeated.)")
            elif special == "zap":
                closest = min(before_distances)
                for k in new_defeats:
                    if before_distances[k] != closest:
                        self.say_once("zap-wrong", "(zap defeated the " + before_names[k] + " at distance "
                                      + str(before_distances[k]) + ", but the closest monster was at distance "
                                      + str(closest) + ".)")
            elif special == "fire":
                biggest = max(len(m) for m in before_names)
                for k in new_defeats:
                    if len(before_names[k]) != biggest:
                        self.say_once("fire-wrong", "(fire burned up the " + before_names[k] + ", but the "
                                      + "biggest monster had " + str(biggest) + " letters.)")

    def count_defeated_now(self):
        if not written("count_defeated"):
            return 0
        return check_count("count_defeated", call("count_defeated", list(self.monsters)))

    def spell_points_now(self):
        if not written("spell_points"):
            return 0
        return check_count("spell_points", call("spell_points", list(self.monsters), list(self.distances)))

    def add_score(self, defeated_before, points_before):
        if not (written("count_defeated") or written("spell_points")):
            return
        new_defeats = self.count_defeated_now() - defeated_before
        if written("spell_points"):
            points = self.spell_points_now() - points_before
        else:
            points = POINTS_PER_DEFEAT * max(0, new_defeats)
        if points != 0:
            self.score += points
            self.board.note(("+" if points > 0 else "") + str(points), "#ffe066")
        if new_defeats >= 2:
            words = {2: "Double defeat!", 3: "Triple defeat!"}
            self.board.callout(words.get(new_defeats, "Mega defeat!"), "#7ee081")

    def add_chain_bonus(self):
        if not written("count_links"):
            return
        links = check_count("count_links", call("count_links", list(self.spell_history)))
        if links > self.links:
            bonus = CHAIN_BONUS * (links - self.links)
            self.score += bonus
            self.board.callout("Chain!  +" + str(bonus), "#9ad1ff")
        self.links = links

    def clean_up(self):
        if not self.cleanup_ready():
            return
        names = list(self.monsters)
        given_names = list(self.monsters)
        given_distances = list(self.distances)
        new_distances = call("remaining_distances", given_names, given_distances)
        if given_names != self.monsters or given_distances != self.distances:
            self.say_once("remaining_distances-changed", "(remaining_distances changed the lists it was "
                          "given.  It should create a new list and leave monsters and distances alone.)")
        given_names = list(self.monsters)
        new_monsters = call("remaining_monsters", given_names)
        if given_names != self.monsters:
            self.say_once("remaining_monsters-changed", "(remaining_monsters changed monsters.  It should "
                          "create a new list and leave monsters alone.)")
        check_names("remaining_monsters", new_monsters)
        check_numbers("remaining_distances", new_distances)
        if len(new_monsters) != len(new_distances):
            self.cleanup_skipped = True
            print("After remaining_monsters and remaining_distances, monsters has "
                  + str(len(new_monsters)) + " items but distances has " + str(len(new_distances))
                  + ".  The two lists have to stay lined up, because the same index is the same "
                  + "monster.  The game will skip the cleanup for the rest of this game.")
            return
        before = self.snapshot()
        self.ids, self.lanes = self.match_ids(names, new_monsters)
        self.monsters = list(new_monsters)
        self.distances = list(new_distances)
        self.board.change(before, self.snapshot(), "cleanup")

    def match_ids(self, old_names, new_names):
        """Works out which monster is which after the lists are cleaned up."""
        alive = [k for k in range(len(old_names)) if old_names[k] != ""]
        if new_names == [old_names[k] for k in alive]:
            keep = alive
        elif new_names == old_names:
            keep = list(range(len(old_names)))
        else:
            keep = []
            start = 0
            for name in new_names:
                found = None
                for k in range(start, len(old_names)):
                    if old_names[k] == name:
                        found = k
                        break
                keep.append(found)
                if found is not None:
                    start = found + 1
        ids, lanes = [], []
        for k in keep:
            if k is None:
                ids.append(self.new_id(""))
                lanes.append(self.rng.randint(0, 2))
            else:
                ids.append(self.ids[k])
                lanes.append(self.lanes[k])
        return ids, lanes

    def new_id(self, name):
        new = self.next_id
        self.next_id += 1
        self.looks[new] = color_for(name) or COLORS[new % len(COLORS)]
        return new

    def run_march(self):
        if not written("march"):
            return
        before = self.snapshot()
        before_distances = list(self.distances)
        returned = call("march", self.distances)
        check_numbers("march", self.distances)
        check_same_size("march", "distances", before_distances, self.distances)
        check_made_new_list("march", "distances", before_distances, self.distances, returned)
        if self.distances == before_distances:
            self.say_once("march", "(march ran, but no distances changed.)")
        self.board.change(before, self.snapshot(), "march")

    def run_add_monster(self):
        before = self.snapshot()
        count = len(self.monsters)
        call("add_monster", self.monsters, self.distances, list(self.names), FAR)
        check_names("add_monster", self.monsters)
        check_numbers("add_monster", self.distances)
        check_lined_up("add_monster", self.monsters, self.distances)
        if len(self.monsters) == count:
            self.say_once("add_monster", "(add_monster ran, but neither list got longer.)")
            return
        while len(self.ids) < len(self.monsters):
            k = len(self.ids)
            self.ids.append(self.new_id(self.monsters[k]))
            taken = [self.lanes[j] for j in range(len(self.lanes)) if self.distances[j] == self.distances[k]]
            free = [lane for lane in range(3) if lane not in taken]
            self.lanes.append(self.rng.choice(free) if free else self.rng.randint(0, 2))
        self.board.change(before, self.snapshot(), "arrive")


# setup is the setup number to play again.  Leave it out for a new random setup.
def play(setup=None):
    if setup is None:
        setup = random.SystemRandom().randint(1000, 9999)
    random.seed(setup)
    game = Game(setup)
    print("Setup " + str(setup) + ".  To play this setup again, run play(" + str(setup) + ").")
    print("Spells are real words with 3 to 6 letters, but not monster names.  Type quit to stop.")
    for note in game.opening_notes():
        print(note)
    if game.ready_specials():
        print("One-use spells: " + ", ".join(game.ready_specials()) + ".")
    game.board = Board(game)

    try:
        while game.result is None:
            spell = input("Turn " + str(game.turn) + ", cast a spell: ").strip().lower()
            if spell == "quit":
                game.result = "quit"
            elif spell != "":
                game.take_turn(spell)
    except Stop as stop:
        print()
        print(stop)
        game.board.oops()
        game.result = "error"

    if game.result == "win":
        print("You win!  You did it in " + str(game.turn) + " spells.")
    if game.score_shown() and game.result in ("win", "lose", "quit"):
        print("Score: " + str(game.score))
    print("To play this setup again, run play(" + str(setup) + ").")


# ---------- Drawing helpers ----------

COLORS = [("#9b59b6", "#d2b4de"), ("#27ae60", "#a9dfbf"), ("#e67e22", "#f5cba7"),
          ("#2e86c1", "#aed6f1"), ("#c0392b", "#f5b7b1"), ("#16a085", "#a3e4d7"),
          ("#b7950b", "#f9e79f"), ("#6c3483", "#d7bde2")]
SPELL_COLORS = {"blast": "#ffe066", "fire": "#ff8c42", "zap": "#fff275",
                "nova": "#f78fb3", "gust": "#9ad1ff"}
LETTER_WIDTH = 9.5
GHOST_ALPHA = 0.32


def dist_x(d):
    return 60 + d * 82


def row_y(row):
    return TOP + 50 + row * 105


def radius_for(word):
    return 10 + 2 * len(word)


def color_for(word):
    if word == "":
        return None
    return COLORS[sum(ord(ch) for ch in word) % len(COLORS)]


def letter_dx(index, count):
    return (index - (count - 1) / 2) * LETTER_WIDTH


def ease(t):
    return t * t * (3 - 2 * t)


def ease_out_back(t):
    s = 1.7
    t = t - 1
    return t * t * ((s + 1) * t + s) + 1


def bounce(t):
    if t < 1 / 2.75:
        return 7.5625 * t * t
    if t < 2 / 2.75:
        t = t - 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    if t < 2.5 / 2.75:
        t = t - 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    t = t - 2.625 / 2.75
    return 7.5625 * t * t + 0.984375


def lerp(a, b, t):
    return a + (b - a) * t


def clamp(value, low=0.0, high=1.0):
    return max(low, min(high, value))


def kept_letters(before, after):
    """Which letters of before are still in after, matched left to right.
    Returns a list with the new index of each old letter, or -1 if it's gone,
    or None if after can't be made by removing letters from before."""
    result = []
    j = 0
    for ch in before:
        if j < len(after) and after[j] == ch:
            result.append(j)
            j = j + 1
        else:
            result.append(-1)
    if j != len(after):
        return None
    return result


def layout(items):
    """Where each monster is drawn.  Monsters sharing a lane and spot stand side by side."""
    groups = {}
    for item in items:
        groups.setdefault((item["lane"], item["d"]), []).append(item["id"])
    spots = {}
    for (lane, d), ids in groups.items():
        for k, i in enumerate(ids):
            spots[i] = (dist_x(d) + (k - (len(ids) - 1) / 2) * 34, row_y(lane))
    return spots


def make_actor(x, y, word, look, **extra):
    actor = {"x": x, "y": y, "r": radius_for(word), "look": look,
             "letters": [(ch, letter_dx(i, len(word)), 0.0, 1.0, "#ffffff") for i, ch in enumerate(word)],
             "alpha": 1.0, "squash": 1.0, "hop": 0.0, "walk": 0.0, "glow": 0.0, "tint": None}
    actor.update(extra)
    return actor


def make_ghost(x, y, alpha=1.0, **extra):
    return make_actor(x, y, "", ("#c9d0ff", "#c9d0ff"), ghost=True, r=17,
                      alpha=alpha * GHOST_ALPHA, **extra)


def draw_ghost(c, a):
    x, y, r = a["x"], a["y"] - a["hop"] + math.sin(a["walk"] * math.pi) * 3, a["r"]
    c.global_alpha = clamp(a["alpha"])
    c.fill_style = "#c9d0ff"
    c.begin_path()
    c.arc(x, y, r, math.pi, 2 * math.pi)
    c.line_to(x + r, y + r)
    for k in range(4):
        c.line_to(x + r - (k + 0.5) * r / 2, y + r - 6 * (k % 2 == 0))
        c.line_to(x + r - (k + 1) * r / 2, y + r)
    c.close_path()
    c.fill()
    c.fill_style = "#1b1f3a"
    c.fill_circle(x - r * 0.35, y - r * 0.15, r * 0.18)
    c.fill_circle(x + r * 0.35, y - r * 0.15, r * 0.18)
    c.global_alpha = 1.0


def draw_actor(c, a):
    if a["alpha"] <= 0.01 or a["look"] is None:
        return
    if a.get("ghost"):
        draw_ghost(c, a)
        return
    body, belly = a["look"]
    if a["tint"]:
        body = belly = a["tint"]
    x, y, r = a["x"], a["y"] - a["hop"], max(0.5, a["r"])
    squash = clamp(a["squash"], 0.05, 1.0)
    ry = r * squash
    rx = r * (2 - squash)
    cy = y + (r - ry)
    step = math.sin(a["walk"] * math.pi * 2) * r * 0.3
    c.global_alpha = clamp(a["alpha"])
    c.fill_style = body
    c.begin_path()
    c.ellipse(x - r * 0.45 + step, y + r * 0.92, r * 0.34, r * 0.2, 0, 0, 2 * math.pi)
    c.fill()
    c.begin_path()
    c.ellipse(x + r * 0.45 - step, y + r * 0.92, r * 0.34, r * 0.2, 0, 0, 2 * math.pi)
    c.fill()
    c.begin_path()
    c.ellipse(x, cy, rx, ry, 0, 0, 2 * math.pi)
    c.fill()
    c.fill_style = belly
    c.begin_path()
    c.ellipse(x, cy + ry * 0.32, rx * 0.55, ry * 0.42, 0, 0, 2 * math.pi)
    c.fill()
    eye = max(2.5, r * 0.27)
    for ex in (x - rx * 0.36, x + rx * 0.22):
        c.fill_style = "#ffffff"
        c.fill_circle(ex, cy - ry * 0.25, eye * min(1, squash * 1.5))
        c.fill_style = "#1b1f3a"
        c.fill_circle(ex - eye * 0.35, cy - ry * 0.25, eye * 0.5 * min(1, squash * 1.5))
    if a["glow"] > 0:
        c.global_alpha = clamp(a["alpha"] * a["glow"] * 0.8)
        c.fill_style = "#ffffff"
        c.begin_path()
        c.ellipse(x, cy, rx, ry, 0, 0, 2 * math.pi)
        c.fill()
    c.font = "bold 15px monospace"
    c.text_align = "center"
    c.text_baseline = "alphabetic"
    label_y = a.get("label_y", a["y"]) + a.get("label_r", a["r"]) + 17
    for ch, dx, dy, alpha, color in a["letters"]:
        if alpha > 0.01:
            c.global_alpha = clamp(alpha * a["alpha"])
            c.fill_style = color
            c.fill_text(ch, a["x"] + dx, label_y + dy - a["hop"])
    c.global_alpha = 1.0


def draw_background(c):
    c.fill_style = "#1b1f3a"
    c.fill_rect(0, 0, WIDTH, HEIGHT)
    for row in range(3):
        y = row_y(row)
        c.fill_style = "#232850"
        c.fill_rect(44, y - 42, WIDTH - 54, 92)
        c.fill_style = "#2b3060"
        for d in range(0, FAR):
            c.fill_rect(dist_x(d) + 41, y - 42, 1, 92)
    # The castle wall at your base.
    wall_top = TOP + 8
    c.fill_style = "#6f7595"
    c.fill_rect(8, wall_top, 28, 306)
    for top in range(0, 3):
        c.fill_rect(8 + top * 10, wall_top - 8, 8, 10)
    c.fill_style = "#555b7a"
    for y in range(wall_top + 12, wall_top + 302, 14):
        c.fill_rect(8, y, 28, 2)
        offset = 8 if (y // 14) % 2 == 0 else 18
        c.fill_rect(offset, y + 2, 2, 12)
    c.fill_style = "#6d7399"
    c.font = "13px sans-serif"
    c.text_align = "center"
    c.text_baseline = "alphabetic"
    for d in range(1, FAR + 1):
        c.fill_text(str(d), dist_x(d), HEIGHT - 8)
    c.fill_style = "#aab0d0"
    c.fill_text("base", 22, HEIGHT - 8)


# ---------- The board: draws the monsters and animates every change ----------

class NullBoard:
    """Stands in for the board when nothing is drawn (for testing)."""
    def __init__(self, game):
        pass

    def change(self, before, after, effect, spell=None):
        pass

    def reject(self, text, color="#ff6b6b"):
        pass

    def note(self, text, color):
        pass

    def callout(self, text, color):
        pass

    def set_hud(self, hud):
        pass

    def finish_turn(self):
        pass

    def win(self):
        pass

    def lose(self):
        pass

    def oops(self):
        pass


class Board:
    def __init__(self, game):
        self.canvas = MultiCanvas(2, width=WIDTH, height=HEIGHT)
        self.back = self.canvas[0]
        self.front = self.canvas[1]
        display(self.canvas)
        self.items = game.snapshot()
        self.hud = game.hud()
        self.seen_ghosts = set()
        self.particles = []
        self.notes = []
        self.message = None
        self.message_t = 0.0
        with hold_canvas():
            draw_background(self.back)
        self.still()

    # ----- one frame -----

    def actors_now(self):
        spots = layout(self.items)
        actors = []
        for item in self.items:
            x, y = spots[item["id"]]
            if item["name"] == "":
                if item["id"] in self.seen_ghosts:
                    actors.append(make_ghost(x, y))
            else:
                actors.append(make_actor(x, y, item["name"], item["look"]))
        return actors

    def frame(self, actors, overlays=(), shake=0.0, flash=0.0, moving=True):
        started = time.time()
        c = self.front
        with hold_canvas():
            c.clear()
            if flash > 0:
                c.global_alpha = clamp(flash * 0.7)
                c.fill_style = "#ff3b3b"
                c.fill_rect(0, 0, 44, HEIGHT)
                c.global_alpha = 1.0
            c.save()
            if shake > 0:
                c.translate(fx.uniform(-shake, shake), fx.uniform(-shake, shake))
            for actor in actors:
                draw_actor(c, actor)
            self.step_particles(c, moving)
            c.restore()
            for overlay in overlays:
                overlay(c)
            self.draw_notes(c, moving)
            if self.message is not None and moving:
                self.message_t = min(1.0, self.message_t + 1 / (FPS * 0.5))
            self.draw_message(c, self.message_t)
            self.draw_hud(c)
        stats["frames"] = stats["frames"] + 1
        stats["seconds"] = stats["seconds"] + time.time() - started

    def draw_hud(self, c):
        hud = self.hud
        c.global_alpha = 1.0
        c.font = "14px sans-serif"
        c.text_baseline = "alphabetic"
        c.text_align = "left"
        if hud["score"] is not None:
            c.fill_style = "#ffe066"
            c.fill_text("Score " + str(hud["score"]), 48, 20)
        c.fill_style = "#8d93b8"
        c.text_align = "right"
        c.fill_text("Monsters left " + str(hud["left"]) + "     Turn " + str(hud["turn"])
                    + "     Setup " + str(hud["setup"]), WIDTH - 12, 20)

    def still(self):
        self.frame(self.actors_now(), moving=False)

    def animate(self, seconds, actors_at, overlays_at=None, shake_at=None, flash_at=None, events=()):
        frames = max(1, round(seconds * FPS))
        pending = sorted(events, key=lambda e: e[0])
        for f in range(1, frames + 1):
            t = f / frames
            while pending and pending[0][0] <= t:
                pending.pop(0)[1]()
            self.frame(actors_at(t),
                       overlays_at(t) if overlays_at else (),
                       shake_at(t) if shake_at else 0.0,
                       flash_at(t) if flash_at else 0.0)
            if WAIT:
                time.sleep(1 / FPS)

    def set_hud(self, hud):
        self.hud = hud
        self.still()

    # ----- particles, notes, and big words -----

    def burst(self, x, y, count, colors, speed=120, gravity=200, life=0.7, size=3.5, up=0.0):
        for _ in range(count):
            angle = fx.uniform(0, 2 * math.pi)
            power = fx.uniform(0.3, 1.0) * speed
            self.particles.append({"x": x, "y": y, "vx": math.cos(angle) * power,
                                   "vy": math.sin(angle) * power - up, "g": gravity,
                                   "life": life * fx.uniform(0.6, 1.0), "max": life,
                                   "size": size * fx.uniform(0.6, 1.3),
                                   "color": fx.choice(colors), "spin": fx.uniform(0, 6)})

    def step_particles(self, c, moving):
        dt = 1 / FPS if moving else 0.0
        alive = []
        for p in self.particles:
            p["life"] = p["life"] - dt
            if p["life"] <= 0:
                continue
            p["vy"] = p["vy"] + p["g"] * dt
            p["x"] = p["x"] + p["vx"] * dt
            p["y"] = p["y"] + p["vy"] * dt
            p["spin"] = p["spin"] + dt * 8
            c.global_alpha = clamp(p["life"] / p["max"])
            c.fill_style = p["color"]
            if p.get("confetti"):
                w = p["size"] * abs(math.cos(p["spin"])) + 1
                c.fill_rect(p["x"] - w / 2, p["y"] - p["size"] / 2, w, p["size"])
            else:
                c.fill_circle(p["x"], p["y"], p["size"])
            alive.append(p)
        self.particles = alive
        c.global_alpha = 1.0

    def note(self, text, color):
        """Small text that floats up from the score."""
        self.notes.append({"text": text, "color": color, "x": 110, "y": 22, "age": 0.0,
                           "life": 1.0, "size": 16})

    def callout(self, text, color):
        """Bigger text that floats up in the middle of the board."""
        self.notes.append({"text": text, "color": color, "x": WIDTH / 2 + 20,
                           "y": TOP + 70 + 34 * len([n for n in self.notes if n["size"] > 20]),
                           "age": 0.0, "life": 1.3, "size": 28})

    def draw_notes(self, c, moving):
        kept = []
        for n in self.notes:
            if moving:
                n["age"] = n["age"] + 1 / FPS
            t = n["age"] / n["life"]
            if t >= 1:
                continue
            c.global_alpha = clamp(1.4 - 1.4 * t)
            c.font = "bold " + str(n["size"]) + "px sans-serif"
            c.text_align = "center" if n["size"] > 20 else "left"
            c.text_baseline = "middle"
            c.fill_style = "#000000"
            c.fill_text(n["text"], n["x"] + 2, n["y"] - 18 * t + 2)
            c.fill_style = n["color"]
            c.fill_text(n["text"], n["x"], n["y"] - 18 * t)
            kept.append(n)
        self.notes = kept
        c.global_alpha = 1.0

    def finish_turn(self):
        """Lets any floating text finish before the next spell."""
        if self.notes:
            longest = max(n["life"] - n["age"] for n in self.notes)
            actors = self.actors_now()
            self.animate(max(0.05, longest), lambda t: actors)
            self.still()

    def draw_message(self, c, t):
        if self.message is None:
            return
        text, color = self.message
        size = 64 * clamp(ease_out_back(clamp(t)), 0.05, 2.0)
        c.global_alpha = clamp(t * 2)
        c.font = "bold " + str(int(size)) + "px sans-serif"
        c.text_align = "center"
        c.text_baseline = "middle"
        c.fill_style = "#000000"
        c.fill_text(text, WIDTH / 2 + 3, HEIGHT / 2 + 3)
        c.fill_style = color
        c.fill_text(text, WIDTH / 2, HEIGHT / 2)
        c.global_alpha = 1.0

    def banner(self, text, color):
        def overlay_at(t):
            def draw(c):
                c.global_alpha = clamp(1 - t * t)
                c.font = "bold 30px sans-serif"
                c.text_align = "center"
                c.text_baseline = "middle"
                c.fill_style = color
                c.fill_text(text, WIDTH / 2 + 20, TOP + 26 - 10 * t)
                c.global_alpha = 1.0
            return [draw]
        return overlay_at

    # ----- every change to the lists -----

    def change(self, before, after, effect, spell=None):
        """Animates from one snapshot of the lists to the next."""
        old = {item["id"]: item for item in before}
        new = {item["id"]: item for item in after}
        old_spots, new_spots = layout(before), layout(after)
        plans, events, zapped = [], [], []
        changed = False
        new_ghosts = []

        order = [item["id"] for item in before] + [item["id"] for item in after if item["id"] not in old]
        for i in order:
            b, a = old.get(i), new.get(i)
            if b is not None and a is not None:
                x0, y0 = old_spots[i]
                x1, y1 = new_spots[i]
                moving = (x0, y0) != (x1, y1)
                changed = changed or moving or b["name"] != a["name"]
                if b["name"] == "" and a["name"] == "":
                    seen = i in self.seen_ghosts
                    if not seen:
                        new_ghosts.append(i)
                        changed = True
                    plans.append(self.plan_ghost(x0, y0, x1, y1, seen, effect))
                elif b["name"] == a["name"]:
                    plans.append(self.plan_move(x0, y0, x1, y1, a["name"], a["look"], effect))
                elif a["name"] == "":
                    plan = self.plan_defeat(x0, y0, b["name"], b["look"], effect, events)
                    if effect == "zap":
                        zapped.append((x0, y0))
                    plans.append(plan)
                elif kept_letters(b["name"], a["name"]) is not None:
                    plans.append(self.plan_shrink(x0, y0, x1, y1, b["name"], a["name"], b["look"]))
                else:
                    plans.append(self.plan_swap(x0, y0, b["name"], a["name"], b["look"]))
            elif b is not None:
                if b["name"] == "" and i not in self.seen_ghosts:
                    continue
                changed = True
                x0, y0 = old_spots[i]
                if b["name"] == "":
                    plans.append({"at": lambda t, x0=x0, y0=y0: [make_ghost(x0, y0, 1 - ease(t))]})
                else:
                    plans.append(self.plan_fade(x0, y0, b["name"], b["look"], fade_in=False))
            else:
                if a["name"] == "":
                    continue
                changed = True
                x1, y1 = new_spots[i]
                if effect == "arrive":
                    plans.append(self.plan_drop(x1, y1, a["name"], a["look"]))
                else:
                    plans.append(self.plan_fade(x1, y1, a["name"], a["look"], fade_in=True))

        overlays = []
        if spell is not None:
            overlays.append(self.banner(spell.upper(), SPELL_COLORS.get(effect, "#ffe066")))
        if effect == "zap":
            overlays.append(self.lightning(zapped))
        if effect == "nova":
            overlays.append(self.nova_ring())
        if effect == "gust":
            overlays.append(self.wind())

        if changed or overlays:
            seconds = {"cleanup": 0.35, "march": 0.6, "gust": 0.8, "arrive": 0.6}.get(effect, 0.9)

            def actors_at(t):
                out = []
                for plan in plans:
                    out.extend(plan["at"](t))
                return out

            def overlays_at(t):
                out = []
                for overlay in overlays:
                    out.extend(overlay(t))
                return out

            self.animate(seconds, actors_at, overlays_at, events=events)
        self.seen_ghosts.update(new_ghosts)
        self.items = after
        self.still()

    def reject(self, text, color="#ff6b6b"):
        actors = self.actors_now()
        self.animate(0.45, lambda t: actors, self.banner(text, color),
                     shake_at=lambda t: 3 * (1 - t))
        self.still()

    def win(self):
        for _ in range(4):
            self.burst(fx.uniform(150, 620), fx.uniform(60, 200), 40,
                       ["#ffe066", "#7ee081", "#9ad1ff", "#ff8c42", "#f78fb3"],
                       speed=260, gravity=260, life=1.6, size=4, up=120)
        for p in self.particles:
            p["confetti"] = True
        self.message = ("You win!", "#7ee081")
        actors = self.actors_now()
        self.animate(1.6, lambda t: actors)

    def lose(self):
        self.message = ("Game over!", "#ff5c5c")
        actors = self.actors_now()
        self.animate(1.0, lambda t: actors,
                     shake_at=lambda t: 7 * (1 - t),
                     flash_at=lambda t: abs(math.sin(t * math.pi * 3)) * (1 - t))
        self.frame(actors, flash=0.35, moving=False)

    def oops(self):
        self.message = ("Oops!", "#ffb347")
        actors = self.actors_now()
        self.animate(0.5, lambda t: actors)

    # ----- plans: how one monster looks at time t (0 to 1) -----

    def plan_move(self, x0, y0, x1, y1, word, look, effect):
        moving = (x0, y0) != (x1, y1)
        hopping = moving and effect != "gust"

        def at(t):
            e = ease(t)
            hop = abs(math.sin(t * math.pi * 2)) * 7 if hopping else 0.0
            return [make_actor(lerp(x0, x1, e), lerp(y0, y1, e), word, look, hop=hop,
                               walk=t * 2 if hopping else 0.0)]
        return {"at": at}

    def plan_ghost(self, x0, y0, x1, y1, seen, effect):
        def at(t):
            e = ease(t)
            alpha = 1.0 if seen else ease(t)
            return [make_ghost(lerp(x0, x1, e), lerp(y0, y1, e), alpha,
                               walk=t * 2 if effect == "march" else 0.0)]
        return {"at": at}

    def plan_fade(self, x, y, word, look, fade_in):
        return {"at": lambda t: [make_actor(x, y, word, look, alpha=ease(t) if fade_in else 1 - ease(t))]}

    def plan_swap(self, x, y, before, after, look):
        return {"at": lambda t: [make_actor(x, y, before, look, alpha=1 - t),
                                 make_actor(x, y, after, color_for(after), alpha=t)]}

    def plan_drop(self, x, y, word, look):
        def at(t):
            drop_y = lerp(-40, y, bounce(t))
            return [make_actor(x, drop_y, word, look, label_y=drop_y)]
        return {"at": at}

    def flying_letters(self, before, kept, after_count, t, drift, color="#ffb347"):
        letters = []
        for i, ch in enumerate(before):
            start = letter_dx(i, len(before))
            if kept[i] >= 0:
                letters.append((ch, lerp(start, letter_dx(kept[i], after_count), ease(t)), 0.0, 1.0, "#ffffff"))
            else:
                rise = ease(clamp(t * 1.3))
                letters.append((ch, start + drift[i] * rise, -48 * rise, 1 - rise,
                                color if t > 0.05 else "#ffffff"))
        return letters

    def plan_shrink(self, x0, y0, x1, y1, before, after, look):
        kept = kept_letters(before, after)
        drift = [fx.uniform(-18, 18) for _ in before]

        def at(t):
            e = ease(t)
            r = lerp(radius_for(before), radius_for(after), ease(clamp(t * 1.4)))
            actor = make_actor(lerp(x0, x1, e), lerp(y0, y1, e), after, look or color_for(before),
                               r=r, glow=clamp(1 - t * 4))
            actor["letters"] = self.flying_letters(before, kept, len(after), t, drift)
            return [actor]
        return {"at": at}

    def plan_defeat(self, x, y, word, look, effect, events):
        kept = [-1] * len(word)
        drift = [fx.uniform(-22, 22) for _ in word]
        r0 = radius_for(word)
        if effect == "fire":
            for k in range(14):
                events.append((k * 0.05, lambda: self.burst(
                    x + fx.uniform(-r0, r0) * 0.6, y, 4, ["#ff8c42", "#ffd166", "#ef476f"],
                    speed=40, gravity=-160, life=0.6, size=4)))

            def at(t):
                gone = ease(clamp((t - 0.35) / 0.45))
                actor = make_actor(x, y, "", look, r=r0 * (1 - gone), tint="#3a2a2a" if t > 0.3 else None,
                                   glow=clamp(0.6 - t), label_r=r0)
                actor["letters"] = self.flying_letters(word, kept, 0, t, drift, "#ff8c42")
                return [actor]
        elif effect == "zap":
            events.append((0.32, lambda: self.burst(x, y, 30, ["#fff275", "#ffffff", "#9ad1ff"],
                                                     speed=220, gravity=0, life=0.45, size=2.5)))

            def at(t):
                gone = ease(clamp((t - 0.32) / 0.25))
                actor = make_actor(x, y, "", look, r=r0 * (1 - gone),
                                   glow=1.0 if t < 0.32 and int(t * 30) % 2 == 0 else 0.0, label_r=r0)
                actor["letters"] = self.flying_letters(word, kept, 0, clamp((t - 0.25) * 1.5), drift)
                return [actor]
        else:
            colors = ["#ffffff", "#d0d4ff", look[0] if look else "#ffffff"]
            if effect == "nova":
                colors = ["#f78fb3", "#ffffff", "#ffd1e3"]
            events.append((0.5, lambda: self.burst(x, y, 22, colors, speed=150, gravity=40,
                                                    life=0.55, size=4)))

            def at(t):
                pop = ease(clamp((t - 0.42) / 0.2))
                actor = make_actor(x, y, "", look, r=r0 * (1 + 0.25 * pop) if pop < 1 else 0,
                                   alpha=1 - pop, glow=clamp(1 - t * 4), label_r=r0)
                actor["letters"] = self.flying_letters(word, kept, 0, t, drift)
                return [actor]
        return {"at": at}

    # ----- spell effects drawn on top -----

    def lightning(self, targets):
        def overlay_at(t):
            if t > 0.34:
                return []

            def draw(c):
                c.stroke_style = "#fff275"
                c.line_width = 3
                for x, y in targets:
                    points = [(x + fx.uniform(-6, 6), 0)]
                    for k in range(1, 7):
                        points.append((x + fx.uniform(-14, 14), y * k / 7))
                    points.append((x, y))
                    c.stroke_lines(points)
                c.line_width = 1
            return [draw]
        return overlay_at

    def nova_ring(self):
        reach = dist_x(NOVA_REACH) + 40

        def overlay_at(t):
            def draw(c):
                c.global_alpha = clamp(1 - t)
                c.stroke_style = "#f78fb3"
                c.line_width = 6
                c.stroke_arc(22, HEIGHT / 2, 20 + ease(clamp(t * 1.6)) * reach, -math.pi / 2, math.pi / 2)
                c.line_width = 1
                c.global_alpha = 1.0
            return [draw]
        return overlay_at

    def wind(self):
        streaks = [(fx.uniform(0, WIDTH), fx.uniform(TOP + 10, HEIGHT - 30), fx.uniform(40, 110))
                   for _ in range(26)]

        def overlay_at(t):
            def draw(c):
                c.stroke_style = "#cfe8ff"
                c.line_width = 2
                c.global_alpha = clamp(1 - t)
                for x, y, length in streaks:
                    x2 = (x + t * 500) % (WIDTH + 100) - 50
                    c.stroke_line(x2, y, x2 + length, y)
                c.global_alpha = 1.0
                c.line_width = 1
            return [draw]
        return overlay_at
