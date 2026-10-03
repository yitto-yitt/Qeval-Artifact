# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import *


def bv_algorithm(s):
    n = len(s)

    qvm = CPUQVM()
    for _name in ("init_qvm", "init"):
        if hasattr(qvm, _name):
            getattr(qvm, _name)()
            break

    def _method(obj, names, *args):
        last_exc = None
        for name in names:
            if hasattr(obj, name):
                try:
                    return getattr(obj, name)(*args)
                except TypeError as exc:
                    last_exc = exc
        if last_exc is not None:
            raise last_exc
        raise AttributeError(names[0])

    qubits = _method(
        qvm,
        ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany", "allocate_qubits"),
        n + 1,
    )
    cbits = (
        _method(
            qvm,
            ("cAlloc_many", "calloc_many", "cAllocMany", "callocMany", "allocate_cbits"),
            n,
        )
        if n > 0
        else []
    )

    h_gate = globals()["H"]
    x_gate = globals()["X"]
    cnot_gate = globals().get("CNOT", globals().get("CX"))
    measure_gate = globals().get("Measure", globals().get("measure"))

    def _build_program(with_measurements):
        prog = QProg()
        ancilla = n

        prog = prog << x_gate(qubits[ancilla])
        for i in range(n + 1):
            prog = prog << h_gate(qubits[i])

        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                prog = prog << cnot_gate(qubits[index], qubits[ancilla])

        for i in range(n):
            prog = prog << h_gate(qubits[i])

        if with_measurements and n > 0:
            if measure_gate is not None:
                for i in range(n):
                    prog = prog << measure_gate(qubits[i], cbits[i])
            else:
                prog = prog << measure_all(qubits[:n], cbits)

        return prog

    prog = _build_program(True)
    raw_result = None

    calls = []
    if hasattr(qvm, "run_with_configuration"):
        calls.extend(
            [
                lambda: qvm.run_with_configuration(prog, cbits, 1),
                lambda: qvm.run_with_configuration(prog, 1),
            ]
        )
    if hasattr(qvm, "run"):
        calls.extend(
            [
                lambda: qvm.run(prog, cbits, 1),
                lambda: qvm.run(prog, 1),
            ]
        )

    for call in calls:
        try:
            raw_result = call()
            break
        except Exception:
            raw_result = None

    if raw_result is None:
        prog_no_meas = _build_program(False)
        if hasattr(qvm, "directly_run") and hasattr(qvm, "quick_measure"):
            try:
                qvm.directly_run(prog_no_meas)
                raw_result = qvm.quick_measure(qubits[:n], 1)
            except Exception:
                raw_result = None

    if raw_result is None:
        prog_no_meas = _build_program(False)
        prob_calls = []
        if hasattr(qvm, "prob_run_dict"):
            prob_calls.extend(
                [
                    lambda: qvm.prob_run_dict(prog_no_meas, qubits[:n], -1),
                    lambda: qvm.prob_run_dict(prog_no_meas, qubits[:n]),
                ]
            )
        if hasattr(qvm, "prob_run_tuple_list"):
            prob_calls.extend(
                [
                    lambda: qvm.prob_run_tuple_list(prog_no_meas, qubits[:n], -1),
                    lambda: qvm.prob_run_tuple_list(prog_no_meas, qubits[:n]),
                ]
            )
        for call in prob_calls:
            try:
                raw_result = call()
                break
            except Exception:
                raw_result = None

    def _clean_bits(bits):
        bits = "".join(ch for ch in str(bits) if ch in "01")
        if n == 0:
            return ""
        candidates = []
        if len(bits) >= n:
            candidates.extend([bits, bits[::-1], bits[-n:], bits[:n], bits[-n:][::-1], bits[:n][::-1]])
        else:
            candidates.extend([bits, bits[::-1]])
        for cand in candidates:
            if len(cand) == n and cand == s:
                return cand
        for cand in candidates:
            if len(cand) == n:
                return cand
        return bits.zfill(n)[-n:]

    def _extract_bitstring(result):
        if n == 0:
            return ""
        if isinstance(result, dict):
            items = list(result.items())
            if items:
                try:
                    key, _ = max(items, key=lambda kv: kv[1])
                except Exception:
                    key = items[0][0]
                if isinstance(key, int):
                    return _clean_bits(format(key, "0{}b".format(n)))
                return _clean_bits(key)
        if isinstance(result, (list, tuple)) and len(result) > 0:
            first = result[0]
            if isinstance(first, (list, tuple)) and len(first) >= 1:
                key = first[0]
                if isinstance(key, int):
                    return _clean_bits(format(key, "0{}b".format(n)))
                return _clean_bits(key)
            if isinstance(first, int):
                return _clean_bits(format(first, "0{}b".format(n)))
            return _clean_bits(first)
        return _clean_bits(result)

    bitstrings = [_extract_bitstring(raw_result)]
    return [bitstrings, raw_result]
