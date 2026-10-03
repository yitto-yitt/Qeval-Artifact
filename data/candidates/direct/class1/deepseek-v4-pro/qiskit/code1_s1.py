# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler

def run_bell_state_simulator():
    # Prepare a phi+ Bell state: |00> + |11>
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    # Transpile with optimization level 1
    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_qc = pm.run(qc)

    # Run on the Aer simulator via Qiskit Runtime Sampler
    sampler = Sampler(backend=backend)
    job = sampler.run([transpiled_qc], shots=8192)
    result = job.result()

    # Extract measurement counts and convert to probability distribution
    pub_result = result[0]
    counts = pub_result.data.meas.get_counts()
    total_shots = sum(counts.values())
    prob_dict = {state: count / total_shots for state, count in counts.items()}
    return prob_dict
