# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
params = [var(f'theta_{i}') for i in range(12)]
def create_efficientSU2():
    circuit = QCircuit()
    idx = 0
    for i in range(3):
        circuit << RY(qubits[i], params[idx]) << RZ(qubits[i], params[idx + 1])
        idx += 2
    circuit << BARRIER(qubits)
    circuit << CNOT(qubits[2], qubits[1])
    circuit << CNOT(qubits[1], qubits[0])
    circuit << BARRIER(qubits)
    for i in range(3):
        circuit << RY(qubits[i], params[idx]) << RZ(qubits[i], params[idx + 1])
        idx += 2
    return circuit
machine.finalize()
