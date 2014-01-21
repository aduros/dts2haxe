declare module OUTER {

    export interface MyInterface {
        // Vars
        name :string;
        optional? :string;
        list :string[];
        anonymousType :{x :number; y :number; optional? :string; method() :void;};
        super :number; // Haxe keyword
        noType;

        // Methods
        methodSimple () :void;
        methodComplex (
            n :number,
            optional? :string,
            list :string[],
            noType,
            anonymous :{x :number; y :number;},
            callback :(event :string, optional? :string) => number[],
            ...varargs :string[]
        ) :number;
        noReturnType ();
    }

    export class MyClass implements MyInterface {
        // Vars
        name :string;
        optional? :string;
        list :string[];
        anonymousType :{x :number; y :number; optional? :string; method() :void;};
        super :number; // Haxe keyword
        noType;

        // Methods
        methodSimple () :void;
        methodComplex (
            n :number,
            optional? :string,
            list :string[],
            noType,
            anonymous :{x :number; y :number;},
            callback :(event :string, optional? :string) => number[],
            ...varargs :string[]
        ) :number;
        noReturnType ();

        constructor (n :number);
        static staticVar :number;
    }

    export enum Color {
        RED, BLUE = 666, GREEN
    }

    interface FloatMap { [key :string] :number; }
    interface ErrorCallback { (err :string) :void; }

    declare module INNER {
        export class InnerClass extends MyClass {
            // Alternate constructor syntax
            new () :InnerClass;
        }
    }

    // Global properties
    export var globalVar :number;
    export function globalFunc (n :number) :number;
}

declare class TopLevelClass {
}
declare var topLevelGlobal :number;
