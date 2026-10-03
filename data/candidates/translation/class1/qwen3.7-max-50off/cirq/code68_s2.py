# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    
    q = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    
    if bomb_live:
        for i in range(cycles):
            circuit.append(cirq.ry(e).on(q))
            circuit.append(cirq.measure(q, key=f'm{i}'))
        circuit.append(cirq.measure(q, key=f'm{cycles}'))
    else:
        for i in range(cycles):
            circuit.append(cirq.ry(e).on(q))
        circuit.append(cirq.measure(q, key='m0'))
        
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    
    if bomb_live:
        m_final = result.measurements[f'm{cycles}']
        m_inter = np.zeros((shots, cycles), dtype=int)
        for i in range(cycles):
            m_inter[:, i] = result.measurements[f'm{i}']
            
        detonations = int(np.sum(m_final == 1))
        dud_predictions = int(np.sum((m_final == 0) & np.any(m_inter == 1, axis=1)))
        live_predictions = int(np.sum((m_final == 0) & np.all(m_inter == 0, axis=1)))
    else:
        m_final = result.measurements['m0']
        live_predictions = int(np.sum(m_final == 0))
        dud_predictions = int(np.sum(m_final == 1))
        detonations = 0
        
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
