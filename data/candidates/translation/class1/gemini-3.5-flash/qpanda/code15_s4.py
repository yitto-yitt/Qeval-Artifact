# EVAL_META: task_id=15, framework=qpanda, class=1
import pyqpanda3.core as pq

def noisy_bell():
    qvm = pq.NoiseQVM()
    qvm.init_qvm()
    
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    # Set noise model to simulate a noisy backend
    qvm.set_noise_model(pq.NOISE_MODEL.DEPOLARIZING_KRAUS_MAP, pq.GateType.HADAMARD_GATE, 0.01)
    qvm.set_noise_model(pq.NOISE_MODEL.DEPOLARIZING_KRAUS_MAP, pq.GateType.CNOT_GATE, 0.02)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0]) \
         << pq.CNOT(qubits[0], qubits[1]) \
         << pq.Measure(qubits[0], cbits[0]) \
         << pq.Measure(qubits[1], cbits[1])
         
    # Run the program
    result = qvm.run_with_configuration(prog, cbits, 1000)
    
    # Calculate probabilities
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
