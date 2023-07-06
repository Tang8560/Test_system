#==========================================================================
# Spectrum Analyzer 268X Interface Library
#
# To access SA268x devices through the API:
#
# 1) Along with one of the following language modules:
#      SA268x_py.py   --  Python API



def power_off(devices):
    devices.write(":SYSTem:POWer:OFF")
    return
#==========================================================================
# SENSE SUBSYSTEM
#==========================================================================

#  6.1 Center Frequency
def center_freq(devices,freq):
    """Sets the center frequency of the spectrum analyzer. Gets the center frequency.
    set: FREQuency:CENTer 0.2 GHz  get: FREQuency:CENTer? """
    output = devices.write("FREQuency:CENTer " + freq)
    return output

# 6.2 Start Frequency
def start_freq(devices,freq):
    """Sets the start frequency of the spectrum analyzer. Gets the start Frequency.
     set: FREQuency:STARt 100 Hz  get: FREQuency:STARt?"""
    output = devices.write("FREQuency:STARt " + freq)
    return output

# 6.3 Stop Frequency
def stop_freq(devices,freq,unit):
    """Sets the stop frequency of the spectrum analyzer. Gets the stop Frequency.
     set: FREQuency:STOP 1.0 GHz  get: FREQuency:STOP?"""
    output = devices.write("FREQuency:STOP " + freq)
    return output

# 6.4 Center Frequency Step Size
def center_freq_step_size(devices,freq,unit):
    """Specifies the center frequency step size. Gets the center frequency step.
     set: FREQuency:CENTer:STEP 2 MHz  get: FREQuency:CENTer:STEP?"""
    output = devices.write("FREQuency:CENTer:STEP " + freq)
    return output

# 6.5 Center Frequency Step Size auto
def center_freq_step_size_auto(devices,state):
    """Specifies whether the step size is set automatically based on the span. Gets center frequency step mode.
     set: FREQuency:CENTer:STEP:AUTO OFF  get: FREQuency:CENTer:STEP:AUTO?"""
    # <state>={OFF,ON or 0,1}
    output = devices.write("FREQuency:CENTer:STEP:AUTO " + state)
    return output

# 6.6 Sets CF -> Steo
def set_center_freq(devices):
    """Sets step value equal to center frequency."""
    output = devices.write("FREQuency:CENTer:SET:STEP")
    return output

# 6.7 Frequency Span
def freq_span(devices,freq):
    """Sets the frequency span. Setting the span to 0 Hz puts the analyzer into zero span
     set: FREQuency:SPAN 1 GHz  get: FREQuency:SPAN?"""
    output = devices.write("FREQuency:SPAN " + freq)
    return output

# 6.8 Span
def span(devices,state):
    """Sets the frequency span.
     parameter={FULL, ZERO, and PREVious}"""
    output = devices.write("FREQuency:SPAN:" + state)
    return output

# 6.9 Zoom
def zoom(devices,parameter):
    """Sets the frequency span to wither halfor double the previous span setting.
     FREQuency:SPAN:HALF   FREQuency:SPAN:DOUBle
     parameter={HALF or DOUBLE}"""
    output = devices.write("FREQuency:SPAN:" + parameter)
    return output

# 6.10 Auto Tune
def auto_tune(devices):
    """Auto tune the spectrum analyzer parameter to display the main signal."""
    output = devices.write("FREQuency:TUNE:IMMediate")
    return output

# 6.11 Reference Level
def reference_level(devices,parameter,unit):
    """Sets the reference level for the Y-axis. Gets reference level.
     set: DISPlay:WINDow:TRACe:Y:RLEVel 20 DBM  get: DISPlay:WINDow:TRACe:Y:RLEVel?"""
    output = devices.write("DISPlay:WINDow:TRACe:Y:RLEVel " + parameter + unit)
    return output

# 6.12 Input Attenuator
def input_attenuator(devices,value):
    """Sets the input attenuator of the spectrum analyzer. Gets the input attenuator.
    set: POWer:ATTenuation 10  get: POWer:ATTenuation?
    value={0 dB 50 dB }"""
    output = devices.write("POWer:ATTenuation " + value)
    return output

# 6.13 Attenuator Auto Mode
def attenuator_automode(devices,state):
    """Turns on/off auto input port attenuator state. Gets input port attenuator state.
    set: POWer:ATTenuation:AUTO OFF get: POWer:ATTenuation:AUTO?
    state={OFF,ON or 1,0}"""
    output = devices.write("POWer:ATTenuation:AUTO " + state)
    return output

# 6.14 Preamp on-off
def preamp(devices,state):
    """Turns the internal preamp on/off. Gets preamp on-off state.
    set: POWer:GAIN ON get: POWer:GAIN?
    state ={OFF,ON or 1,0}"""
    output = devices.write("POWer:GAIN " + state)
    return output

# 6.15 Amplitude Offsets
def amp_offset(devices,value):
    """Sets reference offsets.  Gets reference offsets.
    set: DISPlay:WINDow:TRACe:Y:SCALe:RLEVel:OFFSet 2  get: DISPlay:WINDow:TRACe:Y:SCALe:RLEVel:OFFSet?
    value= {-300dB 300dB}"""
    output = devices.write("DISPlay:WINDow:TRACe:Y:SCALe:RLEVel:OFFSet " + value)
    return output

# 6.16 Amplitude Units
def amp_unit(devices,mode):
    """Specifies amplitude units for the input, output and display. Gets amplitude units.
    set: UNIT:POWer DBMV  get: UNIT:POWer?
    mode={DBM, DBMV, DBUV, V, or W }"""
    output = devices.write("UNIT:POWer " + mode)
    return output

# 6.17 Scale Tupe
def scale_tupe(devices,parameter):
    """Toggles the vertical graticule divisions between logarithmic unit and linear unit.
    The default logarithmic unit is dBm, and the linear unit is V.
    Gets scale type.
    set: DISPlay:WINDow:TRACe:Y:SPACing LINear get: DISPlay:WINDow:TRACe:Y:SPACing?
    parameter={LINear or LOGarithmic}"""
    output = devices.write("DISPlay:WINDow:TRACe:Y:SPACing " + parameter)
    return output

# 6.18 ScaleDiv
def scalediv(devices,integer):
    """Sets the per-division display scaling for the y-axis when scale type of Y axis is set to Log.
    Gets ScaleDiv when scale type of Y axis is set to Log.
    set: DISPlay:WINDow:TRACe:Y:PDIVision 10 dB  get:DISPlay:WINDow:TRACe:Y<:SCALe>:PDIVision?
    integer= {1 dB 10 dB }"""
    output = devices.write("DISPlay:WINDow:TRACe:Y:PDIVision " + integer)
    return output

# 6.19 Correction Off
def corr_Off(devices):
    """Turn off the amplitude correction function off and all of the correction sets are off."""
    output = devices.write("SENSe:CORRection:OFF")
    return output

