# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import *

def create_custom_controlled():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(4)
    
    circuit = QCircuit()
    circuit << X(qubits[1]) << H(qubits[2])
    
    controlled_circuit = circuit.control([qubits[0], qubits[3]])
    
    prog = QProg()
    prog << controlled_circuit
    return prog
