def log(st: str, message: str, prefix=None) -> None:
  match st:
    case 'error':
      print(f"\033[41m{prefix if prefix else 'ERROR'} \033[0m{message}")