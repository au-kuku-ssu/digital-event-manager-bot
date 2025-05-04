from components.reports_evaluation.data.placeholder_jury import PLACEHOLDER_JURY

async def re_check_access_code(code: str):
  """
  Checks if access code is valid.
  """
  jury_data = PLACEHOLDER_JURY

  for juror in jury_data:
    if juror == code:
      return juror

  return None
