# EVAL_META: task_id=71, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(3)

def create_quantum_circuit_based_h0_csx01_h1():
    circuit = QCircuit()
    circuit << H(qubits[0])
    circuit << CSX(qubits[0], qubits[1])
    circuit << H(qubits[1])
    return circuit

if __name__ == "__main__":
    machine.finalize()
