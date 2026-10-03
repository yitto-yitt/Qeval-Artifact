# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_efficientSU2():
    circuit = QCircuit()

    theta = [0.0 for _ in range(12)]

    circuit.insert(RY(qubits[0], theta[0]))
    circuit.insert(RY(qubits[1], theta[1]))
    circuit.insert(RY(qubits[2], theta[2]))
    circuit.insert(RZ(qubits[0], theta[3]))
    circuit.insert(RZ(qubits[1], theta[4]))
    circuit.insert(RZ(qubits[2], theta[5]))

    if "BARRIER" in globals():
        circuit.insert(BARRIER(qubits))

    circuit.insert(CNOT(qubits[1], qubits[2]))
    circuit.insert(CNOT(qubits[0], qubits[1]))

    if "BARRIER" in globals():
        circuit.insert(BARRIER(qubits))

    circuit.insert(RY(qubits[0], theta[6]))
    circuit.insert(RY(qubits[1], theta[7]))
    circuit.insert(RY(qubits[2], theta[8]))
    circuit.insert(RZ(qubits[0], theta[9]))
    circuit.insert(RZ(qubits[1], theta[10]))
    circuit.insert(RZ(qubits[2], theta[11]))

    return circuit

atexit.register(lambda: machine.finalize())
