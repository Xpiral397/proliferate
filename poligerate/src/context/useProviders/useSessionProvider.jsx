import {useState} from "react";
import {TutorContext, tutorViewInitalData} from "../createContext/useTutor";
import {UseSessionContext} from "../createContext/useSession";


export function UseSessionProvider({children}) {
  const data=localStorage.getItem('tutor_data')
  const tutorData=JSON.parse(!data||data=='undefined'? '{}':data);
  const [session, update]=useState(tutorData);
  const updateSession=(data) => {
    if(data.authentication) {
      localStorage.setItem('tutor_data', JSON.stringify(data))
    }
    update(data);
  }
  const tutorContext={session, updateSession}
  return (
    <UseSessionContext.Provider value={tutorContext}>
      {children}
    </UseSessionContext.Provider>
  )
}


