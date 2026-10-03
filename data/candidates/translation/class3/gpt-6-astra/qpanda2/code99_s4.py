# EVAL_META: task_id=99, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def remove_unassigned_parameterized_gates(circuit):
    if isinstance(circuit, pq.VariationalQuantumCircuit):
        filtered = pq.VariationalQuantumCircuit()
        for gate in circuit.get_gates():
            if not gate.get_vars():
                filtered.insert(gate)
        return filtered.feed()

    if isinstance(circuit, pq.QCircuit):
        # Native QCircuit gates contain concrete, already-assigned parameters.
        return pq.QCircuit(circuit)

    raise TypeError("Expected a QCircuit or VariationalQuantumCircuit.")


machine.finalize()