# 6.20 Correction Apply State
def corr_apply_state(devices,parameter):
    """Turns on or off the amplitude corrections.When turned on, only the correction sets that were turned on are enabled.
    When turned off, all of the correction Sets are disabled. If there is no correction enabled, state can not be set to on.
    set: SENSe:CORRection:CSET:ALL:STATe OFF  get: CORRection:CSET:ALL:STATe?
    parameter={OFF,ON or 0,1}"""
    output = devices.write("SENSe:CORRection:CSET:ALL:STATe " + parameter)
    return output

# 6.21 Corretion X State Off
def corr_Xoff(devices,parameter):
    """Turns the amplitude correction function on/off. Gets the amplitude correction function state.
    set:CORRection:CSET2:OFF  get: CORRection:CSET:STATe?
    parameter={1,2,3, or 4]"""
    output = devices.write("CORRection:CSET" + parameter+":OFF")
    return output

# 6.22 Correction Data
def corr_data(devices,parameter):
    """Set correction X data 1,2,3,4  Read correction X data.
    CORRection:CSET2:DATA?
    parameter={1,2,3, or 4}"""
    output = devices.write("CORRection:CSET" + parameter+":DATA?")
    return output

# 6.23 Current Correction Select
def corr_select(devices,cset,parameter):
    """Set current correction for load COR file onto proper CorrectionX. Read current correction.
    set: CORRection:CSET2:SELect 1  get: CORRection:SELect?
    cset={1,2,3, or 4}
    parameter={1,2,3, or 4}"""
    output = devices.write("CORRection:CSET" + cset + ":SELect" + parameter)
    return output

# 6.24 Load Correction Data
def corr_load(devices,parameter,name):
    """Load correction data.
    MMEMory:LOAD:CORRection:CSET parameter name.COR
    (MMEMory:LOAD:CORRection:CSET1 “oldname.COR)
    parameter={1,2,3, or 4}"""
    output = devices.write("MMEMory:LOAD:CORRection:CSET " + parameter + name + ".COR" )
    return output

# 6.25 Input Impedance
def input_imped(devices,value):
    """Set the input impedance for voltage-to-power conversions. Get the input impedance.
    value={50 OHM or 75 OHM}"""
    output = devices.write("CORRection:IMPedance " + value )
    return output

# 6.26 Resolution Bandwidth
def resolution_bandwidth(devices,parameter,unit):
    """Specifies the resolution bandwidth. For numeric entries, all RBW types choose the nearest
    (arithmetically, on a linear scale, rounding up) available RBW to the value entered."""
    # set: BWIDth 1 KHz  get: BWIDth?
    output = devices.write("BWIDth " + parameter + unit)
    return output

# 6.27 Resolution Bandwidth Auto
def resolution_bandwidth_auto(devices,parameter):
    """Turns on/off auto resolution bandwidth state."""
    # set: BWID:AUTO On  get: BWID:AUTO?
    output = devices.write("BWID:AUTO " + parameter)
    return output

# 6.28 Video Bandwidth
def video_bandwidth(devices,parameter,unit):
    """Specifies the video bandwidth."""
    # set: BWIDth:VIDeo 10 KHZ  get: BWIDth:VIDeo?
    output = devices.write("BWIDth:VIDeo " + parameter + unit)
    return output

# 6.29 Video Bandwidth Auto
def video_bandwidth_auto(devices,parameter):
    """Turns on/off auto video bandwidth state."""
    # set: BWIDth:VIDeo:AUTO OFF  get: BWIDth:VIDeo:AUTO?
    output = devices.write("BWIDth:VIDeo " + parameter)
    return output

# 6.30 Video to Resolution Bandwidth Ratio
def video_resolution_bandwidth_ratio(devices,number):
    """Specifi es the ratio of the video bandwidth to the resolution bandwidth
    set: BWIDth:VIDeo:RATio 30  get: BWIDth:VIDeo:RATio?
    number={0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0 }"""
    output = devices.write("BWIDth:VIDeo:RATio " + number)
    return output

# 6.31 Auto Video to Resolution Bandwidth Ratio State
def AVRBRS(devices):
    """Turns on/off auto video to resolution bandwidth ratio."""
    output = devices.write("BWIDth:VIDeo:RATio:CONfig?")
    return output

# 6.32 Filter Type
def filter_type(devices,parameter):
    """Sets fi lter type. Gets fi lter type
    set: FILTer:TYPE EMI  get: FILTer:TYPE?
    parameter={EMI or GAUSS}"""
    output = devices.write("FILTer:TYPE " + parameter)
    return output

# 6.33 Trace Mode
def Trace_Mode(devices,trace,parameter):
    """Selects the display mode for the selected trace.
    TRACe 1,2,3,4:MODE <parameter>
    TRAC1:MODE VIEW
    trace={1,2,3, or 4}
    parameter ={WRITe, MAXHold, MINHold, VIEW, BLANk, AVERage}
    """

    # WRITe   -- puts the trace in the normal mode, updating the data.
    # MAXHold -- displays the highest measured trace value for all the data that has been measured since the function was turned on.
    # MINHold -- displays the lowest measured trace value for all the data that has been measured since the function was turned on.
    # VIEW    -- turns on the trace data so that it can be viewed on the display.
    # BLANk   -- turns off the trace data so that it is not viewed on the display.
    # AVERage -- averages the trace for test period.

    output = devices.write("TRAC"+ trace +":MODE " + parameter)
    return output

# 6.34 Query Trace Data
def q_trace_data(devices,parameter):
    """Returns the current displayed data.
    parameter>={1,2,3, or 4}"""
    output = devices.query("TRACe:DATA? " + parameter)
    return output

# 6.35 Query Trace Sweep State
def q_trace_sweep(devices):
    """Returns 1 if trace scan is completed else returns 0."""
    output = devices.write("TRACe:SWEep:STATe?")
    return output

# 6.36 Trace Data Format
def trace_dataFormat(devices,parameter):
    """Sets trace data type. Gets trace data type.
    set: FORMat ASCii  get: FORMat?
    parameter={ASCii or REAL}"""
    output = devices.write("FORMat " + parameter)
    return output

# 6.37 Trace Math Type
def trace_mathType(devices,parameter):
    """Sets trace math type. Gets trace math type.
    The lower-case parameters should not be neglected, for example:X-Y+Ref->Z can not write as X-Y+R->Z.
    set: TRACe:MATH:TYPE X-Y+Ref->Z  get: TRACe:MATH:TYPE?
    parameter={off,X-Y+Ref->Z,Y-X+Ref->Z,X+Y-Ref->Z,X+Const->Z,X-Const->Z}"""

    # Off        turns off the trace math function.
    # X-Y+Ref->Z math variable X minus math variable Y and add reference level then to output trace.
    # Y-X+Ref->Z math variable Y minus math variable X and add reference level then to output trace.
    # X+Y-Ref->Z math variable X add math variable Y and minus reference level then to output trace.
    # X+Const->Z math variable X add const then to output trace.
    # X-Const->Z math variable X minus const then to output trace.
    output = devices.write("TRACe:MATH:TYPE " + parameter)
    return output

