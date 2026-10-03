# EVAL_META: task_id=68, framework=cirq, class=1
import cirq
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = np.pi / cycles
    
    qubit = cirq.LineQubit(0)
    circuit = cirq.Circuit()
    
    if bomb_live:
        for i in range(cycles):
            circuit.append(cirq.ry(e).on(qubit))
            circuit.append(cirq.measure(qubit, key=f'm_{i}'))
        circuit.append(cirq.measure(qubit, key=f'm_{cycles}'))
        
        sim = cirq.Simulator()
        result = sim.run(circuit, repetitions=shots)
        
        for shot in range(shots):
            final_meas = result.measurements[f'm_{cycles}'][shot][0]
            intermediate_meas = [result.measurements[f'm_{i}'][shot][0] for i in range(cycles)]
            
            if final_meas == 1:
                detonations += 1
            elif 1 in intermediate_meas:
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        for i in range(cycles):
            circuit.append(cirq.ry(e).on(qubit))
        circuit.append(cirq.measure(qubit, key='m_0'))
        
        sim = cirq.Simulator()
        result = sim.run(circuit, repetitions=shots)
        
        for shot in range(shots):
            meas = result.measurements['m_0'][shot][0]
            if meas == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
                
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
