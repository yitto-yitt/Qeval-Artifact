# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT

def convert_qasm_string_to_quantum_circuit():
    qc = QCircuit(2)
    qc << H(qc[0])
    qc << CNOT(qc[0], qc[1])
    return qc
