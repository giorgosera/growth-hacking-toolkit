# This module containts helper functions that can be used across all apps
import re

def is_valid_email(validateString):
	"""
	Receives a string and checks whether this is a valid email addresss. It returns
	True if it is and False otherwise.
	"""
	if re.compile("^.+@.+\..{2,3}$").search(validateString) == None:
		return False
	return True