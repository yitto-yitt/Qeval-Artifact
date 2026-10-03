# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT

def collect_linear_blocks_with_and_without_limit():
    def build_circuit():
        qc = QCircuit()
        qc << H(0)
        qc << CNOT(0, 1)
        qc << CNOT(1, 2)
        qc << CNOT(2, 3)
        qc << CNOT(3, 4)
        return qc

    full_block = build_circuit()
    limited_block = build_circuit()
    return full_block, limited_block
