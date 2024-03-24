// UserContext.js
import { createContext } from 'react';

export const tutorViewInitalData={
    
    authentication: {
        signin: false,
        token: '',
        error: 'Unable to Login'
    },
    studentProfile: {
        profile: {
            user: {},
                full_name: '',
                first_name: '',
                last_name: '',
                email: '',
                phone: '',
                cretedate: '',
                bio: '',
                user_type: '',
                createdAT: ''
        },
        grade_level: 'Grade 1',
        preferred_subject: '',
        learning_goal: '5',
        timeezone:"country"
    },
    tutorProfile: {
        profile: {
            user: {},
            full_name: '...',
            first_name: '...',
            last_name: '',
            email: '',
            phone: '',
            cretedate: '',
            bio: '',
            user_type: '',
            createdAT: ''
        },
        subject: [{
            name: '',
            level: '',
            price: ''
        }],
        grades: '',
        sessionRate: '',
        avaliability_time: {},
        avaliableTime: {},
        createdAt: ""


    }
}
const UseSessionContext = createContext({...tutorViewInitalData });

export { UseSessionContext }