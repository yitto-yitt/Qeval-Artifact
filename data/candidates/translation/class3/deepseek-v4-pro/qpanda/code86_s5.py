# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, H, CNOT

def collect_linear_blocks_with_and_without_limit():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(5)

    cx_gates = [
        CNOT(q[0], q[1]),
        CNOT(q[1], q[2]),
        CNOT(q[2], q[3]),
        CNOT(q[3], q[4]),
    ]

    def _make_block(gates):
        block = QCircuit()
        for gate in gates:
            block << gate
        return block

    full = QCircuit()
    full << H(q[0])
    full << _make_block(cx_gates)

    limited = QCircuit()
    limited << H(q[0])
    limited << _make_block(cx_gates[:2])
    limited << _make_block(cx_gates[2:])

    return full, limited
