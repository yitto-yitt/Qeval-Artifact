# EVAL_META: task_id=14, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator

def bell_each_shot():
    # 1. Create a phi plus Bell circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # 2. Get Aer simulator backend and transpile with optimization level 1
    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_qc = pm.run(qc)
    
    # 3. Run using Qiskit Runtime Sampler
    try:
        from qiskit_ibm_runtime import SamplerV2
        sampler = SamplerV2(backend=backend)
        job = sampler.run([transpiled_qc], shots=10)
        result = job.result()
        pub_result = result[0]
        
        # Extract counts from the classical register
        try:
            counts = pub_result.data.meas.get_counts()
        except AttributeError:
            creg_name = list(pub_result.data.keys())[0]
            counts = getattr(pub_result.data, creg_name).get_counts()
            
        total = sum(counts.values())
        prob_dist = {k: v / total for k, v in counts.items()}
    except Exception:
        from qiskit_ibm_runtime import Sampler
        sampler = Sampler(backend=backend)
        job = sampler.run(transpiled_qc, shots=10)
        result = job.result()
        prob_dist = result.quasi_dists[0].binary_probabilities()
        
    return prob_dist
