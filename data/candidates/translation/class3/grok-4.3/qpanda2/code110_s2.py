# EVAL_META: task_id=110, framework=qpanda2, class=3
from pyqpanda import *
import random
machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(5)
def equivalent_clifford_circuit(circuit, n):
    num_qubits = 2
    used_qubits = circuit.get_used_qubits()
    if len(used_qubits) > 0:
        num_qubits = len(used_qubits)
    qc_list = []
    counter = 0
    while counter < n:
        qc = QCircuit()
        for _ in range(random.randint(3, 8)):
            q_idx = random.randint(0, num_qubits - 1)
            qc.insert(H(qubits[q_idx]))
            qc.insert(S(qubits[q_idx]))
            if num_qubits > 1:
                q2_idx = random.randint(0, num_qubits - 1)
                qc.insert(CNOT(qubits[q_idx], qubits[q2_idx]))
        prog = QProg()
        prog.insert(qc)
        counter += 1
        qc_list.append(qc)
    return qc_list
machine.finalize()
