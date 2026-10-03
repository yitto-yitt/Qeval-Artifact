# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, QCircuit, H, CNOT

def simple_elitzur_vaidman():
    qm = QuantumMachine()
    q = qm.allocate_qubits(2)
    circuit = QCircuit()
    circuit.insert(H(q[0]))
    circuit.insert(CNOT(q[0], q[1]))
    circuit.insert(H(q[0]))
    return circuit
