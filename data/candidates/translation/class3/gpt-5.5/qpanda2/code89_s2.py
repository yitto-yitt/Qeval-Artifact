# EVAL_META: task_id=89, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
atexit.register(machine.finalize)

def create_controlled_hgate():
    circuit = QCircuit()
    circuit << H(qubits[2]).control([qubits[0], qubits[1]])
    return circuit
