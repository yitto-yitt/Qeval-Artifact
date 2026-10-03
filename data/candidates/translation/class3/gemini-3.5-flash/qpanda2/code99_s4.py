# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()

def remove_unassigned_parameterized_gates(circuit):
    if hasattr(circuit, 'get_gate_list'):
        new_circuit = VariationalQuantumCircuit()
        for gate in circuit.get_gate_list():
            if len(gate.get_vars()) == 0:
                new_circuit.insert(gate)
        return new_circuit
    return circuit

machine.finalize()
