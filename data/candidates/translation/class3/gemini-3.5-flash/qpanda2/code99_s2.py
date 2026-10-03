# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *

# Initialize CPUQVM and qAlloc_many at the global scope
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(16)

def remove_unassigned_parameterized_gates(circuit):
    if isinstance(circuit, VariationalQuantumCircuit):
        new_circuit = VariationalQuantumCircuit()
        for gate in circuit.get_gates():
            if len(gate.get_vars()) == 0:
                new_circuit.insert(gate)
        return new_circuit
    return circuit

machine.finalize()
