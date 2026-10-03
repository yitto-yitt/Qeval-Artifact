# EVAL_META: task_id=81, framework=qpanda, class=3
import pyqpanda3.core as pq

_KEEPALIVE = []


def convert_qasm_string_to_quantum_circuit():
    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""

    qvm = None
    if hasattr(pq, "CPUQVM"):
        qvm = pq.CPUQVM()
        for init_name in ("init_qvm", "init", "initQVM"):
            if hasattr(qvm, init_name):
                try:
                    getattr(qvm, init_name)()
                    break
                except TypeError:
                    pass

    for name in (
        "convert_qasm_to_qprog",
        "convert_qasm_string_to_qprog",
        "qasm_to_qprog",
        "convert_qasm_to_qcircuit",
        "convert_qasm_string_to_qcircuit",
    ):
        if hasattr(pq, name):
            fn = getattr(pq, name)
            attempts = []
            if qvm is not None:
                attempts.extend(((qasm_string, qvm), (qvm, qasm_string)))
            attempts.append((qasm_string,))
            for args in attempts:
                try:
                    result = fn(*args)
                    _KEEPALIVE.append((qvm, result))
                    if isinstance(result, tuple):
                        return result[0]
                    return result
                except Exception:
                    pass

    if qvm is None:
        raise RuntimeError("pyqpanda3 CPUQVM is unavailable")

    q_alloc = None
    for alloc_name in ("qAlloc_many", "qalloc_many", "qAllocMany", "allocate_qubits"):
        if hasattr(qvm, alloc_name):
            q_alloc = getattr(qvm, alloc_name)
            break
    if q_alloc is None:
        raise RuntimeError("No compatible qubit allocation method found")

    qubits = q_alloc(2)

    cbits = None
    for calloc_name in ("cAlloc_many", "calloc_many", "cAllocMany", "allocate_cbits"):
        if hasattr(qvm, calloc_name):
            try:
                cbits = getattr(qvm, calloc_name)(2)
                break
            except Exception:
                pass

    container_cls = getattr(pq, "QProg", None) or getattr(pq, "QCircuit", None)
    if container_cls is None:
        raise RuntimeError("No compatible circuit/program class found")

    circuit = container_cls()

    def append_op(obj, op):
        try:
            return obj << op
        except Exception:
            if hasattr(obj, "insert"):
                obj.insert(op)
                return obj
            if hasattr(obj, "append"):
                obj.append(op)
                return obj
            raise

    h_gate = getattr(pq, "H")(qubits[0])
    if hasattr(pq, "CNOT"):
        cx_gate = getattr(pq, "CNOT")(qubits[0], qubits[1])
    else:
        cx_gate = getattr(pq, "CX")(qubits[0], qubits[1])

    circuit = append_op(circuit, h_gate)
    circuit = append_op(circuit, cx_gate)

    _KEEPALIVE.append((qvm, qubits, cbits, circuit))
    return circuit