# 6.38 Trace Math Variable X
def trace_mathX(devices,variable):
    """Sets trace math variable X. Gets trace math variable X.
    set:TRACe:MATH:X A get:TRACe:MATH:X?
    variable={A,B, or C}"""
    output = devices.write("TRACe:MATH:X " + variable)
    return output

# 6.39 Trace Math Variable Y
def trace_mathY(devices,variable):
    """Sets trace math variable Y. Gets trace math variable Y.
    set:TRACe:MATH:Y A get:TRACe:MATH:Y?
    variable={A,B, or C}"""
    output = devices.write("TRACe:MATH:Y " + variable)
    return output

# 6.40 Trace Math Output Z
def trace_mathoutput(devices,variable):
    """Sets trace math output. Gets trace math output.
    set:TRACe:MATH:Z A get:TRACe:MATH:Z?
    variable={A,B, or C}"""
    output = devices.write("TRACe:MATH:Z " + variable)
    return output

# 6.41 Trace Math Const
def trace_mathconst(devices,parameter):
    """Sets trace math const. Gets trace math const.
    set: TRACe:MATH:CONSt 7  get: TRACe:MATH:CONSt?
    parameter={-300dB 300 dB}"""
    output = devices.write("TRACe:MATH:CONSt " + parameter)
    return output

# 6.42 Type of Detection
def type_detection(devices,trace,parameter):
    """Specifies the detection mode. For each trace interval (bucket), average detection displays the average of all the samples within the interval.
    set: DETector:TRAC1 AVERage  get:DETector:TRACe trace?
    DETector:TRACe (trace) (parameter)
    parameter={NEGative, SAMPle, AVERage, NORMAL, QUASi}"""

    # NEGative Negative peak detection displays the lowest sample taken during the interval
    #          being displayed. POSitive: Positive peak detection displays the highest sample
    #          taken during the interval being displayed.

    # SAMPle   Sample detection displays the sample taken during the interval being displayed,
    #          and is used primarily to display noise or noise-like signals. In sample mode, the
    #          instantaneous signal value at the present display point is placed into memory.
    #          This detection should not be used to make the most accurate amplitude measurement of non noise-like signals.

    # AVERage  Average detection is used when measuring the average value of the amplitude
    #          across each trace interval (bucket). The averaging method used by the average detector is set to either video or power as appropriate when the average type is auto coupled.

    # NORMAL   Normal detection selects the maximum and minimum video signal values alternately. When selecting Normal detection,”Norm”appears in the upper-left corner.

    # QUASi    Quasipeak detection is a form of detection where a signal level is weighted based on the repetition
    #          frequency of the spectral components making up the signal. That is to say, the result of a quasi-peak measurement depends on the repetition rate of the signal.
    output = devices.write("DETector:TRAC" + trace + " " + parameter)
    return output

# 6.43 Average Type
def avg_type(devices,mode):
    """Toggle the average type between Log power, power and voltage.
    set: AVERage:TYPE VOLTage  get:AVERage:TYPE?
    mode={LOGPower,POWer, or VOLTage}"""
    output = devices.write("AVERage:TYPE" + mode)
    return output

# 6.44 Average Number
def avg_num(devices,parameter,integer):
    """Specifies the number of measurements that are combined.
    set: AVERage:TRACe1:COUNt 10  get: AVERage:TRACe (parameter):COUNt?
    parameter={1,2,3,or 4}
    integer={1 999}"""
    output = devices.write("AVERage:TRACe" + parameter +":COUNt " + integer )
    return output

# 6.45 Average Restart
def avg_restart(devices,parameter):
    """Restarts the trace average. Only available when average is on.
    AVERage:TRACe(parameter):CLEar
    parameter={1,2,3,or 4}"""
    output = devices.write("AVERage:TRACe" + parameter +":CLEar" )
    return output

# 6.46 SweepMode
def sweep_mode(devices,parameter):
    """Sets sweep mode. Gets sweep mode.
    set: SWEep:MODE SWEep  get: SWEep: MODE?
    parameter={AUTO, FFT, SWEep}"""
    output = devices.write("SWEep:MODE" + parameter )
    return output

# 6.47 Sweep Time
def sweep_time(devices,parameter):
    """Specifies the time in which the instrument sweeps the display. A span value
    of 0 Hz causes the analyzer to enter zero span mode. In zero span the X-axis represents time
    rather than frequency.
    set: SWEep:TIME 5s   get: SWEep:TIME?
    time={917us 1000 s }"""
    output = devices.write("SWEep:TIME" + parameter )
    return output

# 6.48 Sweep Time State
def sweep_timestate(devices,state):
    """Turns on/off auto sweep time state.
    set: SWEep:TIME:AUTO ON  get: SWEep:TIME:AUTO?"""
    output = devices.write("SWEep:TIME:AUTO" + state )
    return output

# 6.49 Sweep Speed
def sweep_speed(devices,parameter):
    """Toggles the sweep speed between normal and accuracy.
    set: SWEep:SPEed NORMal  get: SWEep:SPEed?
    parameter={ACCUracy or NORMal }"""
    output = devices.write("SWEep:SPEed " + parameter )
    return output

# 6.50 Sweep Numbers
def sweep_num(devices,integer):
    """Sets sweep numbers, when single sweep on. Gets sweep numbers, when single sweep on.
    set: SWEep:COUNt 10   get: SWEep:COUNt?
    integer={1 99999 }"""
    output = devices.write("SWEep:COUNt " + integer )
    return output

# 6.51 QPD TIme
def QPD_time(devices,time):
    """Sets QPD Time. Gets QPD Time.
    set: QPD:DWELl:TIME 10s  get: QPD:DWELl:TIME?
    time={0us 10s(qusai-peak: 900us 30ks) }"""
    output = devices.write("QPD:DWELl:TIME " + time )
    return output

# 6.52 Grid Brightness
def grid_brightness(devices,value):
    """Sets grid brightness. Gets grid brightness.
    set: DISPlay:WINDow:TRACe:GRATicule:GRID:BRIGhtness 50 get:TRACe:GRATicule:GRID:BRIGhtness?
    value={0 100 }"""
    output = devices.write("DISPlay:WINDow:TRACe:GRATicule:GRID:BRIGhtnessE " + value )
    return output

# 6.53 Display Line on-off
def display_line_on(devices,parameter):
    """Toggles the display line between on and off. Gets the display line state.
    set: DISPlay:WINDow:TRACe:Y:DLINe:STATe ON  get: DISPlay:WINDow:TRACe:Y:DLINe:STATe?
    parameter={OFF,ON or 0,1 }"""
    output = devices.write("DISPlay:WINDow:TRACe:Y:DLINe:STATe " + parameter )
    return output

# 6.54 Display Line
def display_line(devices,value):
    """Sets the amplitude value for the display line. Gets the amplitude value for the display line.
    set: DISPlay:WINDow:TRACe:Y:DLINe -10   get: DISPlay:WINDow:TRACe:Y:DLINe?
    value={Ref Level Ref Level - 100 dBm }"""
    output = devices.write("DISPlay:WINDow:TRACe:Y:DLINe " + value )
    return output


#==========================================================================
# CALCULATE SUBSYSTEM
#==========================================================================

