import sys
import os

def get_error_msg_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    filename=exc_tb.tb_frame.f_code.co_filename
    lineno=exc_tb.tb_lineno
    error_msg=f"The error was found in filename :{filename} and line no: {lineno} and error message is {error}"

    return error_msg

class CustomException(Exception):
    def __init__(self,error_msg,error_detail:sys):
        super().__init__(error_msg)
        self.error_msg=get_error_msg_detail(error=error_msg,error_detail=error_detail)

    def __str__(self):
        return self.error_msg