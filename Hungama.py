import random
import os
import time
import sys

# ─────────────────────────────────────────────
#   C O L O R   P A L E T T E
# ─────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    ORANGE  = "\033[38;5;214m"
    PINK    = "\033[38;5;213m"
    LIME    = "\033[38;5;154m"

    BG_BLACK  = "\033[40m"
    BG_RED    = "\033[41m"
    BG_GREEN  = "\033[42m"


# ─────────────────────────────────────────────
#   W O R D   B A N K  (with hints)
# ─────────────────────────────────────────────
WORDS = [
    ("python",   "🐍  A popular programming language"),
    ("galaxy",   "🌌  A system of millions of stars"),
    ("thunder",  "⚡  The sound after lightning strikes"),
    ("phantom",  "👻  A ghost or mysterious figure"),
    ("volcano",  "🌋  A mountain that can erupt with lava"),
]


# ─────────────────────────────────────────────
#   H A N G M A N   A R T
#   (stages 0-6, drawn frame by frame)
# ─────────────────────────────────────────────
HANGMAN = [
    # 0 wrong — empty gallows
    r"""
  ╔══════╗
  ║      │
  ║
  ║
  ║
  ║
══╩══════╝
""",
    # 1 wrong — head
    r"""
  ╔══════╗
  ║      │
  ║      O
  ║
  ║
  ║
══╩══════╝
""",
    # 2 wrong — body
    r"""
  ╔══════╗
  ║      │
  ║      O
  ║      │
  ║
  ║
══╩══════╝
""",
    # 3 wrong — left arm
    r"""
  ╔══════╗
  ║      │
  ║      O
  ║     /│
  ║
  ║
══╩══════╝
""",
    # 4 wrong — both arms
    r"""
  ╔══════╗
  ║      │
  ║      O
  ║     /│\
  ║
  ║
══╩══════╝
""",
    # 5 wrong — left leg
    r"""
  ╔══════╗
  ║      │
  ║      O
  ║     /│\
  ║     /
  ║
══╩══════╝
""",
    # 6 wrong — full body (dead)
    r"""
  ╔══════╗
  ║      │
  ║      O
  ║     /│\
  ║     / \
  ║
══╩══════╝
""",
]


# ─────────────────────────────────────────────
#   U T I L I T I E S
# ─────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def slow_print(text, delay=0.03):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def banner():
    print(f"""
{C.CYAN}{C.BOLD}
  ██╗  ██╗ █████╗ ███╗  ██╗ ██████╗ ███╗  ███╗ █████╗ ███╗  ██╗
  ██║  ██║██╔══██╗████╗ ██║██╔════╝ ████╗████║██╔══██╗████╗ ██║
  ███████║███████║██╔██╗██║██║  ███╗██╔████╔██║███████║██╔██╗██║
  ██╔══██║██╔══██║██║╚████║██║   ██║██║╚██╔╝██║██╔══██║██║╚████║
  ██║  ██║██║  ██║██║  ╚███║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║  ╚███║
  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝   ╚══╝
{C.RESET}""")


def divider(char="─", width=50, color=C.DIM):
    print(f"{color}{char * width}{C.RESET}")


def hangman_colored(stage):
    """Print hangman art with color based on danger level."""
    colors = [C.GREEN, C.LIME, C.YELLOW, C.YELLOW, C.ORANGE, C.RED, C.RED]
    art = HANGMAN[stage]
    print(f"{C.BOLD}{colors[stage]}{art}{C.RESET}")


def display_word(word, guessed):
    """Show guessed letters; hide the rest as underscores."""
    revealed = []
    for letter in word:
        if letter in guessed:
            revealed.append(f"{C.GREEN}{C.BOLD}{letter.upper()}{C.RESET}")
        else:
            revealed.append(f"{C.WHITE}_")
    return "  ".join(revealed)


def display_guesses(wrong, max_wrong=6):
    """Show wrong guesses with a live HP-bar style indicator."""
    remaining = max_wrong - len(wrong)
    bar_filled = "█" * remaining
    bar_empty  = "░" * len(wrong)

    if remaining > 3:
        bar_color = C.GREEN
    elif remaining > 1:
        bar_color = C.YELLOW
    else:
        bar_color = C.RED

    wrong_str = "  ".join(
        f"{C.RED}{C.BOLD}{l.upper()}{C.RESET}" for l in sorted(wrong)
    ) if wrong else f"{C.DIM}none yet{C.RESET}"

    print(f"  {C.BOLD}Lives:{C.RESET} {bar_color}{bar_filled}{C.DIM}{bar_empty}{C.RESET}"
          f"  {C.DIM}({remaining} left){C.RESET}")
    print(f"  {C.BOLD}Wrong guesses:{C.RESET}  {wrong_str}")


def render_board(word, guessed, wrong, hint, round_num):
    clear()
    banner()
    divider("═", 54, C.CYAN)
    print(f"  {C.MAGENTA}{C.BOLD}Round {round_num}{C.RESET}"
          f"   {C.DIM}|{C.RESET}"
          f"   {C.CYAN}Hint:{C.RESET} {hint}")
    divider("─", 54, C.DIM)

    hangman_colored(len(wrong))

    divider("─", 54, C.DIM)
    print(f"\n  {C.BOLD}Word:{C.RESET}  {display_word(word, guessed)}")
    print(f"         {C.DIM}({len(word)} letters){C.RESET}\n")
    divider("─", 54, C.DIM)
    display_guesses(wrong)
    divider("═", 54, C.CYAN)


