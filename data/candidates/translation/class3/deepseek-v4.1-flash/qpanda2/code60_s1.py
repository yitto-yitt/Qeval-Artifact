# EVAL_META: task_id=60, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import *

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_cy_gate():
    circuit = pq.QCircuit()
    circuit << pq.Sdagger(qubits[1]) << pq.CNOT(qubits[0], qubits[1]) << pq.S(qubits[1])
    return circuit

machine.finalize()
