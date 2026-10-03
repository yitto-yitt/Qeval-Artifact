# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QMachineType, init_quantum_machine, CNOT, Toffoli

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    machine = init_quantum_machine(QMachineType.CPU)
    if kind == 'full':
        nq = 2 * num_state_qubits + 2
    else:
        nq = 2 * num_state_qubits + 1
    q = machine.qAlloc_many(nq)
    circuit = QCircuit()
    # CDKM ripple-carry logic (majority/unmajority cascade)
    # carry-in handling
    if kind == 'full':
        cin = q[num_state_qubits * 2]
        circuit << CNOT(q[0], cin)
        circuit << Toffoli(q[0], q[num_state_qubits], cin)
    # ripple carry
    for i in range(num_state_qubits - 1):
        a = q[i]
        b = q[i + num_state_qubits]
        c = q[i + 1]
        circuit << Toffoli(a, b, c)
        circuit << CNOT(a, b)
        circuit << Toffoli(c, b, a)
    # final sum and carry-out
    last_a = q[num_state_qubits - 1]
    last_b = q[2 * num_state_qubits - 1]
    if kind == 'full':
        cout = q[2 * num_state_qubits + 1]
        circuit << CNOT(last_a, last_b)
        circuit << Toffoli(last_a, last_b, cout)
    else:
        circuit << CNOT(last_a, last_b)
    # uncompute carries (reverse cascade)
    for i in range(num_state_qubits - 2, -1, -1):
        a = q[i]
        b = q[i + num_state_qubits]
        c = q[i + 1]
        circuit << Toffoli(c, b, a)
        circuit << CNOT(a, b)
        circuit << Toffoli(a, b, c)
    if kind == 'full':
        circuit << Toffoli(q[0], q[num_state_qubits], cin)
        circuit << CNOT(q[0], cin)
    machine.finalize()
    return circuit
