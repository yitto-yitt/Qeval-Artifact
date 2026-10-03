# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)

def remove_unassigned_parameterized_gates(circuit):
    if isinstance(circuit, QCircuit):
        new_circuit = QCircuit()
    else:
        new_circuit = QProg()
    
    for item in circuit:
        if isinstance(item, QGate):
            params = item.get_parameter()
            if not isinstance(params, list):
                params = [params]
            if any(p.is_parameter() for p in params):
                continue
        new_circuit << item
    return new_circuit

machine.finalize()
