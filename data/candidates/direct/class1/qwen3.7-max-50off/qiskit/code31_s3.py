# EVAL_META: task_id=31, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler

def sampler_qiskit():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    sampler = Sampler(options={"simulator": {"seed_simulator": 42}})
    job = sampler.run([qc])
    result = job.result()
    
    dist = result.quasi_dists[0]
    prob_dist = {}
    for key, val in dist.items():
        bitstring = format(key, f'0{qc.num_clbits}b')
        prob_dist[bitstring] = val
    return prob_dist
