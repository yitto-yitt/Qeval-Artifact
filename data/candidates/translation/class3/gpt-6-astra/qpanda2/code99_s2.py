# EVAL_META: task_id=99, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def remove_unassigned_parameterized_gates(circuit):
    if isinstance(circuit, pq.variationalQuantumCircuit):
        circuit = circuit.feed()

    if isinstance(circuit, pq.QCircuit):
        result = pq.QCircuit()
    elif isinstance(circuit, pq.QProg):
        result = pq.QProg()
    else:
        raise TypeError("circuit must be a pyQPanda QCircuit or QProg")

    iterator = circuit.get_first_node_iter()
    end = circuit.get_end_node_iter()

    while iterator != end:
        node = iterator.get_node()
        if node.get_node_type() == pq.NodeType.GATE_NODE:
            gate = pq.cast_qgate(node)
            # Native pyQPanda gates contain only assigned numeric parameters.
            result << gate
        elif node.get_node_type() == pq.NodeType.CIRCUIT_NODE:
            result << pq.cast_qcircuit(node)
        else:
            # Preserve non-gate instructions in programs without interpreting them.
            result << pq.QProg(iterator, iterator)
        iterator = iterator.get_next()

    if isinstance(circuit, pq.QCircuit):
        controls = pq.QVec()
        circuit.get_control_qubits(controls)
        result.set_control(controls)
        result.set_dagger(circuit.is_dagger())

    return result


machine.finalize()
