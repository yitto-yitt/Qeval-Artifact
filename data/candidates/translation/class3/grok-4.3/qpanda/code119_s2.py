# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import *
def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2 * num_state_qubits + 2)
    c = QCircuit()
    c << CDKMRippleCarryAdder(num_state_qubits, kind)(qubits)
    prog = QProg()
    prog << c
    return prog
