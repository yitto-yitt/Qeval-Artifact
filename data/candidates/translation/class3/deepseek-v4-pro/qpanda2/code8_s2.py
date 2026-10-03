# EVAL_META: task_id=8, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, VariationalQuantumGate

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def rx_gate(value=None):
    theta = 0.0 if value is None else value
    circuit = QCircuit()
    circuit.insert(VariationalQuantumGate.RX(q[0], theta))
    return circuit

machine.finalize()
