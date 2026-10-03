# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import *

_INITIALIZED = False

def _ensure_initialized():
    global _INITIALIZED
    if not _INITIALIZED:
        init(QuantumMachineType.CPU_SINGLE_THREAD)
        _INITIALIZED = True

def convert_qasm_string_to_quantum_circuit():
    _ensure_initialized()

    qasm_string = """OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
    h q[0];
    cx q[0],q[1];"""

    qubits = None
    qc = QCircuit()

    for raw_line in qasm_string.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("qreg "):
            count = int(line[line.index("[") + 1:line.index("]")])
            qubits = qAlloc_many(count)

        elif line.startswith("creg "):
            count = int(line[line.index("[") + 1:line.index("]")])
            cAlloc_many(count)

        elif line.startswith("h "):
            idx = int(line[line.index("[") + 1:line.index("]")])
            qc << H(qubits[idx])

        elif line.startswith("cx "):
            args = line[3:].strip().rstrip(";")
            left, right = args.split(",")
            idx0 = int(left[left.index("[") + 1:left.index("]")])
            idx1 = int(right[right.index("[") + 1:right.index("]")])
            qc << CNOT(qubits[idx0], qubits[idx1])

    return qc
