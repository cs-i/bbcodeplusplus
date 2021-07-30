import re
from collections import namedtuple

Token = namedtuple("Token", ["name", "has_params", "has_closing_token"])
ParsedToken = namedtuple("ParsedToken", ["name", "input_string"])

def _multi_replace(olds, news, string):
  for old, new in zip(olds, news):
    string = string.replace(old, new)
  return string

def tokenize(token_types, string):
  unsorted_tokens = []
  for token in token_types:
    # Generate token regex
    if token.has_params is True:
      if token.has_closing_token is False:
        token_regex = r"\[" + token.name + r"[^\]]*?\]"
      else:
        token_regex = r"\[" + token.name + r"[^\]]*?\][^(\[/" + token.name + r"\])]*\[/" + token.name + r"\]"
    else:
      token_regex = r"\[" + token.name + r"\][^(\[/" + token.name + r"\])]*\[/" + token.name + r"\]"
    token_occurences = re.findall(token_regex, string)
    for pos, token_string in enumerate(token_occurences):
      if token.name == 'code':
        break
      code_regex = r"\[code\][^(\[/code\])]*?" + _multi_replace(list(".^$*+?{}[]\\|()"), ["\\" + x for x in list(".^$*+?{}[]\|()")], token_string)
      if re.search(code_regex, string) is None:
        unsorted_tokens.append(token_occurences)
  sorted_tokens = sorted(unsorted_tokens, lambda x: string.find(x))
  return sorted_tokens