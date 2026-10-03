# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_custom_controlled():
    circ = QCircuit()
    circ << X(qubits[1]) << H(qubits[2])
    
    control_qubits = QVec()
    control_qubits.append(qubits[0])
    control_qubits.append(qubits[3])
    
    controlled_circ = circ.control(control_qubits)
    
    prog = QProg()
    prog << controlled_circ
    return prog

if __name__ == '__main__':
    machine.finalize()
