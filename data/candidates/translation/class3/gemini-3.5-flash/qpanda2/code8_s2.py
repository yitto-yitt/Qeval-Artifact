# EVAL_META: task_id=8, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def rx_gate(value=None):
    if value is not None:
        circuit = QCircuit()
        circuit << RX(q[0], value)
        return circuit
    else:
        vqc = VariationalQuantumCircuit()
        theta = var(0.0, True)
        vqc.insert(RX(q[0], theta))
        return vqc

machine.finalize()
