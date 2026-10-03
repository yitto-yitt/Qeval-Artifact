# EVAL_META: task_id=110, framework=qpanda2, class=3
from pyqpanda import *
import random
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)
def equivalent_clifford_circuit(circuit, n):
    num_qubits = 2
    qc_list = []
    counter = 0
    while counter < n:
        qc = QCircuit()
        for _ in range(random.randint(5, 15)):
            q1 = random.randint(0, num_qubits-1)
            q2 = random.randint(0, num_qubits-1)
            r = random.random()
            if r < 0.25:
                qc << H(qubits[q1])
            elif r < 0.5:
                qc << S(qubits[q1])
            elif r < 0.75:
                qc << X(qubits[q1])
            else:
                if q1 != q2:
                    qc << CNOT(qubits[q1], qubits[q2])
        qc_list.append(qc)
        counter += 1
    return qc_list
machine.finalize()
