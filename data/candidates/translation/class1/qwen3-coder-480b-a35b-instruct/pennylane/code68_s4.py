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
            if bomb_live:
                qml.sample(wires=0)  # This simulates intermediate measurement
        return qml.sample(wires=0)

    results = circuit()

    if bomb_live:
        # Reshape results to match the pattern of measurements
        reshaped_results = results.reshape(-1, measurements)
        
        for outcome in reshaped_results:
            # First measurement determines detonation
            if outcome[0] == 1:
                detonations += 1
            elif 1 in outcome[1:]:
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        # For dud bomb, only final measurement matters
        final_measurements = results
        for outcome in final_measurements:
            if outcome == 0:
                live_predictions += 1
            else:
                dud_predictions += 1
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
