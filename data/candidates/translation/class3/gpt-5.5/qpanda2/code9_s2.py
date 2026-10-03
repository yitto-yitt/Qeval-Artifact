# EVAL_META: task_id=9, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_efficientSU2():
    circuit = QCircuit()
    circuit << RY(qubits[0], 0.0) << RY(qubits[1], 0.0) << RY(qubits[2], 0.0)
    circuit << RZ(qubits[0], 0.0) << RZ(qubits[1], 0.0) << RZ(qubits[2], 0.0)
    circuit << BARRIER(qubits)
    circuit << CNOT(qubits[1], qubits[2]) << CNOT(qubits[0], qubits[1])
    circuit << BARRIER(qubits)
    circuit << RY(qubits[0], 0.0) << RY(qubits[1], 0.0) << RY(qubits[2], 0.0)
    circuit << RZ(qubits[0], 0.0) << RZ(qubits[1], 0.0) << RZ(qubits[2], 0.0)
    return circuit

atexit.register(machine.finalize)
