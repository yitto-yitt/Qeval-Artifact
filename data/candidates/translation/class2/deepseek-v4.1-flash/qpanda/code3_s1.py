# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, Qubit, CBit, H, CNOT, Measure, draw_qprog

def create_ghz(drawing=False):
    q = [Qubit(i) for i in range(3)]
    c = [CBit(i) for i in range(3)]
    circuit = QCircuit()
    circuit << H(q[0])
    circuit << CNOT(q[0], q[1])
    circuit << CNOT(q[0], q[2])
    circuit << Measure(q[0], c[0])
    circuit << Measure(q[1], c[1])
    circuit << Measure(q[2], c[2])
    if drawing:
        return circuit, draw_qprog(circuit, 'matplotlib')
    return circuit
