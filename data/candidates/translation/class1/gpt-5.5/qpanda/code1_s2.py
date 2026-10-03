# EVAL_META: task_id=1, framework=qpanda, class=1
import pyqpanda3.core as pq

def run_bell_state_simulator():
    shots = 1000

    def get_attr(names):
        for name in names:
            if hasattr(pq, name):
                return getattr(pq, name)
        raise AttributeError(names[0])

    def call_first(obj, names, *args):
        for name in names:
            if hasattr(obj, name):
                return getattr(obj, name)(*args)
        raise AttributeError(names[0])

    def normalize_result(result, nbits=2):
        if hasattr(result, "items"):
            items = list(result.items())
        else:
            items = list(dict(result).items())

        data = {}
        for key, value in items:
            if isinstance(key, str):
                bitstring = "".join(ch for ch in key if ch in "01")
                if not bitstring:
                    bitstring = key
            elif isinstance(key, int):
                bitstring = format(key, "0{}b".format(nbits))
            elif isinstance(key, (list, tuple)):
                bitstring = "".join(str(int(x)) for x in key)
            else:
                bitstring = str(key)

            val = float(value)
            if val != 0.0:
                data[bitstring] = data.get(bitstring, 0.0) + val

        total = sum(data.values())
        return {key: value / total for key, value in data.items()} if total else {}

    CPUQVM = get_attr(["CPUQVM"])
    QProg = get_attr(["QProg"])
    H = get_attr(["H"])
    CNOT = get_attr(["CNOT", "CX"])
    Measure = get_attr(["Measure"])

    qvm = CPUQVM()
    try:
        for init_name in ("init_qvm", "initQVM", "init"):
            if hasattr(qvm, init_name):
                getattr(qvm, init_name)()
                break

        qubits = call_first(qvm, ["qAlloc_many", "qalloc_many", "qAllocMany"], 2)
        cbits = call_first(qvm, ["cAlloc_many", "calloc_many", "cAllocMany"], 2)

        def build_program(with_measurements):
            prog = QProg()
            prog << H(qubits[0])
            prog << CNOT(qubits[0], qubits[1])
            if with_measurements:
                prog << Measure(qubits[0], cbits[0])
                prog << Measure(qubits[1], cbits[1])
            return prog

        measured_prog = build_program(True)
        result = None

        for run_name in ("run_with_configuration", "runWithConfiguration", "run_with_config"):
            if hasattr(qvm, run_name):
                run_method = getattr(qvm, run_name)
                for args in ((measured_prog, cbits, shots), (measured_prog, shots, cbits)):
                    try:
                        result = run_method(*args)
                        break
                    except TypeError:
                        continue
                if result is not None:
                    break

        if result is None:
            bare_prog = build_program(False)
            for prob_name in ("prob_run_dict", "probRunDict", "prob_run_tuple_list"):
                if hasattr(qvm, prob_name):
                    prob_method = getattr(qvm, prob_name)
                    for args in ((bare_prog, qubits, -1), (bare_prog, qubits), (bare_prog, qubits, shots)):
                        try:
                            result = prob_method(*args)
                            break
                        except TypeError:
                            continue
                    if result is not None:
                        break

        return normalize_result(result, 2)
    finally:
        for fini_name in ("finalize", "finalize_qvm", "finalizeQVM"):
            if hasattr(qvm, fini_name):
                try:
                    getattr(qvm, fini_name)()
                except TypeError:
                    pass
                break
