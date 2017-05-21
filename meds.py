class MEDSProfile(object):
	'''
	text: MEDS string (one per line in data files)
	'''

	def __init__(self, text):

		# header info will be in raw[0]; profiles will sit in each subsquent index.
		self.raw = text.split('\n')

	 	###########################
	 	# format definition
	 	###########################

	 	self.header_format = {
	 		'MKey': [8,0,str],
	 		'One_Deg_sq': [8,8,str],
	 		'Cruise_ID': [10,16,str],
	 		'Obs_Year': [4,26,int],
	 		'Obs_Month': [2,30,int],
	 		'Obs_Day': [2,32,int],
	 		'Obs_Time': [4,34,float],
	 		'Data_Type': [2,38,str],
	 		'Iumsgno': [12,40,str],
	 		'Stream_Source': [1,52,str],
	 		'UFlag': [1,53,str],
	 		'Stn_Number': [8,54,int],
	 		'Latitude': [8,62,float],
	 		'Longitude': [9,70,float],
	 		'Q_Pos': [1,79,str],
	 		'Q_Date_Time': [1,80,str],
	 		'Q_Record': [1,81,str],
	 		'Up_Date': [8,82,str],
	 		'Bul_Time': [12,90,str],
	 		'Bul_Header': [6,102,str],
	 		'Source_ID': [4,108,str],
	 		'Stream_Ident': [4,112,str],
	 		'QC_Version': [4,116,str],
	 		'Data_Avail': [1,120,str],
	 		'No_Prof': [2,121,int],
	 		'Nparms': [2,123,int],
	 		'Nsurfc': [2,125,int],
	 		'Num_Hists': [3,127,int]
	 	}
	 	self.header_offset = 130

	 	self.profile_meta_format = {
	 		'No_Seg': [2,0,int],
	 		'Prof_Type': [4,2,str],
	 		'Dup_flag': [1,6,str],
	 		'Digit_Code': [1,7,str],
	 		'Standard': [1,8,str],
	 		'Deep_Depth': [5,9,float]
	 	}
	 	self.profile_meta_offset = 14

	 	self.surface_parms_format = {
	 		'Pcode': [4,0,str],
	 		'Parm': [10,4,str],
	 		'Q_Parm': [1,14,str]
	 	}
	 	self.surface_parms_offset = 15

	 	self.surface_codes_format = {
	 		'SRFC_Code': [4,0,str],
	 		'SRFC_Parm': [10,4,str],
	 		'SRFC_Q_Parm': [1,14,str]
	 	}
	 	self.surface_codes_offset = 15

	 	self.history_format = {
	 		'Ident_Code': [2,0,str],
	 		'PRC_Code': [4,2,str],
	 		'Version': [4,6,str],
	 		'PRC_Date': [8,10,str],
	 		'Act_Code': [2,18,str],
	 		'Act_Parm': [4,20,str],
	 		'Aux_ID': [8,24,str],
	 		'Previous_Val': [10,32,str]
	 	}
	 	self.history_offset = 42

	 	self.profile_header_format = {
	 		'MKey': [8,0,str],
	 		'One_Deg_sq': [8,8,str],
	 		'Cruise_ID': [10,16,int],
	 		'Obs_Year': [4,26,int],
	 		'Obs_Month': [2,30,int],
	 		'Obs_Day': [2,32,int],
	 		'Obs_Time': [4,34,float],
	 		'Data_Type': [2,38,str],
	 		'Iumsgno': [12,40,str],
	 		'Profile_Type': [4,52,str],
	 		'Profile_Seg': [2,56,int],
	 		'No_Depths': [4,58, int],
	 		'D_P_Code': [1,62,str]
	 	}
	 	self.profile_header_offset = 63

	 	self.level_format = {
	 		'Depth_Press': [6,0,float],
	 		'Depres_Q': [1,6,str],
	 		'Prof_Parm': [9,7,float],
	 		'Prof_Q_Parm': [1,16,str]
	 	}
	 	self.level_offset = 17

	# data methods

	def header(self, parameter):
		start = self.header_format[parameter][1]
		length = self.header_format[parameter][0]
		parse = self.header_format[parameter][2]

		return parse(self.raw[0][start:start+length])

	def profile_metadata(self, parameter, index=0):

		# return None if index out of range
		if index >= self.header('No_Prof'):
			return None

		offset = self.header_offset + self.profile_meta_offset*index
		start = offset + self.profile_meta_format[parameter][1]
		length = self.profile_meta_format[parameter][0]
		parse = self.profile_meta_format[parameter][2]

		return parse(self.raw[0][start:start+length])

	def surface_parameters(self, parameter, index=0):

		# return None if index out of range
		if index >= self.header('Nparms'):
			return None

		offset = self.header_offset + self.profile_meta_offset*self.header('No_Prof') + self.surface_parms_offset*index
		start = offset + self.surface_parms_format[parameter][1]
		length = self.surface_parms_format[parameter][0]
		parse = self.surface_parms_format[parameter][2]

		return parse(self.raw[0][start:start+length])

	def surface_codes(self, parameter, index=0):

		# return None if index out of range
		if index >= self.header('Nsurfc'):
			return None

		offset = self.header_offset + self.profile_meta_offset*self.header('No_Prof') + self.surface_parms_offset*self.header('Nparms') + self.surface_codes_offset*index
		start = offset + self.surface_codes_format[parameter][1]
		length = self.surface_codes_format[parameter][0]
		parse = self.surface_codes_format[parameter][2]

		return parse(self.raw[0][start:start+length])	

	def history(self, parameter, index=0):

		# return None if index out of range
		if index >= self.header('Num_Hists'):
			return None

		offset = self.header_offset + self.profile_meta_offset*self.header('No_Prof') + self.surface_parms_offset*self.header('Nparms') + self.surface_codes_offset*self.header('Nsurfc') + self.history_offset*index
		start = offset + self.history_format[parameter][1]
		length = self.history_format[parameter][0]
		parse = self.history_format[parameter][2]

		return parse(self.raw[0][start:start+length])

	def profile_header(self, parameter, index=0):

		# return None if index out of range
		if index >= len(self.raw)-1:
			return None

		start = self.profile_header_format[parameter][1]
		length = self.profile_header_format[parameter][0]
		parse = self.profile_header_format[parameter][2]

		return parse(self.raw[index+1][start:start+length])

	def profile_data(self, parameter, index=0):

		# return None if index out of range
		if index >= len(self.raw)-1:
			return None

		offset = self.profile_header_offset
		n_levels = self.profile_header('No_Depths', index)
		depth = []
		var = []

		for i in range(n_levels):
			o = offset + self.level_offset*i

			start = o + self.level_format['Depth_Press'][1]
			length = self.level_format['Depth_Press'][0]
			parse = self.level_format['Depth_Press'][2]
			depth.append(parse(self.raw[index+1][start:start+length]))

			start = o + self.level_format[parameter][1]
			length = self.level_format[parameter][0]
			parse = self.level_format[parameter][2]
			var.append(parse(self.raw[index+1][start:start+length]))
	
		return depth, var









