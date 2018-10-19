import logging; logger = logging.getLogger("morse." + __name__)

import morse.core.sensor

from morse.core.services import service, async_service
from morse.core import status
from morse.helpers.components import add_data, add_property

import bge


class Screenshots( morse.core.sensor.Sensor ):
	"""Write here the general documentation of your sensor.
	It will appear in the generated online documentation.
	"""
	_name = "Screenshots"
	_short_desc = ""

	def __init__(self, obj, parent=None):
		logger.info("%s initialization" % obj.name)
		# Call the constructor of the parent class
		morse.core.sensor.Sensor.__init__(self, obj, parent)

		# Do here sensor specific initializations

		self.filename = '/tmp/morse_screenshot_#'

		logger.info('Component initialized')

	@service
	def get_current_distance(self):
		""" This is a sample (blocking) service (use 'async_service' decorator
		for non-blocking ones).

		Simply returns the value of the internal counter.

		You can access it as a RPC service from clients.
		"""
		logger.info("%s is %sm away" % (self.name, self.local_data['distance']))

		#return self.local_data['distance']

	def default_action(self):
		""" Main loop of the sensor.

		Implements the component behaviour
		"""

		bge.render.makeScreenshot( self.filename )


