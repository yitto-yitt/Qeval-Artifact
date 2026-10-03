# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.initQVM()
qubits = machine.qAlloc_many(3)
def create_efficientSU2():
    circuit = QCircuit()
    for i in range(3):
        circuit << RY(qubits[i], 0) << RZ(qubits[i], 0)
    circuit << BARRIER(qubits)
    circuit << CNOT(qubits[0], qubits[1])
    circuit << CNOT(qubits[1], qubits[2])
    circuit << BARRIER(qubits)
    for i in range(3):
        circuit << RY(qubits[i], 0) << RZ(qubits[i], 0)
    return circuit
machine.finalize()
