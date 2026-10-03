# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1
    
    dev = qml.device("default.qubit", wires=1, shots=shots)

    @qml.qnode(dev)
    def circuit():
        for i in range(cycles):
            qml.RY(e, wires=0)
        
        results = []
        if bomb_live:
            for i in range(cycles):
                results.append(qml.sample(qml.PauliZ(0)))
            results.append(qml.sample(qml.PauliZ(0)))  # final measurement
        else:
            results.append(qml.sample(qml.PauliZ(0)))  # just final measurement
        
        return [qml.expval(r) for r in results]  # This won't work as intended; need to collect samples differently

    # Need to run multiple times to get sample outcomes
    dev = qml.device("default.qubit", wires=1, shots=shots)
    
    @qml.qnode(dev)
    def run_experiment():
        for i in range(cycles):
            qml.RY(e, wires=0)
        
        # Collect all measurements if bomb is live
        if bomb_live:
            outcomes = []
            for i in range(cycles):
                outcomes.append(qml.sample(qml.PauliZ(0)))
            outcomes.append(qml.sample(qml.PauliZ(0)))  # final measurement
            return outcomes
        else:
            # Only final measurement if bomb is not live
            return qml.sample(qml.PauliZ(0))
    
    results = run_experiment()
    
    if bomb_live:
        # Convert results to bit strings and count outcomes
        # results shape will be (measurements, shots) -> each row is outcomes for one measurement
        # Transpose so we have (shots, measurements)
        if len(results.shape) > 1:
            result_transposed = results.T
        else:
            result_transposed = results.reshape(-1, 1)
            
        for shot_idx in range(shots):
            # Convert -1,1 values to 0,1
            bits = [(1 - result_transposed[shot_idx][i]) // 2 for i in range(len(result_transposed[shot_idx]))]
            bit_string = ''.join(map(str, bits))
            
            if bit_string[0] == '1':  # First measurement determines detonation
                detonations += 1
            elif '1' in bit_string[1:]:  # Any later measurement being 1 indicates dud
                dud_predictions += 1
            else:  # All later measurements are 0 means live prediction
                live_predictions += 1
    else:
        # For non-live bomb case, results is 1D array of final measurements
        for outcome in results:
            if outcome == 1:  # |0> state measured -> corresponds to '0'
                live_predictions += 1
            else:  # |1> state measured -> corresponds to '1'
                dud_predictions += 1
        # No detonations possible if bomb isn't live
        detonations = 0
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
