# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)

def inv_circuit(n):
    circuit = QCircuit()
    circuit << H(qubits[1])
    circuit << H(qubits[2])
    circuit << CNOT(qubits[1], qubits[3])
    circuit << CNOT(qubits[2], qubits[4])
    return circuit.dagger()

if __name__ == "__main__":
    machine.finalize()
