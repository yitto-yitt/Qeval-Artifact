# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import VariationalQuantumCircuit

def remove_unassigned_parameterized_gates(circuit):
    if isinstance(circuit, VariationalQuantumCircuit):
        new_circuit = VariationalQuantumCircuit()
        for gate in circuit.get_gates():
            if len(gate.get_vars()) == 0:
                new_circuit.insert(gate)
        return new_circuit
    return circuit
