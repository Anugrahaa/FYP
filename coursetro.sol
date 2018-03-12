pragma solidity ^0.4.18;

contract Coursetro {
    
   string fName;
   uint age;
   address owner;
   
   event Instructor(
       string name,
       uint age);
   
   function Coursetro() public{
       owner = msg.sender;
   }
   
   
   function setInstructor(string _fName, uint _age) public {
       fName = _fName;
       age = _age;
       Instructor(_fName, _age);
   }
   
   function getInstructor() public constant returns (string, uint) {
       return (fName, age);
   }
    
}