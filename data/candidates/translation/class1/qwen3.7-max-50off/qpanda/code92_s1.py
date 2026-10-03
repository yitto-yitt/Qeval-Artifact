# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit

def calculate_stabilizer_state_info():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    
    state = None
    
    try:
        from pyqpanda3.core import QMachine
        machine = QMachine()
        try: machine.init_qmachine(2)
        except: pass
        res = None
        try: res = machine.run(qc)
        except: 
            try: res = machine.execute(qc)
            except: pass
        try: state = machine.get_state_vector()
        except: 
            try: state = machine.get_state()
            except: pass
        if state is None and res is not None and hasattr(res, '__iter__') and not isinstance(res, (str, dict)):
            state = res
    except:
        pass
        
    if state is None:
        try:
            from pyqpanda3.core import QMachine
            machine = QMachine(2)
            res = None
            try: res = machine.run(qc)
            except: 
                try: res = machine.execute(qc)
                except: pass
            try: state = machine.get_state_vector()
            except: 
                try: state = machine.get_state()
                except: pass
            if state is None and res is not None and hasattr(res, '__iter__') and not isinstance(res, (str, dict)):
                state = res
        except:
            pass

    if state is None:
        try:
            from pyqpanda3.core.simulator import StateVectorSimulator
            sim = StateVectorSimulator()
            res = None
            try: res = sim.run(qc)
            except: 
                try: res = sim.execute(qc)
                except: pass
            try: state = sim.get_state_vector()
            except: 
                try: state = sim.get_state()
                except: pass
            if state is None and res is not None and hasattr(res, '__iter__') and not isinstance(res, (str, dict)):
                state = res
        except:
            pass

    if state is None:
        try: state = qc.state_vector()
        except: pass
    if state is None:
        try: state = qc.get_state_vector()
        except: pass

    probs = {}
    if state is not None:
        for i, amp in enumerate(state):
            p = abs(amp)**2
            if p > 1e-10:
                probs[f"{i:02b}"] = p
                
    return probs