# ─────────────────────────────────────────────
#   G A M E   L O G I C
# ─────────────────────────────────────────────
def play_round(word, hint, round_num, score):
    guessed = set()
    wrong   = set()
    max_wrong = 6

    while True:
        render_board(word, guessed, wrong, hint, round_num)

        # Win check
        if all(l in guessed for l in word):
            print(f"\n  {C.BG_GREEN}{C.BOLD}  🎉  YOU GOT IT!  🎉  {C.RESET}\n")
            slow_print(f"  {C.GREEN}The word was:  {C.BOLD}{word.upper()}{C.RESET}", 0.04)
            bonus = (max_wrong - len(wrong)) * 10
            print(f"  {C.YELLOW}+{bonus} bonus points  {C.DIM}(unused lives × 10){C.RESET}\n")
            time.sleep(1.5)
            return score + 100 + bonus, True

        # Lose check
        if len(wrong) >= max_wrong:
            hangman_colored(6)
            print(f"\n  {C.BG_RED}{C.BOLD}  💀  GAME OVER  💀  {C.RESET}\n")
            slow_print(f"  {C.RED}The word was:  {C.BOLD}{word.upper()}{C.RESET}", 0.04)
            print()
            time.sleep(1.5)
            return score, False

        # Get input
        print(f"\n  {C.CYAN}▶  Guess a letter:{C.RESET} ", end="")
        try:
            guess = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(f"\n\n  {C.YELLOW}Game interrupted. Goodbye!{C.RESET}\n")
            sys.exit()

        # Validate
        if len(guess) != 1 or not guess.isalpha():
            print(f"  {C.YELLOW}⚠  Enter a single letter only.{C.RESET}")
            time.sleep(0.9)
            continue

        if guess in guessed or guess in wrong:
            print(f"  {C.DIM}You already tried  '{guess.upper()}'.{C.RESET}")
            time.sleep(0.9)
            continue

        # Evaluate
        if guess in word:
            guessed.add(guess)
            count = word.count(guess)
            print(f"  {C.GREEN}✔  '{guess.upper()}' is in the word!"
                  f"  ({count}×){C.RESET}")
        else:
            wrong.add(guess)
            remaining = max_wrong - len(wrong)
            if remaining == 1:
                print(f"  {C.RED}✘  '{guess.upper()}' — not there.  "
                      f"{C.BOLD}Last chance!{C.RESET}")
            else:
                print(f"  {C.RED}✘  '{guess.upper()}' — nope.  "
                      f"{C.DIM}{remaining} lives left.{C.RESET}")

        time.sleep(0.8)


def show_score_board(score, wins, rounds):
    clear()
    banner()
    divider("═", 54, C.CYAN)
    print(f"\n  {C.BOLD}{C.MAGENTA}── S C O R E B O A R D ──{C.RESET}\n")
    print(f"  {C.CYAN}Rounds played :{C.RESET}  {rounds}")
    print(f"  {C.GREEN}Words cracked :{C.RESET}  {wins}")
    print(f"  {C.RED}Words missed  :{C.RESET}  {rounds - wins}")
    print(f"  {C.YELLOW}{C.BOLD}Total score   :{C.RESET}  {C.YELLOW}{C.BOLD}{score}{C.RESET}\n")

    if wins == rounds:
        slow_print(f"  {C.LIME}🏆  Perfect run!  You guessed every word!{C.RESET}", 0.03)
    elif wins > rounds // 2:
        slow_print(f"  {C.GREEN}👍  Solid work — more wins than losses!{C.RESET}", 0.03)
    else:
        slow_print(f"  {C.ORANGE}💪  Tough luck — the gallows won this time.{C.RESET}", 0.03)

    divider("═", 54, C.CYAN)
    print()


def intro():
    clear()
    banner()
    divider("═", 54, C.CYAN)
    slow_print(f"\n  {C.CYAN}Welcome to  {C.BOLD}HANGMAN{C.RESET}{C.CYAN}  —"
               f" the classic word-guessing game.{C.RESET}", 0.025)
    print(f"""
  {C.DIM}Rules:{C.RESET}
    •  A secret word is chosen at random.
    •  Guess one letter at a time.
    •  {C.RED}6 wrong guesses{C.RESET} and the man is hanged. 💀
    •  Crack the word before that to score points!

  {C.DIM}Scoring:{C.RESET}
    •  +{C.GREEN}100{C.RESET} pts  per word solved
    •  +{C.YELLOW}10{C.RESET} pts   per unused life (bonus)
""")
    divider("─", 54, C.DIM)
    print(f"  {C.CYAN}How many rounds? {C.DIM}(1 – 5, default 3):{C.RESET} ", end="")
    try:
        raw = input().strip()
        n = int(raw) if raw.isdigit() and 1 <= int(raw) <= 5 else 3
    except (EOFError, KeyboardInterrupt):
        n = 3
    return n


# ─────────────────────────────────────────────
#   M A I N
# ─────────────────────────────────────────────
def main():
    num_rounds = intro()

    word_pool = random.sample(WORDS, min(num_rounds, len(WORDS)))
    score = 0
    wins  = 0

    for i, (word, hint) in enumerate(word_pool, start=1):
        score, won = play_round(word, hint, i, score)
        if won:
            wins += 1

        if i < num_rounds:
            print(f"  {C.DIM}Press Enter for round {i + 1}…{C.RESET}", end="")
            try:
                input()
            except (EOFError, KeyboardInterrupt):
                break

    show_score_board(score, wins, num_rounds)

    print(f"  {C.DIM}Play again? (y / n):{C.RESET} ", end="")
    try:
        again = input().strip().lower()
    except (EOFError, KeyboardInterrupt):
        again = "n"

    if again == "y":
        main()
    else:
        slow_print(f"\n  {C.CYAN}Thanks for playing!  "
                   f"Stay curious. 🧠{C.RESET}\n", 0.03)


if __name__ == "__main__":
    main()
