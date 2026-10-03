# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)
cbits = machine.cAlloc_many(16)


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QCircuit()
    for node in circuit:
        node_iter = node
        try:
            gate = QGate(node_iter)
        except Exception:
            new_circuit.insert(node_iter)
            continue

        has_unassigned = False
        try:
            params = gate.gate_matrix()
            angle = None
            try:
                angle = gate.gate_angle()
            except Exception:
                angle = None
            if angle is not None and (angle != angle):
                has_unassigned = True
        except Exception:
            has_unassigned = False

        if not has_unassigned:
            new_circuit.insert(gate)

    return new_circuit


machine.finalize()
