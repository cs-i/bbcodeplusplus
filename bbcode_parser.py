import re
from collections import namedtuple
from typing import Callable, Dict, List

Token = namedtuple("Token", ["name", "has_params", "has_closing_token"])
ParsedToken = namedtuple("ParsedToken", ["name", "input_string"])

def _multi_replace(olds: List[str], news: List[str], string: str) -> str:
  for old, new in zip(olds, news):
    string = string.replace(old, new)
  return string

def _tokenize(token_types, string: str) -> List[ParsedToken]:
  tokens = []
  for token in token_types:
    unparsed_tokens = []
    # Generate token regex
    if token.has_params is True:
      if token.has_closing_token is False:
        token_regex = r"\[" + token.name + r"[^\]]*?\]"
      else:
        token_regex = r"\[" + token.name + r"[^\]]*?\][^(\[/" + token.name + r"\])]*\[/" + token.name + r"\]"
    else:
      token_regex = r"\[" + token.name + r"\][^(\[/" + token.name + r"\])]*\[/" + token.name + r"\]"
    token_occurences = re.findall(token_regex, string)
    # Remove occurences between code tags
    for pos, token_string in enumerate(token_occurences):
      if token.name == 'code':
        break
      code_regex = r"\[code\][^(\[/code\])]*?" + _multi_replace(list(".^$*+?{}[]\\|()"), ["\\" + x for x in list(".^$*+?{}[]\|()")], token_string)
      if re.search(code_regex, string) is None:
        unparsed_tokens.append(token_string)
      # Change token class
      for x in unparsed_tokens:
        parsed_token = ParsedToken(token.name, x)
        tokens.append(parsed_token)
  return tokens

def _parse_tokens(replace_functions: List[Callable], parsed_tokens: List[ParsedToken], string: str) -> str:
  for token in parsed_tokens:
    replace_function = replace_functions[token.name]
    replaced_string = replace_function(token.input_string)
    string = string.replace(token.input_string, replaced_string)
  return string


class Parser:
  def __init__(self) -> None:
    self.tokens: List[Token] = []
    self.token_functions: Dict[str, Callable] = {}
    self.pre_replacer: Callable = lambda x: _multi_replace(['<', '>'], ['&lt', '&gt'], x)
  
  def add_token(self, name: str, has_params: bool, has_closing_token: bool, token_function: Callable[[str], str]) -> None:
    token = Token(name, has_params, has_closing_token)
    self.tokens.append(token)
    self.token_functions.append(token_function)
  
  def translate(self, bbcode_string: str) -> str:
    """translate(self: Parser, bbcode_string: str)
    Translates a BBCode++ string into raw HTML."""
    sanitized_string: str = self.pre_replacer(bbcode_string)
    tokens: List[ParsedToken] = _tokenize(self.tokens, sanitized_string)
    output_string: str = _parse_tokens(self.token_functions, tokens, sanitized_string)
    return output_string