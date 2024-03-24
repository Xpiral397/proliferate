import { useState } from "react";
import { TutorContext, tutorViewInitalData } from "../createContext/useTutor";
import { UseSessionContext } from "../createContext/useSession";
import {Logout as signOut} from "../../api/logout";
import {useNavigate} from 'react-router-dom'


export function UseSessionProvider({ children }) {


    const data = localStorage.getItem('tutor_data')
    const tutorData = JSON.parse(!data || data == 'undefined' ? '{}' : data);

  
  const [session, update]=useState(tutorData);
  const navigate = useNavigate()
    const updateSession = (data) => {
        const sessionData = data()
        if (sessionData) {
            localStorage.setItem('tutor_data', JSON.stringify(sessionData))
        }
        update(data);
    }
  const Logout=(Provider) => {
    update({})
    signOut(Provider)
    navigate('/signin')
    }
    const tutorContext = { session, updateSession, Logout }
  return (<UseSessionContext.Provider value={tutorContext} > {children}
    </UseSessionContext.Provider>
    )
}