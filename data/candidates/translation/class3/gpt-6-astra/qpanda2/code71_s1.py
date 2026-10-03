# EVAL_META: task_id=71, framework=qpanda2, class=3
import atexit
from math import pi
from pyqpanda import CPUQVM, QCircuit, QProg, H, T, RX

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
atexit.register(machine.finalize)


def create_quantum_circuit_based_h0_csx01_h1():
    circuit = QCircuit()
    circuit << H(qubits[0])
    circuit << T(qubits[0])
    circuit << RX(qubits[1], pi / 2).control([qubits[0]])
    circuit << H(qubits[1])

    program = QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
