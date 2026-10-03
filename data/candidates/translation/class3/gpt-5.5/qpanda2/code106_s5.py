# EVAL_META: task_id=106, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def compose_cnot_dihedral():
    circ1 = QCircuit()
    circ1.insert(CNOT(qubits[0], qubits[1]))
    circ1.insert(T(qubits[0]))

    circ2 = QCircuit()
    circ2.insert(CNOT(qubits[0], qubits[1]))
    circ2.insert(T(qubits[0]))
    circ2.insert(X(qubits[1]))

    composed_circuit = QCircuit()
    composed_circuit.insert(circ1)
    composed_circuit.insert(circ2)

    composed_prog = QProg()
    composed_prog.insert(composed_circuit)

    machine.prob_run_dict(composed_prog, qubits, -1)
    return composed_prog


atexit.register(machine.finalize)
