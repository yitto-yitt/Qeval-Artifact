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
                qml.sample(qml.PauliZ(wires=0))
        return qml.sample(qml.PauliZ(wires=0))

    results = circuit()

    if bomb_live:
        # Reshape results to match measurement pattern
        reshaped_results = results.reshape(-1, measurements)
        for outcome in reshaped_results:
            # Convert from {-1, 1} to {0, 1}
            bits = [(1 - x) // 2 for x in outcome]
            if bits[0] == 1:  # First measurement is 1 (detonation)
                detonations += 1
            elif 1 in bits[1:]:  # Any subsequent measurement is 1 (dud prediction)
                dud_predictions += 1
            else:  # All subsequent measurements are 0 (live prediction)
                live_predictions += 1
    else:
        # Only final measurement matters when bomb is not live
        outcomes = [(1 - x) // 2 for x in results]
        for bit in outcomes:
            if bit == 0:  # Measured 0 -> live prediction
                live_predictions += 1
            else:  # Measured 1 -> dud prediction
                dud_predictions += 1
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
