# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def remove_unassigned_parameterized_gates(circuit):
    if isinstance(circuit, VariationalQuantumCircuit):
        new_circ = VariationalQuantumCircuit()
        for gate in circuit.get_gates():
            if len(gate.get_vars()) == 0:
                new_circ.insert(gate)
        return new_circ
    return circuit

machine.finalize()
