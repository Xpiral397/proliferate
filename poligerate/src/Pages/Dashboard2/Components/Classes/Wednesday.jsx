import React, {useState, useEffect, useContext} from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCalendarDays, faClock, faL, faMagnifyingGlass, faMap, faMapMarked, faUser} from '@fortawesome/free-solid-svg-icons';
import noClass from '../../../../Assets/no-class.png'
import classData from '../../Components/ScheduleClassData'
import AddClassPopup from '../AddClassModal';
import JoinClassModal from '../JoinClassModal';
import {UseSessionContext} from '../../../../context/createContext/useSession';
import {useMyClasses} from '../../../../api/tutor/class/getMyClasses';
import {updateClass} from '../../../../api/tutor/class/updateClasses';
import {createClasses} from '../../../../api/tutor/class/createClass';
import {getDay} from '../../../../helper/getDay';

const Monday=() => {
  const [classdata, setClassdata]=useState([]);
  const [showModal, setShowModal]=useState(false);
  const [searchQuery, setSearchQuery]=useState('');
  const [showJoinModal, setShowJoinModal]=useState(false);

  // Create a unique formData for each class box
  const [formData, setFormData]=useState({
    subject: '',
    studentName: '',
    grade: '',
    date: '',
    startTime: '',
    endTime: '',
    id: '',
  });

  const {session, updateSession}=useContext(UseSessionContext)
  useEffect(() => {
    useMyClasses().then((data) => {
      data=data.filter(items => {console.log(getDay(items.date),'lop'); return getDay(items.date)==="Wednesday"})
      console.log(data, 'class 2025', )
      setClassdata(data)
    })
  }, [classData])


  const handleJoinNow=() => {
    setShowJoinModal(true);
  };

  const closeJoinModal=() => {
    setShowJoinModal(false);
  };

  const OpenModal=() => {
    // Generate a new random class id and reset formData
    generateRandomClassId();
    setShowModal(true);
  };

  const closeModal=() => {
    setShowModal(false);
  };

  useEffect(() => {
    generateRandomClassId();
  }, []);

  const generateRandomClassId=() => {
    const randomClassId=Math.floor(100+Math.random()*900);
    setFormData({
      name: '',
      students: [],
      
      tutor:"",
      grade: '',
      date: '',
      start_time: '',
      end_time: '',
      id: "",
    });
  };

  const handleInputChange=(e) => {
    const {name, value}=e.target;
    console.log(name,value)
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit=(e) => {
    e.preventDefault();

    // Check if the classid already exists in classdata
    const existingClassIndex=classdata.findIndex((item) => item.name ===formData.name);

    if(existingClassIndex!==-1) {
      // If classid exists, update the existing class data
      const updatedClassData=[...classdata];
      updatedClassData[existingClassIndex]=formData;
      setClassdata(updatedClassData);
      updateClass(formData.classid, formData)
    } else {
      // If classid doesn't exist, add the new class data
      setClassdata((prevData) => [...prevData, formData]);
      createClasses(formData)
    }

    // Generate a new random class id and reset formData
    generateRandomClassId();
    closeModal();
  };

 


  return (
    <div className="grid grid-cols-3 gap-3 inter">
      <button className='addClass text-[#186BAD] underline absolute top-32 right-0 text-lg poppins' onClick={OpenModal}>Add subject and availability</button>
      {classData?.length===0? (
        <div className="flex flex-col gap-3 absolute top-[20rem] rounded-xl border-[1px] border-[#000000] right-[30rem] w-[250px] h-[250px] justify-center items-center">
          <div className="">
            <img src={noClass} alt="" />
          </div>
          <div className="flex flex-col gap-2 justify-center items-center">
            <p className='text-[#898A8B]'>No Classes</p>
          </div>
        </div>
      ):(
        <>
          {classdata.map((item, index) => (
            <div className="">
              <JoinClassModal
                showModal={showJoinModal}
                closeModal={closeJoinModal}
              // roomId={formData.classid}
              />
              <div
                className="classBox p-3 cursor-pointer rounded-lg flex flex-col justify-center items-center bg-[#186BAD]"
                onClick={handleJoinNow}
                key={item?.id??index}
              >
                <div className="flex flex-col justify-center gap-2 text-center text-[#fff]">
                  <div className="head text-center">
                    <h2 className="font-semibold text-lg py-3">
                      {item?.name}
                    </h2>
                    <hr />
                  </div>
                  <p className="rounded flex gap-5 items-center justify-center">
                    <FontAwesomeIcon icon={faUser} />
                    {typeof item?.students=="object"&&item?.students.map(e => <p>{e}</p>)}
                    {typeof item?.students=="string"&&item?.students}
                  </p>
                  <div className="flex justify-between gap-20 my-4">
                    <p className=' flex gap-x-1 items-center'>
                      <FontAwesomeIcon icon={faMapMarked} />
                      {item.id}
                    </p>
                    <p className=' flex gap-x-1 items-center'>
                      <FontAwesomeIcon icon={faClock} />
                      {item.start_time} - {item.end_time}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </>
      )}
      {showModal&&(
        <AddClassPopup
          showModal={showModal}
          closeModal={closeModal}
          formData={formData}
          handleSubmit={handleSubmit}
          handleInputChange={handleInputChange}
        />
      )}
    </div>
  );
}

export default Monday;

