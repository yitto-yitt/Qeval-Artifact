# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, CPUQVM, RX


def rx_gate(value=None):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc()
    circuit = QCircuit()
    if value is None:
        theta = 0.0
    else:
        theta = float(value)
    circuit.insert(RX(q, theta))
    prog = QProg()
    prog.insert(circuit)
    qvm.finalize()
    return circuit
