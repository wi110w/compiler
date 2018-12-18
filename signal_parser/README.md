This is a laboratory assignment # 2: build a parser.
It takes tokens from specified sub-grammar of SIGNAL language:
```
<signal-program> --> <program>
<program> --> PROGRAM <procedure-identifier>;
	   <block>;
<block> --> <declarations>
    BEGIN
        <statements-list>
    END
<statements-list> --> <empty>
<declarations> --> <procedure-declarations>
<procedure-declarations> --> <procedure> <procedure-declarations> |
	   <empty>
<procedure> --> PROCEDURE <procedure-identifier> <parameters-list>;
<parameters-list> --> ( <declarations-list> ) |
	   <empty>
<declarations-list> --> <declaration> <declarations-list> |
	   <empty>
<declaration> --><variable-identifier> 
    <identifiers-list> : <attribute> <attributes-list>;
<identifiers-list> --> , <variable-identifier> <identifiers-list> |
	   <empty>
<attributes-list> --> <attribute> <attributes-list> |
	   <empty>
<variable-identifier> --> <identifier>
<procedure-identifier> --> <identifier>

<attribute> --> SIGNAL      |
	   COMPLEX	  |
	   INTEGER	  |
	   FLOAT	  |
	   BLOCKFLOAT |
	   EXT
<identifier> --> <letter><string>
<string> --> <letter><string> |
	   <digit><string> |
	   <empty>
<digit> --> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
<letter> --> A | B | C | D | ... | Z
```
And build a tree according to rules of grammar.