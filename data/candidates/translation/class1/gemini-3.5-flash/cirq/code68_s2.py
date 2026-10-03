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
            circuit.append(cirq.ry(e)(q))
            circuit.append(cirq.measure(q, key=f'm{i}'))
        circuit.append(cirq.measure(q, key=f'm{cycles}'))
    else:
        for i in range(cycles):
            circuit.append(cirq.ry(e)(q))
        circuit.append(cirq.measure(q, key='m0'))
        
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    
    if bomb_live:
        m_final = result.measurements[f'm{cycles}'].flatten()
        m_intermediates = [result.measurements[f'm{i}'].flatten() for i in range(cycles)]
        
        for shot in range(shots):
            if m_final[shot] == 1:
                detonations += 1
            else:
                any_intermediate_one = False
                for i in range(cycles):
                    if m_intermediates[i][shot] == 1:
                        any_intermediate_one = True
                        break
                if any_intermediate_one:
                    dud_predictions += 1
                else:
                    live_predictions += 1
    else:
        m_final = result.measurements['m0'].flatten()
        for shot in range(shots):
            if m_final[shot] == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
        detonations = 0
        
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
