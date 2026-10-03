# EVAL_META: task_id=69, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    circuit = QCircuit()
    circuit << H(qubits[0])
    circuit << CP(qubits[0], qubits[1], PI/2)
    circuit << H(qubits[1])
    circuit << CP(qubits[1], qubits[0], -PI/2)
    return circuit

if __name__ == "__main__":
    machine.finalize()
