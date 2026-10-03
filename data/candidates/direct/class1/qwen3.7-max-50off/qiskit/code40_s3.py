# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def init_random_3qubit(desired_vector):
    qc = QuantumCircuit(3)
    state_prep = StatePreparation(desired_vector)
    qc.append(state_prep, [0, 1, 2])
    qc.measure_all()

    backend = AerSimulator()
    sampler = SamplerV2(mode=backend)

    job = sampler.run([qc], shots=1024)
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total_shots = sum(counts.values())
    probs = {bitstring: count / total_shots for bitstring, count in counts.items()}

    return probs
