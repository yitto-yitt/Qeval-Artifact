# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_custom_controlled():
    circuit = QCircuit()
    circuit << X(q[1]) << H(q[2])
    
    control_qubits = QVec()
    control_qubits.append(q[0])
    control_qubits.append(q[3])
    
    controlled_circuit = circuit.control(control_qubits)
    
    prog = QProg()
    prog << controlled_circuit
    return prog

machine.finalize()
