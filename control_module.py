class ControlModel():
    control_mode:tuple
    jump_multipliers:tuple
    speed_multipliers:tuple
    activity:bool = False
    controle_ativo:function
    controle_passivo:function