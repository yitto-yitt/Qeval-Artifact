# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, Qubit, Measure

try:
    from pyqpanda3.core import CBit
except ImportError:
    from pyqpanda3.core import Cbit as CBit


def create_quantum_circuit_with_one_qubit_and_measure():
    q = Qubit()
    c = CBit()
    qc = QCircuit()
    qc << Measure(q, c)
    return qc