# 7.1 Marker ON/OFF
def marker_on(devices,trace,parameter):
    """Toggles the selected marker status between on and off. Gets marker state.
    set: CALCulate:MARK1:STATe ON   get: CALCulate:MARKer(trace):STATe?
    trace={1,2,3,4}
    parameter={OFF,ON or 0,1}"""
    output = devices.write("CALCulate:MARK" + trace + ":STATe " + parameter )
    return output


# 7.2 Marker All Off
def marker_all_off(devices):
    """Turn all the markers off."""
    output = devices.write("CALCulate:MARKer:AOFF" )
    return output

# 7.3 Marker Mode
def marker_mode(devices,trace,mode):
    """Selects the type of markers that you want to activate. Gets the type of markers.
    set: CALCulate:MARK1:MODE POSition get: CALCulate:MARKer(parameter):MODE?
    trace={1,2,3,4}
    mode={POSition, DELTa,BAND, OFF}"""
    output = devices.write("CALCulate:MARK" + trace +":MODE " + mode )
    return output

# 7.4 Marker to Trace
def marker_trace(devices,trace):
    """Assigns the specified marker to the designated trace 1, 2, 3 or 4. Gets the specified marker to the designated trace.
    set: CALCulate:MARK:TRAC 1   get: CALCulate:MARKer(trace):TRACe?
    trace={1,2,3,4}"""
    output = devices.write("CALCulate:MARK:TRAC " + trace)
    return output

# 7.5 Marker Relative To
def marker_relative(devices,trace):
    """Sets marker relative to. Gets marker relative to.
    set:CALCulate:MARKer1:RELative:TO:MARK 3  get: CALCulate:MARKer<trace>:RELative:TO:MARKer?
    trace={1,2,3,4}"""
    output = devices.write("CALCulate:MARKer1:RELative:TO:MARK " + trace)
    return output

# 7.6 Marker X Value
def markerX(devices,trace,parameter):
    """Positions the designated marker on its assigned trace at the specified trace X value. The value
    is in the X-axis units, which can be a frequency or time. The query returns the current X value of the
    designated marker. When the readout mode is frequency, the query returns the X value of the span of the marker in integer
    and the unit is “Hz”. When the readout mode is time or period, the query returns the X value of the span of the marker in scientific
    notation and the unit is “s”.
    set: CALCulate:MARKer4:X 0.4 GHz; CALCulate:MARKer4:X 200 ms
    get: CALCulate:MARKer4:X?
    trace={1,2,3,4}
    parameter={0 Hz 3.2 GHz(3.0 GHz, 2.1 GHz, 1.8 GHz, 1.5 GHz, 1.0 GHz) or 10 ms 1000s }
    """
    output = devices.write("CALCulate:MARKer" + trace + ":X " + parameter)
    return output

# 7.7 Reference Marker X Value
def ref_markerX(devices,trace,parameter):
    """Positions the designated reference marker on its assigned trace at the specified trace X value.
    The value is in the X-axis units, which can be a frequency or time. The query returns the current X value of the designated
    reference marker. This command only can be used when marker mode is DELTa, BAND, Reference Command: :CALCulate:MARKer
    1, 2, 3, 4:MODE When the readout mode is frequency, the query returns the X value of the span of the marker in integer and the unit is “Hz”.
    When the readout mode is time or period, the query returns the X value of the span of the marker in scientific notation and the unit is “s”.
    trace={1,2,3,4}
    parameter={0 Hz 3.2 GHz(3.0 GHz, 2.1 GHz, 1.8 GHz, 1.5 GHz, 1.0 GHz) or 10 ms 1000s }
    """
    output = devices.write("CALCulate:MARKer" + trace + ":X:REFerence " + parameter)
    return output

# 7.8 Marker Delta X Value
def markerdX(devices,trace,parameter):
    """This command positions the designated delta marker on its assigned trace at the specified trace
    X value. The value is in the X-axis units, which can be a frequency or time. The query returns the current
    X value of the designated delta marker.
    This command only can be used when marker mode is DELTa, BAND, Reference Command: CALCulate:
    MARKer 1, 2, 3, 4:MODE When the readout mode is frequency, the query returns the X value of the span of the marker in integer
    and the unit is “Hz”.When the readout mode is time or period, the query returns the X value of the span of the marker in scientific notation
    and the unit is “s”.
    trace={1,2,3,4}
    parameter={0 Hz 3.2 GHz(3.0 GHz, 2.1 GHz, 1.8 GHz, 1.5 GHz, 1.0 GHz) or 10 ms 1000s }
    """
    output = devices.write("CALCulate:MARKer" + trace + ":X:CENTer " + parameter)
    return output

# 7.9 Center Pair Marker X Value
def center_pair_markerX(devices,trace,parameter):
    """Sets the center frequency of the center pair marker and the default unit is Hz. Gets the center
    frequency of the center pair marker. This command only can be used when marker mode is DELTa, BAND,
    Reference Command:
    CALCulate:MARKer 1, 2, 3, 4:MODE When the readout mode is frequency, the query returns
    the X value of the span of the marker in integer and the unit is “Hz”. When the readout mode is time or period, the query returns the
    X value of the span of the marker in scientific notation and the unit is “s”.
    trace={1,2,3,4}
    parameter={0 Hz 3.2 GHz(3.0 GHz, 2.1 GHz, 1.8 GHz, 1.5 GHz, 1.0 GHz) or 10 ms 1000s }
    """
    output = devices.write("CALCulate:MARKer" + trace + ":X:DELTa " + parameter)
    return output

# 7.10 Span Pair Marker X Value
def span_Pair_markerX(devices,trace,parameter):
    """Sets the X value corresponding to the span of the Span Pair marker. Gets the X value corresponding
    to the span of the Span Pair marker. This command only can be used when marker mode is DELTa,
    BAND, Reference Command:
    CALCulate:MARKer 1, 2, 3, 4:MODE When the readout mode is frequency, the query returns
    the X value of the span of the marker in integer and the unit is “Hz”. When the readout mode is time or period, the query returns the
    X value of the span of the marker in scientific notation and the unit is “s”.
    trace={1,2,3,4}
    parameter={0 Hz 3.2 GHz(3.0 GHz, 2.1 GHz, 1.8 GHz, 1.5 GHz, 1.0 GHz) or 10 ms 1000s }
    """
    output = devices.write("CALCulate:MARKer" + trace + ":X:SPAN " + parameter)
    return output


# 7.11 Query Marker Y Value
def q_makerY(devices,trace):
    """Reads the current Y value for the designated marker.
    Reads the results of noise marker.
    Make sure that Marker is on
    trace={1,2,3,4}"""
    output = devices.query("CALCulate:MARKer" + trace + ":Y?")
    return output

# 7.12 Reference Marker Y Value
def ref_makerY(devices,trace):
    """Gets the current Y value for the designated reference marker.
    Only avaliable when marker mode is DELTa or BAN.
    trace={1,2,3,4}"""
    output = devices.query("CALCulate:MARKer" + trace + ":Y:REFerence?")
    return output

