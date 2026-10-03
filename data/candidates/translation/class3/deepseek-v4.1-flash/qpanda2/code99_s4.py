# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(10)
cbits = cAlloc_many(10)

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QCircuit()
    for node in circuit.get_sequence():
        if isinstance(node, QGate):
            var = node.get_var()
            if var is not None:
                if isinstance(var, (list, tuple)):
                    if any(not v.is_assigned() for v in var):
                        continue
                else:
                    if not var.is_assigned():
                        continue
        new_circuit << node
    return new_circuit

machine.finalize()
