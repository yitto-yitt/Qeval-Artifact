# EVAL_META: task_id=105, framework=qpanda, class=3
import pyqpanda3.core as pq


def initialize_cnot_dihedral():
    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    qubits = machine.qAlloc_many(2)

    circ = pq.QCircuit()
    circ << pq.CNOT(qubits[0], qubits[1])
    circ << pq.T(qubits[0])

    if not hasattr(initialize_cnot_dihedral, "_machines"):
        initialize_cnot_dihedral._machines = []
    initialize_cnot_dihedral._machines.append(machine)

    return circ
