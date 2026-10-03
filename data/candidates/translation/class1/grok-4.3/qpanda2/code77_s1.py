# EVAL_META: task_id=77, framework=qpanda2, class=1
import math
import pyqpanda as pq

def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))
    machine = pq.init_quantum_machine(pq.QMachineType.CPU_SINGLE_THREAD)
    qubits = machine.qAlloc_many(num_qubits)
    prog = pq.QProg()
    circuit = pq.QCircuit()
    circuit.insert(pq.amplitude_encode(qubits, amplitudes))
    prog.insert(circuit)
    machine.finalize()
    return prog
