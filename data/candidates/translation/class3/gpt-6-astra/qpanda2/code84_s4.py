# EVAL_META: task_id=84, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def controlled_custom_unitary_circuit():
    if hasattr(controlled_custom_unitary_circuit, "_circuit"):
        return controlled_custom_unitary_circuit._circuit

    circuit = pq.QCircuit()
    circuit << pq.U3(qubits[1], 0.3, 0.2, 0.1).control([qubits[0]])

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)

    controlled_custom_unitary_circuit._circuit = circuit
    return circuit


controlled_custom_unitary_circuit()
machine.finalize()
