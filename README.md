# Typescript .d.ts to Haxe extern generator

Conversion is decent, but still requires manual tweaking for many
libraries. Check the tests/ directory to see what's supported and what
the output looks like.

Also check out https://github.com/Simn/ts2hx for a more complete
generator.

## Usage

```
    (sudo) pip install pyparsing
    ./dts2haxe input.d.ts
```

## What works

* Classes.
* Interfaces (mapped to Haxe typedefs).
* Enums.
* Global variables and functions (placed as statics in a generated "Globals" class).
* Array types.
* Anonymous types.
* Varargs methods.
* Nested modules.
* Escaping Haxe keywords.

## What doesn't work yet

* Generics.
* Method overloading.
* Certain weird JS patterns that don't map well to Haxe.
* Splitting generated Haxe into multiple .hx files.
* Importing external type dependencies. Converting HTML dependencies to js.html.*.
* Preserving jsdoc comments in output.
* Allowing quoted strings for identifiers.

I'm not a Typescript developer, so there may be things I overlooked! If
one of these TODOs is interesting to you, please fork and contribute.
