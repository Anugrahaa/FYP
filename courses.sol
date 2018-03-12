pragma solidity ^0.4.18;

contract Owned {
    address owner;
    
    function Owned() public {
        owner = msg.sender;
    }
    
   modifier onlyOwner {
       require(msg.sender == owner);
       _;
   }
}

contract Courses is Owned {
    
    struct Instructor {
        uint age;
        bytes16 fName;
        bytes16 lName;
    }
    
    mapping (address => Instructor) instructors;
    address[] public instructorAccts;
    
    function setInstructor(address _address, uint _age, bytes16 _fName, bytes16 _lName) public onlyOwner {
        var instructor = instructors[_address];

        instructor.age = _age;
        instructor.fName = _fName;
        instructor.lName = _lName;
        
        instructorAccts.push(_address) -1;

    }
    
    function getInstructors() public view returns (address[]) {
        return instructorAccts;
    }
    
    function getInstructor(address ins) public view returns (uint, bytes16, bytes16) {
        return (instructors[ins].age, instructors[ins].fName, instructors[ins].lName);
    }
    
    function countInstructors() public view returns (uint) {
        return instructorAccts.length;
    }
}