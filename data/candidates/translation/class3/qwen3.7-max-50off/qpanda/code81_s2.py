# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def convert_qasm_string_to_quantum_circuit():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc
