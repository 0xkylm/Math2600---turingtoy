from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

import poetry_version

__version__ = poetry_version.extract(source_file=__file__)


def run_turing_machine(
    machine: Dict,
    input_: str,
    steps: Optional[int] = None,
) -> Tuple[str, List, bool]:
    state = machine["start state"]
    trans_table = machine["table"]
    blank = machine["blank"]
    mem = []
    pos = 0
    step_cp = 0
    tape = list(input_)
    while steps is None or step_cp < steps:
        if pos < 0:
            tape.insert(0, blank)
            pos = 0
        elif pos >= len(tape):
            tape.append(blank)

        symb = tape[pos]
        state_tr = trans_table.get(state, {})
        if symb not in state_tr:
            #  print(
            #      f"First return State {"".join(tape).strip(blank)}, symbol {symb}, mem {mem}"
            #  )
            return "".join(tape).strip(blank), mem, True
        tr = state_tr[symb]
        mem.append(
            {
                "state": state,
                "symbole": symb,
                "mem": "".join(tape),
                "tr": tr,
                "pos": pos,
            }
        )

        if isinstance(tr, str):
            if tr == "R":
                pos += 1
            elif tr == "L":
                pos -= 1
            else:
                #  print(
                #      f"Second return State {"".join(tape).strip(blank)}, symbol {symb}, mem {mem} tr = {tr}"
                #  )
                return "".join(tape).strip(blank), mem, False
        else:
            if "write" in tr:
                tape[pos] = tr["write"]

            if "R" in tr:
                pos += 1
                state = tr["R"]
            if "L" in tr:
                pos -= 1
                state = tr["L"]
        step_cp += 1
    #    print(f"Last State {state}, symbol {symb}, mem {mem}")
    #    print(f"To return {"".join(tape).strip(blank)}")
    return "".join(tape).strip(blank), mem, True
