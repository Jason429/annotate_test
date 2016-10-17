# annotate_test
Project to wrap Python3 functions with live type testing (using annotations)

This is my first GitHub project so it might be a little rough at the start.

ANNOTATE_TEST

This is a Python3 module that could be imported into your projects to have live type checking available for your functions.
Using a simple @annotate_test decorator at the beginning of a function will run that function through the annotation tester.
Any variables that do not have annotations will not be tested against however if the tester is unable to parse (or it is not 
a string as an annotation), the wrapper will fire out an exception (to avoid silent errors from typos).

The annotations are not strictly using direct types like they seem to be declared in PEP 484 annotation type hints (I still
consider myself a beginner for many Python higher level functions) but instead brought about through parsing of data within a 
string annotation.  My intent was to see if I could play with parsing to allow quicker failures (that could be identified 
by good documenting exceptions) while using Python in a functional pattern.  My thought was that this tool could be used at 
the start of input streams where data could be questionable and for final checking of types.

Patterns for annotation are:
def test(a:'str', b:'int|str', c:'tuple[int, bool|int|str, bytes]') -> 'OrderedDict':

(above tests a is type(str), b is type(int or str), c is type(tuple) with position 0 = int, 1 = bool or int or str, 2 = bytes)
(the final return is an OrderedDict type)

Class and Func specific checking use 'Class MyClass' or 'Func funcname' pattern

namedtuple uses '(' and ')' for its pattern matching to be able to verify the name and type of namedtuple as well as values
(e.g. 'namedtuple(tupname[int, bytes, str])' for matching namedtuple named tupname with positional arguments 0,1,2 as int, bytes
and str respectively)

In efforts to develop this correctly, I have also generated 75 tests for both passed and exceptions.  The tests are good
documentation on how the syntax is currently running.
When running unittest_annotation_tester.py with --debug flag, stdout will print out all the exceptions for the tested exceptions.

Below are the Operands that I have included:

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

As I stated above, this is my first foray onto GitHub with code that I have written.  I already recognize that there are many
areas that I consider rough (e.g. The exception handling could be handled by an exception message function rather than how I have
created seperate messages for each exception case).  I was thinking more the brute-force, make it work and test it well.
I do intend to keep coming back to this to keep cleaning it up.

To deploy annotation_test, simply copy annotate_test.py to your Python3 project (to an importable area)
Add : from annotate_test import annotate_test
Then add @annotate_test as a decorator to your functions.

If you find this module useful of have ideas on how to improve it, let me know.  

Jason


