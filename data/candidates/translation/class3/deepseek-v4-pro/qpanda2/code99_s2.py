# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QCircuit()
    for i in range(circuit.get_qgate_num()):
        gate = circuit.get_qgate(i)
        if not gate.is_variational():
            new_circuit.insert(gate)
    return new_circuit

machine.finalize()
