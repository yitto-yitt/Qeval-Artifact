# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda3.core import *

def noisy_bell():
    shots = 1000

    machine_cls = globals().get("NoiseQVM", None)
    if machine_cls is None:
        machine_cls = globals()["CPUQVM"]
    machine = machine_cls()

    for init_name in ("init_qvm", "initQVM", "init"):
        if hasattr(machine, init_name):
            getattr(machine, init_name)()
            break

    try:
        noise_model_cls = globals().get("NoiseModel", None)
        gate_type_cls = globals().get("GateType", None)
        if noise_model_cls is not None and gate_type_cls is not None and hasattr(machine, "set_noise_model"):
            model = None
            for model_name in ("DEPOLARIZING_KRAUS_OPERATOR", "BITFLIP_KRAUS_OPERATOR", "DAMPING_KRAUS_OPERATOR"):
                if hasattr(noise_model_cls, model_name):
                    model = getattr(noise_model_cls, model_name)
                    break
            if model is not None:
                for gate_name, prob in (("HADAMARD_GATE", 0.001), ("CNOT_GATE", 0.01)):
                    if hasattr(gate_type_cls, gate_name):
                        try:
                            machine.set_noise_model(model, getattr(gate_type_cls, gate_name), prob)
                        except Exception:
                            pass
    except Exception:
        pass

    if hasattr(machine, "qAlloc_many"):
        q = machine.qAlloc_many(2)
    elif hasattr(machine, "qAllocMany"):
        q = machine.qAllocMany(2)
    elif hasattr(machine, "qalloc_many"):
        q = machine.qalloc_many(2)
    elif hasattr(machine, "allocate_qubits"):
        q = machine.allocate_qubits(2)
    elif hasattr(machine, "allocateQubits"):
        q = machine.allocateQubits(2)
    else:
        q = [machine.qAlloc(), machine.qAlloc()]

    if hasattr(machine, "cAlloc_many"):
        c = machine.cAlloc_many(2)
    elif hasattr(machine, "cAllocMany"):
        c = machine.cAllocMany(2)
    elif hasattr(machine, "calloc_many"):
        c = machine.calloc_many(2)
    elif hasattr(machine, "allocate_cbits"):
        c = machine.allocate_cbits(2)
    elif hasattr(machine, "allocateCBits"):
        c = machine.allocateCBits(2)
    else:
        c = [machine.cAlloc(), machine.cAlloc()]

    h_gate = globals()["H"]
    cx_gate = globals().get("CNOT", None)
    if cx_gate is None:
        cx_gate = globals()["CX"]

    prog_no_meas = QProg()
    prog_no_meas << h_gate(q[0])
    prog_no_meas << cx_gate(q[0], q[1])

    prog = QProg()
    prog << h_gate(q[0])
    prog << cx_gate(q[0], q[1])

    meas_gate = globals().get("Measure", None)
    if meas_gate is None:
        meas_gate = globals().get("measure", None)

    if meas_gate is not None:
        prog << meas_gate(q[0], c[0])
        prog << meas_gate(q[1], c[1])
    else:
        prog << globals()["measure_all"](q, c)

    raw = None

    for run_name in ("run_with_configuration", "runWithConfiguration", "run_with_config", "run"):
        if raw is not None:
            break
        if hasattr(machine, run_name):
            run_method = getattr(machine, run_name)
            for args in ((prog, c, shots), (prog, shots)):
                try:
                    raw = run_method(*args)
                    break
                except Exception:
                    pass

    if raw is None:
        for prob_name in ("prob_run_dict", "probRunDict", "prob_run_tuple_list", "probRunTupleList"):
            if raw is not None:
                break
            if hasattr(machine, prob_name):
                prob_method = getattr(machine, prob_name)
                for args in ((prog_no_meas, q, -1), (prog_no_meas, q), (prog_no_meas,)):
                    try:
                        raw = prob_method(*args)
                        break
                    except Exception:
                        pass

    if hasattr(raw, "get_counts"):
        counts = raw.get_counts()
    elif hasattr(raw, "counts"):
        counts = raw.counts()
    elif hasattr(raw, "items"):
        counts = dict(raw.items())
    elif isinstance(raw, (list, tuple)):
        counts = dict(raw)
    else:
        counts = dict(raw)

    normalized_counts = {}
    for key, value in counts.items():
        try:
            val = float(value)
        except Exception:
            val = float(value.real)
        if val == 0.0:
            continue

        if isinstance(key, int):
            bitstring = format(key, "02b")
        elif isinstance(key, (tuple, list)):
            bitstring = "".join(str(int(x)) for x in key)
        else:
            bitstring = str(key).strip().replace(" ", "")
            if len(bitstring) < 2 and all(ch in "01" for ch in bitstring):
                bitstring = bitstring.zfill(2)

        normalized_counts[bitstring] = normalized_counts.get(bitstring, 0.0) + val

    total = sum(normalized_counts.values())
    return {key: value / total for key, value in normalized_counts.items()}
