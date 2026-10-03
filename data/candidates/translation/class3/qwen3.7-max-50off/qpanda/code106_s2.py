# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, T, X

def compose_cnot_dihedral():
    try:
        from pyqpanda3.core import QMachine
        qm = QMachine()
        q = qm.allocate_qubits(2)
    except Exception:
        try:
            from pyqpanda3 import QMachine
            qm = QMachine()
            q = qm.allocate_qubits(2)
        except Exception:
            from pyqpanda3.core import Qubit
            q = [Qubit(0), Qubit(1)]

    circ1 = QCircuit()
    circ1 << CNOT(q[0], q[1]) << T(q[0])
    
    circ2 = QCircuit()
    circ2 << CNOT(q[0], q[1]) << T(q[0]) << X(q[1])
    
    composed = QCircuit()
    composed << circ1 << circ2
    
    return composed
