# EVAL_META: task_id=84, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, U3

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

atexit.register(lambda: machine.finalize())

def controlled_custom_unitary_circuit():
    circuit = QCircuit()
    circuit << U3(qubits[1], 0.3, 0.2, 0.1).control([qubits[0]])
    return circuit
