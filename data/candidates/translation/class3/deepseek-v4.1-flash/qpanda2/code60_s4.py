# EVAL_META: task_id=60, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_cy_gate():
    circuit = QCircuit()
    circuit << SDAG(qubits[1])
    circuit << CNOT(qubits[0], qubits[1])
    circuit << S(qubits[1])
    return circuit
