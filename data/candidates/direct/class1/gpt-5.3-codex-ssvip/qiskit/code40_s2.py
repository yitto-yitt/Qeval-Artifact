# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler


def init_random_3qubit(desired_vector):
    sv = Statevector(desired_vector)
    if sv.num_qubits != 3:
        raise ValueError("desired_vector must represent a 3-qubit state (length 8).")

    qc = QuantumCircuit(3, 3)
    qc.initialize(sv.data, [0, 1, 2])
    qc.measure([0, 1, 2], [0, 1, 2])

    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    job = sampler.run([qc], shots=4096)
    result = job.result()

    pub_result = result[0]
    data_bin = pub_result.data.c
    counts = data_bin.get_counts()
    total = sum(counts.values()) if counts else 1
    return {k: v / total for k, v in counts.items()}
