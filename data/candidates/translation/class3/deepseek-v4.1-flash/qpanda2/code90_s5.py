# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_custom_controlled():
    circuit = QCircuit()
    circuit << X(qubits[1]).control([qubits[0], qubits[3]])
    circuit << H(qubits[2]).control([qubits[0], qubits[3]])
    return circuit

machine.finalize()
