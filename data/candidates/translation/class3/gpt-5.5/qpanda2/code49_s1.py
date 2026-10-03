# EVAL_META: task_id=49, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, H, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
atexit.register(machine.finalize)

def simple_elitzur_vaidman():
    circuit = QCircuit()
    circuit << H(qubits[0])
    circuit << CNOT(qubits[0], qubits[1])
    circuit << H(qubits[0])
    return circuit
