# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(1)

def remove_unassigned_parameterized_gates(circuit):
    if isinstance(circuit, QCircuit):
        new_circuit = QCircuit()
    elif isinstance(circuit, QProg):
        new_circuit = QProg()
    else:
        new_circuit = QCircuit()
    for node in circuit:
        if not isinstance(node, VariationalQuantumGate):
            new_circuit << node
    return new_circuit

machine.finalize()
