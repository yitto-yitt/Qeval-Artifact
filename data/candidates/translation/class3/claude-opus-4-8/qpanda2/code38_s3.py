# EVAL_META: task_id=38, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    prog = QCircuit()
    prog << H(qubits[0])
    prog << RZ(qubits[1], theta).control(qubits[0])
    prog << H(qubits[1])
    prog << RY(qubits[0], theta).control(qubits[1])
    return prog

if __name__ == "__main__":
    circuit = create_quantum_circuit_based_h0_crz01_h1_cry10(0.5)
    print(circuit)
    machine.finalize()
