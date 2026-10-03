# EVAL_META: task_id=118, framework=qpanda2, class=3
from pyqpanda import *
import pyqpanda as pq

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_c3sx_circuit():
    circuit = QCircuit()
    circuit << control(SX(qubits[3]), [qubits[0], qubits[1], qubits[2]])
    return circuit

machine.finalize()
