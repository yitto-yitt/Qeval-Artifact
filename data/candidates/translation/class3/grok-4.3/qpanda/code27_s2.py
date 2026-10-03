# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, QCircuit, H, CNOT

def apply_op_back():
    machine = QuantumMachine()
    q = machine.allocate_qubits(3)
    circ = QCircuit()
    circ << H(q[0]) << CNOT(q[0], q[1]) << H(q[0])
    return circ
