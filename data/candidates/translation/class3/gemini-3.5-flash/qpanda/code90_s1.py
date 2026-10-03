# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import *

def create_custom_controlled():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(4)
    
    sub_circuit = QCircuit()
    sub_circuit << X(q[1]) << H(q[2])
    
    control_qubits = QVec()
    control_qubits.append(q[0])
    control_qubits.append(q[3])
    
    controlled_circuit = sub_circuit.control(control_qubits)
    
    prog = QProg()
    prog << controlled_circuit
    
    return prog
