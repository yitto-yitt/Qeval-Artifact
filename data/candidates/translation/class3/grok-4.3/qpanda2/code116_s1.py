# EVAL_META: task_id=116, framework=qpanda2, class=3
import pyqpanda as pq
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)
def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    circuit = pq.QCircuit()
    active = [i for i, p in enumerate(pauli_string) if p != 'I']
    if not active:
        return circuit
    for i, p in enumerate(pauli_string):
        if p == 'X':
            circuit << pq.H(qubits[i])
        elif p == 'Y':
            circuit << pq.SDAG(qubits[i])
            circuit << pq.H(qubits[i])
    for i in range(len(active) - 1):
        circuit << pq.CNOT(qubits[active[i]], qubits[active[i + 1]])
    target = active[-1]
    circuit << pq.RZ(qubits[target], 2 * time)
    for i in reversed(range(len(active) - 1)):
        circuit << pq.CNOT(qubits[active[i]], qubits[active[i + 1]])
    for i in reversed(range(n)):
        p = pauli_string[i]
        if p == 'X':
            circuit << pq.H(qubits[i])
        elif p == 'Y':
            circuit << pq.H(qubits[i])
            circuit << pq.S(qubits[i])
    return circuit
machine.finalize()
