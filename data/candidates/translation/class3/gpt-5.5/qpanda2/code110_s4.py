# EVAL_META: task_id=110, framework=qpanda2, class=3
import random
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(16)

def equivalent_clifford_circuit(circuit, n):
    def _copy_circuit(obj):
        try:
            qc = QCircuit()
            qc.insert(obj)
            return qc
        except Exception:
            try:
                prog = QProg()
                prog.insert(obj)
                return prog
            except Exception:
                return obj

    def _used_qubits(obj):
        try:
            return list(get_all_used_qubits(obj))
        except Exception:
            try:
                prog = QProg()
                prog.insert(obj)
                return list(get_all_used_qubits(prog))
            except Exception:
                return []

    qubits = _used_qubits(circuit)
    result = []

    while len(result) < n:
        qc = _copy_circuit(circuit)

        if qubits:
            repetitions = random.randint(1, max(1, 3 * len(qubits)))
            for _ in range(repetitions):
                if len(qubits) >= 2 and random.random() < 0.45:
                    q0, q1 = random.sample(qubits, 2)
                    gate_type = random.randint(0, 2)
                    if gate_type == 0:
                        qc.insert(CNOT(q0, q1))
                        qc.insert(CNOT(q0, q1))
                    elif gate_type == 1:
                        qc.insert(CZ(q0, q1))
                        qc.insert(CZ(q0, q1))
                    else:
                        qc.insert(SWAP(q0, q1))
                        qc.insert(SWAP(q0, q1))
                else:
                    q0 = random.choice(qubits)
                    gate_type = random.randint(0, 3)
                    if gate_type == 0:
                        qc.insert(H(q0))
                        qc.insert(H(q0))
                    elif gate_type == 1:
                        qc.insert(X(q0))
                        qc.insert(X(q0))
                    elif gate_type == 2:
                        qc.insert(Y(q0))
                        qc.insert(Y(q0))
                    else:
                        qc.insert(Z(q0))
                        qc.insert(Z(q0))

        result.append(qc)

    return result

atexit.register(machine.finalize)