# 7.13 Marker Delta Y Value
def makerdY(devices,trace):
    """Gets the current Y value for the designated delta marker.
    This command only can be used when marker mode is DELTa, BAND
    trace={1,2,3,4}"""
    output = devices.query("CALCulate:MARKer" + trace + ":Y:DELTa?")
    return output

# 7.14 Marker Table
def marker_table(devices,trace):
    """Sets the start frequency to the value of the specified marker frequency. This command is not
    available in zero span. If the Marker is OFF, it will set the marker on center.
    trace={1,2,3,4}"""
    output = devices.write("CALCulate:MARKer" + trace + ":START")
    return output

# 7.15 Marker to Stop Frequency
def marker_stop_freq(devices,trace):
    """Sets the stop frequency to the value of the specified marker frequency. Not available in zero span.
    If the Marker is OFF, it will set the marker on center.
    trace={1,2,3,4}"""
    output = devices.write("CALCulate:MARKer" + trace + ":STOP")
    return output

# 7.16 Marker to Center Frequency
def marker_center_freq(devices,trace):
    """This command sets the center frequency equal to the specified marker frequency,
    which moves the marker to the center of the screen. Not available in zero span.
    If the Marker is OFF, it will set the marker on center."""
    output = devices.write("CALCulate:MARKer" + trace + ":CENTer")
    return output

# 7.17 Marker to Center Frequency Step
def marker_center_freq_step(devices,trace):
    """This command sets the center frequency step equal to the specified marker frequency.
    Not available in zero span. If the Marker is OFF, it will set the marker on center."""
    output = devices.write("CALCulate:MARKer" + trace + ":STEP")
    return output

# 7.18 Marker to Reference Level
def marker_reference_level(devices,trace):
    """Sets the reference level equal to the specified marker frequency.
    If the Marker is OFF, it will set the marker on center"""
    output = devices.write("CALCulate:MARKer" + trace + ":RLEVel")
    return output

# 7.19 Marker Delta to Center Frequency
def markerdelta_center_freq(devices,trace):
    """sets the center frequency equal to the specified delta marker frequency.
    Can be only used in DELTa, BAND marker mode:
    Reference Command:CALCulate:MARKer<trace>:MODE <mode>"""
    output = devices.write("CALCulate:MARKer" + trace + ":DELTa:CENTer")
    return output

# 7.20 Peak Search
def peak_search_setting(devices,mode):
    """Analyzer’s internal peak identification routine is set to recognize a signal as a peak.
    set: CALCulate:MARKer:PEAK:SEARch:MODE MINimum  get: CALCulate:MARKer:PEAK:SEARch:MODE?
    mode={MAXimum or MINImum}"""
    output = devices.write("CALCulate:MARKer:PEAK:SEARch:MODE" + mode)
    return output


# 7.21 Peak Threshold
def peak_threshold(devices,value):
    """Specifies the minimum signal level for the analyzers internal peak identification routine to recognize
    a signal as a peak. This applies to all traces and all windows. Gets the minimum signal level for the analyzers internal
    peak identification routine to recognize a signal as a peak.

    set: CALCulate:MARKer:PEAK:THReshold -50   get: CALCulate:MARKer:PEAK:THReshold?
    value={ -200.0 dBm 200.0 dBm}"""
    output = devices.write("CALCulate:MARKer:PEAK:THReshold" + value)
    return output

# 7.22 Peak Excursion
def peak_excursion(devices,value):
    """Specifies the minimum signal excursion above the threshold for the
    internal peak identification routine to recognize a signal as a peak.

    set: CALCulate:MARKer:PEAK:EXCursion 10    get: CALCulate:MARKer:PEAK:EXCursion?
    value={0 dBm 200.0 dBm}"""
    output = devices.write("CALCulate:MARKer:PEAK:EXCursion" + value)
    return output


# 7.23 Peak Table
def peak_table(devices,parameter):
    """Toggles the peak table between on and off.
    Gets the status of the peak table.
    set: CALCulate:MARKer:PEAK:TABLe ON    get: CALCulate:MARKer:PEAK:TABLe?
    parameter={OFF, ON or 0,1}"""
    output = devices.write("CALCulate:MARKer:PEAK:TABLe" + parameter)
    return output

# 7.24 Query Peak Table Data
def q_peak_table_data(devices):
    """Return peak table data."""
    output = devices.query("CALCulate:PEAK:TABLe?")
    return output

# 7.25 Continuous Peaking Marker
def continuous_peaking_marker(devices,parameter):
    """Toggles the continuous peak search function between on and off.
    Gets the continuous peak search function state.
    set: CALCulate:MARKer1:CPEak ON   get: CALCulate:MARKer<trace>:CPEak?
    parameter={OFF, ON or 0,1}"""
    output = devices.write("CALCulate:MARKer1:CPEak" + parameter)
    return output

# 7.26 Peak Search
def peak_search(devices,trace):
    """Performs a peak search based on the search mode settings. (based on the search
    mode settings, include: peak search mode, peak threshold and peak excursion.
    trace={1,2,3,4}"""
    output = devices.write("CALCulate:MARKer" + trace + ":MAXimum")
    return output

# 7.27 Next Peak Search
def next_peak_search(devices,trace):
    """Places the selected marker on the next highest signal peak of the current marked peak.
    (based on the search mode settings, include: peak search mode, peak threshold and peak excursion."""
    output = devices.write("CALCulate:MARKer" + trace + ":MAXimum:NEXT")
    return output

# 7.28 Marker Peak Left Search
def marker_peak_left(devices,trace):
    """Places the selected marker on the next highest signal peak to the left of the current marked peak.
    (based on the search mode settings, include: peak search mode, peak threshold and peak excursion."""
    output = devices.write("CALCulate:MARKer" + trace + ":MAXimum:LEFT")
    return output


# 7.29 Marker Peak Right Search
def marker_peak_right(devices,trace):
    """Places the selected marker on the next highest signal peak to the right of the current marked peak.
    (based on the search mode settings, include: peak search mode, peak threshold and peak excursion."""
    output = devices.write("CALCulate:MARKer" + trace + ":MAXimum:RIGHt")
    return output

# 7.30 Peak to Peak Search
def pp_search(devices,trace):
    """Positions a pair of delta markers on the highest and lowest points on the trace.
    trace={1,2,3,4}"""
    output = devices.write("CALCulate:MARKer"+ trace + ":PTPeak")
    return output

# 7.31 Marker Function
def marker_func(devices,trace,parameter):
    """Selects the marker function for the designated marker.
    Gets the selected marker function for the designated marker.
    set: CALCulate:MARK1:FUNCtion FCOunt   get:CALCulate:MARKer (trace):FUNCtion"""
    # <parameter>
    # OFF   refers to the normal function.
    # FCOun refers to the frequency counter function.
    # OISe  refers to the noise measurement function.
    # NDB   refers to the N dB bandwith function.
    output = devices.write("CALCulate:MARK"+ trace + ":FUNCtion "+ parameter)
    return output

