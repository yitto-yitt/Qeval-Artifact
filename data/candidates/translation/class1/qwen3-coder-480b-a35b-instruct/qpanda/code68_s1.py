# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda import *
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1
    
    # Initialize QPanda environment
    machine = init(QMachineType.CPU)
    prog = QProg()
    qubits = machine.qAlloc_many(1)
    cbits = machine.cAlloc_many(measurements)
    
    # Build the circuit
    for i in range(cycles):
        prog.insert(RY(qubits[0], e))
        if bomb_live:
            prog.insert(Measure(qubits[0], cbits[i]))
    
    # Final measurement
    prog.insert(Measure(qubits[0], cbits[measurements - 1]))
    
    # Run the circuit
    machine.set_configure(shots)
    result = machine.run_with_configuration(prog, cbits, shots)
    
    # Process results
    counts = result
    if bomb_live:
        for key, value in counts.items():
            # Key is in binary string format, need to check bits
            if key[0] == '1':
                detonations += value
            elif '1' in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = counts.get('0' * measurements, 0)
        dud_predictions = counts.get('1' + '0' * (measurements - 1), 0)
        detonations = 0
        
    # Finalize QPanda environment
    finalize()
    
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
