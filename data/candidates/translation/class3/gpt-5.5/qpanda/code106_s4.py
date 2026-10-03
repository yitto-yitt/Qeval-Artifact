# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, QProg, CNOT, T, X


def compose_cnot_dihedral():
    machine = CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()

    qubits = machine.qAlloc_many(2)

    circ1 = QCircuit()
    circ1 << CNOT(qubits[0], qubits[1])
    circ1 << T(qubits[0])

    circ2 = QCircuit()
    circ2 << CNOT(qubits[0], qubits[1])
    circ2 << T(qubits[0])
    circ2 << X(qubits[1])

    composed_circuit = QCircuit()
    composed_circuit << circ1
    composed_circuit << circ2

    prog = QProg()
    prog << composed_circuit

    try:
        machine.prob_run_dict(prog, qubits, -1)
    except Exception:
        pass

    compose_cnot_dihedral._machine = machine
    compose_cnot_dihedral._qubits = qubits
    compose_cnot_dihedral._program = prog

    return composed_circuit
