# EVAL_META: task_id=84, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def controlled_custom_unitary_circuit():
    circuit = QCircuit()
    circuit << control(U3(0.3, 0.2, 0.1, qubits[1]), qubits[0])
    return circuit

if __name__ == "__main__":
    machine.finalize()
