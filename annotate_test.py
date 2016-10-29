#!/usr/local/bin/python3

# # TODO: Non-standard python3 environment
#         Change as required.

# Usage:
#     Within each type annotation, place a string to check the type.
#     If a type within a set, list, etc is required to be checked,
#       use [...] to identify the type checked.
#     Multiple type can be checked as well.  This is done by using the
#     pipe | in between to check multiple types.
#
#     Example (a: 'Tuple[str|int])
#
#     You don't need to include at type within a tuple is your just want a tuple
#
#     Example (a: 'Tuple')

from functools import wraps
from sys import modules
from inspect import signature, Parameter
import re
from collections import OrderedDict
from importlib import import_module


def _tokenize(operand, name, funcname, split):
    """This is to tokenize the annotation.
split it on | but want to ensure [...] are respected"""
    # To ensure we normalize any lists sent due to recursion

    temp = ''.join(x for x in operand)
    temp = temp.split(split)  # Now back to list top operate on
    count = 0
    temp_str = ''
    final_list = []

    for token in temp:
        token = token.strip()
        if temp_str == '':
            temp_str = token
        else:
            temp_str = split.join((temp_str, token))

        if '[' not in token and count == 0:
            final_list.append(temp_str)
            temp_str = ''
            continue
        if '[' in token:
            count = count + token.count('[')
        if ']' in token:
            count = count - token.count(']')
        if count == 0:
            final_list.append(temp_str)
            temp_str = ''

    if count != 0:
        raise ValueError(
            "Argument \"{}\" at ".format(name) +
            "failed to parse\n" +
            "From Function: {}".format(funcname)
        )
    else:
        return final_list  # Return is list of operands properly parsed