# 7.32 Query Frequency Counter
def q_freq_counter(devices,trace):
    """Query the frequency counter"""
    output = devices.query("CALCulate:MARK"+ trace +":FCOunt:X?")
    return output

# 7.33 N dB Bandwidth Result
def N_dB_bandwidth_result(devices,trace):
    """Gets the result of N dB bandwidth measurement."""
    output = devices.query("CALCulate:MARK"+ trace +":BANDwidth:RESult?")
    return output

# 7.34 N dB Bandwidth Reference Value
def N_dB_bandwidth_ref(devices,value):
    """Sets the reference value of N dB bandwidth measurement.
    Gets the reference value of N dB bandwidth measurement.
    set: CALCulate:MARK1:BANDwidth:NDB 10 DB   get: CALCulate:MARK1:BANDwidth:NDB?"""
    output = devices.write("CALCulate:MARK1:BANDwidth:NDBt "+ value)
    return output

# 7.35 Marker X-Axis Read Out
def markX_readout(devices,trace,parameter):
    """set: CALCulate:MARKer1:X:READout FREQuency   get: CALCulate:MARKer (trace) :X:READout?
    trace={1,2,3,4}
    <parameter={FREQuency,TIME, PERiod}"""
    output = devices.write("CALCulate:MARKer" + trace + "MARKer1:X:READout "+ parameter)
    return output

# 7.36 Limit Test
def limit_test(devices,parameter):
    """Sets limit test.
    parameter={STARt, STOP}"""
    output = devices.write("CALCulate:LLINe:TEST:" +  parameter)
    return output

# 7.37 Limit Test State
def limit_teststat(devices):
    """Gets limit test state."""
    output = devices.query("ALCulate:LLINe:TEST:STAT?")
    return output

# 7.38 Limit Line State
def limit_linestat(devices,line,mode ):
    """Sets limit line state. Gets limit line state.
    set: CALCulate:LLINe1:STATe OFF  get: CALCulate:LLINe<line>:STATe?
    line={1 or 2}
    mode={OFF,ON or0,1}"""
    output = devices.write("CALCulate:LLINe"+ line +":STATe " +mode)
    return output

# 7.39 Limit Type
def limit_type(devices,line,parameter ):
    """Mode sets a limit line to be either an upper or lower type limit line. An upper line will be used
    as the maximum allowable value when comparing with the data. Gets limit type.
    set: CALCulate:LLINe1: TYPE LOWer   get: CALCulate:LLINe<line>:TYPE?
    line={1 or 2}
    parameter ={UPPer or LOWer } """
    output = devices.write("CALCulate:LLINe"+ line +":TYPE " +parameter)
    return output

# 7.40 Limit Mode
def limit_mode(devices,line,mode ):
    """Sets limit mode. Gets limit mode.
    set: CALCulate:LLINe1: MODE POINt  get: CALCulate:LLINe(line):MODE?
    line={1 or 2}
    mode={LINE or POINt }"""
    output = devices.write("CALCulate:LLINe"+ line +":Mode " +mode)
    return output

# 7.41 Limit Line Y-axis Value
def limit_lineY(devices,line,value):
    """Sets the Y-axis value of a limit line. Limit line Y-axis value is set independently and is not affected
    by the X-axis units.  Gets the Y-axis value of a limit line.
    set: CALCulate:LLINe1:Y 5dBm    get: CALCulate:LLINe(line):Y?
    line={1 or 2}
    value={-400 dBm 330 dBm }"""
    output = devices.write("CALCulate:LLINe"+ line +":Y " + value)
    return output

# 7.42 Define Limit Points Data
def def_limit_point_data(devices,line,xaxis,amplitude,xaxis1,amplitude1):
    """Use this command to define the limit points. Gets the defined limit points.
    CALCulate:LLINe<line>:DATA (x-axis),(ampl){,(x-axis), (ampl)}
    set: CALC:LLINe1:DATA 10000000,-20,20000000,-30  get:CALCulate:LLINe<line>:DATA?"""
    output = devices.write("CALCulate:LLINe"+ line +":DATA " + xaxis + amplitude + xaxis1 + amplitude1)
    return output

# 7.43 Add Limit Point Data
def add_limit_point_data(devices,line, xaxis,amplitude):
    """Add limit point data
    X-axis={ 0 3.2GHz}
    Amplitude={ No Range}
    ex. CALCulate:LLINe1:ADD 10000000,-20"""
    output = devices.write("CALCulate:LLINe"+ line +":ADD " + xaxis + amplitude)
    return output

# 7.44 Delete Assigned Limit Point
def del_assigned_limit_point(devices,line, number):
    """Use this command to delete the assigned limit point.
    Xline={ 1 or 2}
    number={ No range}"""
    output = devices.write("CALCulate:LLINe"+ line +":ALL:DELete " + number)
    return output

# 7.45 Delete All Limit Points
def del_all_limit_point(devices,line):
    """Use this command to define all the limits points."""
    output = devices.write("CALCulate:LLINe"+ line +":ALL:DELete")
    return output

#==========================================================================
# MEASUREMENT SUBSYSTEM
#==========================================================================
# 8.1 Main Channel
def main_channel(devices, freq):
    """Specifies the range of integration used in calculating the power in the main channel.
    Gets the range of integration used in calculating the power in the main channel
    set: ACPRatio:BWIDth:INTegration 20 MHz   get: ACPRatio:BWIDth:INTegration?
    freq={100 Hz 3.2 GHz(3.0 GHz, 2.1 GHz, 1.8 GHz, 1.5 GHz, 1.0 GHz }"""
    output = devices.write("ACPRatio:BWIDth:INTegration" +freq )
    return output

# 8.2 Adjacent Channel Bandwidth
def adjacent_channel_bandwidth(devices, freq):
    """Specifies the bandwidth used in calculating the power in the adjacent channel.
    Gets the bandwidth used in calculating the power in the adjacent channel.
    set: ACPRatio:OFFSet:BWIDth 20 MHz    get: ACPRatio:OFFSet:BWIDth?
    freq={100 Hz 3.2 GHz(3.0 GHz, 2.1 GHz, 1.8 GHz, 1.5 GHz, 1.0 GHz }"""
    output = devices.write("ACPRatio:OFFSet:BWIDth" +freq )
    return output

# 8.3 Channel Space
def channel_Space(devices, freq):
    """Sets the space value between the center frequency of main channel power
    and that of the adjacent channel power.
    Gets adjacent channel space
    set: ACPRatio:OFFSets 20 MHz   get:ACPRatio:OFFSet?
    freq={100 Hz 700 MHz }"""
    output = devices.write("ACPRatio:OFFSets" +freq )
    return output

# 8.4 Query Main Channel Power
def q_main_channel_power(devices):
    """Return the main channel power of ACPR measurement."""
    output = devices.query("MEASure:ACPRatio:MAIN?" )
    return output

# 8.5 Query Lower Adjacent Channel Power
def q_lower_adjacent_channel_power(devices):
    """Return the lower adjacent channel power of ACPR measurement."""
    output = devices.query("MEASure:ACPRatio:LOWer:POWer?" )
    return output

