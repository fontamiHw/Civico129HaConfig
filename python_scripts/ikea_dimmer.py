""" Brighten a light, then return to previous brightness state """ 
# from:
# https://community.home-assistant.io/t/brighten-a-light-then-return-to-previous-brightness-state/20802

# Get Params
entity_id  = data.get('entity_id')
action 	   = data.get('action')
br_level = int(data.get('step_brightness'))
color_level = int(data.get('step_color'))

# Get current brightness value
states     = hass.states.get(entity_id)
brightness = states.attributes.get('brightness') or 0
color = states.attributes.get('color_temp') or 0

exit = True
# Set new brightness value
if action == 'arrow_right_click'   : 
  newValue = (color + color_level)
  exit = False
  sub_action = 'color'
if action == 'arrow_left_click' : 
  newValue = (color - color_level)
  exit = False
  sub_action = 'color'
if action == 'brightness_up_click'   : 
  newValue = (brightness + br_level)
  exit = False
  sub_action = 'dimmer'
if action == 'brightness_down_click' : 
  newValue = (brightness - br_level)
  exit = False
  sub_action = 'dimmer'

# if not one of the requested action....... exit
if exit == False :

  # Manage the dimmer of Light
  if sub_action == 'dimmer': 
    if newValue <= 0 			: newValue = 0
    if newValue >= 254			: newValue = 254

    # Call service
    logger.info("New Dimmer value for " + entity_id + " is = " + str(newValue))
    if newValue == 0 :
      logger.info('Tuning off ' + str(entity_id))
      data = { "entity_id" : entity_id }
      hass.services.call('light', 'turn_off', data)
    else :
      logger.info('Dimming' + str(entity_id) + 'from : ' + str(brightness) + ' to ' + str(newValue))
      data = { "entity_id" : entity_id, "brightness" : newValue }
      hass.services.call('light', 'turn_on', data)



  # Manage the color of Light
  if sub_action == 'color': 
    if newValue <= 153 : newValue =500
    if newValue >= 501 : newValue = 153

    # Call service
    logger.info('Coloring' + str(entity_id) + ' from : ' + str(color) + ' to ' + str(newValue))
    data = { "entity_id" : entity_id, "color_temp" : newValue }
    hass.services.call('light', 'turn_on', data)


