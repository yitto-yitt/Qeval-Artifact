# EVAL_META: task_id=119, framework=qpanda2, class=3
import pyqpanda as pq
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(30)
def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == 'half':
        total_qubits = 2 * num_state_qubits
    elif kind == 'full':
        total_qubits = 2 * num_state_qubits + 1
    else:
        total_qubits = 2 * num_state_qubits + 2
    circuit = pq.QCircuit()
    for i in range(num_state_qubits - 1):
        circuit << pq.CNOT(qubits[i], qubits[i + num_state_qubits])
        circuit << pq.Toffoli(qubits[i], qubits[i + num_state_qubits], qubits[i + 1])
    circuit << pq.CNOT(qubits[num_state_qubits - 1], qubits[2 * num_state_qubits - 1])
    if kind in ('full', 'fixed'):
        circuit << pq.CNOT(qubits[num_state_qubits - 1], qubits[total_qubits - 1])
    for i in range(num_state_qubits - 2, -1, -1):
        circuit << pq.Toffoli(qubits[i], qubits[i + num_state_qubits], qubits[i + 1])
        circuit << pq.CNOT(qubits[i], qubits[i + num_state_qubits])
    return circuit
machine.finalize()