# 8.6 Query Lower Adjacent Channel Power Ratio
def q_Lower_adjacent_channel_power_ratio(devices):
    """Return the lower adjacent channel power to main channel power ratio."""
    output = devices.query("MEASure:ACPRatio:LOWer?" )
    return output

# 8.7 Query Upper Adjacent Channel Power
def q_upper_adjacent_channel_power(devices):
    """Return the upper adjacent channel power of ACPR measurement."""
    output = devices.query("MEASure:ACPRatio:UPPer:POWer?" )
    return output

# 8.8 Query Upper Adjacent Channel Power Ratio
def q_upper_adjacent_channel_power_ratio(devices):
    """Return the upper adjacent channel power to main channel power ratio."""
    output = devices.query("MEASure:ACPRatio:UPPer?" )
    return output

# 8.9 Integration BW
def Int_BW(devices, freq ):
    """Specifies the integration bandwidth to calculate the power. Gets the integration bandwidth.
    set: CHPower:BWIDth:INTegration 1.8 GHz  get: CHPower:BWIDth:INTegration? """
    # <freq>={100 Hz 3.2 GHz(3.0 GHz, 2.1 GHz, 1.8 GHz, 1.5 GHz, 1.0 GHz)
    # Zero Span: 0 3.2 GHz(3.0 GHz, 2.1 GHz, 1.8 GHz, 1.5 GHz, 1.0 GHz) }
    output = devices.write("CHPower:BWIDth:INTegration " + freq )
    return output

# 8.10 Channel Span
def channel_span(devices):
    """Sets the analyzer span for the channel power measurement. Be sure the span is set larger than the integration bandwidth."""
    output = devices.write("CHPower:FREQuency:SPAN:POWer")
    return output

# 8.11 Query Channel Power and Power Spectral Density
def q_channel_PSD(devices):
    """Returns scalar results of main channel power, and power density"""
    output = devices.query("MEASure:CHPower?")
    return output

# 8.12 Query Channel Power
def q_channel_power(devices):
    """This command returns the value of the channel power in dBm units."""
    output = devices.query("MEASure:CHPower:CHPower?")
    return output

# 8.13 Query Power Spectral Density
def q_PSD(devices):
    """This command returns the value of the channel power density in dBm/Hz"""
    output = devices.query("MEASure:CHPower:DENSity?")
    return output

# 8.14 Select the Method of OBW
def OBW(devices, parameter):
    """This command toggles the method of OBW measurement between percent and dBc.
    Gets the method of OBW measurement.
    set: OBW:METHod PERCent   get: OBWidth:METHod?
    parameter={PERCent or DBC}"""
    output = devices.write("OBW:PERCent " + parameter)
    return output

# 8.15 Percentage Method of OBW
def percentage_method_OBW(devices, parameter):
    """Edit the percentage of signal power used when determining the occupied bandwidth.
    Press {%} to set the percentage ranging from 10.00% to 99.99%.
    Gets the percentage of signal power.
    set: OBW:PERCent 50  get: OBWidth:PERCent?
    parameter ={10 99.99}"""
    output = devices.write("OBW:PERCent " + parameter)
    return output

# 8.16 dBc Method of OBW
def dBc_OBW(devices, value):
    """Specify the power level used to determine the emission bandwidth as the number of dB
    down from the highest signal point, within the occupied bandwidth span.
    Gets dBc value.
    set: OBWidth:XDB 3  get: OBWidth:XDB?
    value ={0.1 100 }"""
    output = devices.write("OBWidth:XDB " + value)
    return output

# 8.17 Query OBW and Centroid
def q_OBWC(devices):
    """Use this command to query the occupied bandwidth and bandwidth centroid according to the
    method you set."""
    output = devices.query("MEASure:OBWidth?")
    return output

# 8.18 Query OBW
def q_OBW(devices):
    """Use this command to query the occupied bandwidth according to the method you set.
    Query Centroid Result."""
    output = devices.query("MEASure:OBWidth:OBWidth?")
    return output

# 8.19 Query OBW Centroid
def q_OBW_C(devices):
    """Use this command to query the occupied bandwidth according to the method you set."""
    output = devices.query("MEASure:OBWidth:CENTroid?")
    return output

# 8.20 Query Transmit Frequency Error
def q_transmit_freqerror(devices):
    """Use this command to query transmit frequency error."""
    output = devices.query("MEASure:OBWidth:OBWidth:FERRor?")
    return output

# 8.21 T-Power Center Frequency
def tpower_center_freq(devices, freq):
    """Sets T-power center frequency.. Gets T-power center frequency.
    set: TPOWer:FREQuency:CENTer 15KHz   get: TPOWer:FREQuency:CENTer? """
    # <freq>={50 Hz 3.199999950 GHz(2.999999950 GHz, 2.099999950 GHz,
    # 1.799999950 GHz, 1.499999950 GHz, 0.999999950 GHz
    # Zero Span: 0 3.2 GHz(3.0 GHz, 2.1 GHz, 1.8 GHz, 1.5 GHz, 1.0 GHz}
    output = devices.write("TPOWer:FREQuency:CENTer " + freq)
    return output

# 8.22 T-Power Start Line
def tpower_start(devices, time):
    """Sets T-power start line. Gets T-power start line.
    set: TPOWer:LLIMit 0.01   get: TPOWer:LLIMit?
    time={0 1000 s }"""
    output = devices.write("TPOWer:LLIMit " + time)
    return output

# 8.23 T-Power Stop Line
def tpower_stop(devices, time):
    """Sets T-power stop line. Gets T-power stop line.
    set: TPOWer:RLIMit 0.02   get: TPOWer:RLIMit?
    time={0 1000 s }"""
    output = devices.write("TPOWer:RLIMit " + time)
    return output

# 8.24 Query T-Power
def q_tpower(devices):
    """Query the result of T-power measurement."""
    output = devices.query("MEASure:TPOWer?")
    return output

# 8.25 Spectrogram State
def spectrogram_state(devices,parameter):
    """Sets spectrogram state. Gets spectrogram state.
    set: SPECtrogram:STATe PAUSe  get: SPECtrogram:STATe?
    parameter={RUN or PAUSe}"""
    output = devices.write("SPECtrogram:STATe " +parameter)
    return output

# 8.26 Spectrogram Restart
def spectrogram_restart(devices):
    """Restart spectrogram."""
    output = devices.write("SPECtrogram:RESTart")
    return output

# 8.27 Query Third-order Intercept Point result
def q_3intercept_Point_result(devices):
    """Gets the result of Third-order Intercept Point"""
    output = devices.query("MEASure:TOI?")
    return output

# 8.28 Query Third-order Intercept Point
def q_3intercept_Point(devices):
    """Gets the min intercept of the Lower TOI(Lower 3rd) and the Upper TOI(Upper 3rd)"""
    output = devices.query("MEASure:TOI:IP3?")
    return output