def _tester(name: 'str', value: 'from args',
            operand: 'str', funcname: 'str',
            loop: 'str'="no", module: 'str'='') -> None:
    """ Inputs from _parse_func_args :
name = name of variable
value = value set for variable
operand = annotation of variable
funcname = string of func.__name__ (to be included in exceptions)
loop = to identify if this is a recursion (for [str|int] logic

Operands are:
bool
str
int
float
complex
bytes
bytearray
Class <name>
ClassInst <from what class>
Func (for type)
Func <what function> - matches memory pointer
tuple[<type>,<type>,...] - checks if tuple and types
tuple[<type>|<type>] - checks groups for multiple types
set - checks if a Set
frozenset - checks if a Frozenset
set[<type>]  or frozenset[type] - only matches one type
set[<type>|<type>] or frozenset[<type>|<type>] - matches two types
list[type] - checks a list for a single type
list - checks if a list
dict[key type= value type] - checks both key and value for type
dict - checks if a dict
OrderedDict[key=value, key=value] - checks both key and value for type and position
OrderedDict[key|key=value|value] - check overall group
OrderedDict - checks for OrdDict type
namedtuple - check if namedtuple type
namedtuple(constructor[type|type, type, type]) - positional
namedtuple(constructor[type|type|type]) - group, checks all positions

"""

    ########## Start of variable testing ##########

    if operand == 'bool':
        if not isinstance(value, bool):
            if loop == 'no':
                raise ValueError(
                    "Argument \"{}\" was not bool.\n".format(name) +
                    "From Function:  {}".format(funcname))
            else:
                return False
        return True
    if operand == 'str':
        if not isinstance(value, str):
            if loop == "no":
                raise ValueError(
                    "Argument \"{}\" was not string.\n".format(name) +
                    "From Function:  {}".format(funcname))
            else:
                return False
        return True
    if operand == 'int':
        if not isinstance(value, int) or type(value) != int:
            if loop == 'no':
                raise ValueError(
                    "Argument \"{}\" was not int.\n".format(name) +
                    "From Function:  {}".format(funcname))
            else:
                return False
        return True
    if operand == 'float':
        if not isinstance(value, float):
            if loop == 'no':
                raise ValueError(
                    "Argument \"{}\" was not float.\n".format(name) +
                    "From Function:  {}".format(funcname))
            else:
                return False
        return True
    if operand == 'complex':
        if not isinstance(value, complex):
            if loop == 'no':
                raise ValueError(
                    "Argument \"{}\" was not complex.\n".format(name) +
                    "From Function:  {}".format(funcname))
            else:
                return False
        return True
    if operand == 'bytes':
        if not isinstance(value, bytes):
            if loop == 'no':
                raise ValueError(
                    "Argument \"{}\" was not bytes.\n".format(name) +
                    "From Function:  {}".format(funcname))
            else:
                return False
        return True
    if operand == 'bytearray':
        if not isinstance(value, bytearray):
            if loop == 'no':
                raise ValueError(
                    "Argument \"{}\" was not bytearray.\n".format(name) +
                    "From Function:  {}".format(funcname))
            else:
                return False
        return True

    if re.match('Class ', operand):
        try:
            str(value.__name__)
        except:
            raise ValueError(
                "Argument \"{}\" was not a Class ".format(name) +
                "of {}.  NO .__name__ ATTRIBUTE!!!\n".format(
                    operand.split('Class ')[1]) +
                "From Function: {}".format(funcname))
        if str(value.__name__) != str(operand.split('Class ', maxsplit=1)[1]):
            if loop == 'no':
                raise ValueError(
                    "Argument \"{}\" was not a Class". format(name) +
                    "of {}.\n".format(operand.split('Class ')[1]) +
                    "From Function:  {}".format(funcname))
            else:
                return False
        return True

    if re.match('ClassInst ', operand):
        temp = operand.split()[1]
        temp = temp.strip()
        f = str(value.__class__)
        f = f.split('.')[-1][0:-2]
        f = f.strip()
        if f != temp:
            # if not isinstance(value, eval(temp)):
            if loop == 'no':
                raise ValueError(
                    "Argument \"{}\" was not a ClassInst of ".format(name) +
                    "{}.\n".format(operand.split('ClassInst ')[1]) +
                    "From Function:  {}".format(funcname))
            else:
                return False
        return True

    if re.match('Func', operand):
        # Check for only Func keyword first
        if len(operand.split()) == 1:
            if str(value.__class__) != "<class 'function'>":
                raise ValueError(
                    "Argument \"{}\" was not a Function\n".format(name) +
                    "From Function: {}".format(funcname)
                )
            else:
                return True

        # Carry on if a function name was given
        temp = operand.split()[1]
        temp = temp.strip()
        # Check is more than one function sent
        if len(value.__repr__().split()) > 4:
            raise ValueError(
                "More than one \"{}\"".format(operand.split('Func ')[1]) +
                "  function in {} (possible Tuple)\n".format(name) +
                "From Function: {}".format(funcname))
        try:
            if value.__repr__().split()[1] != temp:
                # if eval(temp).__repr__() != value.__repr__():
                if loop == 'no':
                    raise ValueError(
                        "Argument \"{}\" was not a ".format(name) +
                        "Func of {} \n".format(operand.split('Func ')[1]) +
                        "From Function:  {}".format(funcname))
                else:
                    return False
        except:
            raise ValueError(
                "Argument \"{}\" was not a ".format(name) +
                "Func of {} \n".format(operand.split('Func ')[1]) +
                "From Function:  {}".format(funcname))

        return True

    if re.match('tuple', operand):
        if not isinstance(value, tuple):
            if loop == 'no':
                raise ValueError(
                    "Argument \"{}\" was not a tuple.\n".format(name) +
                    "From Function: {}".format(funcname))
            else:
                return False

        if operand.find('[') == -1:
            return True

        temp = operand.split('tuple', maxsplit=1)[1].strip()
        # Test below is to ensure that "[" is in the split
        if "[" in temp:
            if temp.startswith('['):
                temp = temp[1:]
            if temp.endswith(']'):
                temp = temp[0:-1]
            temp = _tokenize(temp, name, funcname, ',')
            # Above is to allow positional checks

            # If using commas for positional, must be the same len as value
            # Below throws an exception if not True
            if len(temp) > 1 and len(temp) != len(value):
                raise ValueError(
                    "Tuple Argument \"{}\" not the same size ".format(name) +
                    "as operand {}\n".format(operand) +
                    "From Function: {}".format(funcname)
                )
            # This is to check positional test e.g. a:'tuple[int,int,str]'
            if len(temp) == len(value):
                count = 0
                for i in temp:
                    tokenized = _tokenize(i, name, funcname, '|')
                    ok = False
                    for send in tokenized:
                        result = _tester(name, value[count],
                                         send, funcname, loop='yes')
                        if result is True:
                            ok = True

                    if ok is not True:
                        raise ValueError(
                            "Tuple Argument \"{}\" at ".format(name) +
                            "position {} ".format(count) +
                            "failed test {}\n".format(tokenized) +
                            "From Function: {}".format(funcname)
                        )
                    ok = False
                    count += 1
                return True

            # temp == 1 if there is not found for positional checking
            if len(temp) == 1 and len(value) >= 1:
                count = 0
                tokenized = _tokenize(temp, name, funcname, '|')
                for i in value:

                    # j = [x.strip().split('|') for x in temp]
                    # j = [x.strip() for x in j[0]]
                    ok = False
                    for send in tokenized:
                        result = _tester(name, i,
                                         send, funcname, loop='yes')
                        if result is True:
                            ok = True
                    if ok is not True:
                        raise ValueError(
                            "Tuple Argument \"{}\" at ".format(name) +
                            "position {} ".format(count) +
                            "failed test {}\n".format(tokenized) +
                            "From Function: {}".format(funcname)
                        )
                    count += 1
                return True

        # This should never display
        print("Fell through Tuple !?!")

    # frozenset must be first or else re.match('set') catches it first
    if re.match('frozenset', operand):
        if not isinstance(value, frozenset):
            if loop == 'no':
                raise ValueError(
                    "Argument \"{}\" was not a frozenset.\n".format(name) +
                    "From Function: {}".format(funcname))
            else:
                return False

        if operand.find('[') == -1:
            return True

        temp = operand.split('set', maxsplit=1)[1].strip()
        # Test below is to ensure that "[" is in the split
        if "[" in temp:
            if temp.startswith('['):
                temp = temp[1:]
            if temp.endswith(']'):
                temp = temp[0:-1]

            count = 0
            tokenized = _tokenize(temp, name, funcname, '|')
            for i in value:
                ok = False
                for send in tokenized:
                    result = _tester(name, i, send, funcname, loop='yes')
                    if result is True:
                        ok = True
                if ok is not True:
                    raise ValueError(
                        "Frozenset Argument \"{}\" at ".format(name) +
                        "position {} ".format(count) +
                        "failed test {}\n".format(tokenized) +
                        "From Function: {}".format(funcname)
                    )
                ok = False
                count += 1
            return True

        # This should never display
        print("Fell through annotate_test.Frozenset")

    if re.match('set', operand):
        if not isinstance(value, set):
            if loop == 'no':
                raise ValueError(
                    "Argument \"{}\" was not a set.\n".format(name) +
                    "From Function: {}".format(funcname))
            else:
                return False

        if operand.find('[') == -1:
            return True

        temp = operand.split('set', maxsplit=1)[1].strip()
        # Test below is to ensure that "[" is in the split
        if "[" in temp:
            if temp.startswith('['):
                temp = temp[1:]
            if temp.endswith(']'):
                temp = temp[0:-1]

            count = 0
            tokenized = _tokenize(temp, name, funcname, '|')
            for i in value:
                ok = False
                for send in tokenized:
                    result = _tester(name, i, send, funcname, loop='yes')
                    if result is True:
                        ok = True
                if ok is not True:
                    raise ValueError(
                        "Set Argument \"{}\" at ".format(name) +
                        "position {} ".format(count) +
                        "failed test {}\n".format(tokenized) +
                        "From Function: {}".format(funcname)
                    )
                ok = False
                count += 1
            return True

        # This should never display
        print("Fell through annotate_test.Frozenset")

    if re.match('list', operand):
        if not isinstance(value, list):
            if loop == 'no':
                raise ValueError(
                    "Argument \"{}\" was not a list.\n".format(name) +
                    "From Function: {}".format(funcname))
            else:
                return False

        if operand.find('[') == -1:
            return True
        temp = operand.split('list', maxsplit=1)[1].strip()
        if "[" in temp:
            if temp.startswith('['):
                temp = temp[1:]
            if temp.endswith(']'):
                temp = temp[0:-1]
            temp = _tokenize(temp, name, funcname, ',')
            # Above is to allow positional checks

            # If using commas for positional, must be the same len as value
            # Below throws an wxception if not True
            if len(temp) > 1 and len(temp) != len(value):
                raise ValueError(
                    "List Argument \"{}\" not the same size ".format(name) +
                    "as operand {}\n".format(operand) +
                    "From Function: {}".format(funcname)
                )
            # This is to check positional test e.g. a:'list[int, str]'
            if len(temp) == len(value):
                count = 0
                for i in temp:
                    tokenized = _tokenize(i, name, funcname, '|')
                    ok = False
                    for send in tokenized:
                        result = _tester(name, value[count],
                                         send, funcname, loop='yes')
                        if result is True:
                            ok = True

                    if ok is not True:
                        raise ValueError(
                            "List Argument \"{}\" at ".format(name) +
                            "position {} ".format(count) +
                            "failed test {}\n".format(tokenized) +
                            "From Function: {}".format(funcname)
                        )
                    ok = False
                    count += 1
                return True

            if len(temp) == 1 and len(value) >= 1:
                count = 0
                tokenized = _tokenize(temp, name, funcname, '|')
                for i in value:
                    ok = False
                    for send in tokenized:
                        result = _tester(name, i,
                                         send, funcname, loop='yes')
                        if result is True:
                            ok = True
                    if ok is not True:
                        raise ValueError(
                            "List Argument \"{}\" at ".format(name) +
                            "position {} ".format(count) +
                            "failed test {}\n".format(tokenized) +
                            "From Function: {}".format(funcname)
                        )
                    count += 1
                return True

        # This should never display
        print("Fell through List !?!")

    if re.match('OrderedDict', operand):
        if not isinstance(value, OrderedDict):
            if loop == 'no':
                raise ValueError(
                    "Argument \"{}\" was not a list.\n".format(name) +
                    "From Function: {}".format(funcname))
            else:
                return False

        if operand.find('[') == -1:
            return True

        temp = operand.split('OrderedDict', maxsplit=1)[1].strip()
        if "[" in temp:
            if temp.startswith('['):
                temp = temp[1:]
            if temp.endswith(']'):
                temp = temp[0:-1]
            temp = _tokenize(temp, name, funcname, ',')
            # Test for positional by using , to seperate
            # Only checks positionally and not by key
            if len(temp) > 1 and len(temp) != len(value):
                raise ValueError(
                    "OrderedDict Argument \"{}\" not ".format(name) +
                    "the same size as operand {}\n".format(operand) +
                    "From Function: {}".format(funcname)
                )

            # This is to test through ['str'=int, [int|str], str] type args
            if len(temp) == len(value):
                count = 0
                key_value = (i for i in value.items())
                key_value = enumerate(key_value)  # Generator num, (key, value)

                for j in temp:  # j = key=value token
                    j = j.split('=', maxsplit=1)  # list[key, value]
                    num, item = next(key_value)
                    if num is not count:
                        raise ValueError(
                            "Something is very wrong in OrderedDict test")
                    valuekey = item[0]
                    valuevalue = item[1]

                    if j[0] != '':  # Check key
                        tokenized = _tokenize(j[0], name, funcname, '|')
                        ok = False
                        for send in tokenized:
                            result = _tester(name, valuekey,
                                             send, funcname, loop='yes')
                            if result is True:
                                ok = True

                        if ok is not True:
                            raise ValueError(
                                "OrderedDict Argument \"{}\" at ".format(name) +
                                "position {} ".format(count) +
                                "failed KEY test {}\n".format(tokenized) +
                                "From Function: {}".format(funcname)
                            )
                        ok = False  # Reset sentinal

                    if len(j) is not 1:
                        tokenized = _tokenize(j[1], name, funcname, '|')
                        ok = False
                        for send in tokenized:
                            result = _tester(name, valuevalue,
                                             send, funcname, loop='yes')
                            if result is True:
                                ok = True

                        if ok is not True:
                            raise ValueError(
                                "OrderedDict Argument \"{}\" at ".format(name) +
                                "position {} ".format(count) +
                                "failed VALUE test {}\n".format(tokenized) +
                                "From Function: {}".format(funcname)
                            )

                        ok = False
                    count += 1
                return True

            # temp == 1 if there is not found , for positional checking
            if len(temp) == 1 and len(value) >= 1:

                j = temp[0].split('=', maxsplit=1)

                if j[0] != '':
                    count = 0
                    tokenized = _tokenize(j[0], name, funcname, '|')
                    for i in value.keys():
                        ok = False
                        for send in tokenized:
                            result = _tester(name, i,
                                             send, funcname, loop='yes')
                            if result is True:
                                ok = True
                                break
                        if ok is not True:
                            raise ValueError(
                                "OrderedDict Argument \"{}\" at ".format(name) +
                                "position {} ".format(count) +
                                "failed KEY test {}\n".format(tokenized) +
                                "From Function: {}".format(funcname)
                            )
                        count += 1

                if len(j) is 2 and j[1] != '':
                    count = 0
                    tokenized = _tokenize(j[1], name, funcname, '|')
                    for i in value.values():
                        ok = False
                        for send in tokenized:
                            result = _tester(name, i,
                                             send, funcname, loop='yes')
                            if result is True:
                                ok = True
                                break
                        if ok is not True:
                            raise ValueError(
                                "OrderedDict Argument \"{}\" at ".format(name) +
                                "position {} ".format(count) +
                                "failed VALUE test {}\n".format(tokenized) +
                                "From Function: {}".format(funcname)
                            )
                        count += 1

                return True

        # This should never display
        print("Fell through OrderedDict!?!")

    if re.match('dict', operand):
        if not isinstance(value, dict):
            if loop == 'no':
                raise ValueError(
                    "Argument \"{}\" was not a dict.\n".format(name) +
                    "From Function: {}".format(funcname))
            else:
                return False

        if operand.find('[') == -1:
            return True
        temp = operand.split('dict', maxsplit=1)[1].strip()
        if "[" in temp:
            if temp.startswith('['):
                temp = temp[1:]
            if temp.endswith(']'):
                temp = temp[0:-1]

            j = temp.split('=', maxsplit=1)

            if j[0] != '':
                count = 0
                tokenized = _tokenize(j[0], name, funcname, '|')
                for i in value.keys():
                    ok = False
                    for send in tokenized:
                        result = _tester(name, i,
                                         send, funcname, loop='yes')
                        if result is True:
                            ok = True
                            break
                    if ok is not True:
                        raise ValueError(
                            "Dict Argument \"{}\" at ".format(name) +
                            "position {} ".format(count) +
                            "failed KEY test {}\n".format(tokenized) +
                            "From Function: {}".format(funcname)
                        )
                    count += 1

            if len(j) is 2 and j[1] != '':
                count = 0
                tokenized = _tokenize(j[1], name, funcname, '|')
                for i in value.values():
                    ok = False
                    for send in tokenized:
                        result = _tester(name, i,
                                         send, funcname, loop='yes')
                        if result is True:
                            ok = True
                            break
                    if ok is not True:
                        raise ValueError(
                            "Dict Argument \"{}\" at ".format(name) +
                            "position {} ".format(count) +
                            "failed VALUE test {}\n".format(tokenized) +
                            "From Function: {}".format(funcname)
                        )
                    count += 1

            return True

        # This should never display
        print("Fell through dict !?!?!?!?")

    if re.match('namedtuple', operand):
        # check for e._fields, e._asdict, e._make,
        # e._source to confirm namedtuple type
        # type only identifies which template it came from as a class
        try:
            if bool(value._fields) and \
               bool(value._asdict) and \
               bool(value._make) and \
               bool(value._source):
                pass  # Quick check for type
        except:
            raise ValueError(
                "Argument \"{}\" was not a namedtuple.\n".format(name) +
                "From Function: {}".format(funcname))

        if operand.find('(') == -1:
            return True

            # Now we are comparing to a namedtuple constructor
        temp = operand.split('namedtuple', maxsplit=1)[1].strip()
        if "(" in temp:
            if temp.startswith('('):
                temp = temp[1:]
            if temp.endswith(')'):
                temp = temp[0:-1]

        # temp should now be namedtuple template and positional options
        # first check that value came from template
        named_template = temp.split('[', maxsplit=1)[0].strip()
        # makes the template an object to test
        general_template_name = named_template

        try:
            # grabbing from root._source
            root_source = eval("modules['__main__']." +
                               named_template + "._source")
            # grabbing from root.__str__(root)  [Root function]

        except:
            raise ValueError(
                "Argument \"{}\" looks for ".format(name) +
                "template \"{}\" ".format(general_template_name) +
                "but does not find it.\n" +
                "From Function: {}".format(funcname)
            )

        try:
            root_name = eval("str(modules['__main__']." +
                             named_template + ".__str__(" +
                             "modules['__main__']." +
                             named_template + "))")
        except:
            raise ValueError(
                "Argument \"{}\" looks for ".format(name) +
                "template \"{}\" ".format(general_template_name) +
                "but does not find it.\n" +
                "From Function: {}".format(funcname)
            )

        # Check both ._source and class/str results for positive check
        if value._source != root_source and value.__class__ != root_name:
            raise ValueError(
                "Argument \"{}\" was not an instance from ".format(name) +
                "namedtuple template \"{}\"".format(general_template_name) +
                " {}\n".format(named_template) +
                "From Function: {}".format(funcname)
            )

        # Test positional values
        if '[' not in temp:  # if there are no positional checks
            return True

        temp = temp.split('[', maxsplit=1)[1].strip()
        if temp.endswith(']'):
            temp = temp[0:-1]
        temp = _tokenize(temp, name, funcname, ',')

        if len(temp) > 1 and len(temp) != len(value):
            raise ValueError(
                "Namedtuple Argument \"{}\" not the same size ".format(name) +
                "as operand {}\n".format(operand) +
                "From Function: {}".format(funcname)
            )

        # This is to check positional test
        #      e.g. a:'namedtuple(<template[int,int,str])'
        if len(temp) == len(value):
            count = 0
            for i in temp:
                tokenized = _tokenize(i, name, funcname, '|')
                ok = False
                for send in tokenized:
                    result = _tester(name, value[count],
                                     send, funcname, loop='yes')
                    if result is True:
                        ok = True

                if ok is not True:
                    raise ValueError(
                        "Namedtuple Argument \"{}\" at ".format(name) +
                        "position {} ".format(count) +
                        "failed test {}\n".format(tokenized) +
                        "From Function: {}".format(funcname)
                    )

                ok = False
                count += 1
            return True

        # temp == 1 if there is not found ',' for positional checking
        if len(temp) == 1 and len(value) >= 1:
            count = 0
            tokenized = _tokenize(temp, name, funcname, '|')
            for i in value:
                ok = False
                for send in tokenized:
                    result = _tester(name, i,
                                     send, funcname, loop='yes')
                    if result is True:
                        ok = True
                if ok is not True:
                    raise ValueError(
                        "Namedtuple Argument \"{}\" at ".format(name) +
                        "position {} ".format(count) +
                        "failed test {}\n".format(tokenized) +
                        "From Function: {}".format(funcname)
                    )
                count += 1
            return True

        # This should never display
        print("Fell through namedtuple")

    ########## End of testing values ##########

    # Test if variable is empty to continue, else fall through
    if operand == str(Parameter.empty):
        return True

    print(operand, "is type", type(operand))
    # Error to raise if not matched
    raise ValueError(
        "Variable {} in function {} ".format(name, funcname) +
        "failed to parse.\nPlease correct annotation or disable @annotate_test"
    )


