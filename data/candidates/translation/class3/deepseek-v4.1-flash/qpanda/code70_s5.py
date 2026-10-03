# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, H, CSWAP, CSdg

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    q = [Qubit(0), Qubit(1), Qubit(2)]
    circuit = QCircuit()
    circuit << H(q[0])
    circuit << CSWAP(q[0], q[1], q[2])
    circuit << H(q[1])
    circuit << CSdg(q[1], q[0])
    return circuit
