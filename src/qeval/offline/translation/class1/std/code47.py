# EVAL_META: task_id=47, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler

def random_coin_flip(samples):
    circuit = QuantumCircuit(1,1)
    circuit.h(0)
    circuit.measure_all()
    backend = AerSimulator()
    sampler = Sampler(mode=backend)
    result = sampler.run([circuit], shots=samples).result()
    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    return {'Heads': counts.get('0', 0) / total, 'Tails': counts.get('1', 0) / total}
