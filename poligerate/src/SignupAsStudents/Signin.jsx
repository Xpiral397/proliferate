import React, {useState, useEffect, useContext} from 'react';
import {Link, useNavigate} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheckCircle} from '@fortawesome/free-solid-svg-icons';
import {useDispatch, useSelector} from 'react-redux';
import {signInAction} from '../Redux/actions/Auth';
import {toast} from 'react-toastify';
import {clearLoginStatus} from '../Redux/reducers/authReducer';
import Header from '../Components/Header';
import {TutorContext} from '../context/createContext/useTutor';
import {Login} from '../api/login';
import Subject from '../Pages/Subject/Subject';
import {UseSessionContext} from '../context/createContext/useSession';

function Signin() {
  const [email, setEmail]=useState('');
  const [password, setPassword]=useState('');
  const [isloading, setIsloading]=useState(false);
  const [showModal, setShowModal]=useState(false)
  const [error, setError]=useState("")
  const {tutor, setTutor}=useContext(TutorContext)
  const {session, updateSession} = useContext(UseSessionContext)
  // New state variables for empty field status and error messages
  const [emailEmpty, setEmailEmpty]=useState(false);
  const [passwordEmpty, setPasswordEmpty]=useState(false);

  const navigate=useNavigate();


  // useEffect(() => {
  //   if(isloading&&authSelector.signingInStatus==='failed') {
  //     toast.error(`${authSelector.signingInError}`);
  //     setIsloading(false);
  //   }
  //   if(authSelector.signingInStatus==='failed'||authSelector.signingInStatus==='completed') {
  //     dispatch(clearLoginStatus());
  //   }
  // }, [isloading, authSelector.signingInStatus, authSelector.signingInError, dispatch]);

  // useEffect(() => {
  //   if(authSelector.signingInStatus==='completed') {
  //     // Show the popup modal
  //     setShowModal(true);
  //     setTimeout(() => {
  //       setShowModal(false);
  //     }, 3000);
  //   }
  // }, [authSelector.signingInStatus, navigate]);

  // const handleLogin=() => {
  //   // Check for empty fields
  //   if(!email||!password) {
  //     setEmailEmpty(!email);
  //     setPasswordEmpty(!password);
  //     return;
  //   }

  //   // Dispatch the login action
  //   dispatch(
  //     signInAction({
  //       email: email,
  //       password: password,
  //     })
  //   );
  //   setIsloading(true);
  // };

  
  useEffect(() => { 
    const data=JSON.parse(localStorage.getItem('tutor_data') !== "undefined"?localStorage.getItem("tutor_data"):'{}')
    console.log(data,'Kow')
    if(session?.authentication?.signin||data?.authentication?.signin) {
      navigate('/tutordashboard');
      // Show the popup modal
      setShowModal(true);
      setTimeout(() => {
        setShowModal(false);
      }, 3000);
    }
    
  }, [session?.authentication?.signin])
  const handleLogin=() => {
    
    console.log(session)
   
    
      // Check for empty fields
      if(!email||!password) {
        setEmailEmpty(!email);
        setPasswordEmpty(!password);
        return;
      }

      // Dispatch the login action

      (async () => {
        try {
          const response=await Login(
            email,
            password
          )
          console.log(response, 'crom');
          if(response.status==401||response.status==500) {

            setError(response.status===401? "User credentials is invalid ":'Server Internal Error')
         
            setIsloading(false)
          }
          else {
            const {
              username,
              email,
              isAdmin,
              first_name,
              last_name,
              token
            }=response.data
            localStorage.setItem('token_data', token)
            toast.success('Login Successful');
            setShowModal(true)
            updateSession(data => {
              return {
                authentication: {
                  user_type: "tutor",
                  token,
                  ...session?.authentication,
                  signin: true,
                  error: "Success"
                },
                tutorProfile: {
                  ...session?.tutorProfile?.profile,
                  profile: {
                    ...session?.tutorProfile?.profile,
                    user: {},
                    full_name: first_name+" "+last_name,
                    first_name,
                    last_name,
                    email,
                    phone: "",
                    username,
                    user_type: "tutor",
                    isAdmin
                  },
                  subject: [],
                  grades: "",
                  sessionRate: "",
                  avaliability_time: {},
                  avaliableTime: {},
                  createdAt: ""
                }
              }
            });
            console.log(session,'kop')
       
            navigate('/tutordashboard');
          }
        } catch(error) {
          console.log(error)
          setError('Unknow Error Occured')
          toast.error('Unable To Reach The Server');
          setIsloading(false)
        }

      })()

      setIsloading(true);
    
  };




  return (
    <div>
      <Header />
      <div className="lg:px-28 px-5  my-16">
        <div className="poppins header text-center">
          <h1 className='lg:text-3xl text-2xl'>Hi, Welcome back!</h1>
        </div>
        <div className="poppins m-auto flex items-center justify-center py-10">
          <div className='form lg:w-min w-[350px]'>
            <div className='mb-3'>
              <p className='text-[#186BAD] text-sm mb-1 font-semibold'>Email</p>
              <input
                type="email"
                placeholder='Email'
                className={`bg-[#F2F1F1] p-3 lg:w-[400px] w-[300px] outline-none rounded-sm ${emailEmpty? 'border-red-500':''}`}
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  setEmailEmpty(false);
                }}
                required
              />
              {/* {emailEmpty && <p className='text-red-500 text-xs mt-1'>This must not be empty</p>} */}
            </div>
            <div className='mb-3'>
              <p className='text-[#186BAD] text-sm mb-1 font-semibold'>Password</p>
              <input
                type="password"
                placeholder='Password'
                className={`bg-[#F2F1F1] p-3 lg:w-[400px] w-[300px] outline-none rounded-sm ${passwordEmpty? 'border-red-500':''}`}
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  setPasswordEmpty(false);
                }}
                required
              />
              {passwordEmpty&&<p className='text-red-500 text-xs mt-1'>This must not be empty</p>}
            </div>
            <div className="lg:w-[400px] w-[300px] flex gap-3 items-baseline my-7" >
              <input type="checkbox" name="" id="" required />
              <p className='text-[#186BAD] font-semibold'>Keep me signed in</p>
            </div>
            <button
              onClick={handleLogin}
              type="submit"
              className={`signup text-white font-semibold py-3 bg-[#186BAD] lg:w-[400px] w-full rounded-lg ${!email||!password? 'opacity-50 cursor-not-allowed':''}`}
              disabled={!email||!password}
            >
              Sign in
            </button>
            <p className='text-[#898A8B] text-center py-5'>Don't have an account? <span className='text-[#186BAD] ml-2'><Link to='/signup'>Sign Up</Link></span></p>
          </div>
        </div>
      </div>

      {/* signup successfull */}
      {showModal&&(
        <div className="popup-modal">
          <FontAwesomeIcon icon={faCheckCircle} className="text-6xl text-[#186BAD] my-2" />
          <h2 className="text-2xl font-bold">Welcome back, Buddy!</h2>
          <p className="my-3 text-[#186BAD] font-semibold">Proceeding to Dashboard...</p>
        </div>
      )}
    </div>
  );
}

export default Signin;
