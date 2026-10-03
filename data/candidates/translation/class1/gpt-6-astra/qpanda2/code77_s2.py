# EVAL_META: task_id=77, framework=qpanda2, class=1
import math
import pyqpanda as pq


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = [
        math.sqrt(probability_dist.get(basis_state, 0))
        for basis_state in range(2**num_qubits)
    ]

    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)

    circuit = pq.QCircuit()
    for qubit in qubits:
        circuit << pq.I(qubit)
    circuit << pq.amplitude_encode(qubits, amplitudes)

    if not hasattr(circuit_from_probability_dist, "_machines"):
        circuit_from_probability_dist._machines = []
    circuit_from_probability_dist._machines.append(machine)

    return circuit
