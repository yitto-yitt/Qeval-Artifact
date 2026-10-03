# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGate, Qubit

def collect_linear_blocks_with_and_without_limit():
    q = Qubit(5)
    
    # Full block (no width restriction)
    circ_full = QCircuit()
    circ_full << QGate("H", q[0])
    sub_full = QCircuit()
    sub_full << QGate("CNOT", q[0], q[1])
    sub_full << QGate("CNOT", q[1], q[2])
    sub_full << QGate("CNOT", q[2], q[3])
    sub_full << QGate("CNOT", q[3], q[4])
    circ_full << sub_full
    
    # Limited block (max_block_width = 3)
    circ_limited = QCircuit()
    circ_limited << QGate("H", q[0])
    sub1 = QCircuit()
    sub1 << QGate("CNOT", q[0], q[1])
    sub1 << QGate("CNOT", q[1], q[2])
    sub2 = QCircuit()
    sub2 << QGate("CNOT", q[2], q[3])
    sub2 << QGate("CNOT", q[3], q[4])
    circ_limited << sub1
    circ_limited << sub2
    
    return circ_full, circ_limited
