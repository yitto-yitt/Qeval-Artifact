# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_custom_controlled():
    circuit = QCircuit()
    g1 = X(qubits[1])
    g1.set_control([qubits[0], qubits[3]])
    circuit << g1
    g2 = H(qubits[2])
    g2.set_control([qubits[0], qubits[3]])
    circuit << g2
    return circuit

if __name__ == "__main__":
    machine.finalize()
