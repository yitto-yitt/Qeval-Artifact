# EVAL_META: task_id=15, framework=qpanda, class=1
import pyqpanda3.core as pq

def noisy_bell():
    try:
        machine = pq.NoiseQVM()
        machine.init_qvm()
        try:
            machine.set_noise_model(pq.NOISE_MODEL.DEPOLARIZING_KRAUS_OPERATOR, pq.GateType.HADAMARD_GATE, 0.01)
            machine.set_noise_model(pq.NOISE_MODEL.DEPOLARIZING_KRAUS_OPERATOR, pq.GateType.CNOT_GATE, 0.02)
        except:
            pass
    except:
        machine = pq.CPUQVM()
        machine.init_qvm()
        
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    
    shots = 1000
    result = machine.run_with_configuration(prog, c, shots)
    
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
