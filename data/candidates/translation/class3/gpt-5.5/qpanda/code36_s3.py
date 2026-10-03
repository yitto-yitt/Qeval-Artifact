# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import *

def bv_function(s):
    n = len(s)
    circuit_cls = globals().get("QCircuit", globals().get("Circuit", None))
    gate_factory = globals().get("CNOT", globals().get("CX", None))

    def _append(circuit, gate):
        try:
            result = circuit << gate
            return circuit if result is None or isinstance(result, bool) else result
        except Exception:
            if hasattr(circuit, "insert"):
                result = circuit.insert(gate)
                return circuit if result is None or isinstance(result, bool) else result
            if hasattr(circuit, "append"):
                result = circuit.append(gate)
                return circuit if result is None or isinstance(result, bool) else result
            raise

    last_error = None

    if circuit_cls is not None and gate_factory is not None:
        for ctor_args in ((n + 1,), ()):
            try:
                qc = circuit_cls(*ctor_args)
                for index, bit in enumerate(reversed(s)):
                    if bit == "1":
                        qc = _append(qc, gate_factory(index, n))
                return qc
            except Exception as exc:
                last_error = exc

    qvm_cls = globals().get("CPUQVM", None)
    if qvm_cls is None or circuit_cls is None or gate_factory is None:
        if last_error is not None:
            raise last_error
        raise RuntimeError("Required pyQPanda3 circuit or gate API is unavailable")

    qvm = qvm_cls()
    for init_name in ("init_qvm", "init", "initQVM"):
        if hasattr(qvm, init_name):
            getattr(qvm, init_name)()
            break

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(n + 1)
    elif hasattr(qvm, "qalloc_many"):
        qubits = qvm.qalloc_many(n + 1)
    elif hasattr(qvm, "qAllocMany"):
        qubits = qvm.qAllocMany(n + 1)
    elif hasattr(qvm, "qAlloc"):
        qubits = [qvm.qAlloc() for _ in range(n + 1)]
    elif hasattr(qvm, "qalloc"):
        qubits = [qvm.qalloc() for _ in range(n + 1)]
    else:
        if last_error is not None:
            raise last_error
        raise RuntimeError("Required pyQPanda3 qubit allocation API is unavailable")

    if not hasattr(bv_function, "_qvms"):
        bv_function._qvms = []
    bv_function._qvms.append(qvm)

    qc = circuit_cls()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc = _append(qc, gate_factory(qubits[index], qubits[n]))
    return qc
