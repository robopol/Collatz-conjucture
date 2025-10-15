import argparse
import time
import sys
import itertools
from typing import List, Tuple, Iterable, Optional
from decimal import Decimal, getcontext
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText


class _Globals:
    max_permutations: int = 200_000  # per-a cap; <=0 means unlimited


GLOBALS = _Globals()


def t_m_from_a_b(a: int, b: int) -> Tuple[int, int]:
    m = b - a
    t = 2 * a - b
    return t, m


def p_vectors_by_combinations(a: int, t: int, limit: Optional[int] = None) -> Iterable[Tuple[int, ...]]:
    count = 0
    for ones_positions in itertools.combinations(range(a), t):
        p = [2] * a
        for pos in ones_positions:
            p[pos] = 1
        yield tuple(p)
        count += 1
        if limit is not None and count >= limit:
            break


def compute_S_for_p(a: int, p: Tuple[int, ...]) -> int:
    s = 0
    total = 0
    for k in range(1, a + 1):
        total += (3 ** (a - k)) * (2 ** s)
        s += p[k - 1]
    return total


def compute_S_mod_D(a: int, b: int, p: Tuple[int, ...], D: int) -> int:
    s = 0
    total_mod = 0
    for k in range(1, a + 1):
        term = (pow(3, a - k, D) * pow(2, s, D)) % D
        total_mod = (total_mod + term) % D
        s += p[k - 1]
    return total_mod


def theorem_filter_T_less_D(a: int, b: int) -> bool:
    t, m = t_m_from_a_b(a, b)
    if t <= 0:
        return False
    getcontext().prec = 50
    left = (Decimal(3) / Decimal(2)) ** Decimal(t) * (Decimal(1) + (Decimal(3) / Decimal(4)) ** Decimal(m))
    return left < Decimal(2)


def check_D_divides_S(a: int,
                      per_a_deadline: Optional[float] = None,
                      stop_on_first: bool = False) -> List[Tuple[int, Tuple[int, ...], int, int]]:
    import math

    b = int(math.floor(a * math.log(3, 2))) + 1
    D = (2 ** b) - (3 ** a)
    witnesses = []
    if D <= 0:
        return witnesses
    t, m = t_m_from_a_b(a, b)
    # Trivial cases
    if t == 0:
        p = tuple([2] * a)
        S = compute_S_for_p(a, p)
        if S % D == 0:
            witnesses.append((a, p, D, S))
        return witnesses
    if t == 1:
        return witnesses  # excluded by theory
    # Strong filter: T < D ⇒ no witness
    if theorem_filter_T_less_D(a, b):
        return witnesses
    # Enumerate combinations with an upper bound on complexity
    max_perms = GLOBALS.max_permutations
    limit_value: Optional[int] = None if (isinstance(max_perms, int) and max_perms <= 0) else max_perms
    checked = 0
    for p in p_vectors_by_combinations(a, t, limit=limit_value):
        if per_a_deadline is not None and time.perf_counter() > per_a_deadline:
            print(f"[TIMEOUT] a={a}: reached per-a time limit after {checked} combinations", flush=True)
            break
        if compute_S_mod_D(a, b, p, D) == 0:
            S = compute_S_for_p(a, p)
            if S % D == 0:
                witnesses.append((a, p, D, S))
                if stop_on_first:
                    break
        checked += 1
    return witnesses


