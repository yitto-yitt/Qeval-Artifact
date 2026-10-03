# EVAL_META: task_id=38, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, QProg, H, RZ, RY

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    circuit = QCircuit()
    circuit << H(qubits[0])
    circuit << RZ(qubits[1], theta).control([qubits[0]])
    circuit << H(qubits[1])
    circuit << RY(qubits[0], theta).control([qubits[1]])

    program = QProg()
    program << circuit
    machine.directly_run(program)
    return circuit


atexit.register(machine.finalize)
