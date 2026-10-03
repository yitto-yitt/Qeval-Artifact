# EVAL_META: task_id=120, framework=qpanda, class=3
import math
from pyqpanda3.core import *

def create_diagonal_circuit(diag):
    num_qubits = int(math.log2(len(diag)))
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)
    
    circuit = QCircuit()
    gate = DiagonalGate(qubits, diag)
    circuit << gate
    return circuit
