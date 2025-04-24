import sys
from .logger import logging


def eror_detailed(error, error_details: sys):
    _, _, error_tb = error_details.exc_info()
    er_fname = error_tb.tb_frame.f_code.co_filename

    error_msg = f'''\n Error occured in {er_fname} \n at line {error_tb.tb_lineno} \n with message: {str(error)}\n'''
    logging.error(error_msg)
    return error_msg


class Custom_Error(Exception):
    def __init__(self, error_msg, eror_details):
        super().__init__(error_msg)
        self.eror_details = eror_details
        self.error_msg = eror_detailed(error_msg, eror_details)

    def __str__(self):
        return self.error_msg


if __name__ == "__main__":
    try:
        pass
    except Exception as e:
        raise Custom_Error(e, sys)