def run_range(a_min: int, a_max: int,
              total_deadline: Optional[float] = None,
              per_a_seconds: Optional[float] = None,
              stop_on_first: bool = False) -> None:
    any_found = False
    for a in range(a_min, a_max + 1):
        if total_deadline is not None and time.perf_counter() > total_deadline:
            print("[TIMEOUT] total time limit reached", flush=True)
            break
        per_a_deadline = None
        if per_a_seconds is not None and per_a_seconds > 0:
            per_a_deadline = time.perf_counter() + per_a_seconds
        w = check_D_divides_S(a, per_a_deadline=per_a_deadline, stop_on_first=stop_on_first)
        if w:
            any_found = True
            print(f"[FOUND] a={a} witnesses:")
            for (aa, p, D, S) in w:
                print(f"  a={aa}, b={sum(p)}, p={p}, D={D}, S={S}, n=S/D={S//D}")
        else:
            print(f"[OK] a={a}: no p in {{1,2}} yields D|S (filters+enumeration up to {GLOBALS.max_permutations} cases)")
    if not any_found:
        print("No witnesses found in range.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Final check D|S(σ) for p∈{1,2}")
    parser.add_argument("--a-min", type=int, default=1)
    parser.add_argument("--a-max", type=int, default=60)
    parser.add_argument("--max-permutations", type=int, default=200000, help="cap on enumerated p-vectors per a (0=unlimited)")
    parser.add_argument("--total-seconds", type=float, default=0.0, help="global time limit in seconds (0 = no limit)")
    parser.add_argument("--per-a-seconds", type=float, default=0.0, help="per-a time limit in seconds (0 = no limit)")
    parser.add_argument("--stop-on-first", action="store_true", help="stop on first witness per a")
    parser.add_argument("--gui", action="store_true", help="launch Tkinter GUI")
    args = parser.parse_args()

    GLOBALS.max_permutations = args.max_permutations

    # Launch GUI by default when no flags are provided, or when --gui is passed
    launch_gui = args.gui or (len(sys.argv) == 1)
    if launch_gui:
        # Build and run GUI
        def build_gui():
            root = tk.Tk()
            root.title("Collatz D|S Checker (p∈{1,2})")

            style = ttk.Style()
            try:
                style.theme_use('clam')
            except Exception:
                pass
            style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'))
            style.configure('Caption.TLabel', font=('Segoe UI', 9), foreground='#555555')
            style.configure('Run.TButton', font=('Segoe UI', 11, 'bold'))
            style.configure('Card.TLabelframe', padding=10)
            style.configure('Card.TLabelframe.Label', font=('Segoe UI', 11, 'bold'))

            menubar = tk.Menu(root)
            def on_about():
                messagebox.showinfo(
                    "About",
                    "Collatz D|S(σ) Checker\n\n"
                    "Enumerates p-vectors in {1,2} for fixed a with b=⌊a log₂3⌋+1\n"
                    "and checks D|S(σ). Uses strong filters and fast modular arithmetic."
                )
            file_menu = tk.Menu(menubar, tearoff=0)
            file_menu.add_command(label="Exit", command=root.destroy)
            help_menu = tk.Menu(menubar, tearoff=0)
            help_menu.add_command(label="About", command=on_about)
            menubar.add_cascade(label="File", menu=file_menu)
            menubar.add_cascade(label="Help", menu=help_menu)
            root.config(menu=menubar)

            container = ttk.Frame(root, padding=12)
            container.grid(row=0, column=0, sticky="nsew")
            root.columnconfigure(0, weight=1)
            root.rowconfigure(0, weight=1)

            ttk.Label(container, text="Final check D|S(σ) for p∈{1,2}", style='Header.TLabel').grid(row=0, column=0, sticky='w')
            ttk.Label(container, text="Choose the range for a (number of U-steps), limits and options.\n"
                                       "The tool enumerates p∈{1,2} with sum b=⌊a·log₂3⌋+1 and tests D∣S(σ).",
                      style='Caption.TLabel', justify='left').grid(row=1, column=0, sticky='w', pady=(2,8))

            cards = ttk.Frame(container)
            cards.grid(row=2, column=0, sticky='nsew')
            container.rowconfigure(2, weight=0)
            container.columnconfigure(0, weight=1)

            params = ttk.Labelframe(cards, text="Parameters", style='Card.TLabelframe')
            limits = ttk.Labelframe(cards, text="Limits & Options", style='Card.TLabelframe')
            params.grid(row=0, column=0, sticky='nsew', padx=(0,8))
            limits.grid(row=0, column=1, sticky='nsew')
            cards.columnconfigure(0, weight=1)
            cards.columnconfigure(1, weight=1)

            a_min_var = tk.IntVar(value=1)
            a_max_var = tk.IntVar(value=60)
            ttk.Label(params, text="a_min:").grid(row=0, column=0, sticky='w')
            ttk.Entry(params, textvariable=a_min_var, width=10).grid(row=0, column=1, sticky='w')
            ttk.Label(params, text="a_max:").grid(row=0, column=2, sticky='w', padx=(10,0))
            ttk.Entry(params, textvariable=a_max_var, width=10).grid(row=0, column=3, sticky='w')
            ttk.Label(params, text="(a is the number of U-steps; for each a we use b=⌊a·log₂3⌋+1)",
                      style='Caption.TLabel').grid(row=1, column=0, columnspan=4, sticky='w', pady=(4,0))

            max_perm_var = tk.IntVar(value=200000)
            total_sec_var = tk.DoubleVar(value=0.0)
            per_a_sec_var = tk.DoubleVar(value=0.0)
            stop_on_first_var = tk.BooleanVar(value=False)

            ttk.Label(limits, text="max_permutations:").grid(row=0, column=0, sticky='w')
            ttk.Entry(limits, textvariable=max_perm_var, width=12).grid(row=0, column=1, sticky='w')
            ttk.Label(limits, text="0 = unlimited", style='Caption.TLabel').grid(row=0, column=2, sticky='w')

            ttk.Label(limits, text="total_seconds:").grid(row=1, column=0, sticky='w', pady=(4,0))
            ttk.Entry(limits, textvariable=total_sec_var, width=12).grid(row=1, column=1, sticky='w', pady=(4,0))
            ttk.Label(limits, text="global time limit (0 = none)", style='Caption.TLabel').grid(row=1, column=2, sticky='w', pady=(4,0))

            ttk.Label(limits, text="per_a_seconds:").grid(row=2, column=0, sticky='w', pady=(4,0))
            ttk.Entry(limits, textvariable=per_a_sec_var, width=12).grid(row=2, column=1, sticky='w', pady=(4,0))
            ttk.Label(limits, text="per-a time limit (0 = none)", style='Caption.TLabel').grid(row=2, column=2, sticky='w', pady=(4,0))

            ttk.Checkbutton(limits, text="stop_on_first (stop after first witness per a)",
                            variable=stop_on_first_var).grid(row=3, column=0, columnspan=3, sticky='w', pady=(6,0))

            out_card = ttk.Labelframe(container, text="Output", style='Card.TLabelframe')
            out_card.grid(row=3, column=0, sticky='nsew', pady=(10,0))
            container.rowconfigure(3, weight=1)

            out = ScrolledText(out_card, width=110, height=24, state=tk.DISABLED)
            out.grid(row=0, column=0, sticky='nsew')
            out_card.rowconfigure(0, weight=1)
            out_card.columnconfigure(0, weight=1)

            class Runner:
                def __init__(self, output_widget: ScrolledText):
                    self.output = output_widget

                def write(self, text: str):
                    self.output.configure(state=tk.NORMAL)
                    self.output.insert(tk.END, text + "\n")
                    self.output.see(tk.END)
                    self.output.configure(state=tk.DISABLED)

                def run(self,
                        a_min: int, a_max: int,
                        max_perms: int, total_seconds: float,
                        per_a_seconds: float, stop_on_first: bool):
                    GLOBALS.max_permutations = max_perms
                    import builtins
                    real_print = builtins.print
                    def patched_print(*args, **kwargs):
                        line = " ".join(str(x) for x in args)
                        self.write(line)
                    builtins.print = patched_print
                    try:
                        total_deadline = None
                        if total_seconds and total_seconds > 0:
                            total_deadline = time.perf_counter() + total_seconds
                        run_range(a_min, a_max,
                                  total_deadline=total_deadline,
                                  per_a_seconds=(per_a_seconds if per_a_seconds > 0 else None),
                                  stop_on_first=stop_on_first)
                    finally:
                        builtins.print = real_print

            runner = Runner(out)

            def on_run():
                try:
                    a_min = int(a_min_var.get())
                    a_max = int(a_max_var.get())
                    max_perm = int(max_perm_var.get())
                    total_sec = float(total_sec_var.get())
                    per_a_sec = float(per_a_sec_var.get())
                except Exception as e:
                    messagebox.showerror("Input error", f"Invalid inputs: {e}")
                    return
                if a_min < 1 or a_max < a_min:
                    messagebox.showerror("Input error", "Require: a_min ≥ 1 and a_max ≥ a_min.")
                    return
                btn_run.configure(state=tk.DISABLED)
                def worker():
                    try:
                        runner.run(a_min, a_max, max_perm, total_sec, per_a_sec, stop_on_first_var.get())
                    finally:
                        btn_run.configure(state=tk.NORMAL)
                import threading
                threading.Thread(target=worker, daemon=True).start()

            btn_run = ttk.Button(container, text="Run check", style='Run.TButton', command=on_run)
            btn_run.grid(row=4, column=0, sticky='e', pady=(8,0))

            root.minsize(980, 660)
            return root

        app = build_gui()
        app.mainloop()
    else:
        total_deadline = None
        if args.total_seconds and args.total_seconds > 0:
            total_deadline = time.perf_counter() + args.total_seconds
        try:
            run_range(args.a_min, args.a_max,
                      total_deadline=total_deadline,
                      per_a_seconds=(args.per_a_seconds if args.per_a_seconds > 0 else None),
                      stop_on_first=args.stop_on_first)
        except KeyboardInterrupt:
            print("\n[ABORTED] Interrupted by user.", file=sys.stderr, flush=True)
            sys.exit(130)