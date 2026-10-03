# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import *


def bv_algorithm(s):
    def _new_machine():
        machine = CPUQVM()
        for name in ("init_qvm", "init", "initialize"):
            if hasattr(machine, name):
                try:
                    getattr(machine, name)()
                    break
                except TypeError:
                    continue
        return machine

    def _alloc_qubits(machine, num):
        for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
            if hasattr(machine, name):
                return [getattr(machine, name)(num)[i] for i in range(num)]
        raise RuntimeError("No qubit allocation method found")

    def _alloc_cbits(machine, num):
        if num == 0:
            return []
        for name in ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany"):
            if hasattr(machine, name):
                return [getattr(machine, name)(num)[i] for i in range(num)]
        raise RuntimeError("No classical bit allocation method found")

    def _gate(names, *args):
        for name in names:
            obj = globals().get(name)
            if obj is not None:
                return obj(*args)
        raise RuntimeError("Required gate not found")

    def _append(program, op):
        try:
            new_program = program.__lshift__(op)
            return program if new_program is None else new_program
        except Exception:
            if hasattr(program, "insert"):
                program.insert(op)
                return program
            if hasattr(program, "append"):
                program.append(op)
                return program
            raise

    def _run(machine, program, cbits, shots):
        for name in ("run_with_configuration", "run_with_config"):
            if hasattr(machine, name):
                return getattr(machine, name)(program, cbits, shots)
        if hasattr(machine, "run"):
            try:
                return machine.run(program, cbits, shots)
            except TypeError:
                return machine.run(program, shots)
        if hasattr(machine, "directly_run"):
            return machine.directly_run(program)
        raise RuntimeError("No execution method found")

    def _counts(result):
        if isinstance(result, dict):
            return result
        if hasattr(result, "get_counts"):
            return result.get_counts()
        if hasattr(result, "items"):
            return dict(result.items())
        return None

    def _bits_from_key(key, width):
        bits = "".join(ch for ch in str(key) if ch in "01")
        if width == 0:
            return ""
        if len(bits) > width:
            bits = bits[-width:]
        return bits.zfill(width)

    def _detect_direct_order():
        try:
            cm = _new_machine()
            cq = _alloc_qubits(cm, 2)
            cc = _alloc_cbits(cm, 2)
            cp = QProg()
            cp = _append(cp, _gate(("X",), cq[0]))
            cp = _append(cp, _gate(("Measure", "measure"), cq[0], cc[0]))
            cp = _append(cp, _gate(("Measure", "measure"), cq[1], cc[1]))
            cres = _run(cm, cp, [cc[1], cc[0]], 1)
            ccounts = _counts(cres)
            if ccounts:
                key = max(ccounts, key=ccounts.get)
                bits = _bits_from_key(key, 2)
                if bits == "01":
                    return True
                if bits == "10":
                    return False
        except Exception:
            pass
        return True

    n = len(s)
    machine = _new_machine()
    q = _alloc_qubits(machine, n + 1)
    c = _alloc_cbits(machine, n)

    prog = QProg()
    ancilla = n

    prog = _append(prog, _gate(("X",), q[ancilla]))
    for qb in q:
        prog = _append(prog, _gate(("H",), qb))

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog = _append(prog, _gate(("CNOT", "CX"), q[index], q[ancilla]))

    for i in range(n):
        prog = _append(prog, _gate(("H",), q[i]))

    for i in range(n):
        prog = _append(prog, _gate(("Measure", "measure"), q[i], c[i]))

    run_cbits = list(reversed(c))
    result = _run(machine, prog, run_cbits, 1)

    if n == 0:
        return [[""], result]

    direct_order = _detect_direct_order()
    need_reverse = not direct_order

    bitstrings = []
    counts = _counts(result)
    if counts:
        for key, value in counts.items():
            try:
                shots = int(round(float(value)))
            except Exception:
                shots = 1
            if shots <= 0:
                continue
            bits = _bits_from_key(key, n)
            if need_reverse:
                bits = bits[::-1]
            bitstrings.extend([bits] * shots)
    elif isinstance(result, (list, tuple)):
        for item in result:
            bits = _bits_from_key(item, n)
            if need_reverse:
                bits = bits[::-1]
            bitstrings.append(bits)

    return [bitstrings, result]