def _parse_func_args(args_temp, kwargs, kwargs_temp, sig, fname):
    """This returns an OrderedDict after filtering args_temp, kwargs
(for values) and kwargs based on the signature of the function.
This is required because kwargs can affect positional args, and *args
or *kwargs can throw off the parsing (Fail early before feeding the function).
The dict format is:
<name of var>:[annotation, parameter kind, is default, value]

For the annotation testing, will use annotation and value
"""
    err = "Exception from module ### {} ###\n".format(fname)
    # To make this a function, needs args, kwargs and sig
    odict = OrderedDict()
    # Create OrderedDict with key = arg name
    #    list = annotation, kind, is default value, actual value / default)
    for i in sig.parameters.values():
        odict[i.name] = [i.annotation, i.kind,
                         'default=yes',
                         i.default]

    # Run through args
    order_pos = []
    order_var_arg = ''
    order_keyword = []
    order_keyword_args = ''

    for i in odict:
        if odict[i][1] == 1:
            order_pos.append(i)
        if odict[i][1] == 2:
            order_var_arg = i
        if odict[i][1] == 3:
            order_keyword.append(i)
        if odict[i][1] == 4:
            order_keyword_args = i

    # This sets values in order and removes the default flags by
    # eating args_temp list against avail available positional arguments
    # If short, exception handles it and doesn't change values

    for i in order_pos:
        try:
            # Reads first item then removes item from list
            odict[i][3] = args_temp[0]
            odict[i][2] = 'default=no'
            args_temp.remove(args_temp[0])
        except:
            pass

    # Test for leftover positional and leave list of values if True
    if len(args_temp) != 0 and order_var_arg == '':
        raise ValueError(err +
                         "Too many args. {} extra argument".format(len(args_temp)))
    if len(args_temp) != 0:
        odict[order_var_arg][3] = args_temp
        odict[order_var_arg][2] = "default=no"

    # Run through keywords
    for i in order_keyword:
        if odict[i][2] == 'default=no':
            raise ValueError(err +
                             "{} already has value".format(i))
        else:
            if kwargs_temp.get(i) is not None:
                odict[i][3] = kwargs[i]
                odict[i][2] = "default=no"
                kwargs_temp.pop(i)

    # Place remaining kwargs if **kwargs exists
    # This is for if VAR_KEYWORDS args get found
    if len(kwargs_temp) != 0 and order_keyword_args != '':
        odict[order_keyword_args][2] = "default=no"
        odict[order_keyword_args][3] = {}
        for i in kwargs_temp:
            if odict.get(i) is not None:
                if odict[i][2] == "default=no":
                    raise ValueError(err +
                                     "{} already exists".format(i))
                else:
                    odict[i][2] = "default=no"
                    odict[i][3] = kwargs_temp[i]
            else:
                odict[order_keyword_args][3][i] = kwargs_temp[i]

    # Check for value!!! This if for if there are no VAR_KEYWORD args
    if len(kwargs_temp) != 0 and order_keyword_args == '':
        for i in kwargs_temp:
            if odict.get(i) is None:
                raise ValueError(
                    "{} variable doesn't exist".format(kwargs_temp))
            else:
                if odict[i][2] == "default=no":
                    raise ValueError(err +
                                     "{} variable is already assigned!".format(kwargs_temp))
                else:
                    odict[i][2] = "default=no"
                    odict[i][3] = kwargs_temp[i]

    # Test for empty values
    for i in odict:
        if odict[i][3] == Parameter.empty and \
           (odict[i][1] == Parameter.POSITIONAL_OR_KEYWORD or
                odict[i][1] == Parameter.KEYWORD_ONLY):
            raise ValueError("Value {} is empty".format(i))

    # Returns OrderedDict of var name annotations, name of functions
    # OrderedDict is in format var_name:(annotation, signature kind,
    #                                    is default('yes'|'no'),
    #                                    value arg given)
    return odict


# Main annotate wrapper
def annotate_test(func):
    """Uses annotations to test.  Syntax is <name>[<type>|<type...] or
                                            <name>[<type>,<type>,...] or
                                            <name>"""
    @wraps(func)
    def helper(*args, **kwargs):
        args_temp = [i for i in args]
        kwargs_temp = kwargs.copy()
        sig = signature(func)

        # Break down into Position and Keyword arguments into an OrderedDict
        order = _parse_func_args(args_temp, kwargs,
                                 kwargs_temp, sig,
                                 func.__module__ + ' ' + func.__repr__())

        # Test
        for i in order:
            _tester(i, order[i][3], str(order[i][0]), str(func.__name__),
                    module=str(func.__module__))

        try:
            func_return = func(*args, **kwargs)
        except Exception as ex:
            raise ex

        # Test return value to annotation
        if sig.return_annotation != sig.empty:
            _tester("RESULT", func_return,
                    sig.return_annotation, str(func.__name__),
                    module=str(func.__module__))
        return func_return
    return helper

# Note above
# The @wraps(func)  <from functools> allows the original function to
# keep its annotations.

# Area for testing:
if __name__ == '__main__':
    # insert code to test directly here
    pass