#==========================================================================
# TRIGGER SUBSYSTEM
#==========================================================================
# 9.1 Trigger Type
def trigger_type(devices,parameter):
    """Specifies the source (or type) of triggering used to start a measurement. Gets trigger type
    TRIGger[:SEQuence]:SOURce (parameter)
    set: TRIGger:SOURce IMMediate   get: TRIGger[:SEQuence]:SOURce?"""
    # <parameter>
    # IMMediate   free-run triggering.
    # VIDeo       triggers on the video signal level.
    # EXTernal    allows you to connect an external trigger source.
    output = devices.write("TRIGger:SOURce " + parameter )
    return output

# 9.2 Video Trigger Level
def video_trigger_level(devices,value):
    """Specifies the level at which a video trigger will occur.
    Video is adjusted using this command, but must also be selected using the command.
    Gets video Trigger Level.

    set: TRIGger:VIDeo:LEVel 0.5 dBm  get: TRIGger:VIDeo:LEVel?
    TRIGger:VIDeo:LEVel (value)  """
    # <value ranges>
    # Unit is dBm: -300 dBm 50 dBm
    # uni is dBmV: -253.01 dBmV 96.99 dBmV
    # unit is dBuV: -193.01 dBuV 156.99 dBuV
    # unit is Volts: 223.61 aV 70.71 V
    # unit is Watts: 1.00E-33 W 100 W
    output = devices.write("TRIGger:VIDeo:LEVel " + value )
    return output

# 9.3 Trigger Edge
def trigger_edge(devices,parameter):
    """Activates the trigger condition that allows the next sweep to start when the external voltage
    (connected to EXT TRIG IN connector) passes through approximately 1.5 volts. The external
    trigger signal must be a 0V to +5V TTL signal. This function only controls the trigger polarity (for positive or negativegoing signals).
    Gets Trigger edge.

    set: TRIGger:RFBurst:SLOPe POSitive   get: TRIGger:RFBurst:SLOPe?
    parameter={POSitive or NEGative}
    """
    output = devices.write("TRIGger:RFBurst:SLOPe " + parameter )
    return output
#==========================================================================
# TG SUBSYSTEM
#==========================================================================
# 10.1 TG On-Off 追蹤發生器 (trace generator)
def TG(devices,state):
    """Sets TG on-off. Gets TG state.
    set: OUTPut ON   get: OUTPut[:STATe]?
    state={OFF, ON or 0,1}"""
    output = devices.write("OUTPut " + state )
    return output

# 10.2 TG Level
def TG_level(devices,value):
    """Sets TG level. Gets TG level.
    set: SOURce:POWer -20  get: SOURce:POWer?
    value={0 dBm -20 dBm }"""
    output = devices.write("SOURce:POWer " + value )
    return output

# 10.3 TG Level Offsets
def TG_level_offset(devices,value):
    """Sets TG level offsets. Gets TG level offsets.
    set: SOURce:CORRection:OFFSet 1  get: SOURce:CORRection:OFFSet?
    value={200 dBm 200 dBm }"""
    output = devices.write("SOURce:CORRection:OFFSet" + value )
    return output

# 10.4 TG Normalize on-off
def TG_normalize(devices,parameter):
    """Sets TG normalize on-off. Gets TG normalize state.
    set: CALCulate:NTData ON  get: CALCulate:NTData?
    parameter={OFF, ON or 0, 1}"""
    output = devices.write("CALCulate:NTData " + parameter )
    return output

# 10.5 TG Normalize Reference Level
def TG_normalize_ref_level (devices,value):
    """Sets TG normalize reference level. Gets TG normalize reference level.
    set: DISPlay:WINDow:TRACe:Y:NRLevel 10  get: DISPlay:WINDow:TRACe:Y:NRLevel?
    value={200 dB 200 dB }"""
    output = devices.write("DISPlay:WINDow:TRACe:Y:NRLevel " +value )
    return output

# 10.6 TG Normalize Reference Position
def TG_normalize_ref_pos(devices,integer):
    """Sets TG normalize reference position. Gets TG normalize reference position.
    set: DISPlay:WINDow:TRACe:Y:NRPosition 10   get: DISPlay:WINDow:TRACe:Y:NRPosition?
    integer ={0 100%}"""
    output = devices.write("DISPlay:WINDow:TRACe:Y:NRPosition " +integer )
    return output

# 10.7 TG Normalize Reference Trace on-off
def TG_normalize_trace(devices,parameter):
    """Sets TG normalize reference trace on-off.
    set: DISPlay:WINDow:NTTRace ON   get: DISPlay:WINDow:NTTRace?
    parameter={OFF, ON or 0, 1}"""
    output = devices.write("DISPlay:WINDow:NTTRace " +parameter )
    return output

#==========================================================================
# DEMOD SUBSYSTEM
#==========================================================================
# 11.1 Demod Mode
def demod_mode(devices,mode):
    """Sets demod mode. Gets demod mode.
    set: DEMod AM  get: DEMod?
    mode={AM, FM, OFF}"""
    output = devices.write("DEMod " +mode )
    return output

# 11.2 Demod Tim
def demod_tim(devices,time):
    """Sets demod time. Gets demod time.
    set: DEMod:TIME 5 ms  get: DEMod:TIME?
    time={5 ms 1000 s}"""
    output = devices.write("DEMod:TIME " + time )
    return output

# 11.3 Earphone
def earphone(devices,parameter):
    """Sets earphone on-off. Gets earphone on-off.
    set: DEMod:EPHone ON  get: DEMod:EPHone?
    parameter={OFF, ON or 0, 1}"""
    output = devices.write("DEMod:EPHone" + parameter )
    return output
# 11.4 Volume
def volume(devices,value ):
    """Sets volume value. Gets volume value.
    set: DEMod:VOLume 5  get:DEMod:VOLume?
    value={0 10}"""
    output = devices.write("DEMod:VOLume" + value )
    return output

#==========================================================================
# CALIBRATION SUBSYSTEM
#==========================================================================

# 12.1 Calibration On-Off
def calibration(devices,parameter):
    """Sets calibration on-off. Gets calibration on-off.
    set: CALibration:STATe ON  get: CALibration:STATe?
    parameter={OFF, ON or 0, 1} """
    output = devices.write("CALibration:STATe" + parameter)
    return output

#==========================================================================
# MEMORY SUBSYSTEM
#==========================================================================
# input : type <str> file <str>
#--------------------------------------------------------------------------

# 13.1 Store File
def store(devices,Type,file):
    """ MMEMory:STORe<Type>,<file>
        <Type>={STA, TRC, COR, CSV, LIM, JPG, BMP, PNG} """
    # MMEMory:STORe STA,ABC.sta
    output = devices.write("MMEMory:STORe" + Type +',' + file)
    return output

# 13.2 Load File
def load(devices,Type,file):
    """MMEMory:LOAD <Type>,<file>
        <Type>={STA, TRC, COR, LIM }"""
    # MMEMory:LOAD STA,ABC.sta
    output = devices.write("MMEMory:LOAD" + Type +',' + file)
    return output

# 13.3 Delete File
def delete(devices,Type,file):
    """MMEMory:DELete <file>"""
    output = devices.write("MMEMory:DELete" + file)
    return output










































