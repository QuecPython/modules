_loc["speed"] = str(float(rmc_data[7]) * 1.852)
                else:
                    self.__current_loc["speed"] = None
                self.__current_loc["course"] = rmc_data[8]
                self.__current_loc["datestamp"] = rmc_data[9]
                gga_data = self.__nmea_parse.GxGGAData
                if len(gga_data) >= 10:
                    self.__current_loc["altitude"] = gga_data[9]
                else: