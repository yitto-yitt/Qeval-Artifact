# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import QMachine, QCircuit, H, CNOT

def convert_qasm_string_to_quantum_circuit():
    qm = QMachine()
    q = qm.alloc_qubits(2)
    circ = QCircuit()
    circ << H(q[0]) << CNOT(q[0], q[1])
    return circ
