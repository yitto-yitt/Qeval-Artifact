# EVAL_META: task_id=119, framework=qpanda, class=3

from pyqpanda3.core import *

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    adder = CDKMRippleCarryAdder(num_state_qubits, kind)
    qc = QCircuit()
    qc << adder
    return qc
