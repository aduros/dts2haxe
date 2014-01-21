@:native("OUTER.MyInterface")
typedef MyInterface = {
    name :String,
    ?optional :String,
    list :Array<String>,
    anonymousType :{
        x :Float,
        y :Float,
        ?optional :String,
        method :(Void -> Void),
    },
    @:native("super")
    super_ :Float,
    noType :Dynamic,
    methodSimple :(Void -> Void),
    methodComplex :(Float -> ?String -> Array<String> -> ?Dynamic -> {
        x :Float,
        y :Float,
    } -> (String -> ?String -> Array<Float>) -> Array<String> -> Float),
    noReturnType :(Void -> Dynamic),
}

@:native("OUTER.MyClass")
extern class MyClass
    // implements MyInterface
{
    var name :String;
    var optional :String;
    var list :Array<String>;
    var anonymousType :{
        x :Float,
        y :Float,
        ?optional :String,
        method :(Void -> Void),
    };
    @:native("super")
    var super_ :Float;
    var noType :Dynamic;
    function methodSimple () :Void;
    function methodComplex (n :Float, ?optional :String, list :Array<String>, noType :Dynamic, anonymous :{
        x :Float,
        y :Float,
    }, callback_ :(String -> ?String -> Array<Float>), ?varargs1 :String, ?varargs2 :String, ?varargs3 :String, ?varargs4 :String, ?varargs5 :String, ?varargs6 :String, ?varargs7 :String, ?varargs8 :String, ?varargs9 :String) :Float;
    function noReturnType () :Dynamic;
    function new (n :Float) :Void;
    static var staticVar :Float;
}

@:native("OUTER.Color")
@:fakeEnum(Int) extern enum Color {
    RED;
    BLUE;
    GREEN;
}

@:native("OUTER.FloatMap")
typedef FloatMap = Dynamic<Float>

@:native("OUTER.ErrorCallback")
typedef ErrorCallback = (String -> Dynamic)

@:native("OUTER.INNER.InnerClass")
extern class InnerClass extends MyClass
{
    function new () :Void;
}

@:native("OUTER")
extern class Globals
{
    static var globalVar :Float;
    static function globalFunc (n :Float) :Float;
}@:native("TopLevelClass")
extern class TopLevelClass
{
}

@:native("window")
extern class Globals
{
    static var topLevelGlobal :Float;
}
