import React, { useEffect, useState } from 'react';
import { faCalendarDays, faEllipsisVertical, faFileExport, faPaperPlane, faPaperclip, faPenToSquare, faPlus, faXmark, faXmarkCircle } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import noAssignment from '../../../Assets/no-assignment.png'
import AddAssignment from '../Components/AddAssignment';
import { AnimatePresence } from 'framer-motion';
import { motion } from 'framer-motion';
import {getAssignment} from '../../../api/tutor/class/getAssignment';
import {deleteAssignment} from '../../../api/tutor/class/deleteAssignment';

const Assignment = () => {

  const [showAddAssignments, setShowAddAssignments] = useState(false);
  const [deleteConfirmation, setDeleteConfirmation] = useState({ isOpen: false, indexToDelete: null });
  
  const handleAddAssignment = () => {
    setShowAddAssignments(true);
  }
  const [tabData, setTabData]=React.useState([]);
  useEffect(() => {
    getAssignment().then((data) => {
      setTabData([...tabData, ...data])
      console.log(data,'kdodp');
    })
  },[])

  const Table = ({ tabData, onDeleteAssignment }) => {
    if (tabData.length === 0) {
      // Display fallback content if tabData is empty
      return (
        <div className="flex flex-col gap-3 absolute top-[18rem] rounded-xl border-[1px] border-[#000000] right-[30rem] w-[250px] h-[250px] justify-center items-center">
          <div className="">
            <img src={noAssignment} alt="" />
          </div>
          <div className="flex flex-col gap-2 justify-center items-center">
            <p className='text-[#898A8B]'>No Assignments</p>
          </div>
        </div>
      );
    }
    return (
      <table className="poppins my-8">
        <thead className=''>
          <tr className=' grid grid-cols-9 bg-[#f3f6f9] items-center rounded-t-2xl' >
            <th className='py-5 text-sm '>{row?.length}</th>
            <th className='py-5 text-sm text-[#B5B5C3]'>Edit</th>
            <th className='py-5 text-sm '>Name</th>
            <th className='py-5 text-sm '>Date</th>
            <th className='py-5 text-sm '>Title</th>
            <th className='py-5 text-sm '>Attachment</th>
            <th className='py-5 text-sm '>Assessment</th>
            <th className='py-5 text-sm '>Send Message</th>
          </tr>
        </thead>
        <tbody className='flex flex-col'>
        {tabData.map((row, index) => (
          <tr 
            key={index} 
            className='border-2 border-[#f3f6f9] grid grid-cols-9  place-items-center'
            >
            <td className=''>
              {row?.id}
              {/* <input type="checkbox" name="" id="" className='ml-2' />  */}
            </td>
            <td className='bg-[#FFAF53] p-1 px-2 rounded-lg text-white'>
              <button>
                <FontAwesomeIcon icon={faPenToSquare} />
              </button>
            </td>
            <td className='py-3 '>{row.student}</td>
            <td className=' py-3  text-center text-[#B5B5C3]'>{row?.end_ate}</td>
            <td className=' py-3  text-center  text-[#186BAD] font-semibold'>{row?.name}</td>
            <td className='text-[#000] flex items-center gap-2'>
              {/* {row.attachment} */}
              <input style={{display: "none"}} id='file' />
                <FontAwesomeIcon icon={faPaperclip} className={` text-lg ${row.attachment < 1 ? 'text-[#B5B5C3]' : 'text-[#0FA958]'}`} />
              <label htmlFor='file'>
              </label>
            </td>
            <td className=' py-3 '>{row?.numberOfClasses}</td>
            <td className=' bg-[#186BAD] px-2 py-1 rounded-lg text-white'>
              <button><FontAwesomeIcon icon={faPaperPlane} /></button>
            </td>
            <td className=' text-[#F64E60] text-3xl'>
                <button
                  className='deleteAssignment'
                  onClick={() => setDeleteConfirmation({ isOpen: true, indexToDelete: row?.id })}
                >
                  <FontAwesomeIcon icon={faXmarkCircle} />
                </button>
              </td>
          </tr>
        ))}
      </tbody>
      </table>
    );
  };

  const handleDeleteAssignment = (index) => {
    // Create a copy of the tabData array
    const updatedTabData = [...tabData];
    // Remove the assignment at the specified index
    updatedTabData.splice(index, 1);
    // Update the state with the new array
    setTabData(updatedTabData);
    deleteAssignment(index)
    // Close the delete confirmation modal
    setDeleteConfirmation({ isOpen: false, indexToDelete: null });
  };



  return (
    <div className="poppins">
      { showAddAssignments ? (
        <AddAssignment/> 
      ) : (
        <div className="p-4">
        <div className="payments flex justify-between items-end mt-8">
          <div className="poppins ">
            <p className={`text-[#B5B5C3] mb-[-2rem] text-sm ${tabData.length === 0 ? 'hidden' : '' }`}>A Total of 125 Assignment Have Listed.</p>
          </div>
          <div className="">
            {/* <button className='mx-3 border-[#696969] border-[1px] bg-[#F6F6F6] hover:bg-[#cacaca] text-[#4F4E4E] transition rounded-xl font-semibold py-[0.3rem] px-8'>Filter Assignment <FontAwesomeIcon icon={faEllipsisVertical} className='ml-3' /></button> */}
            <button className='bg-[#186BAD] text-white items-center transition hover:bg-[#0f3f66] rounded-xl font-semibold py-[0.3rem] px-8' onClick={handleAddAssignment}>ADD NEW<FontAwesomeIcon icon={faPlus} className='ml-3'/></button>
          </div>
        </div>
        <Table tabData={tabData} onDeleteAssignment={handleDeleteAssignment} />
    </div>
      ) }

      <AnimatePresence>
        {deleteConfirmation.isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="delete-confirmation-modal poppins fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 "
            >
            <div className="bg-white p-8 rounded-md shadow-2xl">
              <p className="text-lg mb-4">Are you sure you want to delete this?</p>
              <div className="flex justify-end">
                <button className="mr-4 text-[#186BAD] font-bold" onClick={() => handleDeleteAssignment(deleteConfirmation.indexToDelete)}>
                  Ok
                </button>
                <button className="text-gray-500 font-bold" onClick={() => setDeleteConfirmation({ isOpen: false, indexToDelete: null })}>
                  Cancel
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Assignment;
