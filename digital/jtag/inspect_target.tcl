# Sourced inside a preconnected Vivado batch job.
set devices [get_hw_devices -of_objects [current_hw_target]]
foreach device $devices {
    puts "[get_property NAME $device]: [get_property PART $device]"
}
set devices
