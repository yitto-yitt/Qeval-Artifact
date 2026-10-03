# EVAL_META: task_id=110, framework=qpanda2, class=3
from pyqpanda import *
import random
import atexit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(64)
c = machine.cAlloc_many(64)

def equivalent_clifford_circuit(circuit, n):
    qubits = []
    try:
        qubits = list(circuit.get_used_qubits())
    except Exception:
        try:
            qubits = list(get_all_used_qubits(circuit))
        except Exception:
            try:
                qubits = list(q[:circuit.num_qubits])
            except Exception:
                qubits = []

    qc_list = []
    num_qubits = len(qubits)

    for _ in range(n):
        try:
            qc = QCircuit()
            qc << circuit
        except Exception:
            qc = QProg()
            qc << circuit

        if num_qubits > 0:
            depth = random.randint(1, max(2, 4 * num_qubits + 4))
            for _ in range(depth):
                if num_qubits >= 2 and random.random() < 0.35:
                    i, j = random.sample(range(num_qubits), 2)
                    qc << CNOT(qubits[i], qubits[j])
                    qc << CNOT(qubits[i], qubits[j])
                else:
                    gate = random.choice([H, X, Y, Z])
                    qb = qubits[random.randrange(num_qubits)]
                    qc << gate(qb)
                    qc << gate(qb)

        qc_list.append(qc)

    return qc_list

atexit.register(machine.finalize)
