// {
//     // let a = 12;
//     var a = 12;
// }

// console.log(a);


// var a = [];
// for (var i = 0; i < 10; i++) {
//     a[i] = function () {
//         console.log(i);
//     };
// }
// a[6]();

// var a = [];
// for (let i = 0; i < 10; i++) {
//     // console.log(i)
//   a[i] = function () {
//     console.log(i);
//   };
// }
// a[6]();
// console.log(a);



// let a = 1;
// let b = 2;
// let str = `aaaaa${a}${b}`;
// console.log(str);


// console.log('\`yo\` world')


// var f = function(a){
//     return a;
// }

// console.log(f(1));

// var name = '张三';
// var person = {
//     name: '小马哥',
//     age: 18,
//     fav: function () {
//         // console.log(this);
//         console.log(this.name);
//     }
// }
// person.fav();

// var person2 = {
//     name: '小马哥',
//     age: 18,
//     fav: ()=> {
//         // console.log(this);
//         console.log(this.name);
//     }
// }
// person2.fav()





// var person = {
//     name:'aa',
//     age:18,
//     fav(){console.log(this);}
// }
// person.fav();



// function Animal(name,age){
//     this.name = name;
//     this.age = age;
// }


// var dog = new Animal('dog',12);

// Animal.prototype.showname = function(){
//     console.log(this.name)
// }

// console.log(dog.name);
// console.log(dog.age);
// dog.showname();



class Animal{
    constructor(name,age){
        this.name = name;
        this.age = age;

    }

    showname(){
        console.log(this);
        console.log(this.name);
        console.log(this.age);
    }
}

var d = new Animal('dog',18);
d.showname();









