# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import *
import pyqpanda3.core as pq


def random_coin_flip(samples):
    shots = int(samples)

    if hasattr(pq, "CPUQVM"):
        qvm = pq.CPUQVM()
    elif hasattr(pq, "init_quantum_machine"):
        qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    else:
        raise RuntimeError("No compatible pyQPanda3 quantum machine found")

    for init_name in ("init_qvm", "init", "initQVM"):
        if hasattr(qvm, init_name):
            try:
                getattr(qvm, init_name)()
            except TypeError:
                pass
            break

    try:
        if hasattr(qvm, "qAlloc_many"):
            qubits = qvm.qAlloc_many(1)
        elif hasattr(qvm, "qalloc_many"):
            qubits = qvm.qalloc_many(1)
        elif hasattr(qvm, "qAlloc"):
            qubits = [qvm.qAlloc()]
        else:
            raise RuntimeError("No compatible qubit allocation method found")

        if hasattr(qvm, "cAlloc_many"):
            cbits = qvm.cAlloc_many(1)
        elif hasattr(qvm, "calloc_many"):
            cbits = qvm.calloc_many(1)
        elif hasattr(qvm, "cAlloc"):
            cbits = [qvm.cAlloc()]
        else:
            raise RuntimeError("No compatible classical bit allocation method found")

        q0 = qubits[0]
        c0 = cbits[0]

        prog = pq.QProg()

        def append_op(op):
            nonlocal prog
            try:
                new_prog = prog << op
                if new_prog is not None:
                    prog = new_prog
                return
            except Exception:
                pass
            if hasattr(prog, "insert"):
                new_prog = prog.insert(op)
                if new_prog is not None:
                    prog = new_prog
                return
            raise RuntimeError("No compatible program append method found")

        append_op(pq.H(q0))

        measured = False
        for meas_name in ("Measure", "measure", "M"):
            if hasattr(pq, meas_name):
                try:
                    append_op(getattr(pq, meas_name)(q0, c0))
                    measured = True
                    break
                except Exception:
                    pass

        if not measured:
            for meas_all_name in ("measure_all", "MeasureAll"):
                if hasattr(pq, meas_all_name):
                    try:
                        append_op(getattr(pq, meas_all_name)(qubits, cbits))
                        measured = True
                        break
                    except Exception:
                        pass

        if not measured:
            raise RuntimeError("No compatible measurement method found")

        result = None
        run_errors = []

        if hasattr(qvm, "run_with_configuration"):
            for args in ((prog, cbits, shots), (prog, [c0], shots), (prog, shots, cbits), (prog, shots, [c0])):
                try:
                    result = qvm.run_with_configuration(*args)
                    break
                except Exception as exc:
                    run_errors.append(exc)

        if result is None and hasattr(qvm, "run"):
            for args in ((prog, cbits, shots), (prog, shots), (prog, shots, cbits)):
                try:
                    result = qvm.run(*args)
                    break
                except Exception as exc:
                    run_errors.append(exc)

        if result is None:
            raise run_errors[-1] if run_errors else RuntimeError("No compatible run method found")

        if hasattr(result, "get_counts"):
            counts = result.get_counts()
        elif hasattr(result, "to_dict"):
            counts = result.to_dict()
        else:
            counts = dict(result)

        heads = 0.0
        tails = 0.0

        for key, value in counts.items():
            val = float(value)
            if isinstance(key, bool):
                bit = "1" if key else "0"
            elif isinstance(key, int):
                bit = str(key & 1)
            else:
                s = str(key).strip().lower()
                if s in ("false", "f"):
                    bit = "0"
                elif s in ("true", "t"):
                    bit = "1"
                else:
                    bits = "".join(ch for ch in s if ch in "01")
                    bit = bits[-1] if bits else s[-1]
            if bit == "0":
                heads += val
            elif bit == "1":
                tails += val

        total = heads + tails
        return {"Heads": heads / total, "Tails": tails / total}

    finally:
        for fin_name in ("finalize", "finalize_qvm", "destroy"):
            if hasattr(qvm, fin_name):
                try:
                    getattr(qvm, fin_name)()
                except Exception:
                    pass
                break
